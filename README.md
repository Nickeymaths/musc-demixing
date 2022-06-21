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
+ Sử dụng thư viện spleeter để phân tách thành các thành phần như đã mô tả phía trên
#### Sinh lời tự động (Auto lyric seperation)
+ Sử dụng kaldi, với pretrained model giọng đọc để tự động nhận dạng lời bài hát
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
