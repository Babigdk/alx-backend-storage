#!/usr/bin/env python3
""" Redis Module """
import requests
import time
from functools import wraps

# Cache dictionary to store URL responses and their access counts
cache = {}

def get_page(url: str) -> str:
    # Check if the URL is already cached and not expired
    if url in cache and time.time() - cache[url]['timestamp'] < 10:
        cache[url]['count'] += 1
        return cache[url]['content']

    # If not cached, make the request and cache the response
    response = requests.get(url)
    content = response.text

    # Store the response and access count in the cache
    cache[url] = {
        'content': content,
        'count': 1,
        'timestamp': time.time()
    }

    return content

# Decorator to add caching behavior to functions
def cache_response(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]

        if url in cache and time.time() - cache[url]['timestamp'] < 10:
            cache[url]['count'] += 1
            return cache[url]['content']

        response = func(*args, **kwargs)
        cache[url] = {
            'content': response,
            'count': 1,
            'timestamp': time.time()
        }

        return response

    return wrapper

# Apply the decorator to the get_page function
get_page = cache_response(get_page)

# Test the function
url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
content = get_page(url)
print(content)
