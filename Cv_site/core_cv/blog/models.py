from django.db import models
from accounts.models import CustomUser as User
from PIL import Image
from django.utils import timezone


def customer_image_file_path(instance, filename):
    import os
    import uuid
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('upload/blog_pic/', filename)


class BlogManager(models.Manager):
    pass


class Blog(models.Model):
    objects = BlogManager()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(default='blog_default.jpg',
                              upload_to=customer_image_file_path)
    created_at = models.DateTimeField(default=timezone.now)

    # image resize

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)

        try:
            img = Image.open(self.image.path)
            output_size = (300, 300)

            if img.height > 300 or img.width > 300:
                img.thumbnail(output_size)
                img.save(self.image.path)
        except IOError:
            print(f'where is the file for img working ?')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:blog_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_at", ]
        db_table = 'blog'
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'

    def __str__(self) -> str:
        return "Post : " + self.title


class BlogComment(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "comment by [" + str(self.author.username) + "]"

    class Meta:
        ordering = ["-created_at", ]
