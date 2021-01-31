import re

from django.contrib.postgres.search import SearchQuery


def combine_query(q1, q2):
    return q1 | q2 if q1 else q2


def consume(qs):
    pattern = re.compile(
        r'\+\s*(?P<and>[\w,\s,",(,),+]+)|"(?P<phrase>[\w,\s]+)"|(?P<keywords>[\w]+)',
        re.IGNORECASE,
    )

    results = pattern.findall(qs)
    query = None

    for result in results:
        if result[0]:    # And
            query = query & consume(result[0])

        if result[1].strip():    # Phrase
            query = combine_query(
                query, SearchQuery(result[1].strip(), search_type="phrase"))

        if result[2].strip():    # Keywords
            query = combine_query(
                query, SearchQuery(result[2].strip(), search_type="plain"))
    return query
