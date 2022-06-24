from django.views.generic import TemplateView
from django.shortcuts import render ,redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from geopy.geocoders import Nominatim
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth import login, authenticate, get_user_model, logout as django_logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.core import paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import Http404  
from .models import *
from .forms import *
from django.db.models import CharField, Value, Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.text import slugify
from .notifications import *

User = get_user_model()

NEWS_COUNT_PER_PAGE = 9

  
def error_404_view(request, exception):
    
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


def error_500_view(request, *args, **argv):
    
    # we add the path to the the 500.html file
    # here. The name of our HTML file is 500.html
    return render(request, '500.html')


class Index(LoginRequiredMixin,TemplateView):
	index_page = 'index.html'
	login_url = 'accounts:login'
	def get(self, request, *args, **kwargs):
		page = int(request.GET.get('page', 1))
		search_option = request.GET.get('search_option', None)
		if search_option:
			posts = UserPosts.objects.filter(title__icontains=search_option,post_type='public').order_by('datetime').annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk')))).annotate(is_follow=Exists(Follow.objects.filter(user_from=request.user,user_to = OuterRef('user__pk'))))
		else:
			following_user_ids = Follow.objects.filter(user_from = request.user).values_list('user_to__id', flat=True)
			posts = UserPosts.objects.filter(Q(user_id__in=following_user_ids) | Q(user = request.user),post_type='public').order_by('-datetime').annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk')))).annotate(is_follow=Exists(Follow.objects.filter(user_from=request.user,user_to = OuterRef('user__pk'))))
		
		p = paginator.Paginator(posts, NEWS_COUNT_PER_PAGE)
		try:
			post_page = p.page(page)
		except paginator.EmptyPage:
			post_page = paginator.Page([], page, p)

		if not request.is_ajax():
			context = {
			    'posts': post_page,
			}
			return render(request,self.index_page,context)
		else:
			content = ''
			for post in post_page:
				content += render_to_string('posts-item.html',{'post': post},request=request)
			return JsonResponse({
				"content": content,
				"end_pagination": True if page >= p.num_pages else False,
			})


class Notifications(LoginRequiredMixin,TemplateView):
	template_name = 'notifications.html'
	login_url = 'accounts:login'

	def get(self, request, *args, **kwargs):
		page = request.GET.get('page', 1)

		notifications = Notification.objects.filter(user=request.user)
		if page == 1:
			for notification in notifications.filter(is_seen=False):
				notification.is_seen = True
				notification.save()

		paginator = Paginator(notifications, 5)
		try:
			notifications = paginator.page(page)
		except PageNotAnInteger:
			notifications = paginator.page(1)
		except EmptyPage:
			notifications = paginator.page(paginator.num_pages)

		context = {
			'notifications': notifications,
		}
		return render(request, self.template_name, context)

class EditProfile(LoginRequiredMixin,TemplateView):
	template_name = 'edit.html'
	login_url = 'accounts:login'

	def get_context_data(self):
		context = super(EditProfile, self).get_context_data()
		request = self.request
		context['user'] = request.user
		return context

	def post(self, request, *args, **kwargs):
		super(EditProfile, self).get(request, *args, **kwargs)
		response = {}
		user = request.user
		fname   = request.POST.get('fname')
		email   = request.POST.get('email').strip().replace(" ","")
		username   = request.POST.get('username').strip().replace(" ","")
		bio        = request.POST.get('bio')
		website    = request.POST.get('website')
		gender     = request.POST.get('gender')
		phone      = request.POST.get('phone')
		image      = request.FILES.get('image')
		try:
			user = User.objects.get(email=user.email)
			if user.username is not username:
				user.username = username
			if user.email is not email:
				user.email = email
			if image:
				user.image = image
			user.website = website
			user.gender = gender
			user.bio = bio
			user.phone = phone
			user.fullname = fname
			user.save()
			response['error'] = False
			response['message'] = 'Successfully updated.'
			response['image'] = user.image.url
		except Exception as e:
			response['error'] = True
			if 'UNIQUE constraint' in str(e.args):
				if 'accounts_user.email' in str(e.args):
					response['message'] = 'Given email is already exists.'
				elif 'accounts_user.username' in str(e.args):
					response['message'] = 'Given username is already exists.'
			else:
				response['message'] = str(e)	
		return JsonResponse(response)


