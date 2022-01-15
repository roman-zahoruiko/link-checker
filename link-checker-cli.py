from main.classes import LinkChecker
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(
    prog='link-checker-cli.py', description="This script accept URL and make validity checks."
)
parser.add_argument('-url', '--url', type=str, help="URL to check", required=True)
parser.add_argument('-log', '--log', action='store_true', help="File with strings to count", required=False)
args = parser.parse_args()

if __name__ == '__main__':
    if args.log:
        lc = LinkChecker(args.url, log=True)
    else:
        lc = LinkChecker(args.url)
    result = []
    lc.check_scheme()
    result.append(lc.check_availability())
    if lc.url_available:
        result.append(lc.check_robots())
        result.append(lc.check_content())
    pprint(result)
