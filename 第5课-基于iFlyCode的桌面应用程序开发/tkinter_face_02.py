import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class FaceRecognitionApp:
    def __init__(self, root):
        # 初始化主窗口
        self.root = root
        self.root.title("AI人脸识别系统")
        self.root.geometry("800x600")
        
        # 加载预训练的人脸检测模型
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # 创建界面组件
        self.create_widgets()
        
        # 存储当前图像数据
        self.current_image = None
        self.displayed_photo = None

    def create_widgets(self):
        """创建并布局所有界面组件"""
        # 图像显示区域 (使用Frame作为容器)
        self.image_frame = tk.Frame(self.root, bg="#f5f5f5", relief="groove", borderwidth=2)
        self.image_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # 图像标签
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 按钮面板
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # 创建按钮
        btn_style = {'width': 20, 'height': 2, 'font': ('微软雅黑', 14)}
        
        self.open_btn = tk.Button(button_frame, text="打开图像", command=self.open_image, **btn_style)
        self.open_btn.pack(side=tk.LEFT, padx=30)
        
        self.detect_btn = tk.Button(button_frame, text="人脸识别", command=self.detect_faces, **btn_style)
        self.detect_btn.pack(side=tk.RIGHT, padx=30)

    def open_image(self):
        """打开并显示本地图像"""
        # 弹出文件选择对话框
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")],
            title="选择图像文件"
        )
        
        if not file_path:  # 用户取消选择
            return
            
        try:
            # 使用PIL加载图像
            img = Image.open(file_path)
            self.current_image = img
            
            # 调整图像尺寸以适应显示区域
            max_size = (760, 500)  # 略小于窗口尺寸
            img.thumbnail((max_size[0], max_size[1]))
            
            # 转换为Tkinter可用的格式
            photo = ImageTk.PhotoImage(img)
            
            # 更新显示
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 保持引用防止被垃圾回收
            self.displayed_photo = photo
            
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图像:\n{str(e)}")

    def detect_faces(self):
        """执行人脸检测并在图像上绘制矩形框"""
        if self.current_image is None:
            messagebox.showwarning("提示", "请先打开一张图像！")
            return
            
        try:
            # 将PIL图像转换为OpenCV格式
            img_array = np.array(self.current_image)
            # OpenCV使用BGR格式，而PIL是RGB，需要转换
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # 检测人脸
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # 在检测到的人脸区域绘制矩形框
            for (x, y, w, h) in faces:
                cv2.rectangle(img_bgr, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # 转换回PIL格式用于显示
            result_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(result_img)
            
            # 更新显示
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.displayed_photo = photo
            
            # 显示检测结果
            messagebox.showinfo("检测结果", f"共检测到 {len(faces)} 张人脸")
            
        except Exception as e:
            messagebox.showerror("错误", f"人脸检测失败:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()