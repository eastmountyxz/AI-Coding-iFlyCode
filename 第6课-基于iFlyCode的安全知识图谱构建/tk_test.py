import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageApp(tk.Tk):
    """图像处理应用程序主类"""
    def __init__(self):
        super().__init__()
        self.title("AI Image Processing System")
        self.geometry("800x600")  # 初始窗口大小，后续会根据图片调整
        self.resizable(True, True)  # 允许窗口缩放

        # ===================================
        # 数据属性初始化
        # ===================================
        self.current_image = None      # 当前加载的图片对象（PIL格式）
        self.image_path = None         # 当前图片的文件路径
        self.tk_image = None           # Tkinter兼容的图片对象

        # ===================================
        # UI组件创建与布局
        # ===================================
        self.create_widgets()

    def create_widgets(self):
        """创建并布置所有UI控件"""
        # 顶部面板 - 放置按钮
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, pady=10)

        # 定义按钮列表及其对应命令
        button_specs = [
            ("打开图像", self.open_image),
            ("图像灰度处理", self.placeholder_action),
            ("图像镜像", self.placeholder_action),
            ("图像直方图均衡化", self.placeholder_action),
            ("图像Sobel锐化", self.placeholder_action),
            ("均值滤波处理", self.placeholder_action)
        ]

        # 使用循环生成按钮并添加到网格中
        for i, (text, command) in enumerate(button_specs):
            btn = tk.Button(top_frame, text=text, width=15, height=2, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)

        # 中央区域 - 用于显示图像
        self.image_label = tk.Label(self, borderwidth=2, relief="solid")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # 状态栏 - 显示当前操作信息
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open_image(self):
        """打开本地图片文件并将其显示在界面上"""
        # 弹出文件选择对话框
        filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes, title="选择一张图片")

        if not filepath:  # 用户取消选择
            return

        try:
            # 尝试加载图像
            img = Image.open(filepath)
            self.current_image = img
            self.image_path = filepath

            # 转换为Tkinter可用的格式
            self.tk_image = ImageTk.PhotoImage(img)

            # 更新标签中的图像内容
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image  # 保持引用防止被垃圾回收

            # 根据图片尺寸调整窗口大小（留出边距）
            new_width = max(800, int(img.size[0] * 1.2))
            new_height = max(600, int(img.size[1] * 1.2))
            self.geometry(f"{new_width}x{new_height}")

            self.status_var.set(f"已加载: {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片:\n{str(e)}")
            self.status_var.set("加载失败")

    def placeholder_action(self):
        """占位函数，用于尚未实现的功能按钮"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片！")
            return
        feature_name = self.master.focus_get().cget("text")  # 获取当前激活按钮的文字
        messagebox.showinfo("功能占位", f"该功能正在开发中: {feature_name}")
        self.status_var.set(f"点击了: {feature_name}")

if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()