import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Processing System")
        self.geometry("800x600")  # 初始窗口大小，之后会根据图片调整
        
        # 当前加载的图片变量
        self.current_image = None
        self.image_path = None
        
        # 创建顶部框架用于放置控制按钮
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10, fill='x')
        
        # 定义六个按钮及其对应的命令
        buttons_info = [
            ("打开图像", self.open_image),
            ("图像灰度处理", self.placeholder_action),
            ("图像镜像", self.placeholder_action),
            ("图像直方图均衡化", self.placeholder_action),
            ("图像Sobel锐化", self.placeholder_action),
            ("均值滤波处理", self.placeholder_action)
        ]
        
        # 使用循环创建并排列按钮
        for i, (text, command) in enumerate(buttons_info):
            btn = tk.Button(self.control_frame, text=text, width=15, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # 创建画布用于显示图像
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill='both', expand=True)
        
        # 绑定窗口大小变化事件以确保图像居中显示
        self.bind("<Configure>", self.on_resize)
    
    def open_image(self):
        """打开本地图片文件并在画布上显示"""
        filetypes = [("所有支持的文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png")]
        filepath = filedialog.askopenfilename(title="选择一张图片", filetypes=filetypes)
        
        if not filepath:
            return  # 用户取消了选择
        
        try:
            img = Image.open(filepath)
            self.current_image = img
            self.image_path = filepath
            
            # 将PIL图像转换为Tkinter兼容格式
            tk_img = ImageTk.PhotoImage(img)
            
            # 清除之前的旧图像引用避免内存泄漏
            if hasattr(self, 'old_photo'):
                del self.old_photo
            self.old_photo = tk_img
            
            # 在画布上显示新图像
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
            
            # 根据图片尺寸调整窗口大小
            width, height = img.size
            self.geometry(f"{width}x{height}")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片:\n{str(e)}")
    
    def placeholder_action(self):
        """占位符动作，用于未实现的功能按钮"""
        if self.current_image is None:
            messagebox.showwarning("警告", "请先打开一张图片！")
        else:
            messagebox.showinfo("提示", f"该功能正在开发中...\n当前图片路径: {self.image_path}")
    
    def on_resize(self, event):
        """当窗口大小改变时重新绘制图像以保证居中显示"""
        if hasattr(self, 'old_photo') and self.old_photo is not None:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.old_photo)

if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()