docker build -t zabbix-cloud-metrics-apis .

docker run -v /etc/localtime:/etc/localtime:ro -p 5000:5000 -t zabbix-cloud-metrics-apis-v1.1