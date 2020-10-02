from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView


class MembersOnlyStarWarsUniverse(LoginRequiredMixin, GraphQLView):
    """ Mixins to make the universe of Start Wars private """
    # not being user actually
    pass
