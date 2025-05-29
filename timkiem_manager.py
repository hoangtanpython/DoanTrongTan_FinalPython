import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TimKiemManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.selected_id = None
        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame tìm kiếm
        self.frame_search = tk.Frame(self.frame, bg="#ffffff")
        self.frame_search.pack(pady=10, fill=tk.X)

        font = ("Arial", 15)
        tk.Label(self.frame_search, text="Tìm theo tên hoặc loại:", font=font, bg="#ffffff", fg="#333333").pack(side=tk.LEFT, padx=5)
        self.entry_search = tk.Entry(self.frame_search, font=font, bg="#f0f0f0", width=30)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        # Gán phím Enter cho ô tìm kiếm
        self.entry_search.bind("<Return>", lambda event: self.search_data())

        # Nút chức năng với chiều dài đồng nhất
        tk.Button(self.frame_search, text="Tìm", command=self.search_data, bg="#4a90e2", fg="white", font=font, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_search, text="Hiển thị tất cả", command=self.fetch_data, bg="#50c878", fg="white", font=font, width=20).pack(side=tk.LEFT, padx=5)

        # Tùy chỉnh Treeview để đồng bộ với LinhKienManager
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#ffffff", foreground="#333333", fieldbackground="#e0e0e0")
        style.map("Custom.Treeview", background=[("selected", "#50c878")])

        self.cols = ("ID", "Tên", "Loại", "Số lượng", "Giá")
        self.tree_search = ttk.Treeview(self.frame, columns=self.cols, show="headings", style="Custom.Treeview")
        for col in self.cols:
            self.tree_search.heading(col, text=col)
            self.tree_search.column(col, width=150)
        self.tree_search.pack(fill=tk.BOTH, expand=True)
        self.tree_search.bind("<<TreeviewSelect>>", self.on_tree_select)

    def fetch_data(self):
        for row in self.tree_search.get_children():
            self.tree_search.delete(row)
        rows = self.db.fetch_all_linh_kien()
        if not rows:
            messagebox.showinfo("Thông báo", "Không có dữ liệu linh kiện để hiển thị.")
        for row in rows:
            formatted_row = list(row)
            formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
            self.tree_search.insert("", tk.END, values=formatted_row)

    def search_data(self):
        keyword = self.entry_search.get()
        for row in self.tree_search.get_children():
            self.tree_search.delete(row)
        rows = self.db.fetch_linh_kien_by_keyword(keyword)
        if not rows:
            messagebox.showinfo("Thông báo", f"Không tìm thấy linh kiện với từ khóa '{keyword}'.")
        for row in rows:
            formatted_row = list(row)
            formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
            self.tree_search.insert("", tk.END, values=formatted_row)

    def on_tree_select(self, event):
        selected = self.tree_search.selection()
        if selected:
            values = self.tree_search.item(selected[0])["values"]
            self.selected_id = values[0]