import time
import numpy as np
from typing import List, Optional
import threading
import pandas as pd
import requests
import plotly.express as px

from processes import process1, process2  # Assuming the process functions are in a separate module

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """Calculate the mean difference between two lists of integers."""
    return np.mean([data1[i] - data2[i] for i in range(len(data1))])

offload_url = 'http://172.20.10.4:5001'

def run(offload: Optional[str] = None) -> float:
    data = generate_data()
    data1, data2 = None, None
    threads = []

    if offload in ['process1', 'both']:
        def offload_process1():
            nonlocal data1
            response = requests.post(f"{offload_url}/process1", json={'data': data})
            data1 = response.json()
        thread1 = threading.Thread(target=offload_process1)
        thread1.start()
        threads.append(thread1)
    else:
        data1 = process1(data)

    if offload in ['process2', 'both']:
        def offload_process2():
            nonlocal data2
            response = requests.post(f"{offload_url}/process2", json={'data': data})
            data2 = response.json()
        thread2 = threading.Thread(target=offload_process2)
        thread2.start()
        threads.append(thread2)
    else:
        data2 = process2(data)

    for thread in threads:
        thread.join()

    return final_process(data1, data2)

def main():
    modes = [None, 'process1', 'process2', 'both']
    rows = []
    for mode in modes:
        times = []
        for _ in range(5):  # Run each mode 5 times
            start_time = time.time()
            run(mode)
            times.append(time.time() - start_time)
        rows.append([mode, np.mean(times), np.std(times)])

    df = pd.DataFrame(rows, columns=['Mode', 'Mean time', 'Std time'])
    fig = px.bar(df, x='Mode', y='Mean time', error_y='Std time',
                 labels={'Mode': 'Offloading Mode', 'Mean time': 'Average Execution Time (s)'},
                 title='Performance Analysis of Offloading Modes')
    fig.write_image("makespan.png")

if __name__ == '__main__':
    main()
