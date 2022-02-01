import graphene
from profiles.schema import AuthMutation
from profiles.types import FollowRequestsType
from profiles.models import CustomUser, FollowRequests


class ProfilesMutation(AuthMutation, graphene.ObjectType):
       class Arguments:
            pass

class RequestToFollow(graphene.Mutation):
    class Arguments:
        user = graphene.String()
    request = graphene.Field(FollowRequestsType)
    msg = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, user):
        profile_to_user = CustomUser.objects.get(username=user)
        profile_from_user = CustomUser.objects.get(username=info.context.user)
        request = FollowRequests.objects.filter(from_user=profile_from_user, to_user=profile_to_user).first()
        msg = 'The request already exists' if request else 'Request created'
        if not request:
            request = FollowRequests.objects.create(from_user=profile_from_user, to_user=profile_to_user)
        return RequestToFollow(request=request, msg=msg)
    
    
class AcceptRequest(graphene.Mutation):
    class Arguments:
        id = graphene.Int()   
    msg = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, id):
        profile = CustomUser.objects.get(username=info.context.user)
        request = FollowRequests.objects.get(pk=id, to_user=profile)
        profile_user_follower = request.from_user
        # Add like a friend
        profile.friends.add(profile_user_follower)
        profile.save()
        # Delete the request
        request.delete()
        msg = "Request accepted! you have a new friend!"
        return AcceptRequest(msg=msg)
    
    
class RefuseRequest(graphene.Mutation):
    class Arguments:
        id = graphene.Int()   
    msg = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, id):
        profile = CustomUser.objects.get(username=info.context.user)
        request = FollowRequests.objects.get(pk=id, to_user=profile).delete()
        msg = "Request refused!"
        return AcceptRequest(msg=msg)
    
class DeleteFollower(graphene.Mutation):
    class Arguments:
        user = graphene.String()
    msg = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, user):
        profile = CustomUser.objects.get(username=info.context.user)
        profile_to_delete = CustomUser.objects.get(username=user)
        profile.friends.remove(profile_to_delete)
        msg = f"{user} deleted"
        return DeleteFollower(msg=msg)
    
class DeleteFollowing(graphene.Mutation):
    class Arguments:
        user = graphene.String()
    msg = graphene.String()

    @classmethod
    def mutate(cls, root, info, user):
        profile = CustomUser.objects.get(username=user)
        profile_to_delete = CustomUser.objects.get(username=info.context.user)
        profile.friends.remove(profile_to_delete)
        msg = f"{user} and you are no longer friends"
        return DeleteFollowing(msg=msg)
            
    
class RequestsMutation(graphene.ObjectType):
    send_request_to_follow = RequestToFollow.Field()
    accept_request = AcceptRequest.Field()
    refuse_request = RefuseRequest.Field()
    delete_follower = DeleteFollower.Field()
    delete_following = DeleteFollowing.Field()