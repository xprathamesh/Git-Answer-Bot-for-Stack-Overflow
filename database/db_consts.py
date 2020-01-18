# BigQuery dataset links
from typing import List, NamedTuple

GITBUT_URI = "elated-nectar-258022.gitbot"
STACKOVERFLOW_URI = "elated-nectar-258022.stackoverflow"

# Shared data structures

# Structured format for storing parts linking to a column in a table.
# Can hold multiple columns if needed.
TableCols = NamedTuple('TableCols',
                       [('uri', str),
                       ('table', str),
                       ('cols', List[str])])

# Post = NamedTuple('Post',
#                   [
#                       ('title', str),
#                       ('body', str),
#                       ()
#                   ])

Cond = NamedTuple('Cond',
                   [
                       ('fst', TableCols or str),
                       ('comparison', str),
                       ('snd', TableCols or str)
                   ])