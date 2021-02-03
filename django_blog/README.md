# port_site_1
creating the portfolio dynamic site 
first using the : https://www.youtube.com/watch?v=9cKsq14Kfsw&t=467s
second will use the : https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
database for use psql .

so front end is bootstrap 4 
backend Django 



correy shefler lesson to create blog 
https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p




# crete the db at first
$ python manage.py makemigrations 
$ python manage.py migrate

# create the admin for web app 
$ python manage.py createsuperuser


# django ORM system -----------------------------------------------
thru the models use the orm command for use db 
using the python shell to work with django objects 

$ python manage.py shell 
$ from django.contrib.auth.models import User
$ from blog.models import Post


$ User.objects.all()
$ User.objects.filter(username='anton')

# if name if unique will return the first in query 
$ user = User.objects.filter(username='anton').first() 
$ user.id
$ user.pk

# find user by id 
$ user = User.objects.get(id=1)
$ user = User.objects.filter(username='name1')

# add new Post terminal 
$ user1 = User.objects.get(username='user1').first()
$ post_1 = Post(title='title_1', content='content_title_1', author=user1)
$ post_1.save()

# get set with user posts 
$ user.post_set.all()

# create post via set
$ user.post_set.create(title='post3', content='content_post3')



# user app -------------------------------------
configure the template and the static folder for user app 
register the app at the settings.py 
add users to the urls path 

for user interface installing the crispy forms that will add some style for the forms 
https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs

# one to chose to work with ( then look to document to how use it)
$ pip install django-crispy-forms
$ pip install django-bootstrap4
add forms to the django settings , i am using the bootstrap4 type 

update the user profile 
$ pip install Pillow  

create signal that user has created and signal will create the new profile for the new user 
# in this example the post_save was not executed do defined manually in the users/__init__.py 
# default_app_config = 'users.apps.UsersConfig'


create , update the user profile instance 


