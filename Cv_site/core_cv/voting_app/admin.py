from django.contrib import admin
from . import models


class CustomVoting(admin.ModelAdmin):
    list_display = ['pk', 'is_active', 'short_description',
                    'counter_positive', 'counter_negative', 'date_posted', 'date_end']
    list_display_links = ['pk', 'short_description',]


admin.site.register(models.Voting, CustomVoting)
admin.site.register(models.VotingChoices)
