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
### Dữ liệu sử dụng
+ Sử dụng tập dữ liệu: 
### Phương pháp
#### Tách thành phần âm thanh (Demixing)
+ Sử dụng thư viện spleeter để phân tách thành các thành phần như đã mô tả phía trên
#### Sinh lời tự động (Auto lyric seperation)
+ Sử dụng kaldi, với pretrained model giọng đọc để tự động nhận dạng lời bài hát
### Tạo môi trường
```console
$ conda env create -n musc-demixing
$ conda activate musc-demixing
$ cd musc-demixing
$ pip install -r requirements.txt
```
### Chạy ứng dụng
```console
$ python3 musc-demixing.py
```
