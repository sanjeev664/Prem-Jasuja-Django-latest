import re
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
import sys
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

def username_validation(username):
	#^(?![-._])(?!.*[_.-]{2})[\w.-]{4,12}(?<![-._])$
	if username.isdigit():
		message = "Your username cannot contain only numbers."
		valid = False
		return {'message':message,'valid':valid}
	if len(username) <= 3 or len(username) > 12:
		message = "Username length should be 4-12"
		valid = False
		return {'message':message,'valid':valid}
	if not re.match('^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{4,12}$', username):
		message = 'Usernames can only use letters, numbers and underscores or periods between letters'
		valid = False
		return {'message':message,'valid':valid}
	return {'valid':True}

account_sid = 'ACbc61f61f171919e15e98ab0e368f3967'
auth_token = '2a1457974cf0ab453693ca78fa08f8bf'
account_number = '+16104631587'

class CommonClass:

	@staticmethod
	def send_mail(subject_template_name,email_template_name,context,to_email,html_email_template_name=None,from_email=settings.EMAIL_HOST_USER):
		subject = loader.render_to_string(subject_template_name, context)
		subject = "".join(subject.splitlines())
		body = loader.render_to_string(email_template_name, context)
		email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
		if html_email_template_name is not None:
			html_email = loader.render_to_string(html_email_template_name, context)
			email_message.attach_alternative(html_email, "text/html")
		email_message.send()
  
	@staticmethod
	def key_utils(user,subject_template_name,email_template_name,current_site,domain_override=None,use_https=False,token_generator=default_token_generator,):
		current_site = current_site
		site_name = current_site.name
		domain = current_site.domain
		site_name = domain = domain_override
		user_email = user.email

		context = {
			"email": user.email,
			"domain": domain,
			"site_name": site_name,
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			"token": token_generator.make_token(user),
			"protocol": "https" if use_https else "http",
			"base_url":settings.BASE_URL
			}
		CommonClass.send_mail(
		        subject_template_name,
		        email_template_name,
		        context,
		        user_email,
		    )
  
	@staticmethod
	def send_message_to_phone(subject_template_name,email_template_name,context, user):
		""" for sending message to phone """
		
		subject = loader.render_to_string(subject_template_name, context)
		subject = "".join(subject.splitlines())
		body = loader.render_to_string(email_template_name, context)
		client = Client(account_sid, auth_token)
		msg = client.messages.create(subject,
			from_=account_number,
			body=body,
			to=user,
		)
		try:
			msg.sid
		except TwilioRestException as e:
			return False
		return True

	@staticmethod
	def key_utils_phone(user,subject_template_name,email_template_name,current_site,domain_override=None,use_https=False,token_generator=default_token_generator,):
		current_site = current_site
		site_name = current_site.name
		domain = current_site.domain
		site_name = domain = domain_override
		user_phone = user.phone

		context = {
			"phone": user.phone,
			"domain": domain,
			"site_name": site_name,
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			"token": token_generator.make_token(user),
			"protocol": "https" if use_https else "http",
			"base_url":settings.BASE_URL
			}
		CommonClass.send_mail(
		        subject_template_name,
		        email_template_name,
		        context,
		        user_phone,
		    )
