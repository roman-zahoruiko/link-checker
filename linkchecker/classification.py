import urllib.request, socket, urllib.error, urllib.parse

# url = 'https://mail.ru'
# url = 'http://konstankino.com'
url = 'https://gb.ru/robots.txt'
# url = 'http://www.google.com'
# url = 'https://zahoruiko.in.ua'


def check_scheme(url_to_check):
    """ Check for http(s) scheme, add http if not scheme """
    url_parse = urllib.parse.urlparse(url_to_check)
    if not url_parse.scheme:
        url_parse = url_parse._replace(scheme='http')
        print("The protocol is not provided (http or https), fall-back to http")
        if not url_parse.netloc:
            failed_netloc = url_parse.path  # To avoid "///" without given "//" in uri
            url_parse = url_parse._replace(netloc=failed_netloc, path='')
        url_to_check = urllib.parse.urlunparse(url_parse)
    return url_to_check


# print(check_scheme('konstankino.com'))


def check_availability(url_to_check):
    """ Check the website for validity. Expected URL with valid scheme. """
    try:
        response = urllib.request.urlopen(url_to_check, timeout=3)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print(f'No data retrieved because {error}')
        return '(False, "website is unavailable")'
    except socket.timeout:
        print(f'Socket timed out, URL: {url_to_check}')
        return '(False, "website is unavailable")'
    else:
        response_cheme = urllib.parse.urlsplit(response.url).scheme
        response_netloc = urllib.parse.urlsplit(response.url).netloc
    if response:
        url_parse = urllib.parse.urlparse(url_to_check)
        if url_parse.netloc == response_netloc and url_parse.scheme == response_cheme:
            return '(True, "the website valid as is")'
        elif url_parse.netloc == response_netloc and url_parse.scheme != response_cheme:
            return f'(True, "the website redirects to {response_cheme}")'
        elif url_parse.netloc != response_netloc:
            return f'(False, "the website redirects to {response.url} location")'
        else:
            return f'Something went wrong. Status:, {response.status}'

# print(check_availability(url))

# def check_robots(url_to_check):
#
