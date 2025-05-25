import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Biến toàn cục
selected_id = None

# Hàm kết nối CSDL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="linhkien_maytinh"
    )

# Hàm lấy và hiển thị dữ liệu
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM linh_kien")
    rows = cursor.fetchall()
    for row in rows:
        formatted_row = list(row)
        formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
        tree.insert("", tk.END, values=formatted_row)
    conn.close()

def on_tree_select(event):
    global selected_id
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])["values"]
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, values[1])
        entry_loai.delete(0, tk.END)
        entry_loai.insert(0, values[2])
        entry_soluong.delete(0, tk.END)
        entry_soluong.insert(0, values[3])
        gia_str = str(values[4]).replace(".", "").replace(" VNĐ", "")
        entry_gia.delete(0, tk.END)
        entry_gia.insert(0, gia_str)
        selected_id = values[0]

def search_data(keyword):
    for row in tree_search.get_children():
        tree_search.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM linh_kien WHERE ten LIKE %s OR loai LIKE %s"
    like_keyword = f"%{keyword}%"
    cursor.execute(query, (like_keyword, like_keyword))
    rows = cursor.fetchall()
    for row in rows:
        formatted_row = list(row)
        formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
        tree_search.insert("", tk.END, values=formatted_row)
    conn.close()

def add_linh_kien():
    ten = entry_ten.get()
    loai = entry_loai.get()
    soluong = entry_soluong.get()
    gia = entry_gia.get()
    if not ten or not loai or not soluong or not gia:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO linh_kien (ten, loai, so_luong, gia) VALUES (%s, %s, %s, %s)",
            (ten, loai, int(soluong), float(gia))
        )
        conn.commit()
        conn.close()
        fetch_data()
        entry_ten.delete(0, tk.END)
        entry_loai.delete(0, tk.END)
        entry_soluong.delete(0, tk.END)
        entry_gia.delete(0, tk.END)
        messagebox.showinfo("Thành công", "Đã thêm linh kiện.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thêm được dữ liệu.\n{e}")

def update_linh_kien():
    global selected_id
    try:
        id = selected_id
        ten = entry_ten.get()
        loai = entry_loai.get()
        soluong = int(entry_soluong.get())
        gia = float(entry_gia.get())
        if not ten or not loai:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE linh_kien SET ten=%s, loai=%s, so_luong=%s, gia=%s WHERE id=%s",
            (ten, loai, soluong, gia, id)
        )
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Thành công", "Đã cập nhật linh kiện.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật.\n{e}")

def delete_linh_kien():
    global selected_id
    try:
        if selected_id is None:
            messagebox.showwarning("Chưa chọn linh kiện", "Vui lòng chọn một linh kiện để xóa từ bảng.")
            return
        id = selected_id
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa linh kiện với ID {id}?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM linh_kien WHERE id = %s", (id,))
            conn.commit()
            conn.close()
            fetch_data()
            messagebox.showinfo("Đã xóa", "Linh kiện đã được xóa.")
            entry_ten.delete(0, tk.END)
            entry_loai.delete(0, tk.END)
            entry_soluong.delete(0, tk.END)
            entry_gia.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa.\nChi tiết: {str(e)}")

