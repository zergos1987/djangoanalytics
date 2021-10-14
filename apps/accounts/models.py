from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.timezone import now
from user_agents import parse

now = timezone.now()



# Create your models here.
class app(models.Model):
    test_field = models.CharField(max_length=150)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'accounts'

    def __str__(self):
        return self.test_field


# RelatedObjectDoesNotExist at /adminlogin/
# User has no user_extra_details.
# $ python manage.py shell
# > from django.contrib.auth.models import User
# > from apps.accounts.models import user_extra_details
# > users = User.objects.filter(user_extra_details=None)
# > for user in users:
# >     user_extra_details.objects.create(user=user)

class user_extra_details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_extra_details")
    full_name = models.CharField(max_length=300, blank=True, null=True)
    department = models.CharField(max_length=800, blank=True, null=True)
    center = models.CharField(max_length=800, blank=True, null=True)
    position = models.CharField(max_length=800, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    email_signup_confirmed = models.BooleanField(default=False)
    ldap_is_active = models.BooleanField(default=False)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'accounts'

    __init_full_name = None
    __init_department = None
    __init_center = None
    __init_position = None

    def __init__(self, *args, **kwargs):
        super(user_extra_details, self).__init__(*args, **kwargs)
        self.__init_full_name = self.full_name
        self.__init_department = self.department
        self.__init_center = self.center
        self.__init_position = self.position

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.full_name != self.__init_full_name or \
            self.department != self.__init_department or \
            self.center != self.__init_center or \
            self.position != self.__init_position:
            pass

        super(user_extra_details, self).save(force_insert, force_update, *args, **kwargs)
        self.__init_full_name = self.full_name
        self.__init_department = self.department
        self.__init_center = self.center
        self.__init_position = self.position


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if user_extra_details.objects.filter(user=instance).count() == 0:
        instance.is_active = False
        user_extra_details.objects.get_or_create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.user_extra_details.save()
#     print(instance.user_extra_details.full_name)




class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    dt = models.DateTimeField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True)
    request_method = models.CharField(max_length=30, null=True)
    username = models.CharField(max_length=256, null=True)
    device = models.CharField(max_length=100, null=True)
    browser_family = models.CharField(max_length=100, null=True)
    browser_version = models.CharField(max_length=100, null=True)
    os_family = models.CharField(max_length=100, null=True)
    os_version = models.CharField(max_length=100, null=True)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'accounts'

    def __unicode__(self):
        return '{0} - {1} - {2} - {3} - {4} - {5} - {6} - {7} - {8} - {9}'.format(
        	self.dt, 
        	self.action, 
        	self.request_method, 
        	self.username, 
        	self.ip,
        	self.device,
        	self.browser_family,
        	self.browser_version,
        	self.os_family,
        	self.os_version)

    def __str__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(
        	self.dt, 
        	self.action, 
        	self.request_method, 
        	self.username, 
        	self.ip)



class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    remove_session = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'accounts'

    def __str__(self):
        return '{0} - {1} - {2} - {3}'.format(
            self.user, 
            self.session, 
            self.remove_session,
            self.created_at)


#Remove user sessin from admin page - UserSessions
@receiver(post_save, sender=UserSession)
def my_handler(sender, instance, **kwargs):
    UserSessionExists = UserSession.objects.filter(session=instance.session)
    if UserSessionExists[0].remove_session == True:
        uid = instance.session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        Session.objects.filter(usersession__user=user).delete()


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    device = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(device)

    AuditEntry.objects.create(
    	action='user_logged_in', 
    	dt=now, ip=ip, 
    	request_method=request.method, 
    	username=user.username,
    	device=user_agent.device.family,
    	browser_family=user_agent.browser.family,
    	browser_version=user_agent.browser.version_string,
    	os_family=user_agent.os.family,
    	os_version=user_agent.os.version_string)

    # Prevent multi-loggin for users same use
    # remove other sessions
    #Session.objects.filter(usersession__user=user).delete()

    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        #userID=user.id,
        user=user,
        session=Session.objects.get(pk=request.session.session_key)
    )


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    device = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(device)

    if user:
        AuditEntry.objects.create(
        	action='user_logged_out', 
        	dt=now,
        	request_method=request.method,  
        	ip=ip, 
        	username=user.username,
        	device=user_agent.device.family,
        	browser_family=user_agent.browser.family,
        	browser_version=user_agent.browser.version_string,
        	os_family=user_agent.os.family,
        	os_version=user_agent.os.version_string)

    Session.objects.filter(usersession__user=user).delete()
        


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(
    	action='user_login_failed', 
    	username=credentials.get('username', None))
