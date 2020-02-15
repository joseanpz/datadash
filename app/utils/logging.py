import logging


def setup_logging():
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("logs/analitica.log", mode='a')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s  [%(trace_uuid)s] [%(process)d] [%(levelname)s] [%(name)s] '
        '[%(funcName)s] [%(lineno)d ].  %(message)s',
        '[%Y-%m-%d %H:%M:%S %z]')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
