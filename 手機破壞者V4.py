import multiprocessing

def stress_cpu():
    while True:
        pass

if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count() * 4):  # CPU核心數乘以4個進程
        p = multiprocessing.Process(target=stress_cpu)
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
