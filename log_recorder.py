import logging

# 配置日志格式和文件
log_format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

logging.basicConfig(
    filename='logs/log.log',
    level=logging.WARNING,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

logging.warning('a')