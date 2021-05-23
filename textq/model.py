from typing import Optional, Iterable, Tuple
import hashlib
import pickle

class Region:
    def __init__(self, polygon: Iterable[Tuple], text: Optional[str] = None, confidence: Optional[float] = 1.0):
        self.polygon = polygon
        self.text = text
        self.confidence = confidence

    def __repr__(self):
        return "<" + \
               "[" + ", ".join(("(" + ", ".join(map(str, vertex)) + ")" for vertex in self.polygon)) + "]" + \
               ', "{}" '.format(self.text) + \
               ", {:.02f}".format(self.confidence) + \
               ">"

class Hashable:
    @staticmethod
    def _hash_bytes(input_bytes):
        return hashlib.sha512(input_bytes).hexdigest()

    @staticmethod
    def _hash_string(input_string):
        return hashlib.sha512(input_string.encode('utf8')).hexdigest()

    @staticmethod
    def _combine_hashes(*hashes):
        return Hashable._hash_string("".join(hashes))

    def compute_hash(self) -> str:
        return self._hash_bytes(pickle.dumps(self))
