import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2

class ImageApp:
    def __init__(self, root):
        """初始化主窗口和组件"""
        self.root = root
        self.root.title("AI Image Processing System")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # 处理窗口关闭事件
        
        # 设置初始窗口大小并允许自适应调整
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        # 创建主容器框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧面板 - 用于显示图像
        self.image_panel = tk.Label(self.main_frame)
        self.image_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 右侧面板 - 放置控制按钮
        self.control_panel = tk.Frame(self.main_frame)
        self.control_panel.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        
        # 配置网格布局权重使组件随窗口大小变化而调整
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # 创建功能按钮
        self.create_buttons()
        
        # 存储当前打开的图像数据
        self.current_image = None
        self.displayed_photo = None
        
    def create_buttons(self):
        """创建所有操作按钮并绑定事件"""
        buttons_config = [
            ("打开图像", self.open_image),
            ("图像灰度处理", self.grayscale_image),
            ("图像镜像", self.mirror_image),
            ("图像直方图均衡化", self.histogram_equalization),
            ("图像Sobel锐化", self.sobel_edge_detection),
            ("均值滤波处理", self.mean_filter)
        ]
        
        for text, command in buttons_config:
            btn = tk.Button(self.control_panel, text=text, width=20, height=2,
                          command=command)
            btn.pack(fill=tk.X, pady=5)
    
    def open_image(self):
        """打开图像文件并在界面中显示"""
        # 弹出文件选择对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")]
        )
        
        if not file_path:  # 如果用户取消选择
            return
            
        try:
            # 使用PIL加载图像
            img = Image.open(file_path)
            self.current_image = img
            
            # 转换为Tkinter可用的格式
            photo = ImageTk.PhotoImage(img)
            
            # 如果之前有显示的图片，先释放资源
            if self.displayed_photo:
                self.image_panel.config(image="")
                self.displayed_photo = None
                
            # 显示新图片
            self.image_panel.config(image=photo)
            self.image_panel.image = photo  # 保持引用防止被垃圾回收
            self.displayed_photo = photo
            
            # 根据图片尺寸调整窗口大小（保留一些边距）
            new_width = max(img.width + 40, 400)
            new_height = max(img.height + 40, 300)
            self.root.geometry(f"{new_width}x{new_height}")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图像: {str(e)}")
    
    def grayscale_image(self):
        """占位函数 - 将来在此实现灰度转换"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
        messagebox.showinfo("功能开发中", "该功能尚未实现，正在努力开发中...")
    
    def mirror_image(self):
        """占位函数 - 将来在此实现镜像效果"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
        messagebox.showinfo("功能开发中", "该功能尚未实现，正在努力开发中...")
    
    def histogram_equalization(self):
        """占位函数 - 将来在此实现直方图均衡化"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
        messagebox.showinfo("功能开发中", "该功能尚未实现，正在努力开发中...")
    
    def sobel_edge_detection(self):
        """占位函数 - 将来在此实现Sobel边缘检测"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
        messagebox.showinfo("功能开发中", "该功能尚未实现，正在努力开发中...")
    
    def mean_filter(self):
        """占位函数 - 将来在此实现均值滤波"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
        messagebox.showinfo("功能开发中", "该功能尚未实现，正在努力开发中...")
    
    def on_close(self):
        """窗口关闭时的清理工作"""
        if hasattr(self, 'current_image') and self.current_image is not None:
            self.current_image.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
