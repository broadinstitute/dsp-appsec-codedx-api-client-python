FROM python:alpine3.7
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
CMD echo "hello" && python3 ./examples/upload_analysis_cmd.py ${URL} ${API_KEY} ${PROJECT} ${FILE_PATH}