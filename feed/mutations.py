import graphene
from graphql_auth import mutations
from feed.models import Feed
from profiles.models import CustomUser
from feed.types import FeedType

    
class CreateFeed(graphene.Mutation):
    class Arguments:
        feed = graphene.String()
        visibility = graphene.String()
    feed = graphene.Field(FeedType)
    
    @classmethod
    def mutate(cls, root, info, feed, **kwargs):
        profile = CustomUser.objects.get(username=info.context.user)
        feed = Feed.objects.create(feed=feed, user=profile, visibility=kwargs.get('visibility'))
        return CreateFeed(feed=feed)        
    
    
class UpdateFeedVisibility(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        visibility = graphene.String()
    feed = graphene.Field(FeedType)
    
    @classmethod
    def mutate(cls, root, info, id, visibility):
        profile = CustomUser.objects.get(username=info.context.user)
        feed_object = Feed.objects.get(pk=id)
        setattr(feed_object,'visibility',visibility)
        feed_object.save()
        return UpdateFeedVisibility(feed=feed_object)  


class DeleteFeed(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
    feed = graphene.Field(FeedType)
    msg = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, id):
        msg = 'Feed deleted'
        profile = CustomUser.objects.get(username=info.context.user)
        feed = Feed.objects.get(pk=id, user=profile).delete()
        return DeleteFeed(feed=feed, msg=msg)



class FeedMutation(graphene.ObjectType):
    create_feed = CreateFeed.Field()
    update_feed_visibility = UpdateFeedVisibility.Field()
    delete_feed = DeleteFeed.Field()