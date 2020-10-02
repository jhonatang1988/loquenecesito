import graphene


class StuffPerson(graphene.Interface):
    """ Interface for all real human persons involved in StarWars
        as Directors, stuff, producers, actors. """
    id = graphene.ID(required=True)
    name = graphene.String()
