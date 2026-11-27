from requests import get, RequestException
from contextlib import closing
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import zstandard

LICHESS_URL = 'https://database.lichess.org'

def simple_get(url, max_retries=3):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    Retry up to `max_retries` times on HTTP errors with a 1-second delay.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }
        for _ in range(max_retries):
            with closing(get(url, stream=True, headers=headers)) as resp:
                if is_good_response(resp):
                    return resp.content
                else:
                    print(f"Recieved a HTTP {resp.status_code} ERROR for {url}.")
                    print("Retrying in 1 second...")
                    time.sleep(1)
        print("-------------------------------------")
        print(f"Retrieving {url} FAILED. Visit this URL in your browser to confirm correctness.")
        print("-------------------------------------")
        return None
    except RequestException as e:
        print(f"The following error occurred during HTTP GET request to {url}: {str(e)}")
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_dom(LICHESS_URL):

    html = simple_get(LICHESS_URL)
    dom = BeautifulSoup(html, 'html.parser')

    return dom

def scrape(dom, month="2018-06"):
    for link_el in dom.find_all("a"):
        link = link_el.get("href", "")
        if link.endswith(f"lichess_db_standard_rated_{month}.pgn.zst"):
            return LICHESS_URL + "/" + link
    return None

dom = get_dom(LICHESS_URL)
url = scrape(dom)
print(url)

if url is not None:
    filename = url.split("/")[-1]
    urlretrieve(url, filename)

    out_name = filename.removesuffix(".zst")
    with open(filename, "rb") as file_in, open(out_name, "wb") as file_out:
        zstandard.ZstdDecompressor().copy_stream(file_in, file_out)