FROM python:alpine3.8
RUN addgroup -S codedxuser && adduser -S -G codedxuser codedxuser
COPY . /app/
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
USER codedxuser
WORKDIR /app/examples/
ENTRYPOINT ["python3"]
