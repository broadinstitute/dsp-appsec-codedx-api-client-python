from apiclient.APIs import CodeDXClient

# API key and base url from Code DX
api_key = ""
base_url = ""
project = ""

cdx = CodeDXClient.CodeDX(base_url, api_key)

res = cdx.get_pdf(project)
