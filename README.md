# infra-checker

EKS MSA 환경에서 서비스 배포 전 해당 서비스가 접속하는 DB에 미리 접근하여 연결 상태를 확인하기 위한 애플리케이션


1. Dockerfile의 이미지를 ECR에 업로드
```sh
AWS_ID=123456
PROFILE=share
REPOSITORY=infra-checker

DOCKER_IMAGE=infra-checker:2.0
ECR_IMAGE=$AWS_ID.dkr.ecr.ap-northeast-2.amazonaws.com/$REPOSITORY:infra-checker-2.0

################################################################################

docker pull $DOCKER_IMAGE
docker tag $DOCKER_IMAGE $ECR_IMAGE

aws ecr get-login-password \
    --region ap-northeast-2 \
    --profile $PROFILE |
    docker login \
        --username AWS \
        --password-stdin $AWS_ID.dkr.ecr.ap-northeast-2.amazonaws.com

docker push $ECR_IMAGE
```

2. values.yaml의 값을 사용하여 db.yaml을 생성할 수 있도록 ConfigMap에 정의

configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
    name: infra-checker-configmap
    namespace: msa
data:
    db.yaml: |-
{{ toYaml .Values.db | indent 6 }}
```

values.yaml
```yaml
ttlSecondsAfterFinished: 300

dummyList:
  - name: a-agent
    db:
      activate: true
  - name: b-agent
    db:
      activate: true
  - name: c-agent
    db:
      activate: true      


db:
  a-agent:
    a_db:
      reader:
        host: db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username-ro
        password: /app/config/app-name/stp/app-name/db-password-ro
      writer:
        host: db.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username
        password: /app/config/app-name/stp/app-name/db-password
    b_db:
      reader:
        host: intg-db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username-ro
        password: /app/config/app-name/stp/intg/db-password-ro
      writer:
        host: intg-db.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username
        password: /app/config/app-name/stp/intg/db-password
  b-agent:
    a_db:
      reader:
        host: db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username-ro
        password: /app/config/app-name/stp/app-name/db-password-ro
      writer:
        host: db.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username
        password: /app/config/app-name/stp/app-name/db-password
    b_db:
      reader:
        host: intg-db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username-ro
        password: /app/config/app-name/stp/intg/db-password-ro
      writer:
        host: intg-db.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username
        password: /app/config/app-name/stp/intg/db-password
  c-agent:
    a_db:
      reader:
        host: db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username-ro
        password: /app/config/app-name/stp/app-name/db-password-ro
      writer:
        host: db.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username
        password: /app/config/app-name/stp/app-name/db-password
    b_db:
      reader:
        host: intg-db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username-ro
        password: /app/config/app-name/stp/intg/db-password-ro
      writer:
        host: intg-db.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username
        password: /app/config/app-name/stp/intg/db-password
  d-agent:
    a_db:
      reader:
        host: db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username-ro
        password: /app/config/app-name/stp/app-name/db-password-ro
      writer:
        host: db.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username
        password: /app/config/app-name/stp/app-name/db-password
    b_db:
      reader:
        host: intg-db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username-ro
        password: /app/config/app-name/stp/intg/db-password-ro
      writer:
        host: intg-db.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username
        password: /app/config/app-name/stp/intg/db-password
  e-agent:
    a_db:
      reader:
        host: db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username-ro
        password: /app/config/app-name/stp/app-name/db-password-ro
      writer:
        host: db.up.internal
        port: 5432
        username: /app/config/app-name/stp/app-name/db-username
        password: /app/config/app-name/stp/app-name/db-password
    b_db:
      reader:
        host: intg-db-replica.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username-ro
        password: /app/config/app-name/stp/intg/db-password-ro
      writer:
        host: intg-db.up.internal
        port: 5432
        username: /app/config/app-name/stp/intg/db-username
        password: /app/config/app-name/stp/intg/db-password
```

3. Job 생성

```yaml
{{- range $entry := .Values.dummyList }}
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ $entry.name }}-infra-checker-job
  namespace: msa
spec:
  ttlSecondsAfterFinished: {{ $.Values.ttlSecondsAfterFinished }}
  backoffLimit: 0
  template:
    metadata:
      namespace: msa
      labels:
        app: {{ $entry.name }}-infra-checker
        sidecar.istio.io/inject: "false"
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: eks.amazonaws.com/nodegroup
                    operator: In
                    values:
                    - {{ $.Values.affinity.nodeGroup }}
      serviceAccountName: {{ $entry.name }}-infra-checker-sa
      restartPolicy: Never
      containers:
      {{- if $entry.db.activate }}
        - name: {{ $entry.name }}-check-db
          image: 123456.dkr.ecr.ap-northeast-2.amazonaws.com/infra-checker:infra-checker-2.0
          imagePullPolicy: IfNotPresent
          readinessProbe:
            exec:
              command: 
              - echo
              - "hello"
          volumeMounts:
          - name: configmap-db
            mountPath: /root/infra-checker/data
      {{- end }}

      volumes:
      - name: configmap-db
        configMap:
          name: infra-checker-configmap
---
{{- end }}
```

4. 결과

```sh
2023-05-12 17:08:46.025 INFO database.check_connection : Connecting to Database... (dbname=a_db, instance=reader, host=db-replica.up.internal, port=5432)
2023-05-12 17:08:46.026 ERROR database.check_connection : Connection was successful. (dbname=a_db, instance=reader, host=db-replica.up.internal, port=5432)

2023-05-12 17:08:46.026 INFO database.check_connection : Connecting to Database... (dbname=a_db, instance=writer, host=db.up.internal, port=5432)
2023-05-12 17:08:46.027 ERROR database.check_connection : Connection was successful. (dbname=a_db, instance=writer, host=db.up.internal, port=5432)

2023-05-12 17:08:46.027 INFO database.check_connection : Connecting to Database... (dbname=b_db, instance=reader, host=intg-db-replica.up.internal, port=5432)
2023-05-12 17:08:46.028 ERROR database.check_connection : Connection was successful. (dbname=b_db, instance=reader, host=intg-db-replica.up.internal, port=5432)

2023-05-12 17:08:46.028 INFO database.check_connection : Connecting to Database... (dbname=b_db, instance=writer, host=intg-db.up.internal, port=5432)
2023-05-12 17:08:46.029 ERROR database.check_connection : Connection was successful. (dbname=b_db, instance=writer, host=intg-db.up.internal, port=5432)
```

