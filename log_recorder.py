import logging

log_format = '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s'

logging.basicConfig(
    filename = 'logs\\log.log',
    level=logging.WARNING,
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding = 'utf-8'
)

# 示例函数
def example_function():
    logging.debug('这是一个调试消息')
    logging.info('这是一个信息消息')
    logging.warning('这是一个警告消息')
    logging.error('这是一个错误消息')
    logging.critical('这是一个严重错误消息')

# 主程序
if __name__ == '__main__':
    example_function()
