FROM python:3.12.2

ENV APP_HOME /WEBHW4

WORKDIR $APP_HOME

COPY . .

EXPOSE 3000

CMD ["python", "main.py"]