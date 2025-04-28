FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#For Use on Local
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
#For Use with AWS
# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait_aarch64 /wait
RUN chmod +x /wait

CMD /wait && python main.py