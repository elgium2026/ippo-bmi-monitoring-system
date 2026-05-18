from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from .validators import validate_personnel_password

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    bmi = serializers.SerializerMethodField()
    pnp_bmi_classification = serializers.SerializerMethodField()
    who_bmi_classification = serializers.SerializerMethodField()
    weight_to_lose = serializers.SerializerMethodField()
    max_normal_weight = serializers.SerializerMethodField()
    remarks = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'rank', 'rank_classification', 'first_name', 'middle_name',
            'last_name', 'qualifier', 'birthdate', 'age', 'unit', 'unit_other', 'sex',
            'weight_kg', 'height_cm', 'waist_cm', 'hip_cm', 'wrist_cm',
            'bmi', 'pnp_bmi_classification', 'who_bmi_classification',
            'weight_to_lose', 'max_normal_weight', 'remarks',
        ]

    def get_age(self, obj):
        return obj.age

    def get_bmi(self, obj):
        return obj.bmi

    def get_pnp_bmi_classification(self, obj):
        return obj.pnp_bmi_classification

    def get_who_bmi_classification(self, obj):
        return obj.who_bmi_classification

    def get_weight_to_lose(self, obj):
        return obj.weight_to_lose

    def get_max_normal_weight(self, obj):
        return obj.max_normal_weight

    def get_remarks(self, obj):
        return obj.remarks

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    unit_other = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'confirm_password', 'rank', 'rank_classification',
            'first_name', 'middle_name', 'last_name', 'qualifier', 'birthdate',
            'unit', 'unit_other',
        ]

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        validate_personnel_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.is_personnel = True
        user.must_change_password = False
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        data['user'] = user
        return data

class AdminPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        validate_personnel_password(data.get('password'))
        return data

class PersonnelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'rank', 'rank_classification', 'first_name', 'middle_name', 'last_name',
            'qualifier', 'birthdate', 'unit', 'unit_other', 'sex', 'weight_kg',
            'height_cm', 'waist_cm', 'hip_cm', 'wrist_cm',
        ]

class AdminPersonnelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'rank', 'rank_classification', 'first_name', 'middle_name',
            'last_name', 'qualifier', 'birthdate', 'unit', 'unit_other', 'sex',
            'weight_kg', 'height_cm', 'waist_cm', 'hip_cm', 'wrist_cm',
        ]
