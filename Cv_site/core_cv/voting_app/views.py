from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from . import models
from . import serializers
from accounts.my_permissions import IsCommettee, IsOwner
from rest_framework import generics, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, views
from drf_multiple_model.views import ObjectMultipleModelAPIView, FlatMultipleModelAPIView
from rest_framework import mixins
from rest_framework.response import Response


class CreateVotingApi(generics.CreateAPIView):
    '''
    create new voting question , on create have an signal that will create 
    first vote as user that created the question ( choice = pass )
    '''
    serializer_class = serializers.VotingSerializerApi
    permission_classes = [
        permissions.IsAuthenticated, IsCommettee
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateVotingApi(generics.RetrieveUpdateDestroyAPIView):
    # update existing voting data , look by pk
    serializer_class = serializers.UpdateVotingSerializerApi
    permission_classes = [
        permissions.IsAuthenticated, IsCommettee
    ]
    queryset = models.Voting.objects.filter(is_active=True).all()


class ListActiveVoting(generics.ListAPIView):
    # show all active votings
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Voting.objects.filter(is_active=True).all()
    serializer_class = serializers.VotingSerializerApi


class ListUnActiveVoting(generics.ListAPIView):
    # show all un active votings
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Voting.objects.filter(is_active=False).all()
    serializer_class = serializers.VotingSerializerApi


class ListVotingWithChoices(ObjectMultipleModelAPIView):
    #  testing for my self , return 2 query set at once
    permission_classes = [permissions.IsAuthenticated]

    querylist = [
        {
            'queryset': models.Voting.objects.filter(is_active=True).all(),
            'serializer_class': serializers.UtilVotingMessageSerializer
        },
        {
            'queryset': models.VotingChoices.objects.all(),
            'serializer_class': serializers.UtilVotingSerializer
        }
    ]


class AllUserVoteList(views.APIView):
    #  return all user votings
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        my_query = models.VotingChoices.objects.filter(user=request.user).values(
            'pk', 'voting__short_description', 'voting_choice', 'user'
        )

        serializer = serializers.UtilVotingMy(my_query, many=True)
        return Response(serializer.data)


class AllUserUnVoteList(views.APIView):
    #  return all user un votings object
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # all voting that user not did yet

        query_with_user = models.VotingChoices.objects.filter(
            user_id=request.user).all()
        query_all = models.VotingChoices.objects.all()
        query_r1 = query_all.difference(query_with_user)
        query = query_r1.values(
            'voting__pk', 'voting__short_description'
        )

        serializer = serializers.UserUnVotingListSerializer(query, many=True)
        return Response(serializer.data)


class VotingPost(generics.CreateAPIView):
    # make vote as user
    serializer_class = serializers.VotingPostSerializer
    permission_classes = [
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
