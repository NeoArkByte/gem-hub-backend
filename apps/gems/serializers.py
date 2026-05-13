import re
from rest_framework import serializers
from .models import GemListing


class GemListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GemListing
        fields = "__all__"

    def validate_seller_phone(self, value):
        value = value.replace(" ", "")

        pattern = r"^(\+94|0)?7\d{8}$"

        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid Sri Lankan phone number.")

        return value
