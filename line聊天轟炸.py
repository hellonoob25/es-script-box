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
import requests
import time

# 你的 LINE Notify 權杖（Token）
token = 'YOUR_LINE_NOTIFY_TOKEN'

# 要發送的訊息
message = '在嗎'

# 設定 LINE Notify API 的 URL
url = 'https://notify-api.line.me/api/notify'

# 設定 HTTP 標頭
headers = {
    'Authorization': f'Bearer {token}'
}

# 設定資料
data = {
    'message': message
}

# 這裡是重複發送
for i in range(99999999999): 
response = requests.post(url, headers=headers, data=data)
    print(f'第{i+1}次發送結果: {response.status_code}')
    time.sleep(0.2) 
