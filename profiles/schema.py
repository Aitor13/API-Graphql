import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from profiles.types import CustomUserType, FollowRequestsType
from profiles.models import CustomUser, FollowRequests
from graphql_jwt.decorators import login_required


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

        
class ProfilesQuery(UserQuery, MeQuery, graphene.ObjectType):
    search_user = graphene.List(CustomUserType, user=graphene.String(required=True))
    get_list_requests = graphene.List(FollowRequestsType)
    get_followers = graphene.List(CustomUserType)
    get_who_i_follow = graphene.List(CustomUserType)
    
    @login_required
    def resolve_search_user(self, info, user):
        return CustomUser.objects.filter(username__contains=user)
    
    @login_required
    def resolve_get_list_requests(self, info):
        profile = CustomUser.objects.get(username=info.context.user)
        return FollowRequests.objects.filter(to_user=profile)

    @login_required
    def resolve_get_followers(self, info):
        follower_profile = get_follower_profile(info.context.user)
        return follower_profile
    
    @login_required
    def resolve_get_who_i_follow(self, info):
        user_i_follow_list = CustomUser.objects.filter(friends__username=info.context.user) 
        return user_i_follow_list
    
        
def get_follower_profile(user):
    return CustomUser.objects.get(username=user).friends.all()
    

