"""
AI 隨身翻譯助手 (AI Translator Overlay) - macOS 版本
按下熱鍵呼叫懸浮視窗，輸入文字後按 Enter 翻譯並複製到剪貼簿。
"""
import threading
import customtkinter as ctk
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from deep_translator import GoogleTranslator

# 設定熱鍵 (可自訂) - macOS 使用 Command+Shift+A
HOTKEY_MODIFIERS = {Key.cmd, Key.shift}
HOTKEY_KEY = KeyCode.from_char('a')

# 支援的語言
LANGUAGES = {
    '1': ('zh-TW', '中文'),
    '2': ('en', '英文'),
    '3': ('ko', '韓文'),
    '4': ('ja', '日文'),
}

def select_language():
    """讓用戶選擇來源語言和目標語言"""
    print("\n🌐 AI 翻譯助手 - 語言設定")
    print("=" * 30)
    
    # 選擇來源語言
    print("\n選擇來源語言 (預設為中文, 按 Enter 用預設):")
    for key, (code, name) in LANGUAGES.items():
        print(f"  {key}. {name}")
    
    source_choice = input("\n請輸入數字: ").strip()
    if source_choice == '' or source_choice not in LANGUAGES:
        source_choice = '1'  # 預設中文
    source_code, source_name = LANGUAGES[source_choice]
    
    # 選擇目標語言
    print(f"\n選擇目標語言 (預設為英文, 按 Enter 用預設):")
    for key, (code, name) in LANGUAGES.items():
        print(f"  {key}. {name}")
    
    target_choice = input("\n請輸入數字: ").strip()
    if target_choice == '' or target_choice not in LANGUAGES:
        target_choice = '2'  # 預設英文
    target_code, target_name = LANGUAGES[target_choice]
    
    print(f"\n✅ 設定完成: {source_name} → {target_name}")
    print("=" * 30)
    
    return source_code, target_code, source_name, target_name

class TranslatorApp:
    def __init__(self, source_lang='zh-TW', target_lang='en', source_name='中文', target_name='英文'):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.source_name = source_name
        self.target_name = target_name
        self.current_keys = set()
        
        # 設定主題
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 建立主視窗
        self.root = ctk.CTk()
        self.root.title("AI 翻譯助手")
        self.root.geometry("350x60")
        self.root.attributes("-topmost", True)  # 最上層顯示
        self.root.withdraw()  # 預設隱藏

        # macOS 視窗設定 (無邊框 + 半透明)
        self.root.overrideredirect(True)
        self.root.configure(fg_color="#16213e")
        self.root.attributes("-alpha", 0.95)

        # 建立主框架
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#16213e")
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 水平容器 (輸入框 + 關閉按鈕)
        self.input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#1a1a2e")
        self.input_frame.pack(pady=5, padx=5, fill="x", expand=True)

        # 輸入框
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="輸入文字，按 Enter 翻譯...",
            width=280,
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
        self.translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)

        # 啟動全域熱鍵監聽器
        self.start_hotkey_listener()

    def start_hotkey_listener(self):
        """啟動 pynput 熱鍵監聽"""
        def on_press(key):
            self.current_keys.add(key)
            # 檢查是否按下完整熱鍵組合
            if HOTKEY_MODIFIERS.issubset(self.current_keys) and HOTKEY_KEY in self.current_keys:
                self.root.after(0, self.toggle_window)
        
        def on_release(key):
            self.current_keys.discard(key)
        
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def toggle_window(self):
        """切換視窗顯示/隱藏"""
        if self.root.state() == "withdrawn":
            self.show_window()
        else:
            self.hide_window()

    def show_window(self):
        """顯示視窗"""
        self.entry.configure(border_color="#565b5e")
        self.entry.delete(0, "end")
        
        self.root.deiconify()
        self.center_window()
        self.entry.focus_set()

    def center_window(self):
        """將視窗置中於螢幕"""
        self.root.update_idletasks()
        width = 350
        height = 60
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 3
        self.root.geometry(f"{width}x{height}+{x}+{y}")

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
        self.entry.configure(border_color="#565b5e")
        self.hide_window()

    def run(self):
        """啟動應用程式"""
        print(f"\n🚀 AI 翻譯助手已啟動！")
        print(f"🌐 翻譯方向: {self.source_name} → {self.target_name}")
        print(f"⌨️  熱鍵: Command+Shift+A")
        print(f"\n💡 關閉此視窗即可結束程式")
        print(f"⚠️  請確保已在「系統偏好設定 → 安全性與隱私 → 輔助使用」中授權")
        self.root.mainloop()


def main():
    source_code, target_code, source_name, target_name = select_language()
    app = TranslatorApp(source_code, target_code, source_name, target_name)
    app.run()


if __name__ == "__main__":
    main()
