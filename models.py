from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (ModificationDateTimeField,
                                         CreationDateTimeField, AutoSlugField)


import logging
logger = logging.getLogger(__name__)

from hashlib import sha1
from base64 import b64encode

class TimeStampedModel(models.Model):
    """ TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))
    	

    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True

class JanrainUser(TimeStampedModel):
    user       = models.ForeignKey(User, related_name='janrain_user')
    username   = models.CharField(max_length=512, blank=False)
    provider   = models.CharField(max_length=64, blank=False)
    identifier = models.URLField(max_length=512, blank=False)
    avatar     = models.URLField(max_length=512, blank=True)
    url        = models.URLField(max_length=512, blank=True)

    class Meta:
        ordering = ["user", "provider"]

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name



def user_get_or_create(profile = None):
	"""
	input: {janrain profile}
	output: (DJANGO USER OBJ, JANRAIN USER OBJ)
	takes a profile dict obj and creates a new janrain user 
	object & django user object if they do not exist. Else it will 
	create a new janrain user and django user object and return a 
	tuple with (DJANGO USER OBJ, JANRAIN USER OBJ)."""

	#verify profile is not None and is indeed a dictionary object
	if profile is None:
		raise Exception('Janrain profile dictionary is empty')

	if type(profile) is not dict:
		raise Exception('Required input must be a dictionary type NOT ' + str(type(profile)))

	#create user hash from the identifier
	hashed_user = b64encode(sha1(profile['identifier']).digest())

	#create user in django user table if they do not exist
	try:
		django_user = User.objects.get(username = hashed_user)
		django_user.set_password("bismillah")
	except ObjectDoesNotExist:
		logger.debug("user already exists..")
		django_user = User.objects.create_user(username = hashed_user)
		django_user.email = profile['email']
		django_user.set_password("bismillah")
		django_user.first_name = profile.get('first_name') #not neccessary to set
		django_user.last_name = profile.get('last_name') #not neccessary to set
		django_user.is_active = True
		django_user.is_staff = False
		django_user.is_superuser = False
		django_user.save()


	#create or get user from janrain table...  
	new_janrain_user = JanrainUser.objects.get_or_create(
		user = django_user,
		username = profile.get('username'),
		identifier = profile.get('identifier'),
		provider = profile.get('provider'),
		)

	return (django_user, new_janrain_user[0])