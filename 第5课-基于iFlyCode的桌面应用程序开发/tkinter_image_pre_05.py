import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import os

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
        self.original_image = None      # 原始彩色图像
        self.processed_image = None     # 处理后的图像
        self.displayed_photo = None     # 当前显示的图片对象
        
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
            self.original_image = img
            self.processed_image = img  # 初始时处理后的图像就是原图
            
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
        """实现图像灰度处理功能"""
        if self.original_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
            
        try:
            # 将PIL图像转为numpy数组（注意：PIL默认是RGB顺序）
            img_array = np.array(self.original_image)
            
            # 直接使用OpenCV的COLOR_RGB2GRAY进行转换（不需要先转BGR）
            gray_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # 将结果转回PIL格式
            self.processed_image = Image.fromarray(gray_image)
            
            # 更新显示
            photo = ImageTk.PhotoImage(self.processed_image)
            self.image_panel.config(image=photo)
            self.image_panel.image = photo
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"灰度处理失败: {str(e)}")
    
    def mirror_image(self):
        """实现图像水平镜像功能"""
        if self.original_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
            
        try:
            # 将PIL图像转为numpy数组
            img_array = np.array(self.original_image)
            
            # 使用OpenCV实现水平翻转（参数1表示沿y轴翻转）
            mirrored_array = cv2.flip(img_array, 1)
            
            # 将结果转回PIL格式
            self.processed_image = Image.fromarray(mirrored_array)
            
            # 更新显示
            photo = ImageTk.PhotoImage(self.processed_image)
            self.image_panel.config(image=photo)
            self.image_panel.image = photo
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"镜像处理失败: {str(e)}")
    
    def histogram_equalization(self):
        """实现直方图均衡化功能"""
        if self.original_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
            
        try:
            # 将PIL图像转为numpy数组
            img_array = np.array(self.original_image)
            
            # 判断是否为彩色图像（3通道）
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                # 彩色图像处理：转换到YCrCb空间
                ycrcb_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2YCrCb)
                y_channel = ycrcb_img[:, :, 0]
                
                # 对Y通道进行直方图均衡化
                equalized_y = cv2.equalizeHist(y_channel)
                
                # 重新组合YCrCb图像
                ycrcb_img[:, :, 0] = equalized_y
                
                # 转换回RGB空间
                equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2RGB)
            else:
                # 灰度图像直接均衡化
                equalized_img = cv2.equalizeHist(img_array)
            
            # 将结果转回PIL格式
            self.processed_image = Image.fromarray(equalized_img)
            
            # 更新显示
            photo = ImageTk.PhotoImage(self.processed_image)
            self.image_panel.config(image=photo)
            self.image_panel.image = photo
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"直方图均衡化失败: {str(e)}")
    
    def sobel_edge_detection(self):
        """实现Sobel锐化功能"""
        if self.original_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
            
        try:
            # 将PIL图像转为numpy数组
            img_array = np.array(self.original_image)
            
            # 转换为灰度图像
            gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # 计算水平和垂直梯度
            grad_x = cv2.Sobel(gray_img, cv2.CV_64F, dx=1, dy=0, ksize=3)
            grad_y = cv2.Sobel(gray_img, cv2.CV_64F, dx=0, dy=1, ksize=3)
            
            # 合并梯度（绝对值并归一化）
            abs_grad_x = np.absolute(grad_x)
            abs_grad_y = np.absolute(grad_y)
            combined_grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
            
            # 归一化到0-255范围
            normalized_grad = cv2.normalize(combined_grad, None, 0, 255, cv2.NORM_MINMAX)
            final_grad = normalized_grad.astype(np.uint8)
            
            # 将结果转回PIL格式
            self.processed_image = Image.fromarray(final_grad)
            
            # 更新显示
            photo = ImageTk.PhotoImage(self.processed_image)
            self.image_panel.config(image=photo)
            self.image_panel.image = photo
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"Sobel锐化失败: {str(e)}")
    
    def mean_filter(self):
        """实现均值滤波功能"""
        if self.original_image is None:
            messagebox.showwarning("提示", "请先打开一张图片")
            return
            
        try:
            # 将PIL图像转为numpy数组
            img_array = np.array(self.original_image)
            
            # 应用均值滤波（5x5核）
            blurred_img = cv2.blur(img_array, (5, 5))
            
            # 将结果转回PIL格式
            self.processed_image = Image.fromarray(blurred_img)
            
            # 更新显示
            photo = ImageTk.PhotoImage(self.processed_image)
            self.image_panel.config(image=photo)
            self.image_panel.image = photo
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"均值滤波失败: {str(e)}")
    
    def on_close(self):
        """窗口关闭时的清理工作"""
        if hasattr(self, 'original_image') and self.original_image is not None:
            self.original_image.close()
        if hasattr(self, 'processed_image') and self.processed_image is not None:
            self.processed_image.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()