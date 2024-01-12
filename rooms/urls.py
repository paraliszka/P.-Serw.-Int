from django.urls import path
from . import views

urlpatterns = [
    path("rooms", views.RoomList.as_view(), name=views.RoomList.name),
    path("rooms/create", views.RoomCreate.as_view(), name=views.RoomCreate.name),
    path("rooms/<int:pk>", views.RoomDetail.as_view(), name=views.RoomDetail.name),
    path("topics", views.TopicsList.as_view(), name=views.TopicsList.name),
    path("topics/<int:pk>", views.TopicDetail.as_view(), name=views.TopicDetail.name),
    path("message", views.MessagesList.as_view(), name=views.MessagesList.name),
    path("rooms/<int:pk>/message/create", views.MessageCreate.as_view(), name=views.MessageCreate.name),
    path("message/<int:pk>", views.MessageDetail.as_view(), name=views.MessageDetail.name),
    path("rooms/<int:pk>/rate", views.RoomRatingCreate.as_view(), name=views.RoomRatingCreate.name),
    path("user-rated-rooms/", views.UserRatedRoomsList.as_view(), name=views.UserRatedRoomsList.name),
]