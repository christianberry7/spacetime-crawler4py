from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
from bs4 import BeautifulSoup

from tokenizer import Tokenizer

import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.token = Tokenizer()
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            untokenized_text = self.extract_text(resp)
            tokenized_text = self.token.Tokenize(untokenized_text)
            print(sorted(tokenized_text.items(),key = lambda i : i[1], reverse = True))
            print(self.token.Final_dict())
            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)

    def extract_text(self, resp) -> list:
        blank_list = []
        try:
            soup = BeautifulSoup(resp.raw_response.content, features= 'html.parser')
            for iter in list(soup.find_all("title") + soup.find_all("p")):
                a = iter.get_text(strip=True,separator = ' ')
                blank_list += (a.split())
        except:
            pass
        return(blank_list)