class EditWritePost(LoginRequiredMixin,TemplateView):
	template_name = 'edit-write-post.html'
	login_url = 'accounts:login'

	def get_context_data(self,  *args, **kwargs):
		pk=self.kwargs["pk"]
		context = super(EditWritePost, self).get_context_data()
		try:
			post=UserPosts.objects.get(id=pk)
		except:
			raise Http404
		context['post'] = post
		return context

	def post(self, request, *args, **kwargs):
		super(EditWritePost, self).get(request, *args, **kwargs)
		pk=self.kwargs["pk"]
		response = {}
		post=UserPosts.objects.get(id=pk)
		title = request.POST.get('title')
		seo_url = request.POST.get('seo_url')
		if seo_url:
			slug=seo_url
		else:
			slug_string = f'{self.title}'
			slug=slugify(slug_string)
		try:
			post.title = request.POST.get('title')
			post.post_type = request.POST.get('post_type')
			post.post_description = request.POST.get('post_description')
			post.meta_description = request.POST.get('meta_description')
			post.seo_title = request.POST.get('seo_title')
			post.seo_url = request.POST.get('seo_url')
			post.slug = slug
			post.save()
			response['status'] = 200
			response['message'] = 'Successfully updated.'
			response['success_url']='/',
		except Exception as e:
			response['status'] = 400
			response['message'] = "Someting Went Wrong"	
		return JsonResponse(response)

class GetSavedPostdView(LoginRequiredMixin,TemplateView):
	render_page = 'saved-posts.html'
	login_url = 'accounts:login'

	def get(self, request, *args, **kwargs):
		pk=self.kwargs["pk"]
		page = int(request.GET.get('page', 1))
		try:
			user=User.objects.get(id=pk)
		except:
			raise Http404
		user_post_save_ids = PostSave.objects.filter(user=user).values_list('post__id',flat=True)
		saved_post = UserPosts.objects.filter(id__in=user_post_save_ids).annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk'))))
		p = paginator.Paginator(saved_post, NEWS_COUNT_PER_PAGE)
		try:
			posts = p.page(page)
		except paginator.EmptyPage:
			posts = paginator.Page([], page, p)
		if not request.is_ajax():
			context = {
			 	'posts':posts,
			}
			return render(request, self.render_page, context)
		else:
			content = ''
			for post in posts:
				content += render_to_string('profile-posts-item.html',{'post': post},request=request)
			return JsonResponse({
			    "content": content,
			    "end_pagination": True if page >= p.num_pages else False,
			})
		

class Profile(LoginRequiredMixin,TemplateView):
	profile_page = 'profile.html'
	login_url = 'accounts:login'

	def post_paginator(self,posts, page):
		p = paginator.Paginator(posts, NEWS_COUNT_PER_PAGE)
		try:
			posts = p.page(page)
		except paginator.EmptyPage:
			posts = paginator.Page([], page, p)
		return posts

	def get(self, request, *args, **kwargs):
		pk=self.kwargs["pk"]
		page = int(request.GET.get('page', 1))
		location=request.GET.get('location', None)
		datetime=request.GET.get('datetime', None)
		post_type=request.GET.get('post_type', None)

		try:
			user=User.objects.get(id=pk)
		except:
			raise Http404

		posts = UserPosts.objects.filter(user=user).order_by('datetime')

		if location:
			posts = posts.filter(location__icontains=location)
		if datetime:
			posts = posts.filter(datetime__date=datetime)

		posts = posts.annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk'))))

		user_post_save_ids = PostSave.objects.filter(user=user).values_list('post__id',flat=True)
		saved_post = UserPosts.objects.filter(id__in=user_post_save_ids).annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk'))))

		if Follow.objects.filter(user_from=request.user,user_to = user).exists():
			is_follow = True
		else:
			is_follow = False
		followers = Follow.objects.filter(user_to = user).count()
		following = Follow.objects.filter(user_from = user).count()
		
		context = {
		 	'user':user,
		 	'followers':followers,
		 	'following':following,
		 	'is_follow':is_follow,
		 	'days':UserPosts.objects.filter(user=pk).count(),
		 	'public_posts':self.post_paginator(posts.filter(post_type='public'),page),
		 	'private_posts':self.post_paginator(posts.filter(post_type='private'),page),
		 	'draft_posts':self.post_paginator(posts.filter(post_type='draft'),page),
		 	'saved_posts':self.post_paginator(saved_post,page),
		}
		return render(request, self.profile_page, context)


