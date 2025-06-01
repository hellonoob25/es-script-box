import tkinter as tk
import time

def fade_out(window, duration=1, steps=20):
    for i in range(steps):
        alpha = 1 - (i + 1) / steps
        window.attributes('-alpha', alpha)
        window.update()
        time.sleep(duration / steps)
    window.destroy()
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
import time
import requests

webhook_url = "你的 Discord Webhook URL"
for i in range(100):
    data = {"content": f"這是第 {i+1} 條訊息"}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 429:  # 被限制
        retry_after = response.json().get('retry_after', 5)
        print(f"被限制，等待 {retry_after} 秒")
        time.sleep(retry_after)
    else:
        print(f"已送出第 {i+1} 條訊息，狀態碼：{response.status_code}")
        time.sleep(1)  # 建議設為 1 秒或以上
