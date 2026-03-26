import uuid
from django.utils.translation import gettext_lazy as _
from os import path
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager,Group,Permission,AbstractUser
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models.manager import EmptyManager
from core.models import UserType,Gender,Title,MaritalStatus,SystemStatus
from mptt.models import TreeForeignKey
from django.core.validators import FileExtensionValidator
import base64
from utils.Upload import Upload
from django.contrib.auth.signals import user_logged_in


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = 'get_%s_permissions' % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    created_by = models.ForeignKey('self', null=True, blank=True, verbose_name="Created By",  on_delete=models.CASCADE,related_name="c_%(app_label)s_%(class)s_related",related_query_name="c_%(app_label)s_%(class)ss")
    updated_by = models.ForeignKey('self', null=True, blank=True, verbose_name="Updated By", on_delete=models.CASCADE,related_name="u_%(app_label)s_%(class)s_related",related_query_name="u_%(app_label)s_%(class)ss")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    serial_number = models.CharField(max_length=100,null=True,blank=True,editable=False,unique=True)
    whitelist_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Whitelist IP Address")
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children',on_delete=EmptyManager)
    avatar = models.FileField(max_length=250,verbose_name="Picture",null=True, blank=True, upload_to=Upload,validators=[FileExtensionValidator(['png','jpeg','jpg'])])

    gender = TreeForeignKey(Gender, null=True, blank=True, verbose_name="Gender",  on_delete=models.CASCADE,related_name="gender_%(app_label)s_%(class)s_related",related_query_name="gender_%(app_label)s_%(class)ss")
    title = TreeForeignKey(Title, null=True, blank=True, verbose_name="Prefix Title",  on_delete=models.CASCADE,related_name="title_%(app_label)s_%(class)s_related",related_query_name="title_%(app_label)s_%(class)ss")
    first_name = models.CharField(max_length=150,null=False, blank=False, verbose_name="First Name")
    middle_name = models.CharField(max_length=150,null=True, blank=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=150,null=False, blank=False, verbose_name="Last Name")
    type = TreeForeignKey(UserType, null=True, blank=False,  verbose_name="User Type", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    last_login = models.DateTimeField(null=True,blank=True)
    last_activity = models.DateTimeField(null=True,blank=True,editable=False)
    last_logout = models.DateTimeField(null=True,blank=True)

    phone = models.CharField(max_length=20,null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100,null=False, blank=False, verbose_name="Email",unique=True)
    join_date = models.DateField(null=True, blank=True, verbose_name="Date of Joining")
    marital_status = models.ForeignKey(MaritalStatus, null=True, blank=True, verbose_name="Marital Status", on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")
    password_change_date = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    device_token = models.CharField(max_length=250, unique=False, null=True, blank=True)
    device_uuid = models.CharField(max_length=250, unique=False, null=True, blank=True)

    phone_code = models.CharField(max_length=100, unique=False, null=True, blank=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_mobile_user = models.BooleanField(
        _('Dash Mob status'),
        default=False,
        help_text=_('Designates whether the user can log into mobile app.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


    status = TreeForeignKey(SystemStatus, null=True, blank=True, verbose_name="Status", on_delete=models.CASCADE,related_name="status_%(app_label)s_%(class)s_related",related_query_name="%(app_label)s_%(class)ss")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.email
    
   
    def getFullName(self):
        if len(str(self.middle_name)) < 1:
            #return str(self.title.name) + " " +str(self.first_name) + " " +str(self.middle_name) + "  " + str(self.last_name)
            return str(self.first_name) + " " +str(self.middle_name) + "  " + str(self.last_name)
        else:
            #return str(self.title.name) + " " +str(self.first_name) + " " + str(self.last_name)
            return str(self.first_name) + " " + str(self.last_name)

    full_name = property(getFullName)

    def get_avatar_bytes(self):
        if self.avatar is not None and self.avatar  and path.exists(str(self.avatar.path)):
            base64_encode = base64.b64encode(self.avatar.read())
            return base64_encode

        else:
            return None

    user_avatar_raw = property(get_avatar_bytes)
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    def save(self, *args, **kwargs):
        #if self.username is None:
        self.username = self.email
        if self.serial_number is None or len(self.serial_number) < 1:
            from core.utils.SerialNumber import getSerialNumber
            self.serial_number = getSerialNumber()
        super(User, self).save(*args, **kwargs)


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    #class Meta:


class AnonymousUser:
    id = None
    pk = None
    username = ''
    is_staff = False
    is_active = False
    is_superuser = False
    _groups = EmptyManager(Group)
    _user_permissions = EmptyManager(Permission)

    def __str__(self):
        return 'AnonymousUser'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def __int__(self):
        raise TypeError('Cannot cast AnonymousUser to int. Are you trying to use it in place of User?')

    def save(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, module):
        return _user_has_module_perms(self, module)

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False

    def get_username(self):
        return self.username
    def __unicode__(self):
        return str(self.full_name)


