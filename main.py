import tkinter as tk
from tkinter import messagebox
import hashlib
from mysql_conn import MySQLConnection
from user_list import user_list

# 创建数据库连接
sql = MySQLConnection()
conn = sql.conn


def hash_password(password):
    # 创建MD5哈希对象
    md5_hash = hashlib.md5()

    # 将密码转换为字节串并进行哈希处理
    md5_hash.update(password.encode('utf-8'))

    # 获取哈希值的十六进制表示
    hashed_password = md5_hash.hexdigest()

    return hashed_password


def validate_input():
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if not entered_username or not entered_password:
        messagebox.showerror("输入错误", "用户名和密码不能为空。")
        return False

    return True


def check_login():
    if not validate_input():
        return

    entered_username = username_entry.get()
    entered_password = password_entry.get()

    # 在数据库中查询用户名和密码
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE name = %s"
    cursor.execute(query, (entered_username,))
    result = cursor.fetchone()
    sql.close_connection()

    if result and result[0] == hash_password(entered_password):
        messagebox.showinfo("登录成功", "欢迎回来，管理员！")
        window.destroy()
        user_list(entered_username)
    else:
        messagebox.showerror("登录失败", "用户名或密码错误，请重试。")


# 创建主窗口
window = tk.Tk()
window.title("用户登录")

# 禁用窗口的放大功能
window.resizable(False, False)

# 创建用户名标签和输入框
username_label = tk.Label(window, text="用户名:")
username_entry = tk.Entry(window)
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry.grid(row=0, column=1, padx=10, pady=5)
username_entry.focus()

# 创建密码标签和输入框
password_label = tk.Label(window, text="密码:")
password_entry = tk.Entry(window, show="*")
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry.grid(row=1, column=1, padx=10, pady=5)

# 创建登录按钮
login_button = tk.Button(window, text="登录", command=check_login, width=19, bg="grey", fg="white")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.E)

# 运行主循环
window.mainloop()
