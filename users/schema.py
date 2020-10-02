import graphene
from graphql_auth import relay


class AuthMutation(graphene.ObjectType):
    """
    allow users to register, verify_acounts, auth with token, and update 
    account
    """
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    token_auth = relay.ObtainJSONWebToken.Field()
    update_account = relay.UpdateAccount.Field()
