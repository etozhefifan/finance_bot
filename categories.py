import database
from typing import List, NamedTuple


class Category(NamedTuple):
    codename: str
    name: str
    is_basic_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        categories = database.fetchall(
            'category', 'codename name is_basic_expense aliases'.split()
        )
        self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories):
        for index, category in enumerate(Categories):
            aliases = category['aliases'].split(',')
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category['codename'])
            aliases.append(category['name'])
            categories[index]['aliases'] = aliases

    def get_all_categories(self):
        return self._categories

    def get_category(self, category_name):
        finded = None
        other_category = None
        for category in self._categories:
            if category['codename'] == 'other':
                other_category = category
            for alias in category['aliases']:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
