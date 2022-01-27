from django.contrib.auth import get_user_model
from profiles.models import FollowRequests
from graphql_jwt.utils import jwt_encode, jwt_payload
import json
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer

class ProfileTests(GraphQLTestCase):
    
    GRAPHQL_URL = "/graphql"
      
    def setUp(self):
        self.user1 = get_user_model().objects.create(username="test", password='1234')
        self.user2 = get_user_model().objects.create(username="test2", password='1234')
        self.payload = jwt_payload(self.user1)
        self.token = jwt_encode(self.payload)
        self.headers = {'HTTP_AUTHORIZATION': f'JWT {self.token}'}
      
        
    def test_create_request(self):
        response = self.query(
            '''
            mutation requestToFollow($username: String!){
              sendRequestToFollow(user:$username){
               msg
                }
              }
            ''',
        op_name="requestToFollow",
        variables={"username": self.user2.username},
        headers=self.headers
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['sendRequestToFollow']['msg'], 'Request created')
        
        
    def test_accept_request(self):
        follow = mixer.blend(FollowRequests, to_user=self.user1, from_user=self.user2)
        response = self.query(
            '''
            mutation acceptRequest($id: Int!){
                acceptRequest(id:$id){
                    msg
                }
            }
            ''',
            op_name="acceptRequest",
            variables={'id':follow.id},
            headers=self.headers
            )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['acceptRequest']['msg'], 'Request accepted! you have a new friend!')
        
        
    def test_refuse_request(self):
        follow = mixer.blend(FollowRequests, to_user=self.user1, from_user=self.user2)
        response = self.query(
            '''
            mutation refuseRequest($id: Int!){
                refuseRequest(id:$id){
                    msg
                }
            }
            ''',
            op_name="refuseRequest",
            variables={'id':follow.id},
            headers=self.headers
            )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['refuseRequest']['msg'], 'Request refused!')
        
        
    def test_delete_follower(self):
        self.user1.friends.add(self.user2)
        response = self.query(
            '''
            mutation deleteFollower($username: String!){
                deleteFollower(user:$username){
                    msg
                }
            }
            ''',
            op_name="deleteFollower",
            variables={'username':self.user2.username},
            headers=self.headers
            )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['deleteFollower']['msg'], f'{self.user2.username} deleted')
        
        
    def test_delete_following(self):
        self.user2.friends.add(self.user1)
        response = self.query(
            '''
            mutation deleteFollowing($username: String!){
                deleteFollowing(user:$username){
                    msg
                }
            }
            ''',
            op_name="deleteFollowing",
            variables={'username':self.user1.username},
            headers=self.headers
            )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['deleteFollowing']['msg'], f'{self.user1.username} and you are no longer friends')
        
        
        
        