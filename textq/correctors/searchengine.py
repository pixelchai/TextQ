from abc import ABC
from . import base
from bs4 import BeautifulSoup
import requests
import fuzzysearch

USER_AGENT_STRING = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

class SearchEngineCorrector(base.BaseCorrector, ABC):
    pass

class DuckDuckGoCorrector(SearchEngineCorrector):
    def __init__(self, fuzzy=True):
        self.fuzzy = fuzzy

    def _get_soup(self, url, params):
        headers = {
            "User-Agent": USER_AGENT_STRING
        }
        return BeautifulSoup(requests.get(url, params=params, headers=headers).content)

    def correct(self, text: str) -> str:
        soup = self._get_soup("https://html.duckduckgo.com/html/", {"q": text})

        def parse_did_you_mean():
            elm_did_you_mean = soup.find(id="did_you_mean")
            if elm_did_you_mean is not None:
                return elm_did_you_mean.find("a").text
            return None

        text = parse_did_you_mean() or text
        return text