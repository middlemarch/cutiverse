# Standard
import logging
import random

# Project
from dopameme.constants import ADJECTIVES, NOUNS, MODIFIERS, EXCLUDE

LOG = logging.getLogger(__name__)


class SearchObj:
    """Representation of a search query that can be rendered."""

    __slots__ = ("exclude", "noun", "adjective", "include_modifier", "modifier")

    def __init__(self, **kwargs):
        # Randomly select an index for each type
        adjective_idx = random.randint(0, len(ADJECTIVES) - 1)
        noun_idx = random.randint(0, len(NOUNS) - 1)
        modifier_idx = random.randint(0, len(MODIFIERS) - 1)

        rand_noun = NOUNS[noun_idx]
        rand_adj = ADJECTIVES[adjective_idx]
        rand_mod = MODIFIERS[modifier_idx]

        self.exclude = EXCLUDE
        self.noun = kwargs.get("noun", rand_noun) or rand_noun
        self.adjective = kwargs.get("adjective", rand_adj) or rand_adj

        # Add a modifier (sometimes)
        self.include_modifier = bool(random.randint(0, 1))
        self.modifier = kwargs.get("modifier", rand_mod) or rand_mod

    @property
    def default_str(self):
        term_list = []
        term_list.extend(self.adjective.split(" "))
        term_list.extend(self.noun.split(" "))
        if self.include_modifier:
            term_list.append(f'"{self.modifier}"')
        term_list.extend(self.exclude)
        return " ".join(term_list)

    @property
    def display_str(self):
        """A printable representation of the search terms."""
        term_list = []
        term_list.extend(self.adjective.split(" "))
        term_list.extend(self.noun.split(" "))
        if self.include_modifier:
            term_list.extend(self.modifier.split(" "))
        return " ".join(term_list)
