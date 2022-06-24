from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import gettext_lazy as _

from django.conf import settings
# from djrichtextfield.models import RichTextField
import uuid

class User(AbstractUser):
    id                  = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username            = CharField(max_length=10,  unique=True)
    fullname            = CharField(blank=True, null=True, max_length=20)
    phone               = CharField(_('phone'), max_length=13, blank=True, null=True)
    gender              = CharField(default='', blank=True, max_length=20, null=True, verbose_name='gender')
    email               = EmailField(_('email address'), unique=True)
    dob                 = DateField(blank=True, null=True)
    image               = ImageField(upload_to="user_img", null=True, blank=True)
    address             = TextField(default='', blank=True, null=True)
    bio                 = TextField(default='', blank=True, null=True)
    website             = CharField(blank='', null=True, max_length=70)
    country             = CharField(blank=True, null=True, max_length=50)
    state               = CharField(blank=True, null=True, max_length=50)
    city                = CharField(blank=True, null=True, max_length=50)
    zipcode             = CharField(blank=True, null=True, max_length=20)
    jwt_secret          = UUIDField(default=uuid.uuid4, editable=False)
    isDeleted           = BooleanField(default=False)
    created             = DateTimeField(auto_now_add=True)
    updated             = DateTimeField(auto_now=True)

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['username', "phone"]

    def __str__(self):
        return "{}".format(self.email)

    @property
    def unseen_notifications(self):
        return self.noti_to_user.filter(is_seen=False).count()


class OTP(Model):
    user        = ForeignKey(User, related_name = 'user_otp',on_delete=CASCADE, null = True, blank =True)
    otp         = CharField(blank=True, null=True, max_length=256)
    ip          = CharField(blank=True, null=True, max_length=256)
    status      = CharField(blank=True, null=True, max_length=256)
    counter     = IntegerField(default=0, blank=False)
    isDeleted   = BooleanField(default=False)

    class Meta:
        db_table = "user_otp"
