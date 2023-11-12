import time
import asyncio
import concurrent.futures


def work(latency):
    time.sleep(latency)


def sequential(latency, executionUnitsCount):
    for _ in range(executionUnitsCount):
        work(latency)


def run_async_io(latency, executionUnitsCount):
    asyncio.run(async_io_tasks(latency, executionUnitsCount))


async def async_work(latency):
    await asyncio.sleep(latency)


async def async_io_tasks(latency, executionUnitsCount):
    tasks = [asyncio.create_task(async_work(latency)) for _ in range(executionUnitsCount)]
    
    await asyncio.gather(*tasks)

# Do work using OS Threads
def run_threads(latency, executionUnitsCount):
    with concurrent.futures.ThreadPoolExecutor(max_workers=executionUnitsCount) as executor:
        executor.map(work, [latency] * executionUnitsCount)

# Do work using OS Processes
def run_processes(latency, executionUnitsCount):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(work, [latency] * executionUnitsCount)


if __name__ == '__main__':
    testCases = [ (0.1,  i) for i in range(1000, 2001, 200)]
    variants = [run_threads, run_async_io]
    
    for i, t in enumerate(testCases):
        latency, executionUnitsCount = t
        print(f"Parallelism\: {executionUnitsCount}")
        
        for j, variant in enumerate(variants):
            start = time.perf_counter()

            r = variant(latency, executionUnitsCount)

            end = time.perf_counter()
        print()
