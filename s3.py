import boto3
import logging


class S3:
    def __init__(self, data, region='ap-northeast-2'):
        self.data = data
        self.region = region
        self.method = ['aws s3 ls', 'aws s3 cp']

    def check_connection(self):
        for bucket_name in self.data.keys():
            try:
                session = boto3.Session(aws_access_key_id=self.data[bucket_name]['accessKeyId'],
                                        aws_secret_access_key=self.data[bucket_name]['accessKeySecret'],
                                        region_name=self.region)
                s3 = session.client('s3')

                for m in self.method:
                    if m == 'aws s3 ls':
                        result = s3.list_objects(Bucket=bucket_name)
                    elif m == 'aws s3 cp':
                        result = s3.put_object(Bucket=bucket_name,
                                               Body=b'test file',
                                               Key=self.data[bucket_name]['path'][1:] + 'test/test.txt',
                                               ACL='bucket-owner-full-control')

                    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                        logging.info('SUCCESS (bucket_name={}, method={})'.format(bucket_name, m))
                    else:
                        logging.error('FAIL. (bucket_name={}, mehotd={})'.format(bucket_name, m))
                        raise ConnectionError

            except Exception as e:
                logging.error(e)
                logging.error('S3 Client Connection Failed. (bucket_name={})'.format(bucket_name))
