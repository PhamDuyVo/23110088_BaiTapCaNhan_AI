# 23110088_BaiTapCaNhan_AI
Bài tập cá nhân HK1 2025-2026 môn TTNT
BÁO CÁO BÀI TẬP CÁ NHÂN MÔN TRÍ TUỆ NHÂN TẠO 
1. THÔNG TIN CÁ NHÂN

Họ và tên: Võ Phạm Duy  
Mã số sinh viên: 23110088  
Môn học: Trí tuệ Nhân tạo  
Lớp: Sáng thứ 2 - thứ 6, tiết 1 - 4  

2. TỔNG QUAN VỀ BÀI TOÁN: N QUÂN xe (N-rooks Problem)
2.1. Mô tả Bài toán

Bài toán đặt N quân xe (rooks) lên một bàn cờ N × N (0 < N < 9) sao cho không có hai quân xe nào tấn công nhau theo hàng, cột hoặc đường chéo.

Mục tiêu (Goal State):
Đặt N quân xe sao cho mỗi hàng, mỗi cột và mỗi đường chéo chỉ có tối đa một quân xe. Điều này đảm bảo không có hai quân xe nào đe dọa lẫn nhau.

2.2. Biểu diễn Trạng thái

Trạng thái của bài toán được biểu diễn bằng một danh sách các bộ (hàng, cột), mô tả vị trí của các quân xe đã đặt.

Trạng thái ban đầu: Một danh sách rỗng [], tương ứng với bàn cờ trống.

Trạng thái đích: Một danh sách gồm N bộ (hàng, cột), trong đó không trùng hàng, cột, hoặc chéo, ví dụ: [(0, 1), (1, 3), (2, 0), (3, 2)] cho N = 4.

3. CẤU TRÚC GIAO DIỆN VÀ CHỨC NĂNG
3.1. Cấu Trúc Và Chức Năng

Ứng dụng được xây dựng bằng thư viện customtkinter trong Python, với giao diện hiện đại, trực quan và hỗ trợ trực quan hóa các bước thuật toán.


Bảng điều khiển bên phải

Combobox: Cho phép chọn thuật toán giải 

Nút “PLAY”: Thực thi thuật toán được chọn.

Nút “Reset”: Xóa toàn bộ quân xe khỏi bàn cờ.

Bàn cờ “Các bước thực hiện”: Hiển thị trực quan quá trình tìm kiếm lời giải từng bước của thuật toán.

Hai bàn cờ:

Bàn cờ bên phải: Là bàn cờ mục tiêu (goal) cho phép người dùng click chuột vào ô cờ để chọn vị trí cho quân xe

Bàn cờ bên trái: Là bàn cờ được sinh ra bởi thuật toán đang được chọn

3.2. Lưu ý về Mã nguồn và Hiển thị

Sinh Trạng thái:
Các thuật toán tìm kiếm sinh trạng thái bằng cách đặt từng quân  lần lượt theo hàng, loại bỏ các vị trí bị đe dọa. Điều này giúp giảm không gian tìm kiếm và tăng tốc độ giải.

Trực quan hóa:
Giao diện cập nhật từng bước đi của thuật toán trên bàn cờ bên trái, đồng thời hiển thị kết quả cuối cùng ở bàn cờ bên phải. Người dùng có thể quan sát quá trình Backtracking, DFS hay CSP một cách rõ ràng.

Logging:
Mọi hành động như thử đặt quân xe, quay lui, loại bỏ vị trí bị tấn công, cắt tỉa đều được ghi lại chi tiết trong ô log, giúp hiểu rõ cách thuật toán hoạt động.

3.3. Cấu Trúc Bài Làm
```
/23110088_BaiTapCaNhanAI
│
├── GIF/
│   ├── AC3.gif
│   ├── AStar.gif
│   ├── Alpha_Beta.gif
│   ├── And_Or.gif
│   ├── BFS.gif
│   ├── Backtracking.gif
│   ├── Beam.gif
│   ├── Belief_State.gif
│   ├── DFS.gif
│   ├── DLS.gif
│   ├── Forward_Checking.gif
│   ├── Genetic_Algorithm.gif
│   ├── Greedy.gif
│   ├── Hill_Climbing.gif
│   ├── IDS.gif
│   ├── Minimax.gif
│   ├── Partially_Observable.gif
│   ├── Simulated_Annealing.gif
│   └── UCS.gif
│
├── 23110088_BTCN_AI/
│   ├── Algorithm.py
│   ├── UI.py
│   
├── Main.py
└── README.md
```

Chức năng các FILE& FOLDER:  
Folder: 23110088_BTCN_AI là folder chứa 2 file quan trọng nhất của bài làm, trong đó:  
  Algorithm.py: là file chứa mã nguồn các nhóm thuật toán đã  
  UI.py: sẽ gọi lại file Algorithm.py, đây là file chứa giao diện, chức năng của bài. Bài toán cũng được chạy ở file này.  
Folder: GIF sẽ chứa các gif là minh họa cách hoạt động của từng thuật toán.  
File README.md là tài liệu hướng dẫn chung của bài làm. Chứa các thông tin người làm, thông tin bài làm, ...
