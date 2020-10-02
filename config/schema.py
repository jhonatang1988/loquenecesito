import graphene
import universe.schema
from graphql_auth.schema import UserQuery, MeQuery
import users.schema


class Query(UserQuery, MeQuery, universe.schema.Query, graphene.ObjectType):
    """ a mixture to combine all app query objects into one"""
    pass


class Mutation(users.schema.AuthMutation,
               universe.schema.CharacterMutations,
               universe.schema.PlanetMutations,
               universe.schema.MovieMutations,
               graphene.ObjectType):
    """a mixture to combine all app mutations objects into one"""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
