from django.contrib.auth.models import Group


def add_to_group(sender, instance, created, **kwargs):
    if created:
        # add user to the group ?
        if instance.role == 'committee':
            g = Group.objects.get(name='committee_group')
            g.user_set.add(instance)
