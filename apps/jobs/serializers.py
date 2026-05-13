import re
from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"

    def validate_phone(self, value):
        value = value.replace(" ", "")

        pattern = r"^(\+94|0)?7\d{8}$"

        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid Sri Lankan phone number.")

        return value
