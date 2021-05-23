import re
from abc import ABC, abstractmethod
from typing import Iterable
import wordninja
import pkg_resources

from . import base

_RGX_SPACE = re.compile(r"\s+")

class WordSplittingCorrector(base.BaseCorrector):
    @abstractmethod
    def split(self, text: str) -> Iterable[str]:
        pass

    def correct(self, text: str) -> str:
        ret = ""
        for word in _RGX_SPACE.split(text):
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

class SymSpellCorrector(WordSplittingCorrector):
    def __init__(self):
        from symspellpy.symspellpy import SymSpell
        self.sym_spell = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def split(self, text: str) -> Iterable[str]:
        result = self.sym_spell.word_segmentation(text)
        for split in _RGX_SPACE.split(result.corrected_string):
            yield split