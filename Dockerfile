FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# requirements 먼저 복사
COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 프로젝트 복사
COPY ./app /code

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]