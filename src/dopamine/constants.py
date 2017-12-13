"""Static Variables"""
from __future__ import unicode_literals
import re

THREADS = 8  # Threads to use when checking URLS
"""Default concurrency setting."""

ADJECTIVES = (
    'adorable',
    'aegyo',
    'baby',
    'charming',
    'cute',
    'darling',
    'kawaii',
    'little',
    'snuggly',
    'sweet',
    'tiny',
)
"""Search term - adjectives."""

NOUNS = (
    'alpaca',
    'axolotl',
    'baby duck',
    'baby sloth',
    'bear',
    'bird',
    'birdy',
    'bunny',
    'cat',
    'deer',
    'doe',
    'dog',
    'doggie',
    'dolphin',
    'duckling',
    'echidna',
    'fawn',
    'frog',
    'hampster',
    'harp seal',
    'hedgehog',
    'junco',
    'kitten',
    'kitty',
    'koala',
    'newt',
    'owl',
    'pangolin',
    'piggy',
    'puppy',
    'quokka',
    'rabbit',
    'raccoon',
    'seal',
    'squirrel',
    'turtle',
    'wolf pup',
    'wolf',
)
"""Search term - nouns."""

MODIFIERS = (
    'cuddle',
    'cuddling',
    'hat',
    'house',
    'playing',
    'sleeping',
    'wearing onesie',
)
"""Optional search terms - modifiers."""

EXCLUDE = (
    '-disgusting',
    '-gross',
    '-icky',
    '-poop',
    '-porn',
    '-sexy',
    '-shit',
    '-ugly',
    '-xxx',
)
"""Terms to exclude from searches"""

# Strings that shouldn't appear in any URLs:
URL_EXCLUDE = (
    '?show_error=true',
    'google.com/search',
    'redtube',
    'teepublic',
    'tube8',
    'xnxx',
    'xxx',
    'youporn',
    'zillow',
)
"""Url substrings to exlude."""

RE_STR = r'^.+?({0}).+?'.format('|'.join([re.escape(x) for x in URL_EXCLUDE]))
"""All bad url data concatenated into a regular expression strings."""

BAD_URL_RE = re.compile(RE_STR)
"""Compiled regular expression of bad url substrings."""

JSON_RE = re.compile(r'{.+?}')
"""Regex to find JSON in page."""
