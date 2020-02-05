import xml.etree.ElementTree as ET
import argparse
parser = argparse.ArgumentParser(description='Codedx project')
parser.add_argument('project', type=str, help='The project')
parser.add_argument('url', type=str, help='The "joint project" url')
parser.add_argument('host', type=str, help='The "joint project" host')
args = parser.parse_args()
tree = ET.parse('owasp_report.xml')
if tree.getroot().tag == 'OWASPZAPReport': 
	tree.getroot()[0].set('name', args.url)
	tree.getroot()[0].set('host', args.host)
	tree.getroot()[0].attrib
	for uri in tree.getroot()[0][0].iter('uri'):
		uri_loc = uri.text.split('/')
		if len(uri_loc) < 4:
			uri_loc.append(args.project + '/')
		else:
			uri_loc[3] = args.project + '/' + uri_loc[3]
		uri_loc[2] = 'www.' + args.host
		new_uri = '/'.join(uri_loc)
		uri.text = new_uri

else:
	for issue in tree.getroot():
		path = issue.find('path')
		path.text = '/' + args.project + path.text

output_file = args.project + '-output.xml'
tree.write(output_file)