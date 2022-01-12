"""Static Variables"""
import re


ADJECTIVES = (
    "adorable",
    "aegyo",
    "baby",
    "charming",
    "cute",
    "cutest",
    "darling",
    "kawaii",
    "little",
    "pygmy",
    "small",
    "smol",
    "smooshy",
    "snuggly",
    "softest",
    "sweet",
    "teensy",
    "tiny",
)
"""Search term - adjectives."""

NOUNS = (
    "alpaca",
    "axolotl",
    "bear",
    "bird",
    "birdy",
    "bunny",
    "butterfly",
    "cat",
    "deer",
    "doe",
    "dog",
    "doggie",
    "dolphin",
    "duck",
    "duckling",
    "echidna",
    "fawn",
    "frog",
    "froggy",
    "hampster",
    "harp seal",
    "hedgehog",
    "junco",
    "kitten",
    "kitty",
    "koala",
    "lion",
    "llama",
    "narwhal",
    "newt",
    "owl",
    "ocelot",
    "pangolin",
    "piggy",
    "pony",
    "pupper",
    "puppy",
    "quokka",
    "rabbit",
    "raccoon",
    "seal",
    "sloth",
    "snail",
    "squirrel",
    "tiger",
    "toad",
    "tortoise",
    "turtle",
    "wolf pup",
    "wolf",
)
"""Search term - nouns."""

MODIFIERS = (
    "cuddling",
    "wearing a hat",
    "in a house",
    "playing",
    "sleeping",
    "wearing onesie",
    "in a cup",
    "on a hill",
    "purring",
    "whimpering",
)
"""Optional search terms - modifiers."""

EXCLUDE = (
    "-disgusting",
    "-gross",
    "-icky",
    "-poop",
    "-porn",
    "-sexy",
    "-shit",
    "-ugly",
    "-xxx",
    "-rotten",
    "-horrible",
)
"""Terms to exclude from searches"""

# Strings that shouldn't appear in any URLs:
URL_EXCLUDE = (
    "?show_error=true",
    "amazon",
    "etsy",
    "goldporntube",
    "google.com/search",
    "item",
    "pornhub",
    "pornography",
    "product",
    "redtube",
    "teepublic",
    "tube8",
    "xhampster",
    "xnxx",
    "xxx",
    "yandex.com",
    "youporn",
    "zillow",
)
"""Url substrings to exlude."""

BAD_URL_RE_STR = rf"^.+?({'|'.join([re.escape(x) for x in URL_EXCLUDE])}).+?"
"""All bad url data concatenated into a regular expression strings."""

BAD_URL_RE = re.compile(BAD_URL_RE_STR)
"""Compiled regular expression of bad url substrings."""

IMAGE_URL_RE = re.compile(r"https?.+[.](?:jpg|jpeg|png|webp|gif|tiff)")
"""Match image urls."""

KITTEN = "      |\\__/,|   (`\\\n" "    _.|o o  |_   ) )\n" "---(((---(((---------"
"""Important Art"""
