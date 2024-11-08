FROM python:3.10-slim
LABEL maintainer="dima.kolhac@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY docker_requirements.txt docker_requirements.txt
RUN pip install -r docker_requirements.txt

COPY . .
RUN mkdir -p static/uploads

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user:my_user static

RUN chmod -R 777 static/uploads
USER my_user

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
