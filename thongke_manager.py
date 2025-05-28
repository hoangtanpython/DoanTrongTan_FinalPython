import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ThongKeManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.canvas1 = None
        self.canvas2 = None
        self.setup_ui()

    def setup_ui(self):
        # Frame chính với nền trắng
        self.main_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame cho biểu đồ và nút
        self.chart_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        # Nút làm mới biểu đồ và lịch sử
        button_frame = tk.Frame(self.chart_frame, bg="#ffffff")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Làm mới biểu đồ", command=self.ve_bieu_do, bg="#4a90e2", fg="white", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Làm mới lịch sử", command=self.update_history, bg="#50c878", fg="white", font=("Arial", 10), padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        # Frame cho lịch sử
        self.history_frame = tk.Frame(self.main_frame, bg="#ffffff")
        self.history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Bảng lịch sử bán hàng
        self.ban_hang_frame = tk.Frame(self.history_frame, bg="#ffffff")
        self.ban_hang_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5)

        tk.Label(self.ban_hang_frame, text="Lịch sử bán hàng", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=5)
        self.ban_hang_tree = ttk.Treeview(self.ban_hang_frame, columns=("ID", "Tên", "Loại", "Số lượng", "Tổng tiền"), show="headings", height=5)
        self.ban_hang_tree.heading("ID", text="ID")
        self.ban_hang_tree.heading("Tên", text="Tên")
        self.ban_hang_tree.heading("Loại", text="Loại")
        self.ban_hang_tree.heading("Số lượng", text="Số lượng")
        self.ban_hang_tree.heading("Tổng tiền", text="Tổng tiền")
        for col in ("ID", "Tên", "Loại", "Số lượng", "Tổng tiền"):
            self.ban_hang_tree.column(col, width=100)
        self.ban_hang_tree.pack(fill=tk.BOTH, expand=True)

        # Bảng lịch sử nhập hàng
        self.nhap_hang_frame = tk.Frame(self.history_frame, bg="#ffffff")
        self.nhap_hang_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5)

        tk.Label(self.nhap_hang_frame, text="Lịch sử nhập hàng", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=5)
        self.nhap_hang_tree = ttk.Treeview(self.nhap_hang_frame, columns=("ID", "Tên", "Loại", "Số lượng", "Tổng tiền", "Ngày nhập"), show="headings", height=5)
        self.nhap_hang_tree.heading("ID", text="ID")
        self.nhap_hang_tree.heading("Tên", text="Tên")
        self.nhap_hang_tree.heading("Loại", text="Loại")
        self.nhap_hang_tree.heading("Số lượng", text="Số lượng")
        self.nhap_hang_tree.heading("Tổng tiền", text="Tổng tiền")
        self.nhap_hang_tree.heading("Ngày nhập", text="Ngày nhập")
        for col in ("ID", "Tên", "Loại", "Số lượng", "Tổng tiền", "Ngày nhập"):
            self.nhap_hang_tree.column(col, width=100)
        self.nhap_hang_tree.pack(fill=tk.BOTH, expand=True)

        # Gọi lần đầu để hiển thị dữ liệu
        self.ve_bieu_do()
        self.update_history()

    def ve_bieu_do(self):
        if self.canvas1:
            self.canvas1.get_tk_widget().destroy()
        if self.canvas2:
            self.canvas2.get_tk_widget().destroy()

        # Biểu đồ cột: Số lượng linh kiện theo loại
        data1 = self.db.get_thong_ke_loai()
        loai_list = [item[0] for item in data1]
        so_luong_list = [item[1] for item in data1]

        fig1, ax1 = plt.subplots(figsize=(5, 4))  # Tăng kích thước
        ax1.bar(loai_list, so_luong_list, color='#4a90e2', edgecolor='black')
        ax1.set_title("Số lượng linh kiện theo loại", fontsize=12, pad=15)
        ax1.set_xlabel("Loại", fontsize=10)
        ax1.set_ylabel("Số lượng", fontsize=10)
        plt.xticks(rotation=45, ha="right")

        self.canvas1 = FigureCanvasTkAgg(fig1, master=self.chart_frame)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=tk.LEFT, padx=20, pady=10)

        # Biểu đồ tròn: Doanh thu theo loại linh kiện
        data2 = self.db.get_doanh_thu_loai()
        loai_list2 = [item[0] for item in data2]
        doanh_thu_list = [item[1] for item in data2]

        fig2, ax2 = plt.subplots(figsize=(5, 4))  # Tăng kích thước
        ax2.pie(doanh_thu_list, labels=loai_list2, autopct='%1.1f%%', startangle=90, colors=['#50c878', '#f5a623', '#e94e77', '#4a90e2'])
        ax2.set_title("Tỉ lệ doanh thu theo loại linh kiện", fontsize=12, pad=15)

        self.canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_frame)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=tk.RIGHT, padx=20, pady=10)

    def update_history(self):
        # Cập nhật lịch sử bán hàng
        for row in self.ban_hang_tree.get_children():
            self.ban_hang_tree.delete(row)
        ban_hang_data = self.db.get_lich_su_ban_hang()
        for row in ban_hang_data:
            id, ten, so_luong, gia, loai = row
            formatted_gia = f"{gia:,.0f} VNĐ".replace(",", ".")
            self.ban_hang_tree.insert("", tk.END, values=(id, ten, loai, so_luong, formatted_gia))

        # Cập nhật lịch sử nhập hàng
        for row in self.nhap_hang_tree.get_children():
            self.nhap_hang_tree.delete(row)
        nhap_hang_data = self.db.get_lich_su_nhap_hang()
        for row in nhap_hang_data:
            id, ten, so_luong, gia, ngay_nhap, loai = row
            formatted_gia = f"{gia:,.0f} VNĐ".replace(",", ".")
            self.nhap_hang_tree.insert("", tk.END, values=(id, ten, loai, so_luong, formatted_gia, ngay_nhap))