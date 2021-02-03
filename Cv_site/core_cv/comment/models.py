from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from accounts.models import CustomUser


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        # instance.__class__  -> return the instance by class for more generic use
        content_type = ContentType.objects.get_for_model(instance.__class__)  # return Message
        obj_id = instance.pk  # return message.pk
        return super(CommentManager, self) \
            .filter(content_type=content_type, object_pk=obj_id) \
            .filter(parent=None)

    def all(self):
        return super(CommentManager, self).filter(parent=None)

    def create_by_model_type(self, model_type, pk, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            some_model = model_qs.first().model_class()  # message / comment / obj
            obj_qs = some_model.objects.filter(pk=pk)  # get -> message.pk == pk   /obj

            if obj_qs.exists():
                # in this case creating Comment obj
                # comment.objects = CommentManager()
                instance = self.model()  # crete instance -> comment
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_pk = obj_qs.first().pk

                if parent_obj:
                    instance.parent = parent_obj

                instance.save()
                return instance

        return None


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    objects = CommentManager()
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    """
    generic foreign key
    will crete object with data that referenced to some table (db) with some key 
    without checking if its exist ! 
    
    example:
    just saving the content fot message with pk 2 , 
    its dissent marrow if message with this key is exist al all 
    the comment with this data will be exist ! 
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_pk')

    def __str__(self):
        return f'pk {self.pk} :: comment for "{self.content_type}" ' \
               f'with id {self.object_pk} , by <{self.user.username}>'

    @property
    def is_child(self):  # replies
        # check if obj parent != None
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None

    class Meta:
        ordering = ['-timestamp']
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
