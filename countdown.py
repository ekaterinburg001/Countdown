"""
倒计时应用

一个简单的带GUI的倒计时应用，使用Tkinter实现界面。
用户可以输入倒计时时间（时 分 秒），点击开始按钮后程序开始倒计时，
并在窗口中实时显示剩余时间。倒计时结束后，弹出消息框提示用户。
"""

import tkinter as tk
from tkinter import messagebox
import time


class CountdownApp:
    """倒计时应用类"""
    
    def __init__(self, root):
        """初始化应用
        
        Args:
            root: Tkinter主窗口
        """
        self.root = root
        self.root.title("倒计时应用")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # 设置窗口图标（可选）
        # self.root.iconbitmap("icon.ico")
        
        # 倒计时变量
        self.is_running = False
        self.remaining_time = 0
        self.after_id = None
        
        # 创建GUI组件
        self._create_widgets()
        
        # 设置窗口居中
        self._center_window()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """创建GUI组件"""
        # 创建输入框和标签
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame, text="请输入倒计时时间：").pack(side=tk.LEFT)
        
        # 创建时输入框
        hour_frame = tk.Frame(input_frame)
        hour_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(hour_frame, text="时").pack(side=tk.TOP)
        self.hour_entry = tk.Entry(hour_frame, width=5)
        self.hour_entry.pack(side=tk.TOP)
        self.hour_entry.insert(0, "0")
        
        # 创建分输入框
        minute_frame = tk.Frame(input_frame)
        minute_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(minute_frame, text="分").pack(side=tk.TOP)
        self.minute_entry = tk.Entry(minute_frame, width=5)
        self.minute_entry.pack(side=tk.TOP)
        self.minute_entry.insert(0, "0")
        
        # 创建秒输入框
        second_frame = tk.Frame(input_frame)
        second_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(second_frame, text="秒").pack(side=tk.TOP)
        self.second_entry = tk.Entry(second_frame, width=5)
        self.second_entry.pack(side=tk.TOP)
        self.second_entry.insert(0, "0")
        
        # 设置初始焦点
        self.hour_entry.focus()
        
        # 创建按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_button = tk.Button(button_frame, text="开始", width=10, command=self.start_countdown)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="重置", width=10, command=self.reset_countdown)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 创建显示剩余时间的标签
        self.time_label = tk.Label(self.root, text="00:00:00", font=("Arial", 24))
        self.time_label.pack(pady=20)
    
    def _center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def start_countdown(self):
        """开始倒计时"""
        # 如果倒计时已经在运行，则不执行任何操作
        if self.is_running:
            return
        
        # 获取用户输入的时间
        try:
            hours = int(self.hour_entry.get().strip() or "0")
            minutes = int(self.minute_entry.get().strip() or "0")
            seconds = int(self.second_entry.get().strip() or "0")
            
            # 验证输入值的有效性
            if hours < 0 or minutes < 0 or seconds < 0 or minutes >= 60 or seconds >= 60:
                messagebox.showerror("错误", "小时必须为非负数，分钟和秒数必须在0-59之间！")
                return
            
            # 计算总秒数
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds <= 0:
                messagebox.showerror("错误", "请至少在一个输入框中输入大于0的值！")
                return
                
        except ValueError:
            messagebox.showerror("错误", "请在输入框中输入有效的数字！")
            return
        
        # 设置倒计时状态和时间
        self.is_running = True
        self.remaining_time = total_seconds
        
        # 禁用输入框和开始按钮
        self.hour_entry.config(state=tk.DISABLED)
        self.minute_entry.config(state=tk.DISABLED)
        self.second_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        
        # 开始倒计时
        self._update_countdown()
    
    def _update_countdown(self):
        """更新倒计时显示"""
        if self.remaining_time <= 0:
            # 倒计时结束
            self.time_label.config(text="00:00:00")
            self.is_running = False
            
            # 启用输入框和开始按钮
            self.hour_entry.config(state=tk.NORMAL)
            self.minute_entry.config(state=tk.NORMAL)
            self.second_entry.config(state=tk.NORMAL)
            self.start_button.config(state=tk.NORMAL)
            
            # 创建一个置顶的消息框
            top_window = tk.Toplevel(self.root)
            top_window.withdraw()  # 先隐藏窗口
            top_window.attributes("-topmost", True)  # 设置为置顶窗口
            
            # 显示提示消息
            messagebox.showinfo("提示", "倒计时结束！", parent=top_window)
            
            # 销毁临时窗口
            top_window.destroy()
            return
        
        # 格式化剩余时间
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # 更新显示
        self.time_label.config(text=time_str)
        
        # 减少剩余时间
        self.remaining_time -= 1
        
        # 安排下一次更新
        self.after_id = self.root.after(1000, self._update_countdown)
    
    def reset_countdown(self):
        """重置倒计时"""
        # 如果倒计时正在运行，弹出确认对话框
        if self.is_running:
            if not messagebox.askyesno("确认", "正在倒计时中，确定要重置吗？"):
                return
        
        # 如果倒计时正在运行，取消定时器
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        
        # 重置状态
        self.is_running = False
        self.remaining_time = 0
        
        # 重置显示
        self.time_label.config(text="00:00:00")
        
        # 启用输入框和开始按钮
        self.hour_entry.config(state=tk.NORMAL)
        self.minute_entry.config(state=tk.NORMAL)
        self.second_entry.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        
        # 重置输入框为默认值0
        self.hour_entry.delete(0, tk.END)
        self.hour_entry.insert(0, "0")
        
        self.minute_entry.delete(0, tk.END)
        self.minute_entry.insert(0, "0")
        
        self.second_entry.delete(0, tk.END)
        self.second_entry.insert(0, "0")
        
        # 设置焦点到小时输入框
        self.hour_entry.focus()

    def _on_closing(self):
        """处理窗口关闭事件"""
        # 如果倒计时正在运行，弹出确认对话框
        if self.is_running:
            if messagebox.askyesno("确认", "正在倒计时中，确定要关闭吗？"):
                self.root.destroy()
        else:
            # 如果倒计时未运行，直接关闭窗口
            self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()