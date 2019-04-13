
# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 数据库设置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'foobared'
REDIS_KEY = 'proxies'

# 代理池数量限制
POOL_UPPER_THRESHOLD = 10000

# 状态码
VALID_STATUS_CODES = [200]
# 测试链接
TEST_URL = 'http://www.baidu.com'
# 批量测试最大值
BATCH_TEST_SIZE = 20

# 检测模块循环时间
TESTER_CYCLE = 20
TESTER_ENABLED = True
# 获取模块循环时间
GETTER_CYCLE = 300
GETTER_ENABLED = True

# API配置
API_HOST = '127.0.0.1'
API_PORT = '5555'
API_ENABLED = True


