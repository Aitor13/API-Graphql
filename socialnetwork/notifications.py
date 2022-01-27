from django.core.mail import send_mail

class Email:
    '''
    this is a testing mail class
    '''
    def __init__(self, user_posts, user_send):
        self.user_who_posts = user_posts
        self.user_to_send = user_send
        
    def send(self):
        send_mail('test', f'{self.user_who_posts} has posted new message!', 'from@email.com', [f'{self.user_to_send}'])