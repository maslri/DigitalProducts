from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail
import random

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(
                    username=username,
                    phone_number=phone_number,
                    is_staff=is_staff,
                    is_superuser=is_superuser,
                    date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)
    
    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)
    
    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number' : phone_number})

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(_('username'), max_lenght=32, unique=True,
                                help_text=_(
                                    'Required. 30 characters or fewer starting with a letter. Letters, digital'),
                                validators = [
                                        validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                                  _('Enter a valid username starting with a-z.'
                                                                     'this value my contain only letter numbeer'
                                                                     'and underscore characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique' : _("A user with that username already exists.")
                                }
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    phone_number = models.BigIntegerField(_('mobile number'), unique=True, null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        _('Enter a valid mobile number.'))
                                          ],
                                          error_messages={
                                              'unique' : _("A user with that mobile number already exists.")
                                          }
    )
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                       help_text=_('Designates whether this user should be treated as active.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
    
    def get_short_name(self):
        return self.first_name
    
    def email_user(self,subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    @property
    def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None
    
    def save(self, *arge, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*arge, **kwargs)

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'), max_lenght=150, blank=True)
    avatar = models.ImageField(_('avatar', blank=True))
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.NullBooleanField(_("gender"), help_text=_('female is False, male is True, null is unset'))
    province = models.ForeignKey(verbose_name=_('province'), to='Province', null=True, on_delete=models.SET_NULL)
    # email = models.EmailField(_('email address'), blank=True)
    # phone_number = models.BigIntegerField(_('mobile number'), null=True, blank=True, 
    #                                       validators=[
    #                                           validators.RegexValidator(r'^989[0-3,9]\d{8}$',
    #                                                                     _('Enter a valid mobile number.'))
    #                                       ],
    # )

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    @property
    def get_first_name(self):
        return self.user.first_name
    @property
    def get_last_name(self):
        return self.user.last_name
    @property
    def get_nickname(self):
        return self.nick_name if self.nick_name else self.user.username
    
class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPES = (
        (WEB, _('web')),
        (IOS, _('ios')),
        (ANDROID, _('android')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPES, default=1, verbose_name='device type')