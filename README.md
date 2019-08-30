# codedx-api-client-python
### Set Up
1. Activate a virtual environment
2. Run `pip install -e .`

### Examples
1. Open `examples/download-pdf-report.py`
2. Edit the api_key and base url variables. Enter the project to download.
3. Run `python3 examples/download-pdf-report.py`.

### Usage

#### Upload Report / Run Analysis

1. `docker build --tag codedx-api-wrapper .`
2. `docker run -v $(pwd):/app/ codedx-api-wrapper:latest upload_analysis_cmd.py [API_KEY] [PROJECT_NAME_OR_ID] [PATH_TO_UPLOAD]`

#### Download Report 

1. `docker build --tag codedx-api-wrapper .`
2. `docker run -v $(pwd):/app/ codedx-api-wrapper:latest download_pdf_report.py [API_KEY] [PROJECT_NAME_OR_ID]`


testing commit build