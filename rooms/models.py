from django.db import models
from datetime import date


class Room(models.Model):
    name = models.CharField(max_length=32)
    seats = models.IntegerField(null=True)
    projector = models.BooleanField(default=False)

    def is_currently_booked(self):
        bookings_today = self.bookings.filter(date=date.today())
        return len(bookings_today) != 0


class Booking(models.Model):
    room = models.ForeignKey(Room, null=True,
                             on_delete=models.SET_NULL,
                             related_name='bookings')
    date = models.DateField()
    comment = models.CharField(max_length=128)

    class Meta:
        unique_together = ("room", "date")