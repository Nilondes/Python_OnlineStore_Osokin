FROM python:3.12-slim

WORKDIR online_shop/

COPY requirements.txt /online_shop/

RUN pip install -r requirements.txt

COPY . /online_shop/

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]