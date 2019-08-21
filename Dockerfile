FROM python:alpine3.7
RUN addgroup -S myuser && adduser -S -G myuser myuser
COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
USER myuser
CMD python3 ./codedx-api-wrapper.py https://codedx101.dsp-techops.broadinstitute.org/codedx ${API_KEY} ${USER_ARGS}