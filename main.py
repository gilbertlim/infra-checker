import logging
import os
import re
import platform

from data import Data
from database import Database
from ssm import Ssm


def default_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def main():
    default_logging()

    if platform.system() == 'Darwin':  # mac
        env = 'dev'
        app_name = 'a-agent'
    else:
        regex = re.compile(r'iam-role-[a-z]+-iptv-([a-z]+)-(.*)-re$')
        result = regex.search(os.environ['AWS_ROLE_ARN'])
        env = result.group(1)
        app_name = result.group(2).replace('_', '-')

    data = Data(app_name, './data/db.yaml')

    ssm = Ssm(env, data.data)
    ssm.get_values()

    db = Database(ssm.data)
    db.check_connection()


if __name__ == '__main__':
    main()
