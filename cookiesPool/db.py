import random, redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        # 指定decode_responses=True，连接redis存的数据是字符串格式
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        '''
        获取Hash的名称
        :return:
        '''
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        '''
        设置键值对
        :param username: 用户名
        :param value: 密码或cookies
        :return:
        '''
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        '''
        根据键名获取键值
        :param username: 用户名
        :return:
        '''
        return self.db.hget(self.name(), username)

    def delete(self, username):
        '''
        根据键名删除键值对
        :param username: 用户名
        :return:
        '''
        return self.db.hdel(self.name(), username)

    def count(self):
        '''
        获取数目
        :return: 数目
        '''
        return self.db.hlen(self.name())

    def random(self):
        '''
        随机得到键值，用于随机cookies获取
        :return: 随机cookies
        '''
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        '''
        获得所有账户信息
        :return: 所有用户名
        '''
        return self.db.hkeys(self.name())

    def all(self):
        '''
        获取所有键值对
        :return: 用户名和密码或cookies的映射表
        '''
        return self.db.hgetall(self.name())