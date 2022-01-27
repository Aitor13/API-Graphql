import graphene
from graphql_auth.schema import UserQuery, MeQuery
from feed.models import Feed
from profiles.models import CustomUser
from graphql_jwt.decorators import login_required
from feed.types import FeedType
from django.db.models import Q
from profiles.schema import ProfilesQuery


class FeedQuery(UserQuery, MeQuery, graphene.ObjectType):
    get_all_my_feeds = graphene.List(FeedType)
    get_all_feeds_from_user = graphene.List(FeedType, user=graphene.String(required=True))
    get_timeline_feeds = graphene.List(FeedType)
    
    @login_required
    def resolve_get_all_my_feeds(self, info):
        profile = CustomUser.objects.get(username=info.context.user)
        return Feed.objects.filter(user=profile).order_by('-created_at')
        
    @login_required
    def resolve_get_all_feeds_from_user(self, info, user):
        profile, query = get_feed_visibility(info, user)
        return Feed.objects.filter(query, user=profile)
    
    @login_required
    def resolve_get_timeline_feeds(self, info):
        who_i_follow_list = ProfilesQuery().resolve_get_who_i_follow(info)
        feeds_from_user = []
        for user in who_i_follow_list:
            profile, query = get_feed_visibility(info, user)
            feeds_from_user +=  Feed.objects.filter(query, user=profile)
        feeds_from_user += Feed.objects.filter(user=info.context.user)
        return sorted(feeds_from_user, key=lambda feed: feed.created_at)
    
        
def get_feed_visibility(info, user):
        profile = CustomUser.objects.get(username=user)
        friends = profile.friends.all()
        query = Q(visibility = 'PUB')
        if friends:
            for friend in friends:
                if friend.username == str(info.context.user):
                    query = Q(visibility='PUB') | Q(visibility='PRO')
        return profile, query
