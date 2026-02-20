from multiprocessing import Pool
from Runner.worker import run_single_backtest

def chunk_jobs(jobs,size):
    for i in range(0,len(jobs),size):
        yield jobs[i:i+size]

def run_batched(jobs,workers,batch_size):
    all_results=[]
    
    with Pool(processes=workers) as pool:
        for batch in chunk_jobs(jobs,batch_size):   
            results=pool.map(run_single_backtest,batch)
            all_results.extend(results)
    return all_results

