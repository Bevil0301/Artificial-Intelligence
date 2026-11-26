# UCS – Tìm kiếm theo chi phí đồng nhất

## 1. Các bước thực hiện

1. Tạo nút đầu với chi phí tích lũy g = 0, đưa vào hàng đợi ưu tiên Frontier. Khởi tạo Explored rỗng.
2. Lấy khỏi Frontier nút có g nhỏ nhất. Nếu nhiều nút cùng g, chọn nút được đưa vào trước.
3. Thêm trạng thái vừa lấy vào Explored. Kiểm tra đích ngay lúc này. Nếu đạt đích, lần theo nút cha về nút đầu rồi đảo ngược đường đi.
4. Với mỗi hành động hợp lệ, sinh nút con và tính g(con) = g(cha) + chi phí hành động.
5. Bỏ qua trạng thái đã thuộc Explored. Với trạng thái còn lại, nếu chưa có trong Frontier thì thêm vào. Nếu đã có và tìm được đường rẻ hơn, cập nhật chi phí và nút cha.
6. Lặp lại từ bước 2. Nếu Frontier hết nút thì trả về thất bại.

## 2. Mã giả

```text
function UCS(problem):
    node ← Node(problem.initial_state)
    node.g ← 0
    frontier ← PriorityQueue()          // ưu tiên g nhỏ, hòa thì FIFO
    frontier.insert(node)
    explored ← ∅

    while frontier is not empty:
        node ← frontier.pop_min()
        explored.add(node.state)
        if problem.is_goal(node.state):
            return solution(node)

        for action in problem.actions(node.state):
            child ← child_node(problem, node, action)
            child.g ← node.g + problem.step_cost(node.state, action, child.state)
            if child.state in explored:
                continue
            if child.state not in frontier:
                frontier.insert(child)
            else if child.g < frontier.cost_of(child.state):
                frontier.replace(child.state, child)

    return failure
```

## 3. So với BFS và DFS trong bài

| Đặc điểm | BFS | DFS | UCS |
|---|---|---|---|
| Nút được lấy tiếp | Đầu hàng đợi FIFO | Đỉnh ngăn xếp LIFO | Nút có tổng chi phí g nhỏ nhất |
| Xử lý trùng | Bỏ qua trạng thái đã gặp | Bỏ qua trạng thái đã gặp | Thay nút đang chờ nếu đường mới rẻ hơn |
| Thời điểm kiểm tra đích | Khi sinh nút con, có kiểm tra riêng nút đầu | Khi lấy nút ra | Khi lấy nút có g nhỏ nhất ra |
| Lời giải | Ít bước nhất | Phụ thuộc thứ tự duyệt | Tổng chi phí nhỏ nhất với chi phí cạnh không âm |

Ví dụ: từ S đi thẳng đến G tốn 9. Đi S → A tốn 2, rồi A → G tốn 3. UCS có thể thấy G với g = 9 trước, nhưng sẽ lấy A ra trước G. Lúc đó chi phí tốt nhất của G giảm xuống 5.

## 4. Quy ước chạy tay

Ảnh đề bài chưa cho trọng số riêng. Hai bảng dưới dùng chi phí 1 cho mỗi hành động. Vì vậy g bằng số bước từ nút đầu. Các hàng ghi trạng thái sau khi xử lý Node. Frontier được viết theo thứ tự sẽ lấy ra, từ trái sang phải. Explored ghi theo thứ tự lấy ra và gồm cả nút đích ở vòng cuối. Ký hiệu A(2) nghĩa là nút A có g = 2.

## 5. Vacuum Robot

Ban đầu `(A, D, D)`. Đích `(B, C, C)`. Xét các hành động hợp lệ theo thứ tự suck, left, right.

| Nút | Trạng thái | g |
|---|---|---:|
| A | `(A, D, D)` | 0 |
| B | `(A, C, D)` | 1 |
| C | `(B, D, D)` | 1 |
| D | `(B, C, D)` | 2 |
| E | `(B, D, C)` | 2 |
| F | `(B, C, C)` | 3 |
| G | `(A, D, C)` | 3 |

| Node | Frontier | Explored |
|---|---|---|
| Khởi tạo | A(0) | ∅ |
| A(0) | B(1), C(1) | A |
| B(1) | C(1), D(2) | A, B |
| C(1) | D(2), E(2) | A, B, C |
| D(2) | E(2), F(3) | A, B, C, D |
| E(2) | F(3), G(3) | A, B, C, D, E |
| F(3) | G(3) | A, B, C, D, E, F |

Đường đi **A → B → D → F**. Hành động **suck → right → suck**. Tổng chi phí **3**.

## 6. 8-puzzle

Ban đầu `123/406/758`. Đích `123/456/780`. Xét các hành động hợp lệ theo thứ tự Lên, Xuống, Trái, Phải.

| Nút | Trạng thái | g |
|---|---|---:|
| A | `123/406/758` | 0 |
| B | `103/426/758` | 1 |
| C | `123/456/708` | 1 |
| D | `123/046/758` | 1 |
| E | `123/460/758` | 1 |
| F | `013/426/758` | 2 |
| G | `130/426/758` | 2 |
| H | `123/456/078` | 2 |
| I | `123/456/780` | 2 |
| J | `023/146/758` | 2 |
| K | `123/746/058` | 2 |
| L | `120/463/758` | 2 |
| M | `123/468/750` | 2 |
| N | `413/026/758` | 3 |
| O | `136/420/758` | 3 |
| P | `123/056/478` | 3 |

| Node | Frontier | Explored |
|---|---|---|
| Khởi tạo | A(0) | ∅ |
| A(0) | B(1), C(1), D(1), E(1) | A |
| B(1) | C(1), D(1), E(1), F(2), G(2) | A, B |
| C(1) | D(1), E(1), F(2), G(2), H(2), I(2) | A, B, C |
| D(1) | E(1), F(2), G(2), H(2), I(2), J(2), K(2) | A, B, C, D |
| E(1) | F(2), G(2), H(2), I(2), J(2), K(2), L(2), M(2) | A, B, C, D, E |
| F(2) | G(2), H(2), I(2), J(2), K(2), L(2), M(2), N(3) | A, B, C, D, E, F |
| G(2) | H(2), I(2), J(2), K(2), L(2), M(2), N(3), O(3) | A, B, C, D, E, F, G |
| H(2) | I(2), J(2), K(2), L(2), M(2), N(3), O(3), P(3) | A, B, C, D, E, F, G, H |
| I(2) | J(2), K(2), L(2), M(2), N(3), O(3), P(3) | A, B, C, D, E, F, G, H, I |

Đường đi **A → C → I**. Hành động **Xuống → Phải**. Tổng chi phí **2**.
