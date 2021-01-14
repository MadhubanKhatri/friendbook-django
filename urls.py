from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	path('<str:username>/profile/', views.profile, name='profile'),
	path('upload/', views.upload_post, name='upload_post'),
	path('update_profile/', views.update_profile, name='update_profile'),
	path('add_like/', views.add_like, name='add_like'),
	path('add_comment/', views.add_comment, name='add_comment'),
	path('del_post/', views.del_post, name='delete_post'),

	path('follow_user/', views.follow_user, name='follow_user'),

	path('login/' ,views.user_login, name='user_login'),
	path('logout/' ,views.user_logout, name='user_logout'),


	path('signup/', views.user_signup, name='user_signup'),


	path('search/' ,views.search, name='search_user'),

]