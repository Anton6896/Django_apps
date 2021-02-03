from rest_framework import serializers
from . import models


class VotingSerializerApi(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    detail_url = serializers.HyperlinkedIdentityField(
        view_name='voting_app:detail',
        lookup_field='pk'
    )

    class Meta:
        model = models.Voting
        fields = (
            'detail_url',
            'pk',
            'short_description',
            'long_description',
            'date_end',
            'user',
            'counter_positive',
            'counter_negative',
            'counter_neutral'
        )


class UpdateVotingSerializerApi(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Voting
        fields = (
            'pk',
            'short_description',
            'long_description',
            'date_end',
            'is_active',
            'user',
            'counter_positive',
            'counter_negative',
            'counter_neutral'
        )


# combining two serializers for voting procedure -----------------------

class UtilVotingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Voting
        fields = (
            'pk',
            'short_description',
            'long_description',
            'date_end'
        )


class UtilVotingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.VotingChoices
        fields = (
            'voting_choice',
            'voting',
            'user'
        )

# -------------------------------------------------


class UtilVotingMy(serializers.Serializer):
    pk = serializers.IntegerField()
    user = serializers.CharField(max_length=150, read_only=True)
    voting__short_description = serializers.CharField(
        max_length=255, read_only=True)

    voting_choice = serializers.ChoiceField(
        choices=models.VotingChoices.VOTING_CHOICES)

    def restore_object(self, attrs, instane=None):
        if instane is not None:
            instane.short_description = attrs.get(
                'voting__short_description', instane.short_description)
            instane.voting_choice = attrs.get(
                'voting_choice', instane.voting_choice)
            return instane
        return models.Voting(**attrs)


class VotingPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.VotingChoices
        fields = ['voting_choice', 'user', 'voting']


class UserUnVotingListSerializer(serializers.Serializer):
    voting__pk = serializers.IntegerField()
    voting__short_description = serializers.CharField(
        max_length=255, read_only=True)

    def restore_object(self, attrs, instane=None):
        if instane is not None:
            instane.short_description = attrs.get(
                'voting__short_description', instane.short_description)
            return instane
        return models.Voting(**attrs)


