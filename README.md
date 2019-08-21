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
2. `docker run -v $(pwd):/app/ --name codedx-api-wrapper 
-e API_KEY=[CODEDX_API_KEY]
-e USER_ARGS="ANALYZE [PROJECT_NAME_OR_ID] [PATH_TO_UPLOAD]" codedx-api-wrapper:latest`

#### Download Report 

1. `docker build --tag codedx-api-wrapper .`
2. `docker run -v $(pwd):/app/ --name codedx-api-wrapper 
-e API_KEY=[CODEDX_API_KEY]
-e USER_ARGS="DOWNLOAD_PDF [PROJECT_NAME_OR_ID]" 
codedx-api-wrapper:latest`