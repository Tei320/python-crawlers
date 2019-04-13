from scheduler import Scheduler
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    a = Scheduler()
    a.run()