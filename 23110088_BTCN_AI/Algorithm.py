
import random
import math
import itertools
from collections import deque

# Cấu hình chung
KICH_THUOC = 8
O_SIZE = 60

# Môi trường (sẽ được UI truyền vào)
_board = None
_trang_thai_label = None
_chi_phi_label = None
_start_x_right = None
_left_positions = None
_right_positions = None
_after_id = None

# Biến trạng thái dùng chung cho các thuật toán
_xe_xac_nhan = []
_hang_tim_hien_tai = 0
_map_goal = {}
_hang_doi = deque()
_ngan_xep = []

# Hỗ trợ: thiết lập context (UI gọi 1 lần khi khởi tạo)
def khoi_tao_context(board, trang_thai_label, chi_phi_label, start_x_right, left_positions, right_positions):
    global _board, _trang_thai_label, _chi_phi_label, _start_x_right, _left_positions, _right_positions
    _board = board
    _trang_thai_label = trang_thai_label
    _chi_phi_label = chi_phi_label
    _start_x_right = start_x_right
    _left_positions = left_positions
    _right_positions = right_positions

# Hỗ trợ hủy schedule từ UI
def huy_after():
    global _after_id
    try:
        if _after_id:
            _board.after_cancel(_after_id)
    except Exception:
        pass
    _after_id = None

# Vẽ bàn cờ (UI đã vẽ, nhưng các thuật toán dùng draw để cập nhật vị trí quân)
def ve_xe(positions, mau="red", tag="left_car", sx=0, sy=0):
    # xóa tag trước khi vẽ
    if _board is None: return
    _board.delete(tag)
    for row, col in positions:
        x = sx + col * O_SIZE + O_SIZE // 2
        y = sy + row * O_SIZE + O_SIZE // 2
        _board.create_text(x, y, text="♖", font=("Arial", 24), fill=mau, tags=tag)

# -------------------- Các hàm tiện ích chi phí / heuristic --------------------
def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def tinh_chi_phi_duong_di(path):
    if len(path) < 2: return 0
    total = 0
    for i in range(len(path) - 1):
        total += manhattan(path[i], path[i+1])
    return total

def heuristic_simple(state_len, goal_len):
    return goal_len - state_len

# -------------------- Các thuật toán (đã Việt hóa) --------------------
# Lưu ý: mỗi thuật toán sử dụng/thay đổi các biến module-level và dùng _board.after để animate.

# --- BFS ---
def bfs():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _hang_doi, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="BFS: Đang chạy...")
    animate_bfs()

def animate_bfs():
    global _after_id, _hang_tim_hien_tai, _hang_doi, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="BFS: Đã hoàn thành!"); return
    if not _hang_doi: return
    trial_col = _hang_doi.popleft()
    car = _xe_xac_nhan + [( _hang_tim_hien_tai, trial_col)]
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial_col == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_bfs)

# --- DFS ---
def dfs():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _ngan_xep, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="DFS: Đang chạy...")
    animate_dfs()

def animate_dfs():
    global _after_id, _hang_tim_hien_tai, _ngan_xep, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="DFS: Đã hoàn thành!"); return
    if not _ngan_xep: return
    trial_col = _ngan_xep.pop()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial_col == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_dfs)

# --- UCS (đơn giản dùng tổng khoảng cách Manhattan làm cost) ---
def ucs():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _hang_doi, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="UCS: Đang chạy...")
    animate_ucs()

def animate_ucs():
    global _after_id, _hang_tim_hien_tai, _hang_doi, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="UCS: Đã hoàn thành!"); return
    if not _hang_doi: return
    trial_col = _hang_doi.popleft()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    ve_xe(car, "red", "left_car")
    cost = tinh_chi_phi_duong_di(car)
    _chi_phi_label.config(text=str(cost))
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial_col == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_ucs)

# --- DLS (Depth-Limited Search) ---
def dls(limit=KICH_THUOC):
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _ngan_xep, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _trang_thai_label.config(text=f"DLS: Giới hạn {limit} - Đang chạy...")
    animate_dls(limit)

def animate_dls(limit):
    global _after_id, _hang_tim_hien_tai, _ngan_xep, _xe_xac_nhan
    if _hang_tim_hien_tai >= limit:
        _trang_thai_label.config(text=f"DLS: Đạt giới hạn độ sâu {limit}."); return
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="DLS: Đã hoàn thành!"); return
    if not _ngan_xep: return
    trial_col = _ngan_xep.pop()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    ve_xe(car, "red", "left_car")
    cost = tinh_chi_phi_duong_di(car)
    _chi_phi_label.config(text=str(cost))
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial_col == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _after_id = _board.after(120, lambda: animate_dls(limit))

