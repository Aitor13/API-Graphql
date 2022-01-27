from django.contrib.auth import get_user_model
from profiles.models import FollowRequests
from graphql_jwt.utils import jwt_encode, jwt_payload
import json
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
from feed.models import Feed



class FeedTests(GraphQLTestCase):
    
    GRAPHQL_URL = "/graphql"
      
    def setUp(self):
        self.user1 = get_user_model().objects.create(username="test", password='1234')
        self.user2 = get_user_model().objects.create(username="test2", password='1234')
        self.payload = jwt_payload(self.user1)
        self.token = jwt_encode(self.payload)
        self.headers = {'HTTP_AUTHORIZATION': f'JWT {self.token}'}
      
        
    def test_get_all_my_feeds(self):
        feed = mixer.blend(Feed, user=self.user1, feed='Test feed', visibility='PUB')
        response = self.query(
            '''
            query getAllMyFeeds{
              getAllMyFeeds{
               feed
              }
            }
            ''',
        op_name="getAllMyFeeds",
        headers=self.headers
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['getAllMyFeeds'][0]['feed'], feed.feed)
        
        
    def test_get_all_feeds_from_user(self):
        feed = mixer.blend(Feed, user=self.user2, feed='Test feed', visibility='PUB')
        response = self.query(
            '''
            query getAllFeeds($username: String!){
              getAllFeedsFromUser(user:$username){
               feed
              }
            }
            ''',
        op_name="getAllFeeds",
        variables={'username':self.user2.username},
        headers=self.headers
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['getAllFeedsFromUser'][0]['feed'], feed.feed)
        
        
    def test_get_timeline_feeds(self):
        feed1 = mixer.blend(Feed, user=self.user1, feed='user1 feed')
        feed2 = mixer.blend(Feed, user=self.user2, feed='user2 feed', visibility='PUB')
        self.user2.friends.add(self.user1)
        response = self.query(
            '''
            query getTimelineFeeds{
              getTimelineFeeds{
               feed
              }
            }
            ''',
        op_name="getTimelineFeeds",
        headers=self.headers
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['getTimelineFeeds'][0]['feed'], feed1.feed)
        self.assertEqual(content['data']['getTimelineFeeds'][1]['feed'], feed2.feed)