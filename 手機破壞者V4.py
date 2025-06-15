import os
import time

def create_files():
i = 0
while True:
filename = f"fakefile_{i}.txt"
with open(filename, "w") as f:
f.write("爆炸爆炸～～～" * 1000)
i += 1
if i % 100 == 0:
print(f"已創建 {i} 個檔案")

def stress_cpu():
while True:
pass

if name == "main":
import multiprocessing

# 無限創建檔案的進程  
p1 = multiprocessing.Process(target=create_files)  
p1.start()  

# 多核CPU無限迴圈  
processes = []  
for _ in range(multiprocessing.cpu_count() * 4):  
    p = multiprocessing.Process(target=stress_cpu)  
    processes.append(p)  
    p.start()  

p1.join()  
for p in processes:  
    p.join()


