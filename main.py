import logging
import os
import re
import platform

from data import Data
from database import Database
from ssm import Ssm
from s3 import S3


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

    db_data = Data(app_name, './data/db.yaml')
    s3_data = Data(app_name, './data/s3.yaml')

    if db_data.flag:
        db_ssm = Ssm(env, db_data.data)
        db_ssm.get_db_values()
        db = Database(db_ssm.data)
        db.check_connection()

    if s3_data.flag:
        s3_ssm = Ssm(env, s3_data.data)
        s3_ssm.get_s3_values()
        s3 = S3(s3_ssm.data)
        s3.check_connection()


if __name__ == '__main__':
    main()
