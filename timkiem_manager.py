import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TimKiemManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.selected_id = None  # Định nghĩa selected_id trong lớp
        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.frame_search = tk.Frame(self.frame)
        self.frame_search.pack(pady=10)

        tk.Label(self.frame_search, text="Tìm theo tên hoặc loại:").pack(side=tk.LEFT, padx=5)
        self.entry_search = tk.Entry(self.frame_search)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        tk.Button(self.frame_search, text="Tìm", command=self.search_data).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_search, text="Hiển thị tất cả", command=self.fetch_data).pack(side=tk.LEFT, padx=5)

        self.cols = ("ID", "Tên", "Loại", "Số lượng", "Giá")
        self.tree_search = ttk.Treeview(self.frame, columns=self.cols, show="headings")
        for col in self.cols:
            self.tree_search.heading(col, text=col)
            self.tree_search.column(col, width=120)
        self.tree_search.pack(fill=tk.BOTH, expand=True)
        self.tree_search.bind("<<TreeviewSelect>>", self.on_tree_select)

    def fetch_data(self):
        for row in self.tree_search.get_children():
            self.tree_search.delete(row)
        rows = self.db.fetch_all_linh_kien()
        for row in rows:
            formatted_row = list(row)
            formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
            self.tree_search.insert("", tk.END, values=formatted_row)

    def search_data(self):
        keyword = self.entry_search.get()
        for row in self.tree_search.get_children():
            self.tree_search.delete(row)
        rows = self.db.fetch_linh_kien_by_keyword(keyword)
        for row in rows:
            formatted_row = list(row)
            formatted_row[4] = "{:,.0f} VNĐ".format(row[4]).replace(",", ".")
            self.tree_search.insert("", tk.END, values=formatted_row)

    def on_tree_select(self):
        selected = self.tree_search.selection()
        if selected:
            values = self.tree_search.item(selected[0])["values"]
            self.selected_id = values[0]