class ProfilePostItems(LoginRequiredMixin,TemplateView):

	def get(self, request, *args, **kwargs):
		page = int(request.GET.get('page', 1))
		location=request.GET.get('location', None)
		datetime=request.GET.get('datetime', None)
		post_type=request.GET.get('post_type', None)
		user_id=request.GET.get('user_id', None)
		
		if post_type and  post_type!="saved":
			posts = UserPosts.objects.filter(user=user_id).order_by('datetime')
			posts = posts.filter(post_type=post_type)
		else:
			user_post_save_ids = PostSave.objects.filter(user=user_id).values_list('post__id',flat=True)
			posts = UserPosts.objects.filter(id__in=user_post_save_ids)

		if location:
			posts = posts.filter(location__icontains=location)
		if datetime:
			posts = posts.filter(datetime__date=datetime)

		posts = posts.annotate(is_liked=Exists(UserPosts.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk')))).annotate(is_saved=Exists(PostSave.objects.filter(
            user=self.request.user, post__id=OuterRef('pk'))))
            
		p = paginator.Paginator(posts, NEWS_COUNT_PER_PAGE)
		try:
			posts = p.page(page)
		except paginator.EmptyPage:
			posts = paginator.Page([], page, p)

		content = ''
		for post in posts:
			content += render_to_string('profile-posts-item.html',{'post': post},request=request)
		return JsonResponse({
		    "content": content,
		    "end_pagination": True if page >= p.num_pages else False,
		})


def follow(request,user_to):

   '''
	Method that enables a user to follow another user.
	'''
	
   user=User.objects.get(id=user_to)

   is_follow=False
   if Follow.objects.filter(user_from=request.user,user_to = user).exists():
       Follow.objects.filter(user_from=request.user,user_to = user).delete()
       is_follow=False
   else:
       Follow(user_from=request.user,user_to = user).save()
       is_follow=True

   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WritePost(LoginRequiredMixin,TemplateView):
	template_name = 'write-post-page.html'
	login_url = 'accounts:login'

	def get_context_data(self):
		context = super(WritePost, self).get_context_data()
		request = self.request
		now = datetime.now()
		dt_string = now.strftime("%B %d, %Y %H:%M:%S")
		context['user'] = request.user
		context['form'] = PostCreateForm
		context['datetime'] = dt_string
		return context


	def post(self, request, *args, **kwargs):
		super(WritePost, self).get(request, *args, **kwargs)
		try:
			geolocator = Nominatim(user_agent="geoapiExercises")
			geo_response = geolocator.reverse(request.POST.get('latitude')+","+request.POST.get('longitude'))
			address = geo_response.raw['address']
			location = address['city']+' '+address['country']
		except:
			location = ''
		last_user_post = UserPosts.objects.filter(user=request.user).last()
		if last_user_post:
			day = last_user_post.day+1
		else:
			day = 1
		UserPosts.objects.create(
			user             = request.user,
			title            = request.POST.get('title'),
			post_description = request.POST.get('post_description'),
			seo_title        = request.POST.get('seo_title'),
			seo_url          = request.POST.get('seo_url'),
			meta_description = request.POST.get('meta_description'),
			post_type        = request.POST.get('post_type'),
			# latitude         = request.POST.get('latitude'),
			# longitude        = request.POST.get('longitude'),
			location         = location,
			day              = day
			)
		if not request.is_ajax():
			return redirect('/')
		else:
			return JsonResponse({
			    "status": 200,
			    "message": "Post Created Successfully",
			    "success_url": "/",
			})
		
		
