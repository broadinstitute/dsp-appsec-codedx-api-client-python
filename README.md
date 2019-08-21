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

Add docker command here

#### Download Report 

Add docker command here 


### Docker
1. `docker build --tag codedx-api-wrapper .`
2. `docker run -v $(pwd):/app/ --name codedx-api-wrapper -e API_KEY=[CODEDX_API_KEY] -e PROJECT=[PROJECT_NAME_OR_ID] -e FILE_PATH=[PATH_TO_UPLOAD] codedx-api-wrapper:latest`
