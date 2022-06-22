# UET xử lý tiếng nói - Dự án cuối môn học
## Nhóm 05
### Thành viên
- Phạm Thanh Vĩnh - 19021396
- Nguyễn Văn Tú - 19021384
- Nguyễn Mạnh Tuấn - 19021381
- Bùi Văn Toán - 19021372

### Video demo các chức năng
+ [Tách Lyrics, thành phần bài hát](https://drive.google.com/file/d/1juDw8lrURRmRd_zUH8UEXBIQss05-QOB/view?usp=sharing)
+ [Tải bài hát, thành phần bài hát](https://drive.google.com/file/d/1DREJvj_jmAYWhE_mhWX7oOpVDPnAVtM-/view?usp=sharing)
+ [Mix các thành phần bài hát](https://drive.google.com/file/d/1inT3vwtjpVMcdChQTNVeTzM0eUnD0-BN/view?usp=sharing)
+ [Xóa thành phần bài hát](https://drive.google.com/file/d/1Zuw12Hmk1PIxqyr5ygA1HAJe80UEMpYS/view?usp=sharing)
+ [Thêm bài hát](https://drive.google.com/file/d/1ILOvR609L9NqOmeBfHLvpuB3omrMkCmB/view?usp=sharing)
+ [Điều chỉnh âm lượng](https://drive.google.com/file/d/1fXtYrqjiBo3XOVLG-nBN6yy74BVDnAcm/view?usp=sharing)
+ [Chỉnh tốc độ bài hát](https://drive.google.com/file/d/1i5WvcO224fX0hlPCEB2FFPypFZtrHzx9/view?usp=sharing)
+ [Tua bài hát](https://drive.google.com/file/d/12e_Rkeo12HNl8PHxQ_8p7wG9cxZQImAk/view?usp=sharing)

### Phân công trong nhóm
| Thành viên       | MSSV     | Đóng góp                                                      |
|------------------|----------|---------------------------------------------------------------|
| Bùi Văn Toán     | 19021372 | Phụ trách UI, code UI cơ bản, code logic UI|
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
## Phương pháp
### Tách thành phần âm thanh (Demixing)
Để có thể tách thành phần âm ta phải tiến hành trích xuất đặc trưng âm thanh MFCC, tuy nhiên do audio đầu và thể có kích thước lớn do đó trích xuất trực tiếp sẽ không đủ
RAM, do đó cần làm như sau:

+ Chia audio đầu vào thành nhiều mảnh nhỏ mỗi mảnh có độ dài 30s
+ Sử dụng thư viện spleeter để tách âm cho từng đoạn sau đó ghép lại thành audio tổng thể ban đầu
### Sinh lời tự động (Auto lyric seperation)
Finetune [pretrained model](https://kaldi-asr.org/models/13/0013_librispeech_v1_lm.tar.gz) một mô hình WFST được bởi các mô hình con HMM, Context-dependence-phones, Lexicon, Gramma

`Chuẩn bị dữ liệu, mô hình cần thiết`

<details>
    <summary>Chuẩn bị cấu hình cho G model, tạo graph model G.fst</summary>
    G là một máy automat hữu hạn có đầu vào và đầu ra giống nhau có tác dụng giới hạn các câu có thể của ngôn ngữ, G tất định

- Tập hợp tất cả từ trong ngôn ngữ được lưu trong words.txt thuộc folder language
- Dữ liệu chuỗi từ được sử dụng trong ngôn ngữ được lưu trong corpus.txt thuộc folder language

→ Build ra G.fst
</details>

<details>
    <summary>Chuẩn bị cấu hình cho L model, tạo graph model L.fst</summary>
    Đóng Kleen Union của tất cả WFST tương ứng  mỗi từ, nhận vào chuỗi phones và cho ra chuỗi words

- Từ điển tất cả independence phone của ngôn ngữ được lưu trong file lexicon.txt thuộc folder language
- Các disambig sử dụng (#0, #1, #3) được lưu trong file disambig.txt các ký tự phụ được xử dụng để đảm bảo điều kiện tất điện của WFST L

→ Build ra L.fst và kết hợp với G.fst → LG.fst
</details>

<details>
    <summary>Chuẩn bị cấu hình cho C model, tạo graph model C.fst</summary>
    Context-dependence model nhận vào chuỗi context-dependence phone và dịch ra independence phones

- Từ điển tất cả independence phone của ngôn ngữ được lưu trong file lexicon.txt thuộc folder language
- disambig được lưu trong file disambig.txt

→ Build và kết hợp với LG.fst → CLG.fst
</details>

<details>
    <summary>Chuẩn bị cấu hình cho H model (Acoustic model), tạo graph model H.fst</summary>
    WFST nhận đầu vào là chuỗi trạng thái của HMM cho đầu ra là chuỗi context-dependence phones

- Kiến trúc DNN được lưu trong chain_cleaned/tdnn_1d_sp/configs/network.xconfig
- Sử dụng pretrained DNN model với config được lưu trong chain_cleaned/tdnn_1d_sp/configs/final.config (Input là đặc trưng mfcc có 40 chiều, output là vector 6024 là số pdf-state của mô hình HMM)

→ Make graph cho ra G.fst → Kết hợp với CLG.fst → HCLG.fst
</details>

<details>
    <summary>Decode</summary>

- Trích xuất đặc trưng mfcc của audio đầu vào
    + wav.scp: mapping giữa audioId và audio tương ứng
    + text: mapping giữa audioId và transcript
    + utt2spk: mapping giữa từng file audio với id người nói
    + spk2utt: mapping giữa spk và danh sách audio
- Đưa đặc trưng thu được vào decode
</details> 

## Tạo môi trường
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

## Chạy ứng dụng
```console
$ python3 musc-demixing.py
```
