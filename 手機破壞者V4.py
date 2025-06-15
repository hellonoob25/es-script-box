import os
import time
import multiprocessing

def create_files():
    i = 0
    while True:
        filename = f"fakefile_{i}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("爆炸爆炸～～～" * 1000)
        i += 1
        if i % 100 == 0:
            print(f"已創建 {i} 個檔案")

def stress_cpu():
    while True:
        pass  # 這裡是無限迴圈，會全核心吃滿CPU

if __name__ == "__main__":
    # 啟動一個無限創建檔案的進程
    p1 = multiprocessing.Process(target=create_files)
    p1.start()

    # 啟動多核心 CPU 壓力測試進程（每核心跑4個）
    processes = []
    for _ in range(multiprocessing.cpu_count() * 4):
        p = multiprocessing.Process(target=stress_cpu)
        processes.append(p)
        p.start()

    p1.join()
    for p in processes:
        p.join()
