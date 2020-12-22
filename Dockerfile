  
FROM python:3.8-slim

MAINTAINER jt3183@columbia.edu (modified by dff)

USER root

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENV NAME World

CMD ["python", "app.py"]