# Hàm xử lý bán hàng trong tab
def ban_hang():
    # --- Danh sách lưu ID và thông tin linh kiện ---
    linh_kien_list = []

    # --- Thanh tìm kiếm và combobox chọn linh kiện ---
    search_frame = tk.Frame(tab4)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Tìm linh kiện:").pack(side=tk.LEFT, padx=5)
    entry_search_bh = tk.Entry(search_frame)
    entry_search_bh.pack(side=tk.LEFT, padx=5)

    combo_linh_kien = ttk.Combobox(tab4, state="readonly")
    combo_linh_kien.pack(pady=5)

    # Hàm cập nhật danh sách combobox dựa trên từ khóa
    def cap_nhat_combobox_ban_hang(keyword=""):
        nonlocal linh_kien_list  # ❌ Đừng dùng dòng này — XÓA nó đi
        conn = connect_db()
        cursor = conn.cursor()
        like_kw = f"%{keyword}%"
        cursor.execute("SELECT id, ten, gia FROM linh_kien WHERE ten LIKE %s OR loai LIKE %s", (like_kw, like_kw))
        rows = cursor.fetchall()
        conn.close()

        linh_kien_list.clear()
        for row in rows:
            display = f"{row[1]} (Giá: {row[2]:,.0f} VNĐ)".replace(",", ".")
            linh_kien_list.append((row[0], display))

        combo_linh_kien['values'] = [item[1] for item in linh_kien_list]
        if linh_kien_list:
            combo_linh_kien.current(0)
        else:
            combo_linh_kien.set("")
            tong_tien.set("0 VNĐ")

    cap_nhat_combobox_ban_hang()  # Gọi khi mở tab

    # Nút tìm kiếm
    btn_tim_bh = tk.Button(search_frame, text="Tìm", command=lambda: cap_nhat_combobox_ban_hang(entry_search_bh.get()))
    btn_tim_bh.pack(side=tk.LEFT, padx=5)

    # Các phần tiếp theo: số lượng, tổng tiền, nút bán ...



    # Ô nhập số lượng
    tk.Label(tab4, text="Số lượng:").pack(pady=5)
    entry_so_luong = tk.Entry(tab4)
    entry_so_luong.pack(pady=5)

    # Hiển thị tổng tiền
    def update_tong_tien():
        try:
            so_luong = int(entry_so_luong.get())
            selected_item = combo_linh_kien.get()
            id_linh_kien = next(item[0] for item in linh_kien_list if item[1] == selected_item)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT gia FROM linh_kien WHERE id = %s", (id_linh_kien,))
            gia = cursor.fetchone()[0]
            conn.close()
            tong_tien.set(f"{so_luong * gia:,.0f} VNĐ".replace(",", "."))
        except (ValueError, IndexError):
            tong_tien.set("0 VNĐ")

    tong_tien = tk.StringVar(value="0 VNĐ")
    tk.Label(tab4, text="Tổng tiền:").pack(pady=5)
    tk.Label(tab4, textvariable=tong_tien).pack(pady=5)

    # Cập nhật tổng tiền khi nhập số lượng hoặc thay đổi linh kiện
    entry_so_luong.bind("<KeyRelease>", lambda e: update_tong_tien())
    combo_linh_kien.bind("<<ComboboxSelected>>", lambda e: update_tong_tien())

    # Hàm xác nhận bán
    def confirm_ban():
        try:
            so_luong = int(entry_so_luong.get())
            selected_item = combo_linh_kien.get()
            id_linh_kien = next(item[0] for item in linh_kien_list if item[1] == selected_item)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT gia, so_luong FROM linh_kien WHERE id = %s", (id_linh_kien,))
            gia, so_luong_trong_kho = cursor.fetchone()
            if so_luong > so_luong_trong_kho:
                messagebox.showwarning("Lỗi", "Số lượng bán vượt quá số lượng trong kho!")
                return
            tong = so_luong * gia
            cursor.execute(
                "INSERT INTO ban_hang (id_linh_kien, so_luong, gia) VALUES (%s, %s, %s)",
                (id_linh_kien, so_luong, tong)
            )
            cursor.execute(
                "UPDATE linh_kien SET so_luong = so_luong - %s WHERE id = %s",
                (so_luong, id_linh_kien)
            )
            conn.commit()
            conn.close()
            fetch_data()  # Cập nhật bảng trong tab chính
            messagebox.showinfo("Thành công", f"Đã bán {so_luong} linh kiện với tổng tiền {tong:,.0f} VNĐ.".replace(",", "."))
            entry_so_luong.delete(0, tk.END)  # Xóa ô số lượng sau khi bán
            update_tong_tien()  # Cập nhật lại tổng tiền
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể bán hàng.\nChi tiết: {str(e)}")

    # Nút xác nhận
    btn_confirm = tk.Button(tab4, text="Xác nhận bán", command=confirm_ban)
    btn_confirm.pack(pady=10)
    

# Tạo cửa sổ giao diện chính
root = tk.Tk()
root.title("Quản lý linh kiện máy tính")
root.geometry("800x500")

# Tạo thanh menu
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Làm mới dữ liệu", command=fetch_data)
file_menu.add_separator()
file_menu.add_command(label="Thoát", command=root.quit)

func_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Chức năng", menu=func_menu)
func_menu.add_command(label="Thêm linh kiện", command=add_linh_kien)
func_menu.add_command(label="Cập nhật linh kiện", command=update_linh_kien)
func_menu.add_command(label="Xóa linh kiện", command=delete_linh_kien)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Trợ giúp", menu=help_menu)
help_menu.add_command(label="Hướng dẫn", command=lambda: messagebox.showinfo("Hướng dẫn", "Hãy chọn một tab để quản lý linh kiện!"))
help_menu.add_command(label="Về phần mềm", command=lambda: messagebox.showinfo("Về phần mềm", "Phần mềm Quản lý linh kiện máy tính - Version 1.0"))

