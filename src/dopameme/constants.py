"""Static Variables"""
from __future__ import unicode_literals, absolute_import
import re


ADJECTIVES = (
    'adorable',
    'aegyo',
    'baby',
    'charming',
    'cute',
    'darling',
    'kawaii',
    'little',
    'pygmy',
    'small',
    'smol',
    'snuggly',
    'sweet',
    'teensy',
    'tiny',
)
"""Search term - adjectives."""

NOUNS = (
    'alpaca',
    'axolotl',
    'bear',
    'bird',
    'birdy',
    'bunny',
    'butterfly',
    'cat',
    'deer',
    'doe',
    'dog',
    'doggie',
    'dolphin',
    'duck',
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
    'pony',
    'pupper',
    'puppy',
    'quokka',
    'rabbit',
    'raccoon',
    'seal',
    'sloth',
    'squirrel',
    'toad',
    'tortoise',
    'turtle',
    'wolf pup',
    'wolf',
)
"""Search term - nouns."""

MODIFIERS = (
    'cuddling',
    'wearing a hat',
    'in a house',
    'playing',
    'sleeping',
    'wearing onesie',
    'in a cup',
    'on a hill',
    'purring',
    'whimpering',
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
    '-rotten',
    '-horrible',
)
"""Terms to exclude from searches"""

# Strings that shouldn't appear in any URLs:
URL_EXCLUDE = (
    '?show_error=true',
    'amazon',
    'etsy',
    'google.com/search',
    'item',
    'product',
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

GOOGLE_IMG_RE = re.compile(r'https?.+[.](?:jpg|jpeg|png|webp|gif|tiff)')
"""Match image url destinations in google image results."""

KITTEN = (
    '      |\\__/,|   (`\\\n'
    '    _.|o o  |_   ) )\n'
    '---(((---(((---------'
)
"""Important Art"""
