#创建一个Python3的镜像并录入文件
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY testdb.py /
COPY docker-entrypoint.sh /
RUN chmod +x /testdb.py /docker-entrypoint.sh
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8000