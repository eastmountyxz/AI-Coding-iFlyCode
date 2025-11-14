import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("AI Coding —— Tkinter 示例窗口")
root.geometry("300x200")

# 添加标签
label = tk.Label(root, text="欢迎使用 Tkinter！", font=("Arial", 14))
label.pack(pady=20)

# 定义按钮点击事件
def on_click():
    label.config(text="按钮已被点击！")

# 添加按钮
button = tk.Button(root, text="点击我", command=on_click)
button.pack(pady=10)

# 运行窗口
root.mainloop()
