from typing import Tuple, List

from wikipediaapi import Wikipedia
import heapq

def get_word_frequency(topic: str, n: int) -> Tuple[List[Tuple[str, int]], bool]:
    # Fetch the Wikipedia article text
    wiki_wiki = Wikipedia('WikiWordCount/1.0' ,'en')

    wiki_page = wiki_wiki.page(topic)
    text = wiki_page.text

    if not wiki_page.exists():
        return {}, False

    # Analyze word frequency
    words = text.split()
    word_frequency = {}
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

    min_heap = [(-count, word) for word, count in word_frequency.items()]
    heapq.heapify(min_heap)

    top_words = [heapq.heappop(min_heap) for _ in range(min(n, len(min_heap)))]

    # Convert the format back to (word, count) for the result
    top_words = [(word, -count) for count, word in top_words]

    return top_words, True