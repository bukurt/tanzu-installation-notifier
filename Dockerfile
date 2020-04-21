FROM python:alpine3.11
MAINTAINER Burak Kurt (https://github.com/kurtburak)

COPY get-uaa-token.sh /app/
COPY requirements.txt /app/
COPY run.py /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
RUN apk update
RUN apk add openssh
RUN chmod +x ./run.py
RUN mkdir -p /root/.ssh
RUN touch /root/.ssh/known_hosts
RUN chmod -R 600 /root/.ssh
RUN chmod 700 /root/.ssh
RUN chmod +x run.py
RUN chmod +x *.sh

ENTRYPOINT ["python", "-u"]
CMD ["./run.py"]
