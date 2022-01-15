import re
from urllib.parse import urlparse


# Check https://regex101.com/r/A326u1/5 for reference
DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)"  # http basic authentication [optional]
    r"(?:(?:(?=\S{0,253}(?:$|:))"  # check full domain length to be less than or equal to 253
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"  # check for at least one subdomain, dashes in between allowed
    r"(?:[a-z0-9]{1,63})))"  # check for top level domain, no dashes allowed
    r"|localhost)"  # accept also "localhost" only
    r"(:\d{1,5})?",  # port [optional]
    re.IGNORECASE
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$",  # scheme: http(s) or ftp(s)
    re.IGNORECASE
)


def validate_url(url: str):
    url = url.strip()
    if not url:
        raise Exception("No URL specified")
    if len(url) > 2048:
        raise Exception("URL exceeds its maximum length of 2048 characters (given length={})".format(len(url)))
    result = urlparse(url)
    scheme = result.scheme
    domain = result.netloc
    if not scheme:
        print("No URL scheme specified, trying http.")
        url = "http://" + url
        result = urlparse(url)
        scheme = result.scheme
        domain = result.netloc
    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise Exception("URL scheme must either be http(s) or ftp(s) (given scheme={})".format(scheme))
    if not domain:
        raise Exception("No URL domain specified")
    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise Exception("URL domain malformed (domain={})".format(domain))
    return url


if __name__ == '__main__':
    print(validate_url('konstankino.com'))
    print(validate_url('http://www.konstankino'))
    print(validate_url('https://konstankino.com'))
