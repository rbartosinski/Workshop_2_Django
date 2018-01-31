"""workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rooms.views import Rooms, AddRoom, Reservation, RoomDetails, RoomModify, RoomSearch, RoomDelete


urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^rooms/$', Rooms.as_view(), name='rooms'),
    url(r'^reservation/(?P<room_id>\d+)/$', Reservation.as_view(), name='reservation'),
    url(r'^room_details/(?P<room_id>\d+)/$', RoomDetails.as_view(), name='room_details'),
    url(r'^add_room/$', AddRoom.as_view(), name='add_room'),
    url(r'^room/modify/(?P<room_id>\d+)/$', RoomModify.as_view(), name='room_modify'),
    url(r'^search_room/$', RoomSearch.as_view(), name='search_room'),
    url(r'^delete_room/(?P<room_id>\d+)/$', RoomDelete.as_view(), name='delete_room'),
]
