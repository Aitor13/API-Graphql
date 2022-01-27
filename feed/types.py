from graphene_django import DjangoObjectType
from feed.models import Feed


class FeedType(DjangoObjectType):
    class Meta:
        model = Feed
        fields = '__all__'