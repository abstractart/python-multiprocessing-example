import concurrent.futures
import time
import json
import gc

# CPU Intensive task: generate list and dump it into JSON
def work(size):
    json.dumps(list(range(size)))


# Do work sequentially, one by one
def sequential(size, count):
    for _ in range(count):
        work(size)


# Do work using OS Threads
def run_threads(size, executionUnitsCount):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(work, [size] * executionUnitsCount)

# Do work using OS Processes
def run_processes(size, executionUnitsCount):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(work, [size] * executionUnitsCount)


if __name__ == '__main__':
    # Disable GC for better benchmarking and avoid pauses
    gc.disable()
    
    size = 1000000
    testCases = [ (size,  i) for i in range(1, 12)]
    variants = [sequential, run_threads, run_processes]

    for i, t in enumerate(testCases):
        size, executionUnitsCount = t
        print(f"Parallelism: {executionUnitsCount}, JSON Size: {size}")
        
        for j, variant in enumerate(variants):        
            start = time.perf_counter()

            variant(size, executionUnitsCount)

            end = time.perf_counter()

            print(f"{variant.__name__}, elapsed: {round(end - start, 2)}")
        print()