class GetPost(LoginRequiredMixin,TemplateView):
	template_name = 'post.html'
	login_url = 'accounts:login'

	def get(self, request, *args, **kwargs):
		post_id=self.kwargs["id"]
		slug = self.kwargs["slug"]
		try:
			post = UserPosts.objects.get(id=post_id,slug=slug)
		except:
			raise Http404
		if not post.post_type=="draft":
			if not  post.views.filter(id = request.user.id).exists():
				post.views.add(request.user)
		post.save()
		if Follow.objects.filter(user_from=request.user,user_to = post.user).exists():
			is_follow = True
		else:
			is_follow = False

		is_liked = post.likes.filter(id=self.request.user.id).exists()

		comments = PostComments.objects.filter(post=post).order_by('-created').annotate(is_liked=Exists(PostComments.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk'))))

		context={'post':post,'is_follow':is_follow,'comments':comments,'is_liked':is_liked}
		return render(request, self.template_name,context)



class ProfileSearch(TemplateView):
	index_page = 'profile-search.html'

	def get(self, request, *args, **kwargs):
		page = int(request.GET.get('page', 1))
		search_title = request.GET.get('search_title', None)
		search_option = request.GET.get('search_option', 'user')
		if search_option == "user":
			if search_title:
				users = User.objects.filter(Q(username__icontains=search_title)|Q(fullname__icontains=search_title)).annotate(is_follow=Exists(Follow.objects.filter(
            	user_from=self.request.user, user_to=OuterRef('pk'))))
			else:
				users = User.objects.filter(Q(username__icontains=search_title)|Q(fullname__icontains=search_title)).annotate(is_follow=Exists(Follow.objects.filter(
            	user_from=self.request.user, user_to=OuterRef('id')))).order_by('-created')[:20]
		else:
			url = '/?search_option='+search_title
			return redirect(url)
		return render(request, self.index_page, {'users':users})

def postDeleteView(request,post_id):
	try:
		post = UserPosts.objects.get(pk=post_id)
		post.delete()
	except:
		raise Http404
	return HttpResponseRedirect('/')

class LikePostView(TemplateView):
	""" 
		This class belongs to the like a post functionality.
	"""
	def post(self ,request, post_id):
		try:
			post = UserPosts.objects.get(pk = post_id)

			if post.likes.filter(id = request.user.id).exists():
				post.likes.remove(request.user)
			else:
				post.likes.add(request.user)
				if request.user != post.user:
					post_like_notify(request.user, post.user, post)

			return JsonResponse({
					    "status": 200,
					    "message": "Post Liked Successfully"
					})
		except Exception as e:
			return JsonResponse({
				    "status": 404,
				    "message": "Post Not Found"
				})


class SavePostView(TemplateView):
	""" 
		This class belongs to the save a post functionality.
	"""
	def post(self ,request, post_id):
		try:
			post = UserPosts.objects.get(pk = post_id)
			post_save = PostSave.objects.filter(user=request.user,post=post)

			if post_save.exists():
				post_save.delete()
			else:
				PostSave.objects.create(user=request.user,post=post)

			return JsonResponse({
					    "status": 200,
					    "message": "Post Saved Successfully"
					})
		except:
			return JsonResponse({
				    "status": 404,
				    "message": "Post Not Found"
				})


class PostCommentsDetailView(LoginRequiredMixin, View):
	
    def get(self, request, post_pk, *args, **kwargs):
        post = UserPosts.objects.get(pk=post_pk)
        
        comments = PostComments.objects.filter(post=post).order_by('-created').annotate(is_liked=Exists(PostComments.objects.filter(
            likes__id=self.request.user.id, id=OuterRef('pk'))))
        
        page = request.GET.get('page', 1)
        paginator = Paginator(comments, 10)
        
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context = {
            'post': post,
            'comments': comments,
        }
        return render(request, 'post-comments.html', context)

    def post(self, request, post_pk, *args, **kwargs):
        post = UserPosts.objects.get(pk=post_pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = UserPosts.objects.get(pk=post_pk)
        parent_comment = PostComments.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def commentDeleteView(request,pk):
	try:
		comment = PostComments.objects.get(pk=pk)
		comment.delete()
	except:
		raise Http404
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LikePostCommentView(TemplateView):
	""" 
		This class belongs to the like a comment functionality.
	"""
	def post(self ,request, comment_id):
		try:
			comment = PostComments.objects.get(pk = comment_id)

			if comment.likes.filter(id = request.user.id).exists():
				comment.likes.remove(request.user)
			else:
				comment.likes.add(request.user)
				if request.user != comment.post.user:
					comment_like_notify(request.user, comment.post.user, comment)

			return JsonResponse({
					    "status": 200,
					    "message": "Comment Liked Successfully"
					})
		except:
			return JsonResponse({
				    "status": 404,
				    "message": "Comment Not Found"
				})

