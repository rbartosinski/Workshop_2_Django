from django.urls import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.utils.dateparse import parse_date
from rooms.models import Room, Booking


class Rooms(View):

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, "rooms.html", {
            "rooms": rooms,
        })


class Reservation(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "new_booking.html", {"room": room})

    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        try:
            date = parse_date(request.POST["date"])
        except (ValueError, KeyError):
            return HttpResponseBadRequest("Niepoprawna data")
        if date >= date.today():
            try:
                Booking.objects.create(room=room, date=date,
                                       comment=request.POST.get("comment", ''))
            except IntegrityError:
                return HttpResponseBadRequest("Sala jest już zajęta. Wybierz inną datę.")
            return HttpResponseRedirect(reverse("rooms"))
        else:
            return HttpResponseBadRequest("Przedawniona data rejestracji.")


class AddRoom(View):

    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        seats = request.POST["seats"]
        if seats != '':
            seats_num = request.POST["seats"]
        else:
            seats_num = 0
        if 'projector' in request.POST:
            projector_add = True
        else:
            projector_add = False
        Room.objects.create(name=request.POST.get("name", ''), seats=seats_num,
                               projector=projector_add)
        return HttpResponseRedirect(reverse("rooms"))


class RoomModify(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "room_modify.html", {"room": room})

    def post(self, request, room_id):
        name = request.POST['name']
        seats = int(request.POST['seats'])
        if 'projector' in request.POST:
            projector = True
        else:
            projector = False
        room = get_object_or_404(Room, id=room_id)
        room.name = name
        room.seats = seats
        room.projector = projector
        room.save()
        return HttpResponseRedirect(reverse("rooms"))


class RoomDelete(View):

    def get(self, request, room_id):
        get_object_or_404(Room, id=room_id).delete()
        return HttpResponseRedirect(reverse("rooms"))


class RoomDetails(View):

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        bookings = Booking.objects.filter(room=room_id).all()
        return render(request, 'room_details.html', {
            'room': room,
            'bookings': bookings,
        })


class RoomSearch(View):

    def get(self, request):
        return render(request, 'room_search.html')

    def post(self, request):
            rooms = Room.objects.all()
            name = request.POST.get('name')
            if name != '':
                rooms = rooms.filter(name=name)
            seats_max = request.POST.get('seats_max')
            if seats_max != '':
                rooms = rooms.filter(seats__lte=seats_max)
            seats_min = request.POST.get('seats_min')
            if seats_min != '':
                rooms = rooms.filter(seats__gte=seats_min)
            if 'projector' in request.POST:
                projector = True
                rooms = rooms.filter(projector=projector)
            finded_rooms = rooms
            return render(request, 'room_search.html', {
                'finded_rooms': finded_rooms
            })