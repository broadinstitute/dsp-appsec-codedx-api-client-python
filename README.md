# codedx-api-client-python

## Usage

First, make sure you have permissions to access project on GCR and that you can [push and pull images](https://cloud.google.com/container-registry/docs/pushing-and-pulling).

#### Pull Image from GCR

`docker pull gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest`

#### Get Project ID or Create Project if given does not exist

`docker run --name create-project gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest create_project.py [API-KEY] [YOUR-PROJECT-NAME]`

#### Upload security scan report to CodeDX

`docker run -v $(pwd):/app/scripts/reports --name upload-report gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest upload_analysis.py [API-KEY] [PROJECT] [PATH-TO-REPORT]`