# Tạo Notebook cho các tab
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill=tk.BOTH)

# Tab 1: Danh sách linh kiện
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Danh sách linh kiện")

cols = ("ID", "Tên", "Loại", "Số lượng", "Giá")
tree = ttk.Treeview(tab1, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

frame_form = tk.Frame(tab1)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Tên").grid(row=0, column=0, padx=5)
entry_ten = tk.Entry(frame_form)
entry_ten.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Loại").grid(row=0, column=2, padx=5)
entry_loai = tk.Entry(frame_form)
entry_loai.grid(row=0, column=3, padx=5)

tk.Label(frame_form, text="Số lượng").grid(row=1, column=0, padx=5)
entry_soluong = tk.Entry(frame_form)
entry_soluong.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Giá").grid(row=1, column=2, padx=5)
entry_gia = tk.Entry(frame_form)
entry_gia.grid(row=1, column=3, padx=5)

btn_add = tk.Button(tab1, text="Thêm linh kiện", command=add_linh_kien)
btn_add.pack(pady=5)
btn_update = tk.Button(tab1, text="Cập nhật linh kiện", command=update_linh_kien)
btn_update.pack(pady=5)
btn_delete = tk.Button(tab1, text="Xóa linh kiện", command=delete_linh_kien)
btn_delete.pack(pady=5)
btn_refresh = tk.Button(tab1, text="Làm mới dữ liệu", command=fetch_data)
btn_refresh.pack(pady=5)

# Tab 2: Tìm kiếm linh kiện
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tìm kiếm linh kiện")

frame_search = tk.Frame(tab2)
frame_search.pack(pady=10)

tk.Label(frame_search, text="Tìm theo tên hoặc loại:").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(frame_search, text="Tìm", command=lambda: search_data(entry_search.get()))
btn_search.pack(side=tk.LEFT, padx=5)

btn_show_all = tk.Button(frame_search, text="Hiển thị tất cả", command=fetch_data)
btn_show_all.pack(side=tk.LEFT, padx=5)

tree_search = ttk.Treeview(tab2, columns=cols, show="headings")
for col in cols:
    tree_search.heading(col, text=col)
    tree_search.column(col, width=120)
tree_search.pack(fill=tk.BOTH, expand=True)
tree_search.bind("<<TreeviewSelect>>", on_tree_select)

# Tab 3: Thống kê

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Thống kê")

canvas1 = None
canvas2 = None

def ve_bieu_do():
    global canvas1, canvas2

    # Xóa các biểu đồ cũ nếu có
    if canvas1:
        canvas1.get_tk_widget().destroy()
    if canvas2:
        canvas2.get_tk_widget().destroy()

    conn = connect_db()
    cursor = conn.cursor()

    # Biểu đồ cột: Số lượng linh kiện theo loại
    cursor.execute("SELECT loai, SUM(so_luong) FROM linh_kien GROUP BY loai")
    data1 = cursor.fetchall()
    loai_list = [item[0] for item in data1]
    so_luong_list = [item[1] for item in data1]

    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.bar(loai_list, so_luong_list, color='skyblue')
    ax1.set_title("Số lượng linh kiện theo loại")
    ax1.set_xlabel("Loại")
    ax1.set_ylabel("Số lượng")

    canvas1 = FigureCanvasTkAgg(fig1, master=tab3)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, padx=10)

    # Biểu đồ tròn: Doanh thu theo loại linh kiện
    cursor.execute("""
        SELECT lk.loai, SUM(bh.gia) 
        FROM ban_hang bh 
        JOIN linh_kien lk ON bh.id_linh_kien = lk.id 
        GROUP BY lk.loai
    """)
    data2 = cursor.fetchall()
    loai_list2 = [item[0] for item in data2]
    doanh_thu_list = [item[1] for item in data2]

    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.pie(doanh_thu_list, labels=loai_list2, autopct='%1.1f%%', startangle=90)
    ax2.set_title("Tỉ lệ doanh thu theo loại linh kiện")

    canvas2 = FigureCanvasTkAgg(fig2, master=tab3)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, padx=10)

    conn.close()

# Nút vẽ/làm mới biểu đồ
btn_thong_ke = tk.Button(tab3, text="Làm mới biểu đồ", command=ve_bieu_do)
btn_thong_ke.pack(pady=10)



# Tab 4: Bán hàng
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Bán hàng")
ban_hang()  # Gọi hàm ban_hang để tạo giao diện trong tab 4

# Lần đầu load dữ liệu
fetch_data()

# Chạy giao diện
root.mainloop()