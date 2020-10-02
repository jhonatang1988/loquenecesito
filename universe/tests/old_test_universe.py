import json
import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model


@pytest.fixture
def rq_authenticated(rf, make_user):
    user = make_user(email='tests@example.lan', password='tests')

    request = rf.post('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = user

    return request


@pytest.fixture
def rq_anonymous(rf):
    request = rf.post('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = AnonymousUser()

    return request


class TestUniverse(GraphQLTestCase):
    GRAPHQL_URL = '/universe'

    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.user = get_user_model().objects.create(username='tests')
        self.client.authenticate(self.user)

    def test_all_characters_query(self):
        response = self.query(
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
            '''
            ,
            op_name='allCharacters'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_character_by_name_query(self):
        response = self.query(
            '''
            query characterByName {
                allCharacters(name_Icontains: "sky") {
                    edges {
                        node {
                            name
                        }
                    }
              }
            }
            '''
            ,
            op_name='characterByName'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_character_by_id_query(self):
        response = self.query(
            '''
            query CharacterById {
              character(id: "Q2hhcmFjdGVyTm9kZTo3") {
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
            '''
            ,
            op_name='CharacterById'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_all_users_query(self):
        response = self.query(
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
            '''
            ,
            op_name='allUsers'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_whoAmI_query(self):
        response = self.query(
            '''
            query whoAmI {
              me {
                username
                email
              }
            }
            '''
            ,
            op_name='whoAmI'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_whoAmI_query(self):
        response = self.query(
            '''
            query whoAmI {
              me {
                username
                email
              }
            }
            '''
            ,
            op_name='whoAmI'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_register_user_mutation(self):
        response = self.query(
            '''
            mutation registerPedro {
              register (
                input: {
                  email: "pedro@gmail.com"
                    username: "pedro"
                    password1: "Pedro_1988"
                  password2: "Pedro_1988"
                }
              ) {
                success
                errors
                token
                refreshToken
              }
            }
            '''
            ,
            op_name='registerPedro'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_get_user_pedro_query(self):
        response = self.query(
            '''
            query getPedro {
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
            '''
            ,
            op_name='getPedro'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_login_user_mutation(self):
        response = self.query(
            '''
            mutation loginJuan1 {
              tokenAuth (
                input: {
                  password: "Java_1988"
                  username: "juan1"
                }
              ) {
                token
              }
            }
            '''
            ,
            op_name='loginJuan1'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_update_user_mutation(self):
        response = self.query(
            '''
            mutation updateJuan1 {
              updateAccount (
                input: {
                  lastName: "Perezoso"
                }
              ) {
                success
                errors
                clientMutationId
              }
            }
            '''
            ,
            op_name='updateJuan1'
        )

        content = json.loads(response.content)
        assert 'errors' not in content

    def test_create_character_mutation(self):
        response = self.query(
            '''
            mutation createCharacter {
              createCharacter (
                input: {
                  name: "Wicket Systri Warrick"
                  moviesIds: [
                    {
                      id: "TW92aWVOb2RlOjM="
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
            '''
            ,
            op_name='createCharacter'
        )

        content = json.loads(response.content)
        assert 'errors' not in content
