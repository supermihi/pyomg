from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Alias:
    name: str
    sort_name: str | None


def get_alias(alias_list: list, preferred_locales: Sequence[str]) -> Alias | None:
    alias = None
    sort_name = None
    for locale in [*preferred_locales, None]:
        primary_aliases = [a for a in alias_list if a.get('locale') == locale and a.get('primary') == 'primary']
        if len(primary_aliases) > 0:
            primary_alias = primary_aliases[0]
            if alias is None:
                alias = primary_alias['alias']
            if sort_name is None:
                sort_name = primary_alias.get('sort-name')
    if alias is None:
        return None
    return Alias(alias, sort_name)
