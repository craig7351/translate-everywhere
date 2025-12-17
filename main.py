"""
AI 隨身翻譯助手 (AI Translator Overlay)
按下熱鍵呼叫懸浮視窗，輸入中文後按 Enter 翻譯成英文並複製到剪貼簿。
"""
import threading
import customtkinter as ctk
import keyboard
import pyperclip
import pyautogui
from deep_translator import GoogleTranslator

# 設定熱鍵 (可自訂)
HOTKEY = "shift+alt+a"

class TranslatorApp:
    def __init__(self):
        # 設定主題
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 建立主視窗
        self.root = ctk.CTk()
        self.root.title("AI 翻譯助手")
        self.root.geometry("320x60")
        self.root.attributes("-topmost", True)  # 最上層顯示
        self.root.overrideredirect(True)  # 無邊框
        self.root.withdraw()  # 預設隱藏

        # 設定透明背景
        transparent_color = "#010101"
        self.root.configure(fg_color=transparent_color)
        self.root.attributes("-transparentcolor", transparent_color)

        # 建立主框架 (透明背景)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=transparent_color)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 水平容器 (輸入框 + 關閉按鈕)
        self.input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#16213e")
        self.input_frame.pack(pady=5, padx=5, fill="x", expand=True)

        # 輸入框
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="輸入中文，按 Enter 翻譯...",
            width=260,
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_width=0
        )
        self.entry.pack(side="left", pady=5, padx=(10, 5), fill="x", expand=True)
        self.entry.bind("<Return>", self.translate_text)
        self.entry.bind("<Escape>", self.hide_window)

        # 關閉按鈕
        self.close_btn = ctk.CTkButton(
            self.input_frame,
            text="✕",
            width=30,
            height=30,
            font=ctk.CTkFont(size=14),
            corner_radius=5,
            fg_color="transparent",
            hover_color="#e94560",
            command=self.hide_window
        )
        self.close_btn.pack(side="right", pady=5, padx=(0, 5))

        # 翻譯器
        self.translator = GoogleTranslator(source='zh-TW', target='en')

        # 初始定位
        self.position_at_cursor()

        # 設定全域熱鍵
        keyboard.add_hotkey(HOTKEY, self.toggle_window)

    def position_at_cursor(self):
        """將視窗定位到滑鼠游標位置"""
        self.root.update_idletasks()
        width = 320
        height = 60
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 取得滑鼠位置
        mouse_x, mouse_y = pyautogui.position()
        
        # 確保視窗不超出螢幕邊界
        x = min(mouse_x, screen_width - width)
        y = min(mouse_y, screen_height - height)
        x = max(0, x)
        y = max(0, y)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_window(self):
        """切換視窗顯示/隱藏"""
        if self.root.state() == "withdrawn":
            self.show_window()
        else:
            self.hide_window()

    def show_window(self):
        """顯示視窗"""
        self.root.deiconify()
        self.position_at_cursor()
        self.entry.delete(0, "end")
        self.entry.focus_set()

    def hide_window(self, event=None):
        """隱藏視窗"""
        self.root.withdraw()

    def translate_text(self, event=None):
        """翻譯文字並複製到剪貼簿"""
        text = self.entry.get().strip()
        if not text:
            return

        try:
            # 執行翻譯
            translated = self.translator.translate(text)

            # 複製到剪貼簿
            pyperclip.copy(translated)

            # 顯示成功狀態 (綠色邊框 + 顯示翻譯結果)
            self.entry.configure(border_color="#4ecca3")
            self.entry.delete(0, "end")
            self.entry.insert(0, f"✅ {translated}")
            
            # 延遲後隱藏視窗
            self.root.after(1000, self.reset_and_hide)

        except Exception as e:
            # 顯示失敗狀態 (紅色邊框)
            self.entry.configure(border_color="#ff6b6b")
            self.entry.delete(0, "end")
            self.entry.insert(0, f"❌ 翻譯失敗")
            self.root.after(1500, self.reset_and_hide)
    
    def reset_and_hide(self):
        """重置輸入框狀態並隱藏"""
        self.entry.configure(border_color="#565b5e")  # 預設邊框色
        self.hide_window()

    def run(self):
        """啟動應用程式"""
        print(f"🚀 AI 翻譯助手已啟動！按 {HOTKEY.upper()} 喚出視窗")
        self.root.mainloop()


def main():
    app = TranslatorApp()
    app.run()


if __name__ == "__main__":
    main()
