import logging

# 自定义日志格式化类
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # 将 relativeCreated 转换为整数
        record.relativeCreated = int(record.relativeCreated)
        return super().format(record)

# 配置日志格式和文件
log_format = '%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(relativeCreated)d - %(message)s'
custom_formatter = CustomFormatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

logging.basicConfig(
    filename='logs\\log.log',
    level=logging.DEBUG,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# 获取根日志记录器并设置自定义格式化器
logger = logging.getLogger()
logger.handlers[0].setFormatter(custom_formatter)

def log(level, message):
    if level == 'debug':
        logging.debug(message)
    elif level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
    else:
        logging.error(f'Unknown logging level: {level}')  # 如果传入了未知的日志级别，记录错误信息