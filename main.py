import multiprocessing
import threading
import time
import json

def range_sum(start, finish):
    s = 0

    for i in range(start, finish + 1):
        s += i
    
    return s


def work(n):
    json.dumps([list(range(n))])


def single(n, count):
    for _ in range(count):
        work(n)


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
    tests = [ (1000000,  i) for i in range(1, 13)]

    for t in tests:
        n, count = t
        print(f"Parallelism: {count}, Factorial: {n}")
        
        cases = [single, multi_threads, multi_process]
        for case in cases:
            start = time.perf_counter()

            case(n, count)

            end = time.perf_counter()

            print(f"{case.__name__}, elapsed: {round(end - start, 2)}")
        print()


main()