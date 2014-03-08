import multiprocessing
import Algorithms
import numpy as np

class Worker(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
#             print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

class Task(object):
    def __init__(self, _dispatchers, _meanTimeArrivals, _exOrder):
        self.dispatchers, self.meanTimeArrivals, self.exOrder = _dispatchers, _meanTimeArrivals, _exOrder
    
    def __call__(self):
        from Experiments import run_experiment
        return run_experiment(self.dispatchers, self.meanTimeArrivals, self.exOrder)
    
if __name__ == '__main__':
    
    dispatcher = [
                Algorithms.FCFS,
                Algorithms.FOFO,
                Algorithms.NNBA_I,
                Algorithms.NNBA_IT,
                Algorithms.NNBA_IA,
                Algorithms.NNBA_IAP,
                Algorithms.NNBA_IAT,
                Algorithms.NNBA_IATP,
                ]
    arrivalRates = list(np.arange(0.1, 0.2, 0.05))
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_workers = multiprocessing.cpu_count()
    workers = [ Worker(tasks, results)
                  for i in xrange(num_workers) ]
    for w in workers:
        w.start()
    
    # Enqueue jobs
    num_jobs = 5
    
    jobs = [(0,2),
#             (2,3),
#             (4,5),
#             (5,6),
#             (6,7),
#             (7,8),
            ]
    
    num_jobs = len(jobs)
    for i,j in jobs:
        tasks.put(Task(dispatcher[:], arrivalRates, 1))
    
    # Add a poison pill for each consumer
    for i in xrange(num_workers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1