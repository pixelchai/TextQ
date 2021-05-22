from abc import ABC
from collections import defaultdict

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
            try:
                new_text =elm_did_you_mean.find("a").text
                print(f"Corrected \"{text}\" -> \"{new_text}\". Using did_you_mean")
                return new_text
            except:
                return text

        text = parse_did_you_mean()

        def fuzzy_result_analysis(max_l_dist=3, min_match_count=5):
            web_results_text = ""

            for elm_result in soup.find_all(class_="web-result"):
                try:
                    web_results_text += elm_result.find(class_="result__title").text.strip() + "\n"
                    web_results_text += elm_result.find(class_="result__snippet").text.strip() + "\n"
                except:
                    pass

            # compute the near matches in the web results text and their frequencies
            near_matches = defaultdict(int)  # str, frequency
            for near_match in fuzzysearch.find_near_matches(text, web_results_text, max_l_dist=max_l_dist):
                near_matches[near_match.matched.strip()] += 1

            if len(near_matches) > 0:
                # compute the most frequent near_match
                near_match, freq = max(near_matches.items(), key=lambda x: x[1])

                if freq >= min_match_count:
                    print(f"Corrected \"{text}\" -> \"{near_match}\". Freq: {freq}")
                    return near_match

            return text

        if self.fuzzy and len(text) > 4:
            text = fuzzy_result_analysis()

        return text