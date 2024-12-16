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
worker_class = 'sync'

# 最大客户端并发数量
worker_connections = 2000

# 进程文件
pidfile = '../logs/gunicorn.pid'

# 访问日志和错误日志
accesslog = '../logs/access.log'
errorlog = '../logs/error.log'

# 日志级别
loglevel = 'debug'

# 后台运行
daemon = True

# 超时时间
timeout = 30

# 重载
reload = True
