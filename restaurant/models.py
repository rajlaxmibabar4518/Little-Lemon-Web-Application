from django.db import models


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    class Meta:
        ordering = ["reservation_date", "reservation_slot"]

    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} @ {self.reservation_slot}:00"


class Menu(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.SmallIntegerField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} : {self.price}"
