import collections


class WordDictionary(object):
    def __init__(self):
        self.len2words = collections.defaultdict(list)

    def addWord(self, word):
        self.len2words[len(word)].append(word)

    def search(self, word):
        print self.len2words
        words = self.len2words[len(word)]
        for i, char in enumerate(word):
            words = [w for w in words if char in ('.', w[i])]
            if not words:
                return False
        return True


# Your WordDictionary object will be instantiated and called as such:
import time

st = time.time()
wordDictionary = WordDictionary()
wordDictionary.addWord('word')
wordDictionary.addWord('bat')
wordDictionary.addWord('bn')
print wordDictionary.search('weaea')
print wordDictionary.search('b.')
print(time.time() - st)
