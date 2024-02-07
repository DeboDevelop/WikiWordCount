import os
import yaml

from collections import defaultdict
from queue import PriorityQueue
from typing import Tuple, List

from wikipediaapi import Wikipedia
from flask import current_app

def blacklist_words(word_frequency: dict) -> dict:
    env = current_app.config['FLASK_ENV']
    # Set path based on env
    yaml_path = os.path.join(os.path.dirname(__file__), f'../../flags/{env}.yaml')

    # Open the yaml file
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
        feature_flag = config.get('feature_flag', [])
        blacklisted_words = config.get('blacklisted_words', [])

        # Check whether the feature is turned on
        if feature_flag:
            # Delete the blacklisted word from word_frequency
            for word in blacklisted_words:
                del word_frequency[word]

    return word_frequency    

def get_word_frequency(topic: str, n: int) -> Tuple[List[Tuple[str, int]], bool]:
    # Fetch the Wikipedia article text
    wiki_wiki = Wikipedia('WikiWordCount/1.0' ,'en')

    wiki_page = wiki_wiki.page(topic)
    text = wiki_page.text

    # If the page doesn't exist, return empty list
    if not wiki_page.exists():
        return [], False

    # Analyze word frequency
    words = text.split()
    # Count the word frequency using directory
    word_frequency = defaultdict(int)
    for word in words:
        word_frequency[word] += 1
    
    # Blacklist words
    word_frequency = blacklist_words(word_frequency)

    pq = PriorityQueue()
    # Get top n words using prority queue
    for word, count in word_frequency.items():
        pq.put((count, word))
        if pq.qsize() > n:
            pq.get()

    top_words = [{ 'word': None, 'count': None}] * pq.qsize()

    # Arrange the output before returning result
    for i in range(len(top_words) - 1, -1, -1):
        count, word = pq.get()
        top_words[i] = { 'word': word, 'count': count}

    return top_words, True