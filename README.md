# 23110088_BaiTapCaNhan_AI
BÁO CÁO BÀI TẬP CÁ NHÂN MÔN TRÍ TUỆ NHÂN TẠO.

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
│   ├── AStar.gif
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
  Algorithm.py: là file chứa mã nguồn các nhóm thuật toán đã học 
  UI.py: sẽ gọi lại file Algorithm.py, đây là file chứa giao diện, chức năng của bài. Bài toán cũng được chạy ở file này.  
Folder: GIF sẽ chứa các gif là minh họa cách hoạt động của từng thuật toán.  
File README.md là tài liệu hướng dẫn chung của bài làm. Chứa các thông tin người làm, thông tin bài làm, ...

4. CÁC THUẬT TOÁN ĐÃ TRIỂN KHAI
   
4.1 Beam Search  
![Beam](https://github.com/user-attachments/assets/d36fccf9-bbff-4b95-a0d6-ec70220f25dd)  
4.2 A*  
![A_star](https://github.com/user-attachments/assets/9c212330-0e87-487c-932c-b1115005e126)  
4.3 And-Or search  
![And-Or](https://github.com/user-attachments/assets/8945a533-5618-46ee-b927-04a15374efe7)  
4.3 BackTracking  
![BackTracking](https://github.com/user-attachments/assets/3db06712-c9b8-45e9-8e84-c7722f197910)  
4.4 Belief State  
![BeliefState](https://github.com/user-attachments/assets/1955140f-8e0a-4054-b5df-c7f7117283ec)  
4.5 BFS  
![BFS](https://github.com/user-attachments/assets/f4399c17-b556-41c0-b86a-e13c629c8060)  
4.6 DFS  
![DFS](https://github.com/user-attachments/assets/752d6bef-a0b3-4a83-b885-63cbe7dc7733)  
4.7 IDS  
![IDS](https://github.com/user-attachments/assets/e4067688-5c09-4fc6-bd4d-bafbedd38e8f)  
4.8 DLS  
![DLS](https://github.com/user-attachments/assets/5f68cfe5-be31-4f11-941b-c863f1adb75c)  
4.9 Forward Checking  
![Forward_Checking](https://github.com/user-attachments/assets/72b5e6d7-c331-4718-9312-555c20639079)  
4.10 Genetic  
![GA](https://github.com/user-attachments/assets/d8fce76c-044c-4e10-87b9-6f93df3853d2)  
4.11 Greedy  
![Greedy](https://github.com/user-attachments/assets/979d6bb9-e691-4fb4-af6e-c2d90058aa9a)  
4.12 Hill Climbing  
![Hill_Climbing](https://github.com/user-attachments/assets/ae100721-f2a0-4dcc-8b9a-fb727d99be82)  
4.13 UCS  
![UCS](https://github.com/user-attachments/assets/252cc55a-39bb-4e5a-b6ce-7556c56cb164)  
4.14 Simulated Annealing  
![SA](https://github.com/user-attachments/assets/8be4869c-a61d-4be5-a8d3-8a7cfd1ca4cc)




















