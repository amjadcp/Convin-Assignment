from rest_framework import serializers

class CredentialsSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    client_secret = serializers.CharField()