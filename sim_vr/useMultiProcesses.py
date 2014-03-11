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
#     def __init__(self, _NUM_PRT, _NUM_CUSTOMER, _repetition, _dispatchers, _meanTimeArrivals):
#         self.NUM_PRT, self.NUM_CUSTOMER, self.repetition = _NUM_PRT, _NUM_CUSTOMER, _repetition
#         self.dispatchers, self.meanTimeArrivals = _dispatchers, _meanTimeArrivals
#     
#     def __call__(self):
#         from Experiments import run_experiment
#         return run_experiment(self.NUM_PRT, self.NUM_CUSTOMER, self.repetition, self.dispatchers, self.meanTimeArrivals)

    def __init__(self, _PRT_SPEED, _S2J_SPEED, _J2D_SPEED, _SETTING_TIME, _NUM_CUSTOMER, _NUM_PRT, _dispatcher, _arrivalRate):
        self.PRT_SPEED, self.S2J_SPEED, self.J2D_SPEED, self.SETTING_TIME = _PRT_SPEED, _S2J_SPEED, _J2D_SPEED, _SETTING_TIME  
        self.NUM_CUSTOMER, self.NUM_PRT, self.dispatcher, self.arrivalRate = _NUM_CUSTOMER, _NUM_PRT, _dispatcher, _arrivalRate
    
    def __call__(self):
        from Experiments import run_eachInstance
        return run_eachInstance(self.PRT_SPEED, self.S2J_SPEED, self.J2D_SPEED, self.SETTING_TIME, self.NUM_CUSTOMER, self.NUM_PRT, self.dispatcher, self.arrivalRate)
    
def ex1():
    repetition = 1
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 5000
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

def ex2():
    import os, Experiments, Dynamics, Algorithms
    
    # init. folders
    fileSavePath = Experiments.fileSavePath
    textFilesPath = Experiments.textFilesPath
    graphFilesPath = Experiments.graphFilesPath
    graphWT_FilesPath = Experiments.graphWT_FilesPath
    graphSMM_FilesPath = Experiments.graphSMM_FilesPath
    
    for p in [fileSavePath, textFilesPath, graphFilesPath, graphWT_FilesPath, graphSMM_FilesPath]:
        if not os.path.exists(p): os.makedirs(p)
    
    assert False
    
    Dynamics.logger = Experiments.logger_pass 
    Algorithms.on_notify_assignmentment_point = Experiments.logger_pass  
    Dynamics.on_notify_customer_arrival = Experiments.on_notify_customer_arrival
    
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (10.0, 60.0)  # unit (sec)
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_workers = multiprocessing.cpu_count() - 1
    workers = [ Worker(tasks, results)
                  for i in xrange(num_workers) ]
    for w in workers:
        w.start()
    
    import Algorithms
    repetition = 1
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 5000
    dispatchers = Algorithms.get_all_dispatchers().values()
    arrivalRates = list(np.arange(0.1, 0.25, 0.005))
    for dispatcher in dispatchers:
        for arrivalRate in arrivalRates:
            tasks.put(Task(PRT_SPEED, S2J_SPEED, J2D_SPEED, SETTING_TIME, NUM_CUSTOMER, NUM_PRT, dispatcher, arrivalRate))
    
    # Add a poison pill for each consumer
    for i in xrange(len(dispatchers) * len(arrivalRates)):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
        
def main():
    NUM_PRT, NUM_CUSTOMER, repetition, dispatcher, arrivalRates, jobs = ex1()
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_workers = multiprocessing.cpu_count() - 1
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

if __name__ == '__main__':
    ex2()
