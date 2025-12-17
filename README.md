# 🌐 AI 隨身翻譯助手

一個極簡的 Windows 懸浮翻譯工具。按下熱鍵即可輸入中文，自動翻譯成英文並複製到剪貼簿。

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)

## ✨ 功能

- **全域熱鍵** - 隨時按 `Shift+Alt+A` 呼叫
- **極簡介面** - 透明背景，只有輸入框
- **即時翻譯** - 中文 → 英文，按 Enter 完成
- **自動複製** - 翻譯結果直接進剪貼簿
- **視覺回饋** - 成功綠框 ✅ / 失敗紅框 ❌
- **游標定位** - 視窗出現在滑鼠位置

## 📦 安裝

### 方法一：下載 EXE（推薦）

從 [Releases](https://github.com/craig7351/translate-everywhere/releases) 下載最新版 `translator.exe`，直接執行即可。

### 方法二：從原始碼執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行
python main.py
```

## 🚀 使用方式

1. 執行程式（雙擊 `start.bat` 或 `translator.exe`）
2. 按 `Shift+Alt+A` 喚出輸入框
3. 輸入中文，按 `Enter`
4. 翻譯結果已複製！直接 `Ctrl+V` 貼上

> 按 `Esc` 可關閉輸入框

## ⚙️ 自訂熱鍵

編輯 `main.py` 中的 `HOTKEY` 變數：

```python
HOTKEY = "shift+alt+a"  # 可改為 "ctrl+alt+t" 等
```

## 📄 License

MIT
