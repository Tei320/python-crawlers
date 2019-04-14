import time
from multiprocessing import Process
from api import app
from config import CYCLE, TESTER_MAP, GENERATOR_MAP, API_HOST, API_PORT, GENERATOR_PROCESS, VALID_PROCESS, API_PROCESS
from generator import *
from tester import *

class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies检测完成')
                    del generator
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()

if __name__ == '__main__':
    Scheduler().run()