# --- IDS (Iterative Deepening) ---
_ids_limit = 1
def ids():
    global _map_goal, _ids_limit, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    # bắt đầu từ 1 đến số hàng
    _trang_thai_label.config(text="IDS: Bắt đầu...")
    start_ids_iteration(1)

def start_ids_iteration(limit):
    global _ids_limit, _xe_xac_nhan, _hang_tim_hien_tai, _ngan_xep
    _ids_limit = limit
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _trang_thai_label.config(text=f"IDS: Thử limit = {limit}")
    # đợi 0.5s rồi chạy step
    _board.after(600, lambda: animate_ids_step(limit))

def animate_ids_step(limit):
    global _after_id, _hang_tim_hien_tai, _ngan_xep, _xe_xac_nhan
    if len(_xe_xac_nhan) == min(limit, len(_map_goal)):
        _trang_thai_label.config(text=f"IDS: Thành công ở độ sâu {limit}")
        if limit < len(_map_goal):
            start_ids_iteration(limit + 1)
        return
    if not _ngan_xep:
        # thất bại ở limit hiện tại -> tăng limit
        start_ids_iteration(limit + 1)
        return
    trial_col = _ngan_xep.pop()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial_col == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_ids_step, limit)

# --- A* Search (đơn giản hóa) ---
def a_star():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _hang_doi, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="A*: Đang chạy...")
    animate_a_star()

def animate_a_star():
    global _after_id, _hang_tim_hien_tai, _hang_doi, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="A*: Đã hoàn thành!"); _chi_phi_label.config(text=str(len(_xe_xac_nhan))); return
    if not _hang_doi: return
    trial_col = _hang_doi.popleft()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    # g = số quân đã chốt (+1 nếu nước thử sai)
    g = len(_xe_xac_nhan) + (0 if trial_col == _map_goal.get(_hang_tim_hien_tai) else 1)
    h = heuristic_simple(len(_xe_xac_nhan), len(_map_goal))
    _chi_phi_label.config(text=str(g))
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    if trial_col == _map_goal.get(_hang_tim_hien_tai):
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_a_star)

# --- Greedy Best-First ---
def greedy():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _ngan_xep, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="Greedy: Đang chạy...")
    animate_greedy()

def animate_greedy():
    global _after_id, _hang_tim_hien_tai, _ngan_xep, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Greedy: Đã hoàn thành!"); _chi_phi_label.config(text="0"); return
    if not _ngan_xep: return
    trial_col = _ngan_xep.pop()
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, trial_col)]
    h = heuristic_simple(len(_xe_xac_nhan), len(_map_goal))
    _chi_phi_label.config(text=str(h))
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    if trial_col == _map_goal.get(_hang_tim_hien_tai):
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _ngan_xep.clear(); _ngan_xep.extend(range(KICH_THUOC))
    _after_id = _board.after(120, animate_greedy)

# --- Hill Climbing ---
_hill_current_col = 0
def hill_climbing():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _hill_current_col, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _hill_current_col = random.randint(0, KICH_THUOC - 1)
    _trang_thai_label.config(text="Hill Climbing: Đang chạy...")
    animate_hill()

