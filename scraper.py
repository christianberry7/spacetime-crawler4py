import re
from urllib.parse import urlparse

import bs4
import requests
import re

_LEGAL_DOMAINS = [r'.ics.uci.edu/', r'.cs.uci.edu/', r'.informatics.uci.edu/', r'.stat.uci.edu/', r'today.uci.edu/department/information_computer_sciences/']
LEGAL_DEOMAINS = map(re.compile, _LEGAL_DOMAINS)

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    soup = bs4.BeautifulSoup(resp)
    all_links = [link.get('href') for link in soup.find_all('a', attrs={'href': re.compile('^http://')})]
    legal_links = filter(is_legal, all_links)

    # Check for redundancy in the frontier somewhere 
    # around here and return that filtered link instead
    # to prevent infinite loops
    
    return legal_links

def is_legal(url):
    for domain in LEGAL_DEOMAINS:
        if domain.match(url):
            return True
        return False

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