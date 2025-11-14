import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2  # 新增OpenCV导入
import numpy as np  # OpenCV常用配套库

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Processing System")
        self.geometry("800x600")
        
        self.current_image = None
        self.image_path = None
        
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10, fill='x')
        
        # 更新按钮配置，为灰度处理指定专门的方法
        buttons_info = [
            ("打开图像", self.open_image),
            ("图像灰度处理", self.grayscale_image),      # 替换为实际处理方法
            ("图像镜像", self.placeholder_action),
            ("图像直方图均衡化", self.placeholder_action),
            ("图像Sobel锐化", self.placeholder_action),
            ("均值滤波处理", self.placeholder_action)
        ]
        
        for i, (text, command) in enumerate(buttons_info):
            btn = tk.Button(self.control_frame, text=text, width=15, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill='both', expand=True)
        
        self.bind("<Configure>", self.on_resize)
    
    def open_image(self):
        """打开本地图片文件并在画布上显示"""
        filetypes = [("所有支持的文件", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("JPEG", "*.jpg;*.jpeg"), ("PNG", "*.png")]
        filepath = filedialog.askopenfilename(title="选择一张图片", filetypes=filetypes)
        
        if not filepath:
            return
        
        try:
            img = Image.open(filepath)
            self.current_image = img
            self.image_path = filepath
            
            tk_img = ImageTk.PhotoImage(img)
            
            if hasattr(self, 'old_photo'):
                del self.old_photo
            self.old_photo = tk_img
            
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
            
            width, height = img.size
            self.geometry(f"{width}x{height}")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片:\n{str(e)}")
    
    def grayscale_image(self):
        """实现图像灰度处理功能"""
        if self.current_image is None:
            messagebox.showwarning("警告", "请先打开图像！")
            return
        
        try:
            # 将PIL图像转为numpy数组（RGB顺序）
            rgb_array = np.array(self.current_image)
            # OpenCV默认使用BGR格式，所以需要转换颜色通道顺序
            bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
            # 执行灰度转换
            gray_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2GRAY)
            # 创建新的PIL图像对象
            gray_pil_img = Image.fromarray(gray_array)
            
            # 更新当前图像引用
            self.current_image = gray_pil_img
            
            # 转换为Tkinter可用格式并显示
            tk_img = ImageTk.PhotoImage(gray_pil_img)
            if hasattr(self, 'old_photo'):
                del self.old_photo
            self.old_photo = tk_img
            
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
            
            # 可选：自动调整窗口大小以适应新图像维度
            width, height = gray_pil_img.size
            self.geometry(f"{width}x{height}")
            
        except Exception as e:
            messagebox.showerror("处理失败", f"灰度转换出错:\n{str(e)}")
    
    def placeholder_action(self):
        """其他未实现功能的占位提示"""
        if self.current_image is None:
            messagebox.showwarning("警告", "请先打开图像！")
        else:
            messagebox.showinfo("提示", "该功能正在开发中...")
    
    def on_resize(self, event):
        """窗口大小变化时的响应处理"""
        if hasattr(self, 'old_photo') and self.old_photo is not None:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.old_photo)

if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()