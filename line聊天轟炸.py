import tkinter as tk
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

# 發送 LINE Notify
def send_line_notify():
    token = 'YOUR_LINE_NOTIFY_TOKEN'  # 請填入你自己的 Token
    message = '在嗎'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}

    for i in range(10):  # 建議改成有限次數，例如 10 次
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print(f'✅ 第 {i+1} 次發送成功')
        elif response.status_code == 429:
            print('⚠️ 被限制發送，暫停 10 秒')
            time.sleep(10)
            continue
        else:
            print(f'❌ 發送失敗，狀態碼: {response.status_code}')
        time.sleep(2)  # 每次間隔 2 秒，避免觸發限制

# 執行流程
show_signature()
send_line_notify()
