import os
import multiprocessing

# 监听地址和端口
bind = "127.0.0.1:5000"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 每个工作进程的线程数
threads = 2

# 最大请求数
max_requests = 1000
max_requests_jitter = 50

# 工作模式
worker_class = 'gthread'

# 最大客户端并发数量
worker_connections = 2000

# 进程文件
pidfile = '../logs/gunicorn.pid'

# 访问日志和错误日志
accesslog = '../logs/access.log'
errorlog = '../logs/error.log'
capture_output = True  # 捕获应用程序的标准输出
enable_stdio_inheritance = True  # 继承标准输出

# 日志级别
loglevel = 'debug'

# 后台运行
daemon = True

# 超时时间
timeout = 30

# 重载
reload = True

# 设置日志格式
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [%(process)d] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '../logs/backend.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'app': {  # 应用程序logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
