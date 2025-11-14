import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import cv2
import numpy as np

class ImageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Processing System")
        self.geometry("800x600")
        
        self.current_image = None
        self.image_path = None
        
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10, fill='x')
        
        # 定义所有按钮及其对应的处理方法
        buttons_info = [
            ("打开图像", self.open_image),
            ("图像灰度处理", self.grayscale_image),
            ("图像镜像", self.mirror_image),      # 绑定新实现的镜像方法
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
            rgb_array = np.array(self.current_image)
            bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
            gray_array = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2GRAY)
            gray_pil_img = Image.fromarray(gray_array)
            
            self.current_image = gray_pil_img
            tk_img = ImageTk.PhotoImage(gray_pil_img)
            if hasattr(self, 'old_photo'):
                del self.old_photo
            self.old_photo = tk_img
            
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
            
            width, height = gray_pil_img.size
            self.geometry(f"{width}x{height}")
            
        except Exception as e:
            messagebox.showerror("处理失败", f"灰度转换出错:\n{str(e)}")
    
    def mirror_image(self):
        """实现图像水平镜像功能"""
        if self.current_image is None:
            messagebox.showwarning("警告", "请先打开图像！")
            return
        
        try:
            # 转换为OpenCV兼容格式 (RGB->BGR)
            rgb_array = np.array(self.current_image)
            bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
            # 执行水平翻转 (flipCode=1表示沿y轴镜像)
            flipped_array = cv2.flip(bgr_array, 1)
            # 转回PIL图像对象 (自动识别通道数)
            flipped_pil_img = Image.fromarray(flipped_array)
            
            # 更新当前图像状态
            self.current_image = flipped_pil_img
            tk_img = ImageTk.PhotoImage(flipped_pil_img)
            
            # 清理旧的图片引用避免内存泄漏
            if hasattr(self, 'old_photo'):
                del self.old_photo
            self.old_photo = tk_img
            
            # 更新画布显示
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=tk_img)
            
            # 自适应调整窗口尺寸
            width, height = flipped_pil_img.size
            self.geometry(f"{width}x{height}")
            
        except Exception as e:
            messagebox.showerror("处理失败", f"镜像操作出错:\n{str(e)}")
    
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