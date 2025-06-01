mport tkinter as tk
import time
import requests

# 淡出動畫
def fade_out(window, duration=1, steps=20):
    for i in range(steps):
        alpha = 1 - (i + 1) / steps
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(duration / steps)
    window.destroy()

# 顯示製作人簽名畫面
def show_signature():
    window = tk.Tk()
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    window.geometry("400x100+500+300")
    window.configure(bg='black')
    window.attributes('-alpha', 1)
    label = tk.Label(window, text="製作人:魚生", fg="white", bg="black", font=("Arial", 32))
    label.pack(expand=True, fill="both")
    window.update()
    window.after(2000, lambda: fade_out(window))
    window.mainloop()
import requests
import base64
import os
import time
import re

# === 設定 ===
api_key = "YOUR_OPENAI_API_KEY"  # ⬅️ 換成你的 API 金鑰
sleep_time = 5  # 每輪操作後的等待秒數
loop_count = 0  # 可加上限制，避免過度迴圈

def get_screenshot():
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png ./screenshot.png")

def read_image_base64(path="screenshot.png"):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def call_gpt(img_base64):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "請根據畫面提供明確的操作指令（例如：tap 500 1600 或 swipe 400 1200 400 800），幫我繼續遊戲。"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]
            }
        ],
        "max_tokens": 1000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def extract_commands(gpt_response):
    return re.findall(r"(tap \d+ \d+|swipe \d+ \d+ \d+ \d+)", gpt_response)

def run_commands(commands):
    for cmd in commands:
        shell_cmd = f"adb shell input {cmd}"
        print(f"執行：{shell_cmd}")
        os.system(shell_cmd)
        time.sleep(1)  # 防止執行太快

# === 主程式 ===
print("🔁 開始 GPT 自動玩遊戲 bot...")
while True:
    loop_count += 1
    print(f"\n==== 第 {loop_count} 輪操作 ====")

    print("📸 擷取畫面...")
    get_screenshot()

    print("🧠 分析畫面內容...")
    base64_img = read_image_base64()
    try:
        gpt_response = call_gpt(base64_img)
        print("🤖 GPT 回覆：\n", gpt_response)
    except Exception as e:
        print("❌ GPT API 呼叫錯誤：", e)
        time.sleep(10)
        continue

    cmds = extract_commands(gpt_response)
    if cmds:
        print("✅ 執行指令：", cmds)
        run_commands(cmds)
    else:
        print("⚠️ 沒有偵測到指令，稍後重試")

    print(f"⏳ 等待 {sleep_time} 秒...")
    time.sleep(sleep_time)
