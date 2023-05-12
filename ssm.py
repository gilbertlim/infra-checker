import logging
import platform
import boto3


class Ssm:
    def __init__(self, env, data, region='ap-northeast-2'):
        self.env = env
        self.data = data
        self.region = region

    def get_values(self):
        try:
            if platform.system() == 'Darwin': # mac
                session = boto3.Session(profile_name='dev')
                client = session.client('ssm', region_name=self.region)
            else:
                client = boto3.client('ssm', region_name=self.region)

            for dbname in self.data.keys():
                for rw in self.data[dbname].keys():
                    for cred, v in [(k, v) for (k, v) in self.data[dbname][rw].items() if k == 'username' or k == 'password']:
                        self.data[dbname][rw][cred] = client.get_parameter(Name=v, WithDecryption=True)['Parameter']['Value']
        except Exception as e:
            logging.error(e)
            logging.error('Getting parameters failed. (key={})\n' .format(v))


