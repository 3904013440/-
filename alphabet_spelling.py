import tkinter as tk
from tkinter import messagebox, ttk
import pygame
import os
import random

# 初始化pygame用于播放音频
pygame.mixer.init()

# 外研版三上2025版核心字母表（26个英文字母，含大小写）
ALPHABETS = [
    ('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd'), ('E', 'e'),
    ('F', 'f'), ('G', 'g'), ('H', 'h'), ('I', 'i'), ('J', 'j'),
    ('K', 'k'), ('L', 'l'), ('M', 'm'), ('N', 'n'), ('O', 'o'),
    ('P', 'p'), ('Q', 'q'), ('R', 'r'), ('S', 's'), ('T', 't'),
    ('U', 'u'), ('V', 'v'), ('W', 'w'), ('X', 'x'), ('Y', 'y'), ('Z', 'z')
]

# 音频文件路径（可替换为实际字母发音文件，格式支持mp3/wav）
# 建议：将字母发音文件放在项目的audio文件夹下，命名为a.mp3, A.mp3, b.mp3等
AUDIO_PATH = "audio"
if not os.path.exists(AUDIO_PATH):
    os.makedirs(AUDIO_PATH)

class AlphabetSpellingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("外研2025版三上字母拼写练习")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 初始化变量
        self.current_alphabet = None
        self.user_input = tk.StringVar()
        self.score = 0
        self.total_questions = 0
        
        # 创建界面元素
        self.create_widgets()
        
        # 加载第一个字母
        self.load_random_alphabet()

    def create_widgets(self):
        # 标题区域
        title_frame = tk.Frame(self.root, bg="#f0f8ff")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="外研版三年级上册（2025版）字母拼写练习",
            font=("微软雅黑", 20, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # 字母展示区域
        letter_frame = tk.Frame(self.root, bg="white")
        letter_frame.pack(fill=tk.X, padx=50, pady=20)
        
        self.letter_label = tk.Label(
            letter_frame,
            text="",
            font=("Arial", 60, "bold"),
            bg="white",
            fg="#e74c3c"
        )
        self.letter_label.pack(pady=20)
        
        # 发音按钮
        audio_btn = tk.Button(
            letter_frame,
            text="播放发音",
            font=("微软雅黑", 14),
            bg="#3498db",
            fg="white",
            command=self.play_audio,
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        audio_btn.pack(pady=10)
        
        # 输入区域
        input_frame = tk.Frame(self.root, bg="white")
        input_frame.pack(fill=tk.X, padx=50, pady=10)
        
        input_label = tk.Label(
            input_frame,
            text="请输入对应的字母（大小写均可）：",
            font=("微软雅黑", 14),
            bg="white"
        )
        input_label.pack(side=tk.LEFT, padx=10)
        
        input_entry = tk.Entry(
            input_frame,
            textvariable=self.user_input,
            font=("微软雅黑", 14),
            width=10
        )
        input_entry.pack(side=tk.LEFT, padx=10)
        
        # 操作按钮区域
        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack(pady=20)
        
        check_btn = tk.Button(
            btn_frame,
            text="检查答案",
            font=("微软雅黑", 14),
            bg="#2ecc71",
            fg="white",
            command=self.check_answer,
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        check_btn.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(
            btn_frame,
            text="下一个字母",
            font=("微软雅黑", 14),
            bg="#f39c12",
            fg="white",
            command=self.load_random_alphabet,
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        next_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(
            btn_frame,
            text="重置分数",
            font=("微软雅黑", 14),
            bg="#e74c3c",
            fg="white",
            command=self.reset_score,
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # 分数展示区域
        score_frame = tk.Frame(self.root, bg="white")
        score_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            score_frame,
            text=f"得分：{self.score} / 总题数：{self.total_questions}",
            font=("微软雅黑", 14),
            bg="white",
            fg="#34495e"
        )
        self.score_label.pack()

    def load_random_alphabet(self):
        """加载随机字母"""
        self.current_alphabet = random.choice(ALPHABETS)
        # 随机显示大写或小写字母作为题目
        self.display_type = random.choice([0, 1])
        display_letter = self.current_alphabet[self.display_type]
        self.letter_label.config(text=display_letter)
        # 清空输入框
        self.user_input.set("")

    def play_audio(self):
        """播放当前字母的发音"""
        if not self.current_alphabet:
            messagebox.showwarning("提示", "请先加载字母！")
            return
        
        # 拼接音频文件路径（优先播放对应大小写，无则播放小写）
        letter = self.current_alphabet[0].lower()
        audio_file = os.path.join(AUDIO_PATH, f"{letter}.mp3")
        if not os.path.exists(audio_file):
            audio_file = os.path.join(AUDIO_PATH, f"{self.current_alphabet[0]}.mp3")
        
        try:
            if os.path.exists(audio_file):
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
            else:
                messagebox.showinfo("提示", f"未找到{self.current_alphabet[0]}的发音文件，请添加至audio文件夹！")
        except Exception as e:
            messagebox.showerror("错误", f"播放音频失败：{str(e)}")

    def check_answer(self):
        """检查用户输入的答案"""
        if not self.current_alphabet:
            messagebox.showwarning("提示", "请先加载字母！")
            return
        
        user_answer = self.user_input.get().strip()
        if not user_answer:
            messagebox.showwarning("提示", "请输入字母后再检查！")
            return
        
        # 判定答案（大小写均可）
        correct_answers = [self.current_alphabet[0], self.current_alphabet[1]]
        if user_answer in correct_answers:
            self.score += 1
            messagebox.showinfo("正确", f"恭喜！{user_answer} 是正确答案～")
        else:
            messagebox.showerror("错误", f"答错了😞，正确答案是 {self.current_alphabet[0]} / {self.current_alphabet[1]}")
        
        self.total_questions += 1
        self.update_score_label()
        # 自动加载下一个字母
        self.load_random_alphabet()

    def update_score_label(self):
        """更新分数显示"""
        self.score_label.config(text=f"得分：{self.score} / 总题数：{self.total_questions}")

    def reset_score(self):
        """重置分数"""
        if messagebox.askyesno("确认", "是否确定重置分数？"):
            self.score = 0
            self.total_questions = 0
            self.update_score_label()
            messagebox.showinfo("提示", "分数已重置！")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlphabetSpellingApp(root)
    root.mainloop()
