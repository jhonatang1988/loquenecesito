import json
from graphene_django.utils.testing import graphql_query
from universe.models import Character, Movie, Planet, Person
from universe.enums import JobRoleType

import pytest


@pytest.fixture
def client_query(admin_client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=admin_client,
                             graphql_url='/universe')

    return func


@pytest.fixture
def mixers(admin_client):
    a_movie = Movie.objects.create(name='a_movie_name',
                                   opening_crawl='a_movie_opening_crawl')
    a_character = Character.objects.create(name='a_character_name')
    a_character.movies.set([a_movie])

    a_planet = Planet.objects.create(name='a_planet_name')
    a_planet.movies.set([a_movie])
    a_director = Person.objects.create(name='a_director_name',
                                       job_role=JobRoleType.DIRECTOR)
    a_director.movies.set([a_movie])

    a_producer = Person.objects.create(name='a_producer_name',
                                       job_role=JobRoleType.PRODUCER)
    a_producer.movies.set([a_movie])


def test_all_characters(client_query, mixers):
    response = client_query(
        '''
        query allCharacters {
          allCharacters {
                edges {
              node {
                id
                name
              }
            }
          }
        }
        ''',
        op_name='allCharacters'
    )

    expected = {'data': {'allCharacters': {'edges': [{'node': {
        'id': 'Q2hhcmFjdGVyTm9kZTox', 'name': 'a_character_name'}}]}}}
    content = json.loads(response.content)

    assert expected == content


def test_character_by_name(client_query, mixers):
    response = client_query(
        '''
        query characterByName {
          allCharacters(name_Icontains: "a_character_name") {
            edges {
              node {
                name
              }
            }
          }
        }
        ''',
        op_name='characterByName'
    )

    expected = {'data': {
        'allCharacters': {'edges': [{'node': {'name': 'a_character_name'}}]}}}

    content = json.loads(response.content)

    assert expected == content


def test_character_by_id(client_query, mixers):
    response = client_query(
        '''
        query characterById {
          character(id: "Q2hhcmFjdGVyTm9kZTox") {
            name
            movies {
              edges {
                node {
                  id
                  name
                  openingCrawl
                  directors: persons(jobRole: "DIR") {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                  producers: persons(jobRole: "PDR") {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                  planets {
                    edges {
                      node {
                        id
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
        ''',
        op_name='characterById'
    )

    expected = {'data': {'character': {'name': 'a_character_name', 'movies': {
        'edges': [{'node': {'id': 'TW92aWVOb2RlOjE=', 'name': 'a_movie_name',
                            'openingCrawl': 'a_movie_opening_crawl',
                            'directors': {'edges': [
                                {'node': {'name': 'a_director_name'}}]},
                            'producers': {'edges': [
                                {'node': {'name': 'a_producer_name'}}]},
                            'planets': {'edges': [{'node': {
                                'id': 'UGxhbmV0Tm9kZTox',
                                'name': 'a_planet_name'}}]}}}]}}}}

    content = json.loads(response.content)

    assert expected == content


def test_all_users(client_query, mixers):
    response = client_query(
        '''
        query allUsers {
          users {
            edges {
              node {
                username
                verified
              }
            }
          }
        }
        ''',
        op_name='allUsers'
    )

    expected = {'data': {'users': {
        'edges': [{'node': {'username': 'admin', 'verified': False}}]}}}

    content = json.loads(response.content)

    assert expected == content


def test_who_am_i(client_query, mixers):
    response = client_query(
        '''
        query whoAmI {
          me {
            username
            email
          }
        }
        ''',
        op_name='whoAmI'
    )

    expected = {
        'data': {'me': {'username': 'admin', 'email': 'admin@example.com'}}}

    content = json.loads(response.content)

    assert expected == content


def test_user_auth(client_query, mixers):
    response = client_query(
        '''
        mutation registerJuan1 {
          register (
            input: {
                email: "juan1@gmail.com"
                username: "juan1"
                password1: "kn2rn##3mnd"
                password2: "kn2rn##3mnd"
            }
          ) {
            success
            errors
            token
            refreshToken
          }
        }
        ''',
        op_name='registerJuan1'
    )

    _ = {'data': {'register': {'success': True, 'errors': None,
                               'token': 'nada',
                               'refreshToken': 'nada'}}}

    content = json.loads(response.content)

    assert content['data']['register']['success']

    response2 = client_query(
        '''
        query getJuan1 {
          users (last: 1) {
            edges {
              node {
                id
                username
                email
                verified
                lastName
              }
            }
          }
        }
        ''',
        op_name='getJuan1'
    )

    expected = {'data': {'users': {'edges': [{'node': {
        'id': 'VXNlck5vZGU6Mg==', 'username': 'juan1',
        'email': 'juan1@gmail.com', 'verified': False, 'lastName': ''}}]}}}

    content2 = json.loads(response2.content)

    assert expected == content2

    response3 = client_query(
        '''
        mutation loginJuan1 {
          tokenAuth (
            input: {
              password: "kn2rn##3mnd"
              username: "juan1"
            }
          ) {
            token
          }
        }
        ''',
        op_name='loginJuan1'
    )

    content3 = json.loads(response3.content)

    assert content3['data']['tokenAuth']['token']


def test_create_movie(client_query):
    response = client_query(
        f'''
        mutation createMovie {{
          createMovie (
            input: {{
        name: "The Phantom Menace"
              openingCrawl: "Hue war is coming"
            }}
          ) {{
            movie {{
              id
              name
              openingCrawl
            }}
          }}
        }}
        ''',
        op_name='createMovie'
    )

    expected = {'data': {'createMovie': {
        'movie': {'id': 'TW92aWVOb2RlOjE=', 'name': 'The Phantom Menace',
                  'openingCrawl': 'Hue war is coming'}}}}

    content = json.loads(response.content)

    assert expected == content


def test_create_planet(client_query):
    response = client_query(
        '''
        mutation createPlanet {
          createPlanet (
            input: {
              name: "Naboo"
              moviesIds: [
                {
                  id: "TW92aWVOb2RlOjE="
                }
              ]
            }
          ) {
            planet {
              name
              movies {
                edges {
                  node {
                    name
                  }
                }
              }
            }
          }
        }
        ''',
        op_name='createPlanet'
    )

    expected = {'data': {'createPlanet': {
        'planet': {'name': 'Naboo', 'movies': {'edges': []}}}}}

    content = json.loads(response.content)
    print(content)

    assert expected == content


def test_create_character(client_query):
    response = client_query(
        '''
        mutation createCharacter {
          createCharacter (
            input: {
              name: "Wicket Systri Warrick"
              moviesIds: [
                {
                  id: "TW92aWVOb2RlOjE="
                }
              ]
            }
          ) {
            character {
              name
              movies {
                edges {
                  node {
                    name
                    openingCrawl
                  }
                }
              }
            }
          }
        }
        ''',
        op_name='createCharacter'
    )

    expected = {'data': {'createCharacter': {
        'character': {'name': 'Wicket Systri Warrick',
                      'movies': {'edges': []}}}}}

    content = json.loads(response.content)

    assert expected == content
