from accounts.models import *
from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from .request_utils import get_current_request
from django.db.models.signals import post_save


slug=SlugField()  #models.SlugField()


class UserPosts(Model):
    user = ForeignKey(User, related_name='user_posts', on_delete=CASCADE, null=True, blank=True)
    title = CharField(blank=True, null=True, max_length=256)
    seo_title = CharField(blank=True, null=True, max_length=256)
    seo_url = CharField(blank=True, null=True, max_length=256)
    post_type = CharField(blank=True, null=True, max_length=256, default='public')
    post_description = RichTextField(blank=True, null=True)
    meta_description = CharField(blank=True, null=True, max_length=1000)
    location = CharField(blank=True, null=True, max_length=256)
    latitude = DecimalField(max_digits=9, decimal_places=6, max_length=16, null=True, blank=True)
    longitude = DecimalField(max_digits=9, decimal_places=6, max_length=16, null=True, blank=True)
    datetime = DateTimeField(auto_now_add=True)
    views = ManyToManyField(User, related_name='views', blank=True)
    slug  = CharField(blank=True, null=True, max_length=256)
    day = IntegerField(blank=True, null=True, default=0)
    likes = ManyToManyField(User, related_name='likes', blank=True)
    isDeleted = BooleanField(default=False)

    class Meta:
        db_table = "user_posts"
        verbose_name_plural = 'User Posts'

    def __str__(self):
        return "{}".format(self.title)

    def save(self,*args,**kwargs):
        if self.seo_url:
            self.slug=self.seo_url
        else:
            slug_string = f'{self.title}'
            self.slug=slugify(slug_string)
        super(UserPosts,self).save(*args,**kwargs)


class PostComments(Model):
    comment = TextField()
    created = DateTimeField(auto_now_add=True)
    author = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(UserPosts, on_delete=CASCADE,  related_name='posts_comment',)
    likes = ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = ForeignKey('self', on_delete=CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        request = get_current_request() # request coming by middleware.
        return PostComments.objects.filter(parent=self).order_by('-created').all().annotate(is_liked=Exists(PostComments.objects.filter(
            likes__id=request.user.id, id=OuterRef('pk'))))

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


    class Meta:
        verbose_name_plural = 'Post Comments'

    def __str__(self):
        return self.comment

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.comment
        sender = comment.author
        if post.user != sender:
            notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
            notify.save()
        pass

post_save.connect(PostComments.user_comment_post, sender=PostComments)


class PostSave(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='user_post_save')
    post = ForeignKey(UserPosts, on_delete=CASCADE, related_name='post_save')
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title


class Follow(Model):
    user_from = ForeignKey(User, related_name='rel_from_set', on_delete=CASCADE, null=True, blank=True)
    user_to = ForeignKey(User, related_name='rel_to_set', on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        text_preview = "started following you"
        sender = follow.user_from
        following = follow.user_to
        notify = Notification(sender=sender, user=following,text_preview=text_preview, notification_type=3)
        notify.save()

post_save.connect(Follow.user_follow, sender=Follow)

# Add following field to User dynamically
User.add_to_class('following',
                  ManyToManyField('self',
                                  through=Follow,
                                  related_name='followers',
                                  symmetrical=False))


class Notification(Model):
    NOTIFICATION_TYPES = ((1,'Like'),(2,'Comment'), (3,'Follow'), (4,'Comment Like'))

    post = ForeignKey(UserPosts, on_delete=CASCADE, related_name="noti_post", blank=True, null=True)
    sender = ForeignKey(User, on_delete=CASCADE, related_name="noti_from_user")
    user = ForeignKey(User, on_delete=CASCADE, related_name="noti_to_user")
    notification_type = IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = CharField(max_length=90, blank=True)
    date = DateTimeField(auto_now_add=True)
    is_seen = BooleanField(default=False)


    class Meta:
        db_table = "notification"

    def __str__(self):
        return "{}".format(self.user.username)
