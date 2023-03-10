import os
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    choices = (
        ('blog')
    )

    name = models.CharField(max_length=200)




# def upload_path_handler(instance, filename):
#     return os.path.join(
#         f'user_{instance.headline}', filename
#     )


class Post(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='images/', default="placeholder.png")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(self.headline)
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug
        super(Post, self).save(*args, **kwargs)
