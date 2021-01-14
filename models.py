from django.db import models

# Create your models here.
class User(models.Model):
	full_name = models.CharField(max_length=100)
	user_name = models.CharField(max_length=100)
	email = models.EmailField()
	password = models.CharField(max_length=50)
	bio = models.TextField(default='')
	profile_pic = models.ImageField(upload_to='profile_pic/', default='profile_pic/default.jpg')
	date_joined = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.full_name



class Follower(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	another_user = models.ManyToManyField(User, related_name='another_user')

	def __str__(self):
		return self.user.user_name



class Post(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	img = models.ImageField(upload_to='post_images/')
	desc = models.TextField()
	likes = models.ManyToManyField(User, related_name='likes')
	pub_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-pub_date']

	def __str__(self):
		return self.img.url



class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.CharField(max_length=500)

