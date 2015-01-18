from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    # use a string to represent the class
    def __str__(self):
        return self.name

    # make model appears as Categories instead of Categorys in admin by using a inner class Meta
    class Meta:
        verbose_name_plural =  "Categories"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128, unique=True)
    # use models.URLField to store URL addresses
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_images", blank=True)
    
    def __str__(self):
        return self.user.username