import tkinter as tk
from tkinter import ttk
from mysql_conn import MySQLConnection

# 创建数据库连接
sql = MySQLConnection()


# 定义全局变量
page_number = 1  # 当前页码
page_size = 10  # 每页显示的记录数


def query_user_list(treeview):
    # 计算查询的偏移量
    offset = (page_number - 1) * page_size
    conn = sql.conn
    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询语句
    query = "SELECT * FROM users LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))

    # 获取查询结果
    users = cursor.fetchall()

    # 关闭游标和数据库连接
    cursor.close()
    sql.close_connection()

    # 清空当前的表格
    treeview.delete(*treeview.get_children())

    # 插入查询结果到表格中
    for user in users:
        treeview.insert("", tk.END, values=(user[0], user[1], user[2], user[3]))


def prev_page(treeview):
    global page_number
    if page_number > 1:
        page_number -= 1
        query_user_list(treeview)


def next_page(treeview):
    global page_number

    conn = sql.conn

    # 创建游标对象
    cursor = conn.cursor()

    # 执行查询总记录数的语句
    cursor.execute("SELECT COUNT(*) FROM users")
    total_records = cursor.fetchone()[0]

    print(total_records)
    exit

    # 关闭游标
    cursor.close()

    total_pages = (total_records + page_size - 1) // page_size  # 计算总页数

    if page_number < total_pages:
        page_number += 1
        query_user_list(treeview)


def user_list(username):
    list_window = tk.Tk()
    list_window.title("用户查询")

    # 设置窗口大小
    list_window.geometry("500x400")

    # 禁用窗口的放大功能
    list_window.resizable(False, False)

    # 显示登录的用户信息
    welcome_label = tk.Label(list_window, text=f"欢迎, {username}!")
    welcome_label.pack(padx=10, pady=5)

    # 创建查询按钮
    query_button = tk.Button(list_window, text="查询用户", command=lambda: query_user_list(treeview))
    query_button.pack(padx=10, pady=5)

    # 创建表格用于显示用户列表
    treeview = ttk.Treeview(list_window, columns=("id", "username", "email", "age"), show="headings")
    treeview.heading("id", text="ID")
    treeview.heading("username", text="用户名")
    treeview.heading("email", text="邮箱")
    treeview.heading("age", text="年龄")
    treeview.pack(padx=10, pady=5)

    # 设置列宽度
    treeview.column("id", width=50)
    treeview.column("username", width=150)
    treeview.column("email", width=150)
    treeview.column("age", width=50)

    # 创建滚动条
    scrollbar = ttk.Scrollbar(list_window, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.configure(yscrollcommand=scrollbar.set)

    # 创建分页按钮
    prev_button = tk.Button(list_window, text="上一页", command=lambda: prev_page(treeview))
    prev_button.pack(padx=10, pady=5)

    next_button = tk.Button(list_window, text="下一页", command=lambda: next_page(treeview))
    next_button.pack(padx=10, pady=5)

    # 默认查询第一页的数据
    query_user_list(treeview)

    list_window.mainloop()


user_list("阿康")
