import urllib.request
import urllib.error
import urllib.parse
import shutil
import random
import time

user_agent = ('Mozilla/5.0 (X11; Linux x86_64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/41.0.2272.101 Safari/537.36')

url_header = {
    'User-Agent': user_agent
}


def get_page_source(url, post_values=None, get_values=None, max_request=3):
    # Make it safe for unicode character in string
    url = urllib.parse.quote(url, ':/')

    # Add restful POST data to url and convert to bytes
    if post_values:
        post_data = urllib.parse.urlencode(post_values)
        post_data = post_data.encode('utf-8')
        request = urllib.request.Request(
            url,
            post_data,
            headers=url_header
        )
    elif get_values:
        get_data = urllib.parse.urlencode(get_values)
        request = urllib.request.Request(
            '{}?{}'.format(url, get_data),
            headers=url_header
        )
    else:
        request = urllib.request.Request(url, headers=url_header)

    page_source = None

    while page_source is None:
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                page_source = response.read()
                page_source = page_source.decode('utf-8')
        except UnicodeDecodeError as err:
            print('Decoding to utf-8 failed... Trying ISO-8859-1.')
            page_source = page_source.decode('ISO-8859-1')
        except urllib.error.URLError as err:
            if max_request == 0:
                print(err)
                break
            else:
                print('{}... Retrying ({} attempts left).'.format(err, max_request))
                time.sleep(random.uniform(1, 2.5))
                max_request -= 1
        except ConnectionResetError as err:
            print('Exception - {}'.format(err))
            print('Resetted by peer?')
        except Exception as err:
            print(err)

    return page_source


def download_image(url, file_dir, max_request=3):
    request = urllib.request.Request(url, headers=url_header)

    downloaded = False

    while not downloaded:
        try:
            with urllib.request.urlopen(request, timeout=30) as response, open(file_dir, 'wb') as img_file:
                shutil.copyfileobj(response, img_file)
                downloaded = True
        except urllib.error.URLError as err:
            if max_request == 0:
                print(err)
                break
            else:
                print('{}... Retrying ({} attempts left).'.format(err, max_request))
                time.sleep(random.uniform(1, 2.5))
                max_request -= 1
        except Exception as err:
            print()
            print('    Exception in download_image() - utils.py : {}'.format(err))
            print('    {}'.format(file_dir))
            print('    {}'.format(url))
            print()
            time.sleep(random.uniform(1, 2.5))
