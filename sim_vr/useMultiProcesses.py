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
    def __init__(self, _NUM_PRT, _NUM_CUSTOMER, _repetition, _dispatchers, _meanTimeArrivals):
        self.NUM_PRT, self.NUM_CUSTOMER, self.repetition = _NUM_PRT, _NUM_CUSTOMER, _repetition
        self.dispatchers, self.meanTimeArrivals = _dispatchers, _meanTimeArrivals
        
    
    def __call__(self):
        from Experiments import run_experiment
        return run_experiment(self.NUM_PRT, self.NUM_CUSTOMER, self.repetition, self.dispatchers, self.meanTimeArrivals)
    
    
def ex1():
    repetition = 1
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 2000
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
    arrivalRates = list(np.arange(0.1, 0.25, 0.005))
    
    jobs = [
            (0, 2, 0, len(arrivalRates) // 2),
            (2, 3, 0, len(arrivalRates) // 2),
            (4, 5, 0, len(arrivalRates) // 2),
            (5, 6, 0, len(arrivalRates) // 2),
            (6, 7, 0, len(arrivalRates) // 2),
            (7, 8, 0, len(arrivalRates) // 2),
            
            (0, 2, len(arrivalRates) // 2, len(arrivalRates)),
            (2, 3, len(arrivalRates) // 2, len(arrivalRates)),
            (4, 5, len(arrivalRates) // 2, len(arrivalRates)),
            (5, 6, len(arrivalRates) // 2, len(arrivalRates)),
            (6, 7, len(arrivalRates) // 2, len(arrivalRates)),
            (7, 8, len(arrivalRates) // 2, len(arrivalRates)),
            ]
    return NUM_PRT, NUM_CUSTOMER, repetition, dispatcher, arrivalRates, jobs
      
if __name__ == '__main__':
    NUM_PRT, NUM_CUSTOMER, repetition, dispatcher, arrivalRates, jobs = ex1()
    
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
    num_jobs = len(jobs)
    for i, j, k, x in jobs:
        tasks.put(Task(NUM_PRT, NUM_CUSTOMER, repetition, dispatcher[i:j], arrivalRates[k:x]))
    
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
