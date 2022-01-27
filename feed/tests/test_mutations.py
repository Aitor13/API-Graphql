from django.contrib.auth import get_user_model
from graphql_jwt.utils import jwt_encode, jwt_payload
import json
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
from feed.models import Feed


class FeedTests(GraphQLTestCase):
    
    GRAPHQL_URL = "/graphql"
      
    def setUp(self):
        self.user1 = get_user_model().objects.create(username="test", password='1234')
        self.payload = jwt_payload(self.user1)
        self.token = jwt_encode(self.payload)
        self.headers = {'HTTP_AUTHORIZATION': f'JWT {self.token}'}
        
    def test_create_feed(self):
        response = self.query(
            '''
            mutation createFeed($feed: String!, $visibility: String!){
                createFeed(feed: $feed, visibility: $visibility){
                    feed{
                        feed
                        visibility
                    }
                }
            }
            ''',
            op_name='createFeed',
            variables={'feed':'Test feed','visibility':'PUB'},
            headers=self.headers)
        
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['createFeed']['feed']['feed'], 'Test feed')
        self.assertEqual(content['data']['createFeed']['feed']['visibility'], 'PUB')
        
        
    def test_update_feed_visibility(self):
        feed = mixer.blend(Feed, user=self.user1, feed='Test feed', visibility='PUB')
        response = self.query(
            '''
            mutation updateFeed($id: Int!, $visibility: String!){
                updateFeedVisibility(id: $id, visibility: $visibility){
                    feed{
                        feed
                        visibility
                    }
                }
            }
            ''',
            op_name='updateFeed',
            variables={'id':feed.id,'visibility':'PRO'},
            headers=self.headers)
        
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['updateFeedVisibility']['feed']['feed'], feed.feed)
        self.assertEqual(content['data']['updateFeedVisibility']['feed']['visibility'], 'PRO')
        
        
    def test_delete_feed(self):
        feed = mixer.blend(Feed, user=self.user1, feed='Test feed', visibility='PUB')
        response = self.query(
            '''
            mutation deleteFeed($id: Int!){
                deleteFeed(id: $id){
                    msg
                }
            }
            ''',
            op_name='deleteFeed',
            variables={'id':feed.id},
            headers=self.headers)
        
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['deleteFeed']['msg'], 'Feed deleted')

        