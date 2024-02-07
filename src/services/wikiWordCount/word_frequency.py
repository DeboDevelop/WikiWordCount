import os
import yaml

from collections import defaultdict
from queue import PriorityQueue
from typing import Tuple, List

from wikipediaapi import Wikipedia
from config import Config

def blacklist_words(word_frequency: dict) -> dict:
    env = Config.FLASK_ENV
    yaml_path = os.path.join(os.path.dirname(__file__), f'../../flags/{env}.yaml')

    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
        feature_flag = config.get('feature_flag', [])
        blacklisted_words = config.get('blacklisted_words', [])

        if feature_flag:
            for word in blacklisted_words:
                del word_frequency[word]

    return word_frequency    

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
    
    word_frequency = blacklist_words(word_frequency)

    pq = PriorityQueue()

    for word, count in word_frequency.items():
        pq.put((count, word))
        if pq.qsize() > n:
            pq.get()

    top_words = [(None, None)] * pq.qsize()

    for i in range(len(top_words) - 1, -1, -1):
        count, word = pq.get()
        top_words[i] = (word, count)

    return top_words, True