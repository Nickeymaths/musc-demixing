# UET xử lý tiếng nói - Dự án cuối môn học
## Nhóm 05
### Thành viên
- Phạm Thanh Vĩnh - 19021396
- Nguyễn Văn Tú - 19021384
- Nguyễn Mạnh Tuấn - 19021381
- Bùi Văn Toán - 19021372

### Phân công trong nhóm
| Thành viên       | MSSV     | Đóng góp                                                      |
|------------------|----------|---------------------------------------------------------------|
| Bùi Văn Toán     | 19021372 | Phụ trách UI, code UI cơ bản, code logic UI, tìm hiểu mô hình |
| Nguyễn Văn Tú    | 19021381 | Code UI cơ bản, code logic UI, tìm hiểu mô hình               |
| Nguyễn Mạnh Tuấn | 19021384 | Code UI cơ bản, code logic UI, tìm hiểu mô hình               |
| Phạm Thanh Vĩnh  | 19021396 | Tìm hiểu mô hình, tổ chức thí nghiệm, tinh chỉnh code mô hình |

## Mô tả
### Mô tả chung về ứng dụng
Ứng dụng tùy chỉnh nhạc, xử lý bài hát dành cho producer.
### Mô tả chức năng
Ứng dụng hỗ trợ:
+ Phát nhạc, tạo danh sách nhạc, chuyển bài, tua bài hát, chỉnh tốc độ phát nhạc.
+ Tách bài hát thành vocals (giọng hát) và các nhạc cụ: drums (trống), piano, bass, other (các thành phần khác).
+ Mix các thành phần đã tách thành bài hát mới tùy ý.
+ Cho phép tải bài hát mới hoặc các thành phần tùy ý.
+ Nhận dạng lyrics từ giọng hát, hiển thị lyrics theo thời gian thực.
### Mô tả flow của ứng dụng
+ Người dùng thêm bài hát kỳ từ local vào thư viện bài hát của ứng dụng
+ Bài hát được đưa vào xử lý để tách thành các thành phần vocals, bass, piano, drums, other
+ Thành phần vocals được đưa vào làm đầu vào cho quá trình nhận dạng lyric
+ Những bài hát đã có mặt tại thư viện tức là đã qua bước xử lý tách thành phần và tách lyric. Các thành phần của những bài hát khác nhau có thể được chọn để cùng mix lại và tạo ra bài hát mới
### Dữ liệu sử dụng cho chức năng tách lyric
+ Dataset cho nhận dạng giọng nói [LibriSpeech ASR](https://openslr.magicdatatech.com/12/)
+ Bao gồm 1000 giờ giọng đọc sách nói bằng tiếng Anh được ghi âm với tỉ lệ lấy mẫu 16kHz thuộc dự án [LibriVox](https://librivox.org/)
+ Gồm file audio và transcript tưng ứng cho từng file
### Dữ liệu sử dụng cho chức năng tách thành phần bài hát
+ Dataset được sử dụng [MUSDB18](https://sigsep.github.io/datasets/musdb.html#musdb18-compressed-stems) gồm 150 bài hát với tổng thời lượng khoảng 10h thuộc các thể loại khác nhau trong đó có 100 bài dùng để huấn luyện và 50 bài được dùng để test
+ Mỗi bài có định danh cụ thể và được đặt trong một folder cùng tên chứa 5 thành phần mixture, drums, bass, vocals, other (các âm thanh của nhạc cụ khác)
+ Các bài hát đều là stereophonic được lấy mẫu với sampling rate 44.1kHz
### Phương pháp
#### Tách thành phần âm thanh (Demixing)
Để có thể tách thành phần âm ta phải tiến hành trích xuất đặc trưng âm thanh MFCC, tuy nhiên do audio đầu và thể có kích thước lớn do đó trích xuất trực tiếp sẽ không đủ
RAM, do đó cần lầm như sau:

+ Chia audio đầu vào thành nhiều mảnh nhỏ mỗi mảnh có độ dài 30s
+ Sử dụng thư viện spleeter để tách âm cho từng đoạn sau đó ghép lại thành audio tổng thể ban đầu
#### Sinh lời tự động (Auto lyric seperation)
Finetune [pretrained model](https://kaldi-asr.org/models/13/0013_librispeech_v1_lm.tar.gz) một mô hình WFST được bởi các mô hình con HMM, Context-dependence-phones, Lexicon, Gramma

`Training`

+ C, G, L là [3-gram model](https://kaldi-asr.org/models/13/0013_librispeech_v1_lm.tar.gz)
+ Lexicon từ điển gồm 134k từ có thể lấy ở [CMU dict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)
 Các bước thực hiện
 + Tạo format dữ liệu huấn luyện phù hợp với kaldi gồm 4 file

 ++ wav.scp: mapping giữa audioId và audio tương ứng
 
 ++ text: mapping giữa audioId và transcript
 
 ++ utt2spk: mapping giữa từng file audio với id người nói
 
 ++ spk2utt: mapping giữa spk và danh sách audio
 
 + 3-gram ngôn LM gồm C, L, G (dùng lexicon có sẵn trên)
 
 + Trích xuất đặc trưng MFCC, delta, delta-delta dữ liệu huấn luyện (Kaldi)

 Loop (
 + Train lại mô hình Monophone tức HMM có sẵn với LM
 + Align lại đặc trưng MFCC, delta, delta-delta và 3-grám LM

 )

 + Build graph model HCLG.fst (kaldi)
 
`Decode`

+ Trích xuất đặc trưng MFCC, delta, delta-MFCC
+ Decode kết bằng graph model HCLG.fst đã build (kaldi)

### Tạo môi trường
Tạo môi trường conda cho project
```console
$ conda env create -n musc-demixing python=3.8
$ conda activate musc-demixing
$ cd musc-demixing
```
Cài đặt các module cần thiết
```
# install spleeter for song spleeting
$ conda install -c conda-forge ffmpeg libsndfile
$ pip install spleeter

# Remove default spleeter and install compatiable ffmpeg for python 3.8
$ pip uninstall spleeter FFmpeg ffmpeg-python
$ pip install ffmpeg-python

# install necessary package
$ pip install -r requirements.txt
```
Do ứng dụng sử dụng mô hình được huấn luyện sau đó decode kết quả dựa trên phần mềm kaldi do đó ta cần tải và thiết lập môi trường để có thể chạy được kaldi

```console
$ git clone https://github.com/kaldi-asr/kaldi.git kaldi --depth 1
$ cd kaldi/tools
$ extras/check_dependencies.sh
$ make

$ cd ../src
$ ./configure
$ make depend
$ make
```

### Chạy ứng dụng
```console
$ python3 musc-demixing.py
```
