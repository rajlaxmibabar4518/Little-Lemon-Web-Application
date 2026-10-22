from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "title", "price", "inventory"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]

    def validate_reservation_slot(self, value):
        if not 0 <= value <= 23:
            raise serializers.ValidationError("Slot must be an hour between 0 and 23.")
        return value

    def validate(self, attrs):
        date = attrs.get("reservation_date", getattr(self.instance, "reservation_date", None))
        slot = attrs.get("reservation_slot", getattr(self.instance, "reservation_slot", None))
        clash = Booking.objects.filter(reservation_date=date, reservation_slot=slot)
        if self.instance:
            clash = clash.exclude(pk=self.instance.pk)
        if clash.exists():
            raise serializers.ValidationError("That time slot is already booked for this date.")
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
