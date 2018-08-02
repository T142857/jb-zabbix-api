FROM centos
MAINTAINER toanbs
RUN yum install epel-release -y
RUN yum update -y
RUN yum install python-pip -y
RUN yum install python-pip -y
RUN yum install pytz -y
RUN pip install flask-restful
RUN pip install ZabbixAPI
RUN pip install gunicorn
#RUN timedatectl set-timezone Asia/Ho_Chi_Minh
RUN mkdir /Zabbix_Restfull_Gateway
COPY zabbix-restfull-api /Zabbix_Restfull_Gateway
ENTRYPOINT ["/bin/sh", "/Zabbix_Restfull_Gateway/run.sh"]
EXPOSE 5000
