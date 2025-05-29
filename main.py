import tkinter as tk
from tkinter import ttk
from linhkien_manager import LinhKienManager
from timkiem_manager import TimKiemManager
from banhang_manager import BanHangManager
from thongke_manager import ThongKeManager
from database import Database
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý linh kiện máy tính")
        self.root.geometry("1024x1024")  # Tăng kích thước cửa sổ
        self.root.configure(bg="#f0f0f0")  # Màu nền nhạt cho cửa sổ chính

        # Áp dụng theme cho ttk
        style = ttk.Style()
        style.theme_use("clam")  # Sử dụng theme "clam" cho giao diện hiện đại

        self.db = Database()
        self.setup_notebook()
        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.root, bg="#4a90e2", fg="white")  # Màu xanh dương cho menu
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg="#4a90e2", fg="white")
        menubar.add_cascade(label="File", menu=file_menu)
        # file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg="#4a90e2", fg="white")
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Hướng dẫn", command=lambda: messagebox.showinfo("Hướng dẫn", "Hãy chọn một tab để quản lý linh kiện!"))
        help_menu.add_command(label="Về phần mềm", command=lambda: messagebox.showinfo("Về phần mềm", "Phần mềm Quản lý linh kiện máy tính - Version 1.0"))

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")  # Tùy chỉnh Notebook
        self.notebook.pack(pady=10, expand=True, fill=tk.BOTH)

        # Tùy chỉnh style cho Notebook
        style = ttk.Style()
        style.configure("Custom.TNotebook", background="#e0e0e0", foreground="#333333")
        style.configure("Custom.TNotebook.Tab", background="#4a90e2", foreground="white", padding=5)
        style.map("Custom.TNotebook.Tab", background=[("selected", "#50c878")], foreground=[("selected", "black")])

        # Tab 1: Danh sách linh kiện
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Danh sách linh kiện")
        self.linh_kien_manager = LinhKienManager(self.tab1, self.db)
        self.linh_kien_manager.fetch_data()

        # Tab 2: Tìm kiếm linh kiện
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Tìm kiếm linh kiện")
        self.tim_kiem_manager = TimKiemManager(self.tab2, self.db)
        self.tim_kiem_manager.fetch_data()

        # Tab 3: Thống kê
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Thống kê")
        self.thong_ke_manager = ThongKeManager(self.tab3, self.db)
        self.thong_ke_manager.ve_bieu_do()

        # Tab 4: Bán hàng
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text="Bán hàng")
        self.ban_hang_manager = BanHangManager(self.tab4, self.db, self.linh_kien_manager.fetch_data)
        self.ban_hang_manager.bind_events()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()