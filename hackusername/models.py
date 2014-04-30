# coding=utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _ #para internacionalizacion (varios idiomas)
from django.db import IntegrityError #Usado en la deteccion de errores al guardar modelos
from django.contrib.auth.models import check_password

from registration.models import Event



class MyFacebookBackend(object):
    """
    Autenticacion para facebook
    """

    def authenticate(self, email=None, facebook_id=None):
        try:
            user = MyUser.objects.get(email=email, facebook_id=facebook_id)
        except MyUser.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None


class MyLinkedinBackend(object):
    """
    Autenticacion para facebook
    """

    def authenticate(self, email=None, linkedin_id=None):
        try:
            user = MyUser.objects.get(email=email, linkedin_id=linkedin_id)
        except MyUser.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'cn_my_user'

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={'unique': _(u'This email is already registered.')}
    )
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    commercial_name = models.CharField(max_length=150, null=True, blank=True)
    business_name = models.CharField(max_length=150, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    web = models.URLField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    facebook_id = models.CharField(max_length=20, null=True, blank=True)
    linkedin_id = models.CharField(max_length=20, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email

    """def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True"""

    """
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True"""

    """@property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin"""


class Role(models.Model):

    class Meta:
        db_table = 'cn_role'

    cod = models.CharField(max_length=3)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description


class RoleUser(models.Model):

    class Meta:
        db_table = 'cn_role_user'

    user = models.ForeignKey(MyUser,null=False)
    role = models.ForeignKey(Role,null=False)
    event = models.ForeignKey(Event,null=False)

    def save(self, *args, **kwargs):
        """Guarda el RolUsuario asegurandose de que sea unico por evento"""
        if RoleUser.objects.filter(user=self.user,event=self.event).count()>0:
            raise IntegrityError(_(u'A user can only have one role for one event.'))

        super(RoleUser, self).save(*args, **kwargs)


class Permission(models.Model):

    class Meta:
        db_table = 'cn_permission'

    cod = models.CharField(max_length=3)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description


class RolePermission(models.Model):

    class Meta:
        db_table = 'cn_role_permission'

    permission = models.ForeignKey(Permission,null=False)
    role = models.ForeignKey(Role,null=False)

