from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'))
    nick = models.CharField(_('nick name'), max_length=50, unique=False, help_text="It will be used for games. You can change it later.")
    email = models.EmailField(_('email address'), max_length=254, unique=True, help_text="Required to account verification.")
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    updatedat = models.DateTimeField(verbose_name='updated at',  default=timezone.now)

    def __str__(self):
        return self.username
