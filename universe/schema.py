import graphene
from graphene import relay, ObjectType, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .utils import fromGlobalToObjs
from graphql_jwt.decorators import login_required

from .models import Movie, Character, Planet, Person


class MovieNode(DjangoObjectType):
    """
    Movie Type for graphql
    """

    class Meta:
        model = Movie
        interfaces = (relay.Node,)


class CharacterNode(DjangoObjectType):
    """
    Character Node
    """

    class Meta:
        model = Character
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class PlanetNode(DjangoObjectType):
    """
    Planet Type
    """

    class Meta:
        model = Planet
        interfaces = (relay.Node,)


class PersonNode(DjangoObjectType):
    """
    Person Type
    """

    class Meta:
        model = Person
        filter_fields = ['job_role']
        interfaces = (relay.Node,)


class Query(ObjectType):
    character = relay.Node.Field(CharacterNode)
    all_characters = DjangoFilterConnectionField(CharacterNode)


# InputObjectTypes for mutations
class MovieInput(graphene.InputObjectType):
    id = graphene.ID()


# mutations
# character mutations
class CreateCharacter(relay.ClientIDMutation):
    """
    Creates a new character, it needs movie relay global id
    """

    character = graphene.Field(CharacterNode)

    class Input:
        name = graphene.String(required=True)
        movies_ids = graphene.List(MovieInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        character = Character.objects.create(name=kwargs.get('name'))
        movies = fromGlobalToObjs(kwargs.get('movies_ids'), Movie)
        character.movies.set(movies)
        character.save()
        return CreateCharacter(character=character)


class CreatePlanet(relay.ClientIDMutation):
    """
    Mutation to create planet objects
    """
    planet = graphene.Field(PlanetNode)

    class Input:
        name = graphene.String(required=True)
        movies_ids = graphene.List(MovieInput, required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        planet = Planet.objects.create(name=kwargs.get('name'))
        movies = fromGlobalToObjs(kwargs.get('movies_ids'), Movie)
        planet.movies.set(movies)
        planet.save()
        return CreatePlanet(planet=planet)


class CreateMovie(relay.ClientIDMutation):
    """
    Mutation to create a Movie
    """
    movie = graphene.Field(MovieNode)

    class Input:
        name = graphene.String(required=True)
        opening_crawl = graphene.String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        movie = Movie.objects.create(name=kwargs.get('name'),
                                     opening_crawl=kwargs.get('opening_crawl'))
        return CreateMovie(movie=movie)


class CharacterMutations(AbstractType):
    create_character = CreateCharacter.Field()


class PlanetMutations(AbstractType):
    create_planet = CreatePlanet.Field()


class MovieMutations(AbstractType):
    create_movie = CreateMovie.Field()
