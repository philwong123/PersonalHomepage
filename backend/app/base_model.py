import time
import json
import datetime
from functools import wraps
try:
    from .common_func import CommonFunc
except:
    from common_func import CommonFunc

cf = CommonFunc()

from peewee import Model
from playhouse.pool import PooledMySQLDatabase
import configparser
import os
from config import Config

# 读取配置文件
cf = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), 'config.ini')
cf.read(config_path)

# 使用配置文件中的数据库配置
db = PooledMySQLDatabase(
    database=cf.get('database', 'DB_NAME'),
    max_connections=32,
    stale_timeout=300,
    timeout=None,
    user=cf.get('database', 'DB_USER'),
    password=cf.get('database', 'DB_PASS'),
    host=cf.get('database', 'DB_HOST'),
    port=int(cf.get('database', 'DB_PORT'))
)

class BaseModel(Model):
    class Meta:
        database = db

    def base_complete(self, table, pop_attr=[]):
        self_dict = cf.attr_to_dict(self)
        if 'id' in self_dict:
            _ = table.get(table.id == self_dict['id'])
            for attr in pop_attr:
                self_dict.pop(attr)
            for key in self_dict:
                setattr(self, key, getattr(_, key))
        else:
            raise AttributeError
        return self

    def base_create(self, table, pop_attr=[]):
        self_dict = cf.attr_to_dict(self)
        if 'id' in self_dict:
            self_dict.pop('id')
        for attr in pop_attr:
            self_dict.pop(attr)
        _ = table.create(**self_dict)
        self.id = _.id
        return self

    def base_save(self, table, pop_attr=[]):
        self_dict = cf.attr_to_dict(self)
        _id = self_dict.pop('id')
        for attr in pop_attr:
            self_dict.pop(attr)
        if 'create_time' in self_dict:
            self_dict['create_time'] = datetime.datetime.now()
        table.update(**self_dict).where(table.id == _id).execute()
        return self

# 添加连接管理装饰器
def db_connection(func):
    def wrapper(*args, **kwargs):
        try:
            db.connect(reuse_if_open=True)
            return func(*args, **kwargs)
        finally:
            if not db.is_closed():
                db.close()
    return wrapper
