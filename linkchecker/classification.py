import urllib.request, socket, urllib.error

# url = 'https://mail.ru'
url = 'http://konstankino.com'
# url = 'https://zahoruiko.in.ua'

# response = urllib.request.urlopen(url)
# print(response.status)
# print('______________________________')


def check_availability(url):
    response = []
    try:
        response = urllib.request.urlopen(url, timeout=3)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print(f'No data retrieved because {error}\nURL: {url}')
    except socket.timeout:
        print(f'Socket timed out - URL {url}')
    else:
        # print(response.read().decode('utf-8'))
        print('Status: ', response.status)
    if response and response.status == 200:
        print(response.url)
        return 'True, the website valid as is'


print(check_availability(url))
