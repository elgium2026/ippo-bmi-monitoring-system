import base64
from io import BytesIO

import pyotp
import qrcode
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from openpyxl import Workbook
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, LoginHistory
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    CustomUserSerializer,
    AdminPasswordChangeSerializer,
    PersonnelUpdateSerializer,
    AdminPersonnelUpdateSerializer,
)


def create_login_history(username, action, success, user=None):
    LoginHistory.objects.create(username=username, action=action, success=success, user=user)


def build_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            create_login_history(user.username, 'Signup', True, user)
            return Response({'message': 'Signup successful.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonnelLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.is_personnel:
                create_login_history(request.data.get('username', ''), 'Personnel login attempt with admin account', False)
                return Response({'detail': 'Personnel credentials required.'}, status=status.HTTP_403_FORBIDDEN)
            create_login_history(user.username, 'Personnel login', True, user)
            return Response({
                'tokens': build_tokens(user),
                'user': CustomUserSerializer(user).data,
            })
        create_login_history(request.data.get('username', ''), 'Personnel login failed', False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComputeBMIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PersonnelUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            create_login_history(user.username, 'BMI compute', True, user)
            return Response(CustomUserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.is_personnel:
                create_login_history(user.username, 'Admin login attempt with personnel account', False, user)
                return Response({'detail': 'Admin credentials required.'}, status=status.HTTP_403_FORBIDDEN)
            if not user.is_staff:
                create_login_history(user.username, 'Admin login attempt without staff privileges', False, user)
                return Response({'detail': 'Admin privileges are required.'}, status=status.HTTP_403_FORBIDDEN)
            create_login_history(user.username, 'Admin login', True, user)
            return Response({
                'tokens': build_tokens(user),
                'must_change_password': user.must_change_password,
                'user': CustomUserSerializer(user).data,
            })
        create_login_history(request.data.get('username', ''), 'Admin login failed', False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = AdminPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['password'])
            request.user.must_change_password = False
            request.user.save()
            create_login_history(request.user.username, 'Admin password changed', True, request.user)
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(CustomUser, username=username, is_staff=True, is_personnel=False)
        secret = pyotp.random_base32()
        user.admin_totp_secret = secret
        user.save()

        otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name='Ifugao PPO BMI Monitor')
        image = qrcode.make(otpauth_url)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        qr_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        create_login_history(username, 'Admin forgot password requested', True, user)
        return Response({'qr_code_base64': f'data:image/png;base64,{qr_data}', 'message': 'Scan the QR code with Google Authenticator.'})

class AdminVerifyOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        user = get_object_or_404(CustomUser, username=username, is_staff=True, is_personnel=False)
        if not user.admin_totp_secret:
            return Response({'detail': 'QR code setup is required before verification.'}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({'confirm_password': ['Passwords do not match.']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from .validators import validate_personnel_password
            validate_personnel_password(password)
        except Exception as exc:
            return Response({'password': [str(exc)]}, status=status.HTTP_400_BAD_REQUEST)
        totp = pyotp.TOTP(user.admin_totp_secret)
        if not totp.verify(otp):
            create_login_history(username, 'Admin OTP verification failed', False, user)
            return Response({'detail': 'Invalid authentication code.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.must_change_password = False
        user.save()
        create_login_history(username, 'Admin OTP verification success', True, user)
        return Response({'message': 'Password reset successfully. Please log in with your new password.'})

class AdminPersonnelListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        personnel = CustomUser.objects.filter(is_personnel=True)
        serializer = CustomUserSerializer(personnel, many=True)
        return Response(serializer.data)

class AdminPersonnelDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk, is_personnel=True)
        return Response(CustomUserSerializer(user).data)

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk, is_personnel=True)
        serializer = AdminPersonnelUpdateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_login_history(request.user.username, f'Admin edited personnel {user.username}', True, request.user)
            return Response(CustomUserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk, is_personnel=True)
        username = user.username
        user.delete()
        create_login_history(request.user.username, f'Admin deleted personnel {username}', True, request.user)
        return Response({'message': 'Personnel deleted successfully.'})

class AdminExportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        personnel = CustomUser.objects.filter(is_personnel=True)
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'BMI Reports'
        headers = [
            'UNIT', 'RANK', 'LAST NAME', 'FIRST NAME', 'MIDDLE NAME', 'QLFR', 'BIRTHDATE',
            'AGE', 'SEX', 'WEIGHT (kg)', 'HEIGHT (cm)', 'WAIST (cm)', 'HIP (cm)', 'WRIST (cm)',
            'BMI', 'PNP BMI ACCEPTABLE STANDARD', 'WHO STANDARD', 'Weight to Lose (Kg)',
            'Normal Weight (Kg)', 'REMARKS',
        ]
        sheet.append(headers)
        for person in personnel:
            sheet.append([
                person.unit_other if person.unit == 'Other Units (Please Specify)' else person.unit,
                person.rank,
                person.last_name,
                person.first_name,
                person.middle_name,
                person.qualifier,
                person.birthdate.isoformat() if person.birthdate else '',
                person.age,
                person.sex,
                person.weight_kg,
                person.height_cm,
                person.waist_cm,
                person.hip_cm,
                person.wrist_cm,
                person.bmi,
                person.pnp_bmi_classification,
                person.who_bmi_classification,
                person.weight_to_lose,
                person.max_normal_weight,
                person.remarks,
            ])
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="bmi_reports.xlsx"'
        return response
