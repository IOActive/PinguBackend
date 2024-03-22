FROM python:3.10-slim
# ssh setup
RUN apt update && apt-get install -y --no-install-recommends python3-psycopg2 git make build-essential libpq-dev

WORKDIR /opt/
ADD requirements.txt /opt/
RUN pip3.10 install -r requirements.txt

COPY PinguApi /opt/PinguApi
COPY PinguBackend /opt/PinguBackend
COPY manage.py /opt/
COPY .env /opt/

#CMD ["NONE"]
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

