# codedx-api-client-python

This is an python client for the CodeDx API. See the [CodeDx API Guide](https://codedx.com/Documentation/APIGuide.html) for reference. 

More details about the Python API implementation at [https://broadinstitute.github.io/dsp-appsec-codedx-api-client-python](https://broadinstitute.github.io/dsp-appsec-codedx-api-client-python).

## Download

Install the library using `pip3`

```bash
pip3 install git+https://github.com/broadinstitute/dsp-appsec-codedx-api-client-python.git
```

You can then make API calls using the library. See below for an example.

```python
from codedx_api import CodeDx

cdx = CodeDx("https://codedx.dsp-appsec-dev.broadinstitute.org/codedx", "c112d3a5-53a3-4840-a9f1-38868a7deeaa")

cdx.create_project('WebGoat')
```

The methods return data according to the schema seen in the CodeDx API Guide. For example, the `create_projects` call returns:
```json
{
  "id": 1,
  "name": "WebGoat"
}
```

## Docker Usage

The docker image includes the preinstalled library and includes example scripts for common tasks. 

### Pull Image from GCR

First, make sure you have permissions to access the project on GCR and that you can [push and pull images](https://cloud.google.com/container-registry/docs/pushing-and-pulling).

`docker pull gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest`

### Interactive Python Session

```python
docker run -it --name codedx-tasks gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest
>>> from codedx_api import CodeDx
>>> cdx = CodeDx([YOUR-CODEDX-URL], [CODEDX-API-KEY])
>>> cdx.get_projects()
{YOUR-PROJECTS-JSON}
```

### Run sample scripts

#### Get Project ID or Create Project if given does not exist

`docker run --name create-project gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest create_project.py [API-KEY] [NEW-PROJECT-NAME]`

#### Upload security scan report to CodeDX

`docker run -v $(pwd):/app/scripts/reports --name upload-report gcr.io/dsp-appsec-dev/codedx-api-wrapper:latest upload_analysis.py [API-KEY] [PROJECT] [PATH-TO-REPORT]`

## Development
### Run Updates Locally
```
python setup.py bdist_wheel

pip3 install dist/[WHEEL_FILE]
```

### Testing
CodeDx API uses mocking and unittests to verify functionality.

`python -m unittest discover -s tests -p "*_test.py"`

### Documentation

Documentation can be generated automatically using docstrings.

Run `pdoc --html --output-dir docs codedx_api` to generate documentation.

## Questions

Please contact `appsec@broadinstitute.org` with any questions.
