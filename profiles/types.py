from graphene_django import DjangoObjectType
from feed.models import CustomUser
from profiles.models import FollowRequests


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        exclude = ['password']

class FollowRequestsType(DjangoObjectType):
    class Meta:
        model = FollowRequests
        fields = '__all__'