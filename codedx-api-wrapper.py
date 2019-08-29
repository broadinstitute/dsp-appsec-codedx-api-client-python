from apiclient.APIs import CodeDXClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('base_url', type=str, help='API key from Code DX')
parser.add_argument('api_key', type=str, help='Base url from Code DX')
parser.add_argument('user_args', type=str, help='Arguments', nargs='*')
args = parser.parse_args()

cdx = CodeDXClient.CodeDX(args.base_url, args.api_key)

if args.user_args[0] == "ANALYZE":
	cdx.analyze(args.user_args[1], args.user_args[2])
elif args.user_args[0] == "DOWNLOAD_PDF":
	cdx.download_pdf(args.user_args[1])