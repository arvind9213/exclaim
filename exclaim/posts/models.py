from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User




def upload_location(instance, filename):
    # filebase, extension=filename.split(".")
    # return "%s/%s.%s"%(instance.id,instance.id,extension)
    return "%s/%s"%(instance.id,filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    # image = models.FileField(null=True,blank=True)
    image = models.ImageField(upload_to=upload_location,
            null=True,blank=True,
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(null=True,blank=True)
    url_field = models.TextField(null=True,blank=True)
    embeded_field = models.TextField(null=True,blank=True)
    tags_field = models.TextField(null=True,blank=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    # objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
        # return "/posts/%s/"%(self.id)

    class Meta:
         ordering = ["-timestamp","-updated"]


def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug =new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists =qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug


def pre_save_post_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reciever,sender=Post)


