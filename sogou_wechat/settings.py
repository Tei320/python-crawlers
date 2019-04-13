# redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'foobared'
REDIS_KEY = 'request_queue'

VALID_STATUSES = [200]

MAX_FAILED_TIME = 10

PROXY_POOL_URL = 'http://127.0.0.1:5555/random'