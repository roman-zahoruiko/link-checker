import urllib.request
import urllib.parse
import urllib.robotparser
import urllib.error
import socket


class LinkChecker:

    def __init__(self, url_to_check, log=False):
        self.url_to_check = url_to_check
        self.url_parsed = urllib.parse.urlparse(self.url_to_check)
        self.log = log
        self.message = '...log:'
        self.url_available = False
        if self.url_parsed.netloc and self.url_parsed.path:
            self.url_parsed = self.url_parsed._replace(path='')
            self.url_to_check = urllib.parse.urlunparse(self.url_parsed)
            if self.log:
                print(self.message, "URL path cleaned!")

    def check_scheme(self):
        """ Check for http(s) scheme, add "http" if not """
        if not self.url_parsed.scheme:
            self.url_parsed = self.url_parsed._replace(scheme='http')
            if self.log:
                print(self.message, "The protocol is not provided (http or https), fall-back to http!")
            if not self.url_parsed.netloc:
                failed_netloc = self.url_parsed.path  # To avoid "///" without given "//" in uri
                self.url_parsed = self.url_parsed._replace(netloc=failed_netloc, path='')
            self.url_to_check = urllib.parse.urlunparse(self.url_parsed)
        return self.url_to_check

    def check_availability(self):
        """ Check the website for validity. Expected URL with valid scheme. """
        try:
            response = urllib.request.urlopen(self.url_to_check, timeout=3)
        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            if self.log:
                print(self.message, f'No data retrieved because {error}!')
            return False, 'website is unavailable'
        except socket.timeout:
            if self.log:
                print(self.message, f'Socket timed out, URL: {self.url_to_check}!')
            return False, 'website is unavailable'
        else:
            self.url_available = True
            response_cheme = urllib.parse.urlsplit(response.url).scheme
            response_netloc = urllib.parse.urlsplit(response.url).netloc
        if response:
            if self.url_parsed.netloc == response_netloc and self.url_parsed.scheme == response_cheme:
                return True, 'the website valid as is'
            elif self.url_parsed.netloc == response_netloc and self.url_parsed.scheme != response_cheme:
                return True, f'the website redirects to {response_cheme}'
            elif self.url_parsed.netloc != response_netloc:
                return False, f'the website redirects to {response.url} location'
            else:
                return False, f'Something went wrong. Status:, {response.status}'

    def check_robots(self):
        """ Check the website for robots. Expected URL with valid scheme and availability. """
        url_parsed_robots = self.url_parsed._replace(path='robots.txt')
        url_to_check = urllib.parse.urlunparse(url_parsed_robots)
        if self.log:
            print(self.message, '"/robots.txt" added to path!')
        robot_parser = urllib.robotparser.RobotFileParser()
        robot_parser.set_url(url_to_check)
        robot_parser.read()
        if 'Disallow' in str(robot_parser):  # Not the best check, but it matches the task verbatim
            return False, 'the website rejects robots'
        elif not str(robot_parser) or robot_parser.can_fetch("*", url_to_check):
            return True, 'the website accepts robots'
        else:
            return False, 'Something went wrong'

    def check_content(self):
        """
        Check the website for validity: this validator must detect whether the website is parked or not.
        Looking for keywords 'parking', 'parked', 'buy' + 'domain', 'lease' + 'domain' in page response content or data.
        """
        response = urllib.request.urlopen(self.url_to_check, timeout=10)
        response_data = response.read().decode('utf-8')
        keywords = ['parking', 'parked', 'buy', 'lease', 'domain']
        keywords_indexes = [response_data.find(i) for i in keywords]
        keywords_in = [item != -1 for item in keywords_indexes]
        if self.log:
            print(self.message, 'Markers of parked domain found:', dict(zip(keywords, keywords_in)))
        if keywords_in[0] or keywords_in[1] or keywords_in[2] and keywords_in[4] or keywords_in[3] and keywords_in[4]:
            return False, 'the website is parked'
        else:
            return True, 'the website is not parked'


if __name__ == '__main__':
    link = LinkChecker('konstankino.com', log=True)
    print(link.check_scheme())
    print(link.check_availability())
    print(link.url_available)
    print(link.check_robots())
    print(link.check_content())
