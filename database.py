import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="linhkien_maytinh"
        )
    
    def get_connection(self):
        if not self.conn.is_connected():
            self.conn.reconnect()
        return self.conn
    
    def close(self):
        if self.conn.is_connected():
            self.conn.close()

    def fetch_all_linh_kien(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM linh_kien")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def fetch_linh_kien_by_keyword(self, keyword):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM linh_kien WHERE ten LIKE %s OR loai LIKE %s"
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_linh_kien(self, ten, loai, so_luong, gia):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO linh_kien (ten, loai, so_luong, gia) VALUES (%s, %s, %s, %s)",
            (ten, loai, int(so_luong), float(gia))
        )
        conn.commit()
        conn.close()

    def update_linh_kien(self, id, ten, loai, so_luong, gia):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE linh_kien SET ten=%s, loai=%s, so_luong=%s, gia=%s WHERE id=%s",
            (ten, loai, int(so_luong), float(gia), id)
        )
        conn.commit()
        conn.close()

    def delete_linh_kien(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM linh_kien WHERE id = %s", (id,))
        conn.commit()
        conn.close()

    def get_linh_kien_for_sale(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, ten, gia FROM linh_kien")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_linh_kien_details(self, id_linh_kien):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gia, so_luong FROM linh_kien WHERE id = %s", (id_linh_kien,))
        result = cursor.fetchone()
        conn.close()
        return result

    def ban_hang(self, id_linh_kien, so_luong, gia):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ban_hang (id_linh_kien, so_luong, gia) VALUES (%s, %s, %s)",
            (id_linh_kien, int(so_luong), float(gia))
        )
        cursor.execute(
            "UPDATE linh_kien SET so_luong = so_luong - %s WHERE id = %s",
            (int(so_luong), id_linh_kien)
        )
        conn.commit()
        conn.close()

    def get_thong_ke_loai(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT loai, SUM(so_luong) FROM linh_kien GROUP BY loai")
        result = cursor.fetchall()
        conn.close()
        return result

    def get_doanh_thu_loai(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT lk.loai, SUM(bh.gia) 
            FROM ban_hang bh 
            JOIN linh_kien lk ON bh.id_linh_kien = lk.id 
            GROUP BY lk.loai
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    # Thêm phương thức lấy lịch sử bán hàng
    def get_lich_su_ban_hang(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bh.id, lk.ten, bh.so_luong, bh.gia, lk.loai
            FROM ban_hang bh
            JOIN linh_kien lk ON bh.id_linh_kien = lk.id
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    # Thêm phương thức lấy lịch sử nhập hàng
    def get_lich_su_nhap_hang(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nh.id, lk.ten, nh.so_luong, nh.gia, nh.ngay_nhap, lk.loai
            FROM nhap_hang nh
            JOIN linh_kien lk ON nh.id_linh_kien = lk.id
        """)
        result = cursor.fetchall()
        conn.close()
        return result