import graphene
from profiles.schema import ProfilesQuery as profiles_query
from feed.schema import FeedQuery as feed_query
from profiles.mutations import ProfilesMutation as profiles_mutation
from feed.mutations import FeedMutation as feed_mutation
from profiles.mutations import RequestsMutation as requests_mutation

'''
this module take profiles and feed Apps schema

'''
class Query(profiles_query, feed_query):
    pass

class Mutation(profiles_mutation, feed_mutation, requests_mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)