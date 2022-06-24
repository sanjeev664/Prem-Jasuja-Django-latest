from .models import Notification

def post_like_notify(sender, user, post, *args, **kwargs):
	notify = Notification(sender=sender, user=user, post=post,notification_type=1)
	notify.save()

def comment_like_notify(sender, user, comment, *args, **kwargs):
	text_preview=comment.comment
	notify = Notification(sender=sender, user=user,post=comment.post,text_preview=text_preview, notification_type=4)
	notify.save()


