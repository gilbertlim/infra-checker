FROM python:3.9.16
LABEL name="lsjin" purpose="infra-checker"

RUN pip install boto3 psycopg2 pyyaml

RUN mkdir /root/infra-checker
ADD *.py /root/infra-checker

WORKDIR /root/infra-checker
ENTRYPOINT ["python", "-u"]
CMD ["main.py"]