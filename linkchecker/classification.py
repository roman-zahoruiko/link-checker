import urllib.request
import urllib.error
import urllib.parse
import urllib.robotparser
import socket


def check_scheme(url_to_check):
    """ Check for http(s) scheme, add http if not scheme """
    url_parsed = urllib.parse.urlparse(url_to_check)
    if not url_parsed.scheme:
        url_parsed = url_parsed._replace(scheme='http')
        print("The protocol is not provided (http or https), fall-back to http")
        if not url_parsed.netloc:
            failed_netloc = url_parsed.path  # To avoid "///" without given "//" in uri
            url_parsed = url_parsed._replace(netloc=failed_netloc, path='')
        url_to_check = urllib.parse.urlunparse(url_parsed)
    return url_to_check


# print(check_scheme('//konstankino.com'))


def check_availability(url_to_check):
    """ Check the website for validity. Expected URL with valid scheme. """
    try:
        response = urllib.request.urlopen(url_to_check, timeout=3)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print(f'No data retrieved because {error}')
        return False, 'website is unavailable'
    except socket.timeout:
        print(f'Socket timed out, URL: {url_to_check}')
        return False, 'website is unavailable'
    else:
        response_cheme = urllib.parse.urlsplit(response.url).scheme
        response_netloc = urllib.parse.urlsplit(response.url).netloc
    if response:
        url_parsed = urllib.parse.urlparse(url_to_check)
        if url_parsed.netloc == response_netloc and url_parsed.scheme == response_cheme:
            return True, 'the website valid as is'
        elif url_parsed.netloc == response_netloc and url_parsed.scheme != response_cheme:
            return True, f'the website redirects to {response_cheme}'
        elif url_parsed.netloc != response_netloc:
            return False, f'the website redirects to {response.url} location'
        else:
            return False, f'Something went wrong. Status:, {response.status}'


# res, data = check_availability('https://nbsc.ru/')
# print(res, data)


def check_robots(url_to_check):
    """ Check the website for robots. Expected URL with valid scheme and availability. """
    if "robots.txt" not in url_to_check:
        url_parsed = urllib.parse.urlparse(url_to_check)
        if url_parsed.path != 'robots.txt':
            url_parsed = url_parsed._replace(path='robots.txt')
        url_to_check = urllib.parse.urlunparse(url_parsed)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url_to_check)
    rp.read()
    if 'Disallow' in str(rp):  # Not the best check, but it matches the task verbatim
        return False, 'the website rejects robots'
    elif not str(rp) or rp.can_fetch("*", url_to_check):
        return True, 'the website accepts robots'
    else:
        return False, 'Something went wrong'


# print(check_robots('https://gb.ru/robots.txt'))
# print(check_robots('https://konstankino.com'))


def check_content(url_to_check):
    """
    Check the website for validity: this validator must detect whether the website is parked or not.
    Looking for keywords 'parking', 'parked', 'buy' + 'domain', 'lease' + 'domain' in page response content or data.
    """
    response = urllib.request.urlopen(url_to_check, timeout=10)
    response_data = response.read().decode('utf-8')
    keywords = ['parking', 'parked', 'buy', 'lease', 'domain']
    keywords_indexes = [response_data.find(i) for i in keywords]
    keywords_in = [item != -1 for item in keywords_indexes]
    if keywords_in[0] or keywords_in[1] or keywords_in[2] and keywords_in[4] or keywords_in[3] and keywords_in[4]:
        return False, 'the website is parked'
    else:
        return True, 'the website is not parked'


# print(check_content('http://conversationgrabber.com/'))
# print(check_content('https://crypto-shop.com/'))
print(check_content('https://konstankino.com'))
