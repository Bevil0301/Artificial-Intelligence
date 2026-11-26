# Search Lab

Ứng dụng Pygame mô phỏng BFS, DFS và UCS trên 8-puzzle và robot hút bụi hai phòng.

## Chạy ứng dụng

Từ thư mục chứa `main.py`, chạy:

```shell
python -m pip install -r requirements.txt
python main.py
```

Bấm **Bài toán** hoặc **Thuật toán** ở cuối cửa sổ, sau đó chọn trực tiếp một mục trong danh sách. Trong danh sách thuật toán, có thể gõ để lọc, cuộn chuột hoặc dùng phím lên/xuống và Enter. Esc đóng danh sách. Mỗi bài toán nhớ trạng thái đầu đã chỉnh trong phiên hiện tại. Khi đổi thuật toán, ứng dụng tính lại lời giải trên cùng trạng thái đó. Chọn **Xem quá trình duyệt** để theo dõi Node, Frontier và Explored.

## Cấu trúc

- `main.py` điều khiển cửa sổ, phát lại và chuyển chế độ.
- `search.py` chứa mô hình nút, BFS, DFS, UCS và bảng đăng ký thuật toán.
- `puzzle.py` và `vacuum.py` định nghĩa hành động, chuyển trạng thái, cách vẽ và màn hình chỉnh trạng thái đầu.
- `graphics.py` chứa các thành phần giao diện dùng chung.

## Thêm thuật toán

Viết hàm trong `search.py` với chữ ký `ten_ham(problem, trace)`. Xem BFS và DFS để đối chiếu. Hàm trả về danh sách trạng thái từ đầu đến đích, đồng thời ghi từng vòng vào `trace` bằng bộ ba `(node_state, frontier_preview, frontier_count)`. Bản ghi khởi tạo dùng `None` cho node; các bản ghi tiếp theo dùng trạng thái vừa lấy ra. Phần xem trước chứa tối đa sáu trạng thái theo thứ tự sẽ duyệt. Hai bài toán hiện tại chỉ cho chọn trạng thái đầu có lời giải.

Đăng ký tên hiển thị và hàm trong `ALGORITHMS`. Nút **Thuật toán** tự lấy danh sách từ bảng này.

[Bài UCS và bảng chạy tay](UCS.md)
