FROM python:alpine3.7
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
CMD python3 ./examples/download_pdf_report_cmd.py ${URL} ${API_KEY} ${PROJECT}