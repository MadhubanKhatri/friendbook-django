from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import User, Post, Comment, Follower
from django.contrib import messages
from django.urls import reverse_lazy, reverse


# Create your views here.
def index(request):
	if 'user' in request.session:
		session_user_obj = User.objects.get(user_name=request.session['user'])
		check_follower = Follower.objects.get_or_create(user=session_user_obj)[0]
		check_follower.another_user.add(session_user_obj)
		following_users = Follower.objects.filter(another_user=session_user_obj)

		suggest_users = User.objects.all().exclude(user_name=request.session['user'])[:8]
		
		params = {'following_users': following_users, 'user_obj': session_user_obj, 'suggest_users': suggest_users}
		return render(request, 'home.html', params)
	else:
		return render(request, 'welcome.html')



	
def profile(request, username):
	try:
		user_obj = User.objects.get(user_name=username)
	except:
		messages.warning(request, 'User does not exists.')
		return HttpResponseRedirect(reverse('profile', args=[str(request.session['user'])]))
	user_posts = user_obj.post_set.all().order_by('-id')
	
	# session user object
	try:
		session_user_obj = User.objects.get(user_name=request.session['user'])
	except:
		messages.warning(request, 'You have to login first.')
		return redirect('index')

	# check follower
	check_follower = Follower.objects.get_or_create(user=user_obj)[0]

	#count following
	following_user_count = Follower.objects.filter(another_user=user_obj).count()

	is_followed = False
	if session_user_obj in check_follower.another_user.all():
		is_followed = True


	params = {'posts': user_posts, 'user_data':user_obj, 'is_followed': is_followed, 'followers_count': check_follower.another_user.count(), 'following_count': following_user_count}
	return render(request, 'profile.html', params)



def update_profile(request):
	if request.method == 'POST':
		user_obj = User.objects.get(user_name=request.session['user'])
		try:
			new_img = request.FILES['new_img']
		except:
			new_img = user_obj.profile_pic
		new_email = request.POST['mail']
		new_bio = request.POST['bio']

		
		if new_img:
			user_obj.profile_pic = new_img
		user_obj.email = new_email
		user_obj.bio = new_bio
		user_obj.save()
		
	return HttpResponseRedirect(reverse('profile', args=[str(request.session['user'])]))




def upload_post(request):
	if request.method == 'POST':
		user_obj = User.objects.get(user_name=request.session['user'])
		image_name = request.FILES['file_name']
		desc = request.POST['desc']
		upload_post = Post.objects.create(user=user_obj, img=image_name, desc=desc)
		upload_post.save()
		messages.success(request, 'Post uploaded successfully.')
	return render(request, 'upload.html')


def add_like(request):
	post_id = request.GET['postId']
	user_obj = User.objects.get(user_name=request.session['user'])
	post_obj = Post.objects.get(id=post_id)
	is_liked = False

	if user_obj in post_obj.likes.all():
		post_obj.likes.remove(user_obj)
		is_liked = True
	else:
		post_obj.likes.add(user_obj)
		is_liked = False

	return JsonResponse({'status': 'Ok', 'post_likes': post_obj.likes.count(), 'isLiked': is_liked})




def add_comment(request):
	comment = request.GET['comment']
	post_id = request.GET['post_id']
	
	user_obj = User.objects.get(user_name=request.session['user'])
	post_obj = Post.objects.get(id=post_id)

	add_comment = Comment(user=user_obj, post=post_obj, comment=comment)
	add_comment.save()

	get_comments = Comment.objects.filter(post=post_obj)
	return JsonResponse({'comment': add_comment.comment, 'user': user_obj.full_name, 'comment_count': get_comments.count()})



def follow_user(request):
	userId = request.GET['userId']
	# another user
	user_obj = User.objects.get(id=userId)
	# session user
	session_user_obj = User.objects.get(user_name=request.session['user'])
	# Follower obj
	check_follower = Follower.objects.get_or_create(user=user_obj)[0] #It is <Follower:user_obj>
	
	is_followed = False
	if session_user_obj in check_follower.another_user.all():
		is_followed = True
		check_follower.another_user.remove(session_user_obj)
	else:
		is_followed = False
		check_follower.another_user.add(session_user_obj)
	print('user id: ', userId)
	return JsonResponse({'status': 'Ok', 'isFollowed': is_followed, 'followers_count': check_follower.another_user.count()})



def user_login(request):
	if request.method == 'POST':
		userName = request.POST['uname']
		userPwd = request.POST['pwd']

		check_user = User.objects.filter(user_name=userName, password=userPwd)
		if check_user:
			request.session['user'] = userName
			messages.success(request, f'You have loggedin as {userName}!')
			return redirect('index')
		else:
			messages.warning(request, 'Invalid Username or Password.')
			return redirect('index')
	return redirect('index')



def user_logout(request):
	del request.session['user']
	return redirect('index')



def user_signup(request):
	if request.method == 'POST':
		fullName = request.POST['fname']
		userName = request.POST['uname']
		mail = request.POST['mail']
		userPwd = request.POST['pwd']
		
		new_user = User(full_name=fullName, user_name=userName, email=mail, password=userPwd)
		new_user.save()
		messages.success(request, 'Account has been created successfully.')
	return redirect('index')




def search(request):
	if request.method == 'GET':
		user_query = request.GET['query']

		search_users_uname = User.objects.filter(user_name__icontains=user_query)
		search_users_fname = User.objects.filter(full_name__icontains=user_query)

		search_results = search_users_uname.union(search_users_fname)
		
		params = {'results': search_results}
		return render(request, 'search.html', params)




def del_post(request):
	if request.method == 'GET':
		post_id = request.GET['postId']
		post_obj = Post.objects.get(id=post_id)
		post_obj.delete()

		return JsonResponse({'status': 'Ok', 'id': post_id})
	else:
		return JsonResponse({'status': 'not Ok'})
