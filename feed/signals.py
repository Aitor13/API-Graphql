import django
from profiles.schema import get_follower_profile
from feed.models import Feed
from feed.workers import worker
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiprocessing import Pool
from functools import partial


@receiver(post_save, sender=Feed)
def send_mail_to_followers(sender, instance, **kwargs):
    match_visibility = ['PUB', 'PRO']
    if instance.visibility in match_visibility:
        follower_profile = get_follower_profile(instance.user.username)
        mail_list = [profile.email for profile in follower_profile]
        func_with_param = partial(worker, instance.user.username)
        # Use multiprocess for send mail to users
        with Pool(processes=4) as pool:
            pool.map(func=func_with_param, iterable=mail_list)



