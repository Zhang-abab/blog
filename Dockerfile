#创建一个Python3的镜像并录入文件
FROM python:3.10

RUN sed -i s@/archive\.ubuntu\.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security\.ubuntu\.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/cn/.archive\.ubuntu\.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y gcc g++
RUN apt-get install -y vim

RUN mkdir /usr/src/app

COPY . /usr/src/app/djtest
WORKDIR /usr/src/app/djtest

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

EXPOSE 8000