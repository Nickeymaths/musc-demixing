# UET xử lý tiếng nói - Dự án cuối khóa
## Nhóm 05
### Thành viên
- Phạm Thanh Vĩnh - 19021396
- Nguyễn Văn Tú - 19021384
- Nguyễn Mạnh Tuấn - 19021381
- Bùi Văn Toán - 19021372

### Phân công trong nhóm
| Thành viên       | MSSV     | Đóng góp                                                                      |
|------------------|----------|-------------------------------------------------------------------------------|
| Bùi Văn Toán     | 19021372 |                                                                               |
| Nguyễn Văn Tú    | 19021381 | Correspondence experiment                                                     |
| Nguyễn Mạnh Tuấn | 19021384 | Run deepdream experiment for visualizing                                      |
| Phạm Thanh Vĩnh  | 19021396 | Implement Alexnet conv, deconv, occlusion, visualization, stable experiments  |
## Mô tả
### Mô tả chung về ứng dụng
### Mô tả chức năng
### Dữ liệu sử dụng
### Phương pháp
#### Tách thành phần âm thanh (Demixing)
#### Sinh lời tự động (Auto lyric seperation)
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
