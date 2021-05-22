import re
from abc import ABC, abstractmethod
from typing import Iterable
import wordninja

from . import base


class WordSplittingCorrector(base.BaseCorrector):
    @abstractmethod
    def split(self, text: str) -> Iterable[str]:
        pass

    def correct(self, text: str) -> str:
        ret = ""
        for word in re.split(r"\s+", text):
            if len(word) > 3:
                for word_split in self.split(word):
                    word_split = word_split.strip()

                    if len(word_split) <= 1:
                        if word_split.lower() in ["a", "i"]:
                            ret += word_split + " "
                    else:
                        ret += word_split + " "
            else:
                ret += word + " "

        return ret[:-1]  # remove trailing space

class WordNinjaCorrector(WordSplittingCorrector):
    def split(self, text: str) -> Iterable[str]:
        return wordninja.split(text)

