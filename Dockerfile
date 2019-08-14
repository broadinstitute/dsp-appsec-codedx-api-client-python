FROM python:alpine3.7
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./index.py