def animate_hill():
    global _after_id, _hang_tim_hien_tai, _hill_current_col, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Hill Climbing: Đã hoàn thành!"); return
    target = _map_goal.get(_hang_tim_hien_tai)
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, _hill_current_col)]
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    current_cost = abs(_hill_current_col - target)
    _chi_phi_label.config(text=str(current_cost))
    if current_cost == 0:
        _xe_xac_nhan.append((_hang_tim_hien_tai, _hill_current_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _hill_current_col = random.randint(0, KICH_THUOC - 1)
        _after_id = _board.after(200, animate_hill)
        return
    # tìm neighbor tốt hơn
    best_col = _hill_current_col
    best_cost = current_cost
    if _hill_current_col > 0:
        c = abs((_hill_current_col - 1) - target)
        if c < best_cost:
            best_cost, best_col = c, _hill_current_col - 1
    if _hill_current_col < KICH_THUOC - 1:
        c = abs((_hill_current_col + 1) - target)
        if c < best_cost:
            best_cost, best_col = c, _hill_current_col + 1
    _hill_current_col = best_col
    _after_id = _board.after(200, animate_hill)

# --- Simulated Annealing ---
_sim_current_col = 0
_temperature = 1.0
def simulated_annealing():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _sim_current_col, _temperature, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _sim_current_col = random.randint(0, KICH_THUOC - 1)
    _temperature = 10.0
    _trang_thai_label.config(text="Simulated Annealing: Đang chạy...")
    animate_simanneal()

def animate_simanneal():
    global _after_id, _hang_tim_hien_tai, _sim_current_col, _temperature, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Simulated Annealing: Đã hoàn thành!"); return
    target = _map_goal.get(_hang_tim_hien_tai)
    car = _xe_xac_nhan + [(_hang_tim_hien_tai, _sim_current_col)]
    ve_xe(car, "red", "left_car")
    _board.update_idletasks()
    energy = abs(_sim_current_col - target)
    _chi_phi_label.config(text=str(energy))
    if energy == 0:
        _xe_xac_nhan.append((_hang_tim_hien_tai, _sim_current_col))
        _hang_tim_hien_tai += 1
        if _hang_tim_hien_tai < len(_map_goal):
            _sim_current_col = random.randint(0, KICH_THUOC - 1)
            _temperature = 10.0
        _after_id = _board.after(200, animate_simanneal)
        return
    neighbors = []
    if _sim_current_col > 0: neighbors.append(_sim_current_col - 1)
    if _sim_current_col < KICH_THUOC - 1: neighbors.append(_sim_current_col + 1)
    if not neighbors:
        _after_id = _board.after(120, animate_simanneal); return
    next_col = random.choice(neighbors)
    next_energy = abs(next_col - target)
    delta = next_energy - energy
    if delta < 0 or ( _temperature > 0 and random.random() < math.exp(-delta / _temperature) ):
        _sim_current_col = next_col
    _temperature *= 0.99
    _after_id = _board.after(120, animate_simanneal)

# --- Genetic Algorithm (đơn giản, dùng cặp cột) ---
_population = []
_current_pair = ()
def genetic():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _current_pair, _after_id
    if not _right_positions or len(_right_positions) % 2 != 0:
        _trang_thai_label.config(text="Lỗi: GA cần số lượng goal chẵn!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    used = [c for r,c in _xe_xac_nhan]
    avail = [c for c in range(KICH_THUOC) if c not in used]
    _current_pair = tuple(random.sample(avail, 2))
    _trang_thai_label.config(text="Genetic Algorithm: Đang chạy...")
    animate_ga()

def animate_ga():
    global _after_id, _hang_tim_hien_tai, _current_pair, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Genetic Algorithm: Đã hoàn thành!"); return
    # cặp mục tiêu
    target1 = _map_goal.get(_hang_tim_hien_tai)
    target2 = _map_goal.get(_hang_tim_hien_tai + 1)
    if _current_pair and _current_pair[0] == target1 and _current_pair[1] == target2:
        _xe_xac_nhan.append((_hang_tim_hien_tai, _current_pair[0]))
        _xe_xac_nhan.append((_hang_tim_hien_tai+1, _current_pair[1]))
        _hang_tim_hien_tai += 2
        ve_xe(_xe_xac_nhan, "red", "left_car")
        _board.update_idletasks()
        if _hang_tim_hien_tai < len(_map_goal):
            used = [c for r,c in _xe_xac_nhan]
            avail = [c for c in range(KICH_THUOC) if c not in used]
            _current_pair = tuple(random.sample(avail, 2))
            _after_id = _board.after(400, animate_ga)
        else:
            _trang_thai_label.config(text="Genetic Algorithm: Đã hoàn thành!")
        return
    # tạo dân số ngẫu nhiên (các cặp)
    used = [c for r,c in _xe_xac_nhan]
    avail = [c for c in range(KICH_THUOC) if c not in used]
    all_pairs = list(itertools.combinations(avail, 2))
    pop_size = min(len(all_pairs), 10)
    if pop_size == 0:
        _trang_thai_label.config(text="GA: Không còn cột khả dĩ."); return
    population = random.sample(all_pairs, pop_size)
    # đánh giá fitness: càng gần target càng tốt
    best = None; best_fit = -1
    for p in population:
        f1 = KICH_THUOC - abs(p[0] - target1)
        f2 = KICH_THUOC - abs(p[1] - target2)
        fit = f1 + f2
        if fit > best_fit:
            best_fit, best = fit, p
    _current_pair = best
    cost = abs(best[0] - target1) + abs(best[1] - target2)
    _chi_phi_label.config(text=str(cost))
    # vẽ các candidate tạm thời
    cand = [(_hang_tim_hien_tai, best[0]), (_hang_tim_hien_tai+1, best[1])]
    ve_xe(_xe_xac_nhan, "red", "left_car")
    ve_xe(cand, "#007BFF", "ga_candidate")
    _board.update_idletasks()
    _board.after(300, lambda: _board.delete("ga_candidate"))
    _after_id = _board.after(600, animate_ga)

# --- Beam Search ---
_BEAM_WIDTH = 3
def beam():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _trang_thai_label.config(text="Beam Search: Đang chạy...")
    animate_beam()

def animate_beam():
    global _after_id, _hang_tim_hien_tai, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Beam Search: Đã hoàn thành!"); return
    target = _map_goal.get(_hang_tim_hien_tai)
    used = [c for r,c in _xe_xac_nhan]
    avail = [c for c in range(KICH_THUOC) if c not in used]
    candidates = [(abs(c - target), c) for c in avail]
    candidates.sort(key=lambda x: x[0])
    beam = candidates[:_BEAM_WIDTH]
    beam_positions = [(_hang_tim_hien_tai, c) for _, c in beam]
    ve_xe(_xe_xac_nhan, "red", "left_car")
    ve_xe(beam_positions, "#007BFF", "beam_candidate")
    _chi_phi_label.config(text=str(beam[0][0] if beam else 0))
    _board.update_idletasks()
    # chốt best
    best_col = beam[0][1]
    _after_id = _board.after(400, lambda: finalize_beam(best_col))

def finalize_beam(col):
    global _after_id, _hang_tim_hien_tai, _xe_xac_nhan
    _board.delete("beam_candidate")
    _xe_xac_nhan.append((_hang_tim_hien_tai, col))
    _hang_tim_hien_tai += 1
    ve_xe(_xe_xac_nhan, "red", "left_car")
    _board.update_idletasks()
    _after_id = _board.after(200, animate_beam)

# --- AND-OR (mô phỏng đơn giản) ---
def andor():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _hang_doi, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
    _trang_thai_label.config(text="AND-OR: Đang chạy...")
    animate_andor()

def animate_andor():
    global _after_id, _hang_tim_hien_tai, _hang_doi, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="AND-OR: Đã hoàn thành!"); return
    if not _hang_doi: return
    trial = _hang_doi.popleft()
    ve_xe(_xe_xac_nhan, "red", "left_car")
    ve_xe([(_hang_tim_hien_tai, trial)], "#007BFF", "or_branch")
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    if trial == target:
        _xe_xac_nhan.append((_hang_tim_hien_tai, trial))
        _hang_tim_hien_tai += 1
        _board.delete("or_branch")
        ve_xe(_xe_xac_nhan, "red", "left_car")
        if _hang_tim_hien_tai < len(_map_goal):
            _hang_doi.clear(); _hang_doi.extend(range(KICH_THUOC))
        _after_id = _board.after(400, animate_andor)
    else:
        _after_id = _board.after(120, animate_andor)

# --- Belief State (minh họa) ---
def belief_state():
    global _xe_xac_nhan, _hang_tim_hien_tai, _map_goal, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _xe_xac_nhan, _hang_tim_hien_tai = [], 0
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    _trang_thai_label.config(text="Belief State: Đang chạy...")
    animate_belief()

def animate_belief():
    global _after_id, _hang_tim_hien_tai, _xe_xac_nhan
    if len(_xe_xac_nhan) == len(_map_goal):
        _trang_thai_label.config(text="Belief State: Đã hoàn thành!"); return
    used = [c for r,c in _xe_xac_nhan]
    belief = [c for c in range(KICH_THUOC) if c not in used]
    positions = [(_hang_tim_hien_tai, c) for c in belief]
    ve_xe(_xe_xac_nhan, "red", "left_car")
    ve_xe(positions, "#CCCCCC", "beliefS")
    _board.update_idletasks()
    target = _map_goal.get(_hang_tim_hien_tai)
    _after_id = _board.after(600, lambda: finalize_belief(target))

def finalize_belief(col):
    global _after_id, _hang_tim_hien_tai, _xe_xac_nhan
    _board.delete("beliefS")
    _xe_xac_nhan.append((_hang_tim_hien_tai, col))
    _hang_tim_hien_tai += 1
    ve_xe(_xe_xac_nhan, "red", "left_car")
    _chi_phi_label.config(text=str(len(_xe_xac_nhan)))
    _board.update_idletasks()
    _after_id = _board.after(200, animate_belief)

# --- Backtracking (đệ quy có animation) ---
def an_toa_do(positions):
    return {r: c for r, c in enumerate(positions)}

def check_safe(path, row, col):
    # chỉ kiểm tra cùng cột (theo yêu cầu code gốc), không kiểm tra đường chéo
    for idx, c in enumerate(path):
        if c == col:
            return False
    return True

def backtracking():
    global _map_goal, _xe_xac_nhan, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _trang_thai_label.config(text="Backtracking: Đang chạy...")
    _xe_xac_nhan = []
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    # bắt đầu recursion với path rỗng
    animate_backtracking_step([])

def animate_backtracking_step(path):
    global _after_id
    positions_to_draw = [(r, c) for r, c in enumerate(path)]
    ve_xe(positions_to_draw, "red", "left_car")
    _chi_phi_label.config(text=str(len(path)))
    _board.update_idletasks()
    if len(path) == KICH_THUOC:
        if {r: c for r, c in enumerate(path)} == _map_goal:
            _trang_thai_label.config(text="Backtracking: Đã tìm thấy goal!")
            return True
        else:
            return False
    next_row = len(path)
    for col in range(KICH_THUOC):
        trial = positions_to_draw + [(next_row, col)]
        ve_xe(trial, "red", "left_car")
        _board.update_idletasks()
        _board.after(50)
        if check_safe(path, next_row, col):
            found = animate_backtracking_step(path + [col])
            if found:
                return True
            # quay lui: vẽ lại trạng thái cũ
            ve_xe(positions_to_draw, "red", "left_car")
            _board.update_idletasks()
            _board.after(50)
    return False

# --- Forward Checking ---
def forward_checking():
    global _map_goal, _xe_xac_nhan, _after_id
    if not _right_positions:
        _trang_thai_label.config(text="Lỗi: Hãy đặt mục tiêu ở bàn phải!"); return
    huy_after()
    _trang_thai_label.config(text="Forward Checking: Đang chạy...")
    _xe_xac_nhan = []
    _map_goal = {r: c for r, c in sorted(_right_positions)}
    domains = {r: list(range(KICH_THUOC)) for r in range(KICH_THUOC)}
    animate_forward_step([], domains)

def draw_eliminations(positions):
    _board.delete("elimination_marker")
    for row, col in positions:
        x = col * O_SIZE + O_SIZE // 2
        y = row * O_SIZE + O_SIZE // 2
        _board.create_text(x, y, text="✕", font=("Arial", 20), fill="#555555", tags="elimination_marker")

def animate_forward_step(path, domains):
    positions_to_draw = [(r, c) for r, c in enumerate(path)]
    ve_xe(positions_to_draw, "red", "left_car")
    _chi_phi_label.config(text=str(len(path)))
    eliminated = []
    for r in range(len(path), KICH_THUOC):
        for c in range(KICH_THUOC):
            if c not in domains[r]:
                eliminated.append((r, c))
    draw_eliminations(eliminated)
    _board.update_idletasks()
    if len(path) == KICH_THUOC:
        if {r: c for r, c in enumerate(path)} == _map_goal:
            _trang_thai_label.config(text="Forward Checking: Đã tìm thấy goal!"); return True
        else:
            return False
    next_row = len(path)
    for col in list(domains[next_row]):
        # copy domains
        new_dom = {r: list(d) for r, d in domains.items()}
        for r_future in range(next_row + 1, KICH_THUOC):
            if col in new_dom[r_future]:
                new_dom[r_future].remove(col)
        is_dead = any(not new_dom[r] for r in range(next_row + 1, KICH_THUOC))
        if not is_dead:
            found = animate_forward_step(path + [col], new_dom)
            if found:
                return True
    return False

# -------------------- Map between tên hiển thị và hàm --------------------
MAP_THUAT_TOAN = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "DLS": dls,
    "IDS": ids,
    "A* Search": a_star,
    "Greedy": greedy,
    "Hill Climbing": hill_climbing,
    "Simulated Annealing": simulated_annealing,
    "Genetic Algorithm": genetic,
    "Beam Search": beam,
    "AndOr Search": andor,
    "Belief State Search": belief_state,
    "Back Tracking Search": backtracking,
    "Forward Checking Search": forward_checking
}
