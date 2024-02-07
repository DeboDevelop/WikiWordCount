from collections import defaultdict
from queue import PriorityQueue
from typing import Tuple, List

from wikipediaapi import Wikipedia

def get_word_frequency(topic: str, n: int) -> Tuple[List[Tuple[str, int]], bool]:
    # Fetch the Wikipedia article text
    wiki_wiki = Wikipedia('WikiWordCount/1.0' ,'en')

    wiki_page = wiki_wiki.page(topic)
    text = wiki_page.text

    if not wiki_page.exists():
        return {}, False

    # Analyze word frequency
    words = text.split()
    word_frequency = defaultdict(int)
    for word in words:
        word_frequency[word] += 1
        
    min_heap = PriorityQueue()

    for word, count in word_frequency.items():
        min_heap.put((count, word))
        if min_heap.qsize() > n:
            min_heap.get()

    top_words = [(None, None)] * min_heap.qsize()

    for i in range(len(top_words) - 1, -1, -1):
        count, word = min_heap.get()
        top_words[i] = (word, count)

    return top_words, True