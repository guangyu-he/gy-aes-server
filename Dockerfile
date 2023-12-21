FROM python:3.11
LABEL authors="Guangyu He"

WORKDIR /app
COPY . /app

EXPOSE 8989

RUN export PYTHONPATH=$PYTHONPATH:/app
COPY . /app
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989", "--reload"]
