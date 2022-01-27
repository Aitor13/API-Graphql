from socialnetwork.notifications import Email


def worker(user_who_posts, user_to_send):
    Email(user_who_posts, user_to_send).send()
