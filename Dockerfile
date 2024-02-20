FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y

WORKDIR /app
COPY . .
COPY .kaggle /root/.kaggle   
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]