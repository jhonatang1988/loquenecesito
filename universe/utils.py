"""
several reusable functions
"""
from graphql_relay import from_global_id


def fromGlobalToObjs(movies_ids, model):
    """
    get objects from global relay ids
    """
    movies_pks = []
    for movie_input in movies_ids:
        movies_pks.append(from_global_id(movie_input.id)[1])
    objects = model.objects.filter(id__in=movies_pks)

    return objects
