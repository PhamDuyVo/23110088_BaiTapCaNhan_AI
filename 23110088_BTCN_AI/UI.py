import tkinter as tk
from tkinter import ttk
import Algorithm as alg

SIZE = 8
O_SIZE = 60
LIGHT_COLOR = "#FFFFFF"
DARK_COLOR = "#DCDCDC"

def chessboard(board, sx, sy):
    for i in range(SIZE):
        for j in range(SIZE):
            x1 = sx + j * O_SIZE
            y1 = sy + i * O_SIZE
            x2 = x1 + O_SIZE
            y2 = y1 + O_SIZE
            color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
            board.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def drawcar_local(board, sx, sy, positions, color="pink", tag=""):
    board.delete(tag)
    for row, col in positions:
        x = sx + col * O_SIZE + O_SIZE // 2
        y = sy + row * O_SIZE + O_SIZE // 2
        board.create_text(x, y, text="♖", font=("Arial", 26, "bold"), fill=color, tags=tag)

def main():
    root = tk.Tk()
    root.title("Bài toán 8 quân xe")
    root.geometry("1200x700")
    root.resizable(False, False)

    left_positions = []
    right_positions = []

    # ======= FRAME CHÍNH =======
    main_frame = tk.Frame(root, bg="#f8f8f8")
    main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ======= CANVAS 2 BÀN CỜ =======
    canvas_width = SIZE * O_SIZE * 2 + 40
    canvas_height = SIZE * O_SIZE + 20
    board = tk.Canvas(main_frame, width=canvas_width, height=canvas_height, bg="#f8f8f8",
                      highlightthickness=1, highlightbackground="#aaa")
    board.pack(pady=10)

    sx_left = 10
    sx_right = SIZE * O_SIZE + 40

    chessboard(board, sx_left, 10)
    chessboard(board, sx_right, 10)

    # ======= CLICK BÀN PHẢI =======
    def on_click(event):
        x, y = event.x, event.y
        if sx_right < x < sx_right + SIZE * O_SIZE and 10 <= y < 10 + SIZE * O_SIZE:
            col = (x - sx_right) // O_SIZE
            row = (y - 10) // O_SIZE
            pos = (row, col)
            if pos in right_positions:
                right_positions.remove(pos)
                status_label.config(text="Đã xóa 1 quân ở bàn phải.")
            else:
                is_row = any(r == row for r, c in right_positions)
                is_col = any(c == col for r, c in right_positions)
                if is_row or is_col:
                    status_label.config(text="Vị trí không hợp lệ! Hàng hoặc cột đã có xe.")
                else:
                    right_positions.append(pos)
                    status_label.config(text="Đặt quân xe ở bàn phải làm goal.")
            drawcar_local(board, sx_right, 10, right_positions, color="red", tag="right_car")

    board.bind("<Button-1>", on_click)

    # ======= FRAME ĐIỀU KHIỂN BÊN PHẢI =======
    control = tk.Frame(root, width=280, bg="#f0f0f0", relief=tk.RIDGE, bd=2)
    control.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    control.pack_propagate(False)  # Giữ kích thước cố định

    # ======= Phần căn dưới =======
    bottom_frame = tk.Frame(control, bg="#f0f0f0")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

    # Combo thuật toán
    tk.Label(bottom_frame, text="Chọn thuật toán:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(0,5))
    algo_var = tk.StringVar(value="BFS")
    algorithms = [
        "BFS", "DFS", "UCS", "DLS", "IDS", "A* Search", "Greedy",
        "Hill Climbing", "Simulated Annealing", "Genetic Algorithm",
        "Beam Search", "AndOr Search", "Belief State Search",
        "Back Tracking Search", "Forward Checking Search"
    ]
    combo = ttk.Combobox(bottom_frame, values=algorithms, textvariable=algo_var, state="readonly",
                         width=28, font=("Arial", 11))
    combo.pack(pady=(0, 10))
    combo.bind("<<ComboboxSelected>>", lambda e: status_label.config(text=f"Đã chọn: {algo_var.get()}"))

    # Nút Play & Reset
    btn_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Play", width=12, bg="#4CAF50", fg="white",
              command=lambda: start()).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Reset", width=12, bg="#2196F3", fg="white",
              command=lambda: reset()).grid(row=1, column=0, padx=5, pady=5)


    chi_phi_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    chi_phi_frame.pack(pady=15, fill=tk.X)
    tk.Label(chi_phi_frame, text="Chi phí (Cost):", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
    chi_phi_label = tk.Label(chi_phi_frame, text="0", font=("Consolas", 18, "bold"), bg="#f0f0f0")
    chi_phi_label.pack()

    # Status căn giữa
    status_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    status_frame.pack(pady=5, fill=tk.X)
    status_label = tk.Label(status_frame, text="Trạng thái: Đã sẵn sàng", font=("Arial", 10, "italic"),
                            wraplength=260, justify="center", bg="#f0f0f0", fg="black")
    status_label.pack()

    # ======= Hàm điều khiển =======
    def start():
        alg.khoi_tao_context(board, status_label, chi_phi_label, sx_right, left_positions, right_positions)
        fn = alg.MAP_THUAT_TOAN.get(algo_var.get())
        if fn:
            status_label.config(text=f"Đang chạy thuật toán {algo_var.get()}...")
            fn()
        else:
            status_label.config(text="Thuật toán chưa được hỗ trợ.")

    def reset():
        alg.huy_after()
        status_label.config(text="Đã reset bàn cờ.")
        board.delete("all")
        chessboard(board, 10, 10)
        chessboard(board, sx_right, 10)
        chi_phi_label.config(text="0")
        algo_var.set("BFS")
        left_positions.clear()
        right_positions.clear()
        board.delete("left_car")
        board.delete("right_car")
        board.delete("ga_candidate")
        board.delete("beam_candidate")
        board.delete("beliefS")
        board.delete("or_branch")
        board.delete("elimination_marker")

    alg._right_positions = right_positions
    root.mainloop()

if __name__ == "__main__":
    main()
