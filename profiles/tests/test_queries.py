from django.contrib.auth import get_user_model
from graphql_jwt.utils import jwt_encode, jwt_payload
import json
from graphene_django.utils.testing import GraphQLTestCase
from profiles.models import FollowRequests
from mixer.backend.django import mixer

class ProfileTests(GraphQLTestCase):
      GRAPHQL_URL = "/graphql"
      
      def setUp(self):
            self.user1 = get_user_model().objects.create(username="test", password='1234')
            self.user2 = get_user_model().objects.create(username="test2", password='1234')
            self.payload = jwt_payload(self.user1)
            self.token = jwt_encode(self.payload)
            self.headers = {'HTTP_AUTHORIZATION': f'JWT {self.token}'}
      
        
      def test_search_user(self):
            response = self.query(
            '''
            query searchUser($username: String!){
              searchUser(user:$username){
                username
                }
              }
            ''',
            op_name="searchUser",
            variables={"username": self.user1.username},
            headers=self.headers
             )
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual(content['data']['searchUser'][0]['username'], self.user1.username)
        
        
      def test_get_list_requests(self):
            follow = mixer.blend(FollowRequests, to_user=self.user1, from_user=self.user2)
            response = self.query(
            '''
            query getListRequests{
              getListRequests{
                toUser{
                  username
                }
                }
              }
            ''',
            op_name="getListRequests",
            headers=self.headers
             )
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual(content['data']['getListRequests'][0]['toUser']['username'], self.user1.username)
            
            
      def test_get_followers(self):
            self.user1.friends.add(self.user2)
            response = self.query(
            '''
            query getFollowers{
              getFollowers{
                username
                }
                }
            ''',
            op_name="getFollowers",
            headers=self.headers
             )
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual(content['data']['getFollowers'][0]['username'], self.user2.username)


      def test_get_who_i_follow(self):
            self.user2.friends.add(self.user1)
            response = self.query(
            '''
            query getWhoIFollow{
              getWhoIFollow{
                username
                }
                }
            ''',
            op_name="getWhoIFollow",
            headers=self.headers
             )
            
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual(content['data']['getWhoIFollow'][0]['username'], self.user2.username)        
        