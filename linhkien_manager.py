import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LinhKienManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.selected_id = None
        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Tùy chỉnh Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffffff", foreground="#333333", fieldbackground="#e0e0e0")
        style.map("Custom.Treeview", background=[("selected", "#50c878")])

        self.cols = ("ID", "Tên", "Loại", "Số lượng", "Giá")
        self.tree = ttk.Treeview(self.frame, columns=self.cols, show="headings", style="Custom.Treeview")
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Đảm bảo gán sự kiện TreeviewSelect
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Frame cho form nhập liệu
        self.form_frame = tk.Frame(self.frame, bg="#ffffff", padx=10, pady=10)
        self.form_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Các ô nhập liệu xếp dọc
        font = ("Arial", 15)
        tk.Label(self.form_frame, text="Tên", font=font, bg="#ffffff", fg="#333333").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_ten = tk.Entry(self.form_frame, font=font, bg="#f0f0f0", width=50)
        self.entry_ten.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Loại", font=font, bg="#ffffff", fg="#333333").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_loai = tk.Entry(self.form_frame, font=font, bg="#f0f0f0", width=50)
        self.entry_loai.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Số lượng", font=font, bg="#ffffff", fg="#333333").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_soluong = tk.Entry(self.form_frame, font=font, bg="#f0f0f0", width=50)
        self.entry_soluong.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Giá", font=font, bg="#ffffff", fg="#333333").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_gia = tk.Entry(self.form_frame, font=font, bg="#f0f0f0", width=50)
        self.entry_gia.grid(row=3, column=1, padx=5, pady=5)

        # Frame cho các nút chức năng
        self.button_frame = tk.Frame(self.frame, bg="#ffffff")
        self.button_frame.pack(pady=10)

        # Các nút chức năng với chiều dài đều nhau
        tk.Button(self.button_frame, text="Thêm linh kiện", command=self.add_linh_kien, bg="#4a90e2", fg="white", font=font, width=20).pack(pady=5)
        tk.Button(self.button_frame, text="Cập nhật linh kiện", command=self.update_linh_kien, bg="#50c878", fg="white", font=font, width=20).pack(pady=5)
        tk.Button(self.button_frame, text="Xóa linh kiện", command=self.delete_linh_kien, bg="#e94e77", fg="white", font=font, width=20).pack(pady=5)

    def fetch_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.db.fetch_all_linh_kien()
        for row in rows:
            formatted_row = list(row)
            formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
            self.tree.insert("", tk.END, values=formatted_row)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.entry_ten.delete(0, tk.END)
            self.entry_ten.insert(0, values[1])
            self.entry_loai.delete(0, tk.END)
            self.entry_loai.insert(0, values[2])
            self.entry_soluong.delete(0, tk.END)
            self.entry_soluong.insert(0, values[3])
            gia_str = str(values[4]).replace(".", "").replace(" VNĐ", "")
            self.entry_gia.delete(0, tk.END)
            self.entry_gia.insert(0, gia_str)
            self.selected_id = values[0]
        else:
            self.selected_id = None

    def add_linh_kien(self):
        ten = self.entry_ten.get()
        loai = self.entry_loai.get()
        soluong = self.entry_soluong.get()
        gia = self.entry_gia.get()
        if not ten or not loai or not soluong or not gia:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            self.db.add_linh_kien(ten, loai, soluong, gia)
            self.fetch_data()
            self.entry_ten.delete(0, tk.END)
            self.entry_loai.delete(0, tk.END)
            self.entry_soluong.delete(0, tk.END)
            self.entry_gia.delete(0, tk.END)
            messagebox.showinfo("Thành công", "Đã thêm linh kiện.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thêm được dữ liệu.\n{e}")

    def update_linh_kien(self):
        if self.selected_id is None:
            messagebox.showwarning("Chưa chọn linh kiện", "Vui lòng chọn một linh kiện từ bảng để cập nhật.")
            return
        try:
            id = self.selected_id
            ten = self.entry_ten.get()
            loai = self.entry_loai.get()
            soluong = self.entry_soluong.get()
            gia = self.entry_gia.get()
            if not ten or not loai:
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin.")
                return
            self.db.update_linh_kien(id, ten, loai, soluong, gia)
            self.fetch_data()
            messagebox.showinfo("Thành công", "Đã cập nhật linh kiện.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật.\n{e}")

    def delete_linh_kien(self):
        if self.selected_id is None:
            messagebox.showwarning("Chưa chọn linh kiện", "Vui lòng chọn một linh kiện từ bảng để xóa.")
            return
        try:
            id = self.selected_id
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa linh kiện với ID {id}?")
            if confirm:
                self.db.delete_linh_kien(id)
                self.fetch_data()
                messagebox.showinfo("Đã xóa", "Linh kiện đã được xóa.")
                self.entry_ten.delete(0, tk.END)
                self.entry_loai.delete(0, tk.END)
                self.entry_soluong.delete(0, tk.END)
                self.entry_gia.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa.\nChi tiết: {str(e)}")