# codedx-api-client-python
### Set Up
1. Activate a virtual environment
2. Run `pip install -e .`

### Examples
1. Open `examples/download-pdf-report.py`
2. Edit the api_key and base url variables. Enter the project to download.
3. Run `python3 examples/download-pdf-report.py`.

### Usage
...

### Docker
1. `docker build --tag upload_analysis .`
2. `docker create --name upload_analysis -e API_KEY=[API_KEY] -e URL="[BASE_URL]" -e PROJECT="[PROJECT_NAME_OR_ID]" -e FILE_PATH="./report.xml" upload_analysis:latest`
3. `docker cp [PATH_TO_FILE] upload_analysis:./report.xml`
4. `docker start upload_analysis && docker attach upload_analysis`