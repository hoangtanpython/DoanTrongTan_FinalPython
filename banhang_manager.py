import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class BanHangManager:
    def __init__(self, root, db, update_callback):
        self.root = root
        self.db = db
        self.linh_kien_list = []
        self.cart = []  # Danh sách giỏ hàng (id, tên, số lượng, giá)
        self.update_callback = update_callback
        self.setup_ui()

    def setup_ui(self):
        # Frame chính với nền trắng
        self.main_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Khu vực tìm kiếm
        self.search_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.search_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.search_frame, text="Tìm linh kiện:", bg="#ffffff", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.entry_search_bh = tk.Entry(self.search_frame, font=("Arial", 10))
        self.entry_search_bh.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(self.search_frame, text="Tìm", command=self.update_combobox, bg="#4a90e2", fg="white", font=("Arial", 10), padx=5, pady=2).pack(side=tk.LEFT, padx=5)

        # Khu vực chọn sản phẩm
        self.selection_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.selection_frame.pack(fill=tk.X, pady=5)

        self.combo_linh_kien = ttk.Combobox(self.selection_frame, state="readonly", font=("Arial", 10))
        self.combo_linh_kien.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.combo_linh_kien.bind("<<ComboboxSelected>>", lambda e: self.update_tong_tien())

        # Khu vực nhập số lượng
        self.quantity_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.quantity_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.quantity_frame, text="Số lượng:", bg="#ffffff", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.entry_so_luong = tk.Entry(self.quantity_frame, font=("Arial", 10), width=10)
        self.entry_so_luong.pack(side=tk.LEFT, padx=5)
        self.entry_so_luong.bind("<KeyRelease>", lambda e: self.update_tong_tien())

        # Khu vực tổng tiền
        self.total_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.total_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.total_frame, text="Tổng tiền:", bg="#ffffff", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.tong_tien = tk.StringVar(value="0 VNĐ")
        tk.Label(self.total_frame, textvariable=self.tong_tien, bg="#ffffff", font=("Arial", 10, "bold"), fg="#e94e77").pack(side=tk.LEFT, padx=5)

        # Khu vực nút hành động
        self.action_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.action_frame.pack(fill=tk.X, pady=5)

        tk.Button(self.action_frame, text="Thêm vào giỏ", command=self.add_to_cart, bg="#50c878", fg="white", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(self.action_frame, text="Xác nhận bán", command=self.confirm_ban, bg="#4a90e2", fg="white", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(self.action_frame, text="Hủy giỏ hàng", command=self.clear_cart, bg="#e94e77", fg="white", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        # Bảng giỏ hàng
        self.cart_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.cart_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.cart_tree = ttk.Treeview(self.cart_frame, columns=("Tên", "Số lượng", "Giá", "Thành tiền"), show="headings", height=5)
        self.cart_tree.heading("Tên", text="Tên")
        self.cart_tree.heading("Số lượng", text="Số lượng")
        self.cart_tree.heading("Giá", text="Giá")
        self.cart_tree.heading("Thành tiền", text="Thành tiền")
        for col in ("Tên", "Số lượng", "Giá", "Thành tiền"):
            self.cart_tree.column(col, width=150)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        self.update_combobox()  # Gọi khi khởi tạo

    def update_combobox(self):
        self.linh_kien_list.clear()
        conn = self.db.get_connection()
        cursor = conn.cursor()
        keyword = self.entry_search_bh.get()
        like_kw = f"%{keyword}%"
        cursor.execute("SELECT id, ten, gia FROM linh_kien WHERE ten LIKE %s OR loai LIKE %s", (like_kw, like_kw))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            display = f"{row[1]} (Giá: {row[2]:,.0f} VNĐ)".replace(",", ".")
            self.linh_kien_list.append((row[0], display))

        self.combo_linh_kien['values'] = [item[1] for item in self.linh_kien_list]
        if self.linh_kien_list:
            self.combo_linh_kien.current(0)
        else:
            self.combo_linh_kien.set("")
            self.tong_tien.set("0 VNĐ")
        self.update_tong_tien()

    def update_tong_tien(self):
        try:
            so_luong = int(self.entry_so_luong.get()) if self.entry_so_luong.get() else 0
            selected_item = self.combo_linh_kien.get()
            if selected_item:
                id_linh_kien = next(item[0] for item in self.linh_kien_list if item[1] == selected_item)
                gia = self.db.get_linh_kien_details(id_linh_kien)[0]
                self.tong_tien.set(f"{so_luong * gia:,.0f} VNĐ".replace(",", "."))
        except (ValueError, IndexError, TypeError):
            self.tong_tien.set("0 VNĐ")

    def add_to_cart(self):
        try:
            so_luong = int(self.entry_so_luong.get())
            if so_luong <= 0:
                messagebox.showwarning("Lỗi", "Số lượng phải lớn hơn 0!")
                return
            selected_item = self.combo_linh_kien.get()
            if not selected_item:
                messagebox.showwarning("Lỗi", "Vui lòng chọn linh kiện!")
                return
            id_linh_kien = next(item[0] for item in self.linh_kien_list if item[1] == selected_item)
            gia, so_luong_trong_kho = self.db.get_linh_kien_details(id_linh_kien)
            if so_luong > so_luong_trong_kho:
                messagebox.showwarning("Lỗi", "Số lượng vượt quá số lượng trong kho!")
                return
            ten = selected_item.split(" (Giá:")[0]
            thanh_tien = so_luong * gia
            self.cart.append((id_linh_kien, ten, so_luong, gia, thanh_tien))
            self.update_cart_display()
            self.entry_so_luong.delete(0, tk.END)
            self.tong_tien.set("0 VNĐ")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm vào giỏ.\nChi tiết: {str(e)}")

    def update_cart_display(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        tong_tien_tat_ca = 0
        for item in self.cart:
            id_linh_kien, ten, so_luong, gia, thanh_tien = item
            formatted_gia = f"{gia:,.0f} VNĐ".replace(",", ".")
            formatted_thanh_tien = f"{thanh_tien:,.0f} VNĐ".replace(",", ".")
            self.cart_tree.insert("", tk.END, values=(ten, so_luong, formatted_gia, formatted_thanh_tien))
            tong_tien_tat_ca += thanh_tien
        self.tong_tien.set(f"{tong_tien_tat_ca:,.0f} VNĐ".replace(",", "."))

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()
        self.entry_so_luong.delete(0, tk.END)
        self.tong_tien.set("0 VNĐ")
        messagebox.showinfo("Thông báo", "Giỏ hàng đã được xóa.")

    def confirm_ban(self):
        if not self.cart:
            messagebox.showwarning("Lỗi", "Giỏ hàng trống! Vui lòng thêm linh kiện.")
            return
        try:
            for id_linh_kien, ten, so_luong, gia, thanh_tien in self.cart:
                self.db.ban_hang(id_linh_kien, so_luong, thanh_tien)
            if self.update_callback:
                self.update_callback()
            tong_tien_tat_ca = sum(item[4] for item in self.cart)
            messagebox.showinfo("Thành công", f"Đã bán tất cả linh kiện với tổng tiền {tong_tien_tat_ca:,.0f} VNĐ.".replace(",", "."))
            self.clear_cart()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể bán hàng.\nChi tiết: {str(e)}")

    def bind_events(self):
        self.entry_so_luong.bind("<KeyRelease>", lambda e: self.update_tong_tien())
        self.combo_linh_kien.bind("<<ComboboxSelected>>", lambda e: self.update_tong_tien())