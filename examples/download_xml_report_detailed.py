import argparse
from datetime import date

from codedx_api import CodeDx

# API key and base url from Code DX
parser = argparse.ArgumentParser()
parser.add_argument('base_url', type=str, help='Base URL for Code DX: https://HOST/codedx')
parser.add_argument('api_key', type=str, help='API from Code DX')
parser.add_argument('project', type=str, help='Code DX project name or id')
args = parser.parse_args()

cdx = CodeDx.CodeDx(args.base_url, args.api_key)

report_title = args.project + '_report_' + date.today().strftime("%b%d%y") + ".xml"

res = cdx.get_xml(args.project, include_standards=True, include_source=True, include_rule_descriptions=True, file_name=report_title)