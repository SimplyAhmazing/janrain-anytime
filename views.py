# Create your views here.
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.utils import simplejson as json
from django.http import HttpResponse
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from hashlib import sha1
from base64 import b64encode
from dateutil.parser import parse


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from .models import user_get_or_create

#janrain auth
from libs.utils.janrain import Janrain

#import pdb

@csrf_exempt
def jlogin(request, print_form = False):
	if request.method == 'POST':
		token = request.POST.get('token')
		form = request.POST

		if print_form: print form

		#modify this code before you implement it...
		if token:
			j = Janrain()
			incoming_profile = j.get_simple_info_from_token(token)
			djuser = user_get_or_create(incoming_profile)

			#hashed_user = b64encode(sha1(incoming_profile['identifier']).digest())
			user = auth.authenticate(username = djuser[0].username, password = "bismillah")
			#fn = user.first_name

			if not request.user.is_authenticated():
				auth.login(request, user)

			#return HttpResponse("we got the token from %s" % incoming_profile.get('first_name') )

			return HttpResponse("done")
		else:
			if request.user.is_authenticated():
				#return HttpResponse("aren't you glad you were already logged in!"

				return HttpResponse("done")
			else:
				return HttpResponse("are you sure you're logged in? bkz you're request obj isn't cooperating..")

def janrain_login(fn):
	pass

def is_logged_in(request):
	return HttpResponse(json.dumps({"login_status": request.user.is_authenticated()}), content_type="application/json")

@csrf_exempt
def login(request):
    if request.method == 'POST':
		token = request.POST.get('token')

		#modify this code before you implement it...
		if token:
			j = Janrain()
			incoming_profile = j.get_simple_info_from_token(token)
			djuser = user_get_or_create(incoming_profile)

			#hashed_user = b64encode(sha1(incoming_profile['identifier']).digest())
			user = auth.authenticate(username = djuser[0].username, password = "bismillah")
			#fn = user.first_name

			if not request.user.is_authenticated():
				auth.login(request, user)

			return HttpResponse("we got the token from %s" % incoming_profile.get('first_name') ) #render(request, "eventform2.html")
			

		else:
			if request.user.is_authenticated():
				return HttpResponse("aren't you glad you were already logged in!")
				
			else:
				return HttpResponse("are you sure you're logged in? bkz you're request obj isn't cooperating..")
		
		#return HttpResponse("we didn't get the token :(")

@csrf_exempt	
def testcookie(request):
	if request.method == "POST":
		request.session.set_test_cookie()
		response = HttpResponse("posted cookies")
		#response['Access-Control-Allow-Origin'] = '*'
		#response['Access-Control-Allow-Headers'] = 'Set-Cookie'
		return response         

	else:
		request.session.set_test_cookie()
		response = HttpResponse("getted cookies")
		#response['Access-Control-Allow-Origin'] = '*'
		#response['Access-Control-Allow-Headers'] = 'Set-Cookie'
	return response