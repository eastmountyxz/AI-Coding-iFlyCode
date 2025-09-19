import tkinter as tk
from tkinter import messagebox

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋")
        # 游戏状态常量
        self.BOARD_SIZE = 15
        self.CELL_SIZE = 40
        self.PLAYERS = ['黑', '白']  # 玩家轮流顺序
        self.current_player_idx = 0  # 当前玩家索引
        self.board = [[None]*self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]  # 棋盘数据模型
        
        # 创建画布组件作为棋盘
        self.canvas = tk.Canvas(root, width=self.BOARD_SIZE*self.CELL_SIZE, 
                                height=self.BOARD_SIZE*self.CELL_SIZE, bg='#f0d9b5')
        self.canvas.pack()
        
        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)
        
        # 显示当前轮到谁下棋
        self.status_label = tk.Label(root, text=f"当前回合: {self.PLAYERS[self.current_player_idx]}", font=('Arial', 12))
        self.status_label.pack(pady=10)
        
        # 重置按钮
        self.reset_btn = tk.Button(root, text="重新开始", command=self.reset_game)
        self.reset_btn.pack(pady=5)
        
    def on_click(self, event):
        """处理鼠标点击落子逻辑"""
        # 计算点击位置对应的网格坐标
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        # 确保坐标在有效范围内且该位置为空
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE and self.board[row][col] is None:
            # 更新棋盘状态
            self.board[row][col] = self.current_player_idx
            # 绘制棋子（黑色或白色圆形）
            color = 'black' if self.current_player_idx == 0 else 'white'
            fill_color = color
            outline_color = 'gray' if color == 'white' else 'black'
            x, y = col * self.CELL_SIZE + self.CELL_SIZE//2, row * self.CELL_SIZE + self.CELL_SIZE//2
            self.canvas.create_oval(x - self.CELL_SIZE//2 + 2, y - self.CELL_SIZE//2 + 2,
                                   x + self.CELL_SIZE//2 - 2, y + self.CELL_SIZE//2 - 2,
                                   fill=fill_color, outline=outline_color, width=2)
            
            # 检查是否获胜
            if self.check_win(row, col):
                winner = self.PLAYERS[self.current_player_idx]
                messagebox.showinfo("游戏结束", f"恭喜{winner}获胜！")
                return
            
            # 切换到下一个玩家
            self.current_player_idx = (self.current_player_idx + 1) % len(self.PLAYERS)
            self.status_label.config(text=f"当前回合: {self.PLAYERS[self.current_player_idx]}")
    
    def check_win(self, row, col):
        """检查从指定位置出发是否存在连续五个同色棋子"""
        directions = [(1,0), (0,1), (1,1), (1,-1)]  # 水平、垂直、主对角线、副对角线四个方向
        player = self.board[row][col]
        
        for dr, dc in directions:
            count = 1  # 包括当前位置本身
            # 正向延伸计数
            r, c = row + dr, col + dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # 反向延伸计数
            r, c = row - dr, col - dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False
    
    def reset_game(self):
        """重置游戏状态"""
        self.current_player_idx = 0
        self.board = [[None]*self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.canvas.delete("all")  # 清空画布
        self.status_label.config(text=f"当前回合: {self.PLAYERS[self.current_player_idx]}")
        # 重新绘制网格线
        self.draw_grid()
    
    def draw_grid(self):
        """绘制棋盘网格线"""
        for i in range(self.BOARD_SIZE):
            # 横线
            self.canvas.create_line(0, i * self.CELL_SIZE, self.BOARD_SIZE * self.CELL_SIZE, i * self.CELL_SIZE)
            # 竖线
            self.canvas.create_line(i * self.CELL_SIZE, 0, i * self.CELL_SIZE, self.BOARD_SIZE * self.CELL_SIZE)
        # 标记星位点（传统围棋中的特定参考点）
        star_points = [3,7,11]  # 15路棋盘的标准星位
        for r in star_points:
            for c in star_points:
                self.canvas.create_text((c * self.CELL_SIZE + self.CELL_SIZE/2, r * self.CELL_SIZE + self.CELL_SIZE/2), 
                                       text='·', fill='black', font=('Arial', 8))

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    game.draw_grid()  # 初始化时绘制棋盘网格
    root.mainloop()