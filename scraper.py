import re
from urllib.parse import urlparse

import bs4
import requests
import re

_LEGAL_DOMAINS = r'.ics.uci.edu/|.cs.uci.edu/|.informatics.uci.edu/|.stat.uci.edu/|today.uci.edu/department/information_computer_sciences/'
LEGAL_DOMAINS = re.compile(_LEGAL_DOMAINS)

_TRUNCATE = r'[#].*'
TRUNCATE = re.compile(_TRUNCATE)


def scraper(url, resp):
    # Need to handle redirection loops
    # print(">> [STATUS CODE]", resp.status)
    # print(resp.error)
    if resp.status == requests.codes['bad_request'] or resp.error:
        return []

    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    soup = bs4.BeautifulSoup(resp.raw_response.content, 'html.parser')
    
    all_links = [(link.get('href')) for link in soup.find_all('a', attrs={'href': re.compile(r'^http[s]://')})]
    legal_links = list(filter(is_legal_and_valid, all_links))
    legal_links = set(map(truncate_fragment, legal_links))

    # Debugging purposes
    # print(">> Found all links:\n>> " + "\n>> ".join(all_links))
    # print(">> Returning legal links:\n>> " + "\n>> ".join(legal_links))
    
    return legal_links

def is_legal_and_valid(url):
    # Checks to see if URL is within our intended scope
    if LEGAL_DOMAINS.search(url) is not None:
        return is_valid(url)
    return False

def truncate_fragment(url):
    # Completely removes the fragment portion of the URL
    return TRUNCATE.sub('', url)

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise