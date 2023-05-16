import logging
import platform
import boto3


class Ssm:
    def __init__(self, env, data,  region='ap-northeast-2'):
        self.env = env
        self.data = data
        self.region = region

    def get_db_values(self):
        try:
            if platform.system() == 'Darwin':  # mac
                session = boto3.Session(profile_name='dev')
                client = session.client('ssm', region_name=self.region)
            else:
                client = boto3.client('ssm', region_name=self.region)

            for db_name in self.data.keys():
                for rw in self.data[db_name].keys():
                    for cred, v in [(k, v) for (k, v) in self.data[db_name][rw].items() if k == 'username' or k == 'password']:
                        try:
                            self.data[db_name][rw][cred] = client.get_parameter(Name=v, WithDecryption=True)['Parameter']['Value']
                        except Exception as e:
                            logging.error(e)
                            logging.error('Getting parameters failed. (db_name={}, key_name={})'.format(db_name, v))

        except Exception as e:
            logging.error(e)
            logging.error('SSM Client Error.')

    def get_s3_values(self):
        try:
            if platform.system() == 'Darwin':  # mac
                session = boto3.Session(profile_name='dev')
                client = session.client('ssm', region_name=self.region)
            else:
                client = boto3.client('ssm', region_name=self.region)

            for bucket_name in self.data.keys():
                for k in self.data[bucket_name].keys():
                    if k == 'path':
                        continue

                    try:
                        self.data[bucket_name][k] = client.get_parameter(Name=self.data[bucket_name][k], WithDecryption=True)['Parameter']['Value']
                    except Exception as e:
                        logging.error(e)
                        logging.error('Getting parameters failed. (bucket_name={}, key_name={})' .format(bucket_name, k))

        except Exception as e:
            logging.error(e)
            logging.error('SSM Client Connection Failed')
