import multiprocessing
import threading
import time
import asyncio

def work(n):
    time.sleep(n)


async def async_work(n):
    await asyncio.sleep(n)


def single(n, count):
    for _ in range(count):
        work(n)


def async_io(n, count):
    asyncio.run(async_io_tasks(n, count))

async def async_io_tasks(n, count):
    tasks = [asyncio.create_task(async_work(n)) for _ in range(count)]
    
    await asyncio.gather(*tasks)

def multi_threads(n, count):
    threads = [threading.Thread(target=work, args=(n,)) for _ in range(count)]

    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

def multi_process(n, count):
    processes = [multiprocessing.Process(target=work, args=(n,)) for _ in range(count)]
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()




def main():
    tests = [ (0.2,  i) for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]]

    for t in tests:
        n, count = t
        print(f"Parallelism: {count}, work: {n}")
        
        cases = [multi_threads, multi_process, async_io]
        for case in cases:
            start = time.perf_counter()

            r = case(n, count)

            end = time.perf_counter()

            print(f"{case.__name__}, elapsed: {round(end - start, 2)}")
        print()


main()