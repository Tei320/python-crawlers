from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

base_url = 'https://study.163.com/course/courseLearn.htm?courseId=1017043#/learn/video?lessonId=1303188&courseId=1017043'
server = Server('browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat')
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
chrome_options.add_argument('--disable-gpu')

chrome_driver = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

proxy.new_har(base_url)
driver.get(base_url)

result = proxy.har

for entry in result['log']['entries']:
    print(entry['request']['url'])

server.stop()
driver.quit()