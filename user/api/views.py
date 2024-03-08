import requests
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.utils import timezone
from constance import config
from .serializers import *
from .exceptions import *



# User Registration Api
class UserRegisterView(viewsets.ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer_data = self.get_serializer(
                instance=User.objects.get(
                    email=request.data['email']
                )
            ).data
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                    "data": serializer_data
                },
                status=200
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )




# User Verify Account with otp after Registration Api View
class UserVerifyAccountView(viewsets.ModelViewSet):
    serializer_class = UserVerifyAccountSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.is_active = True
            user.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Success",
                },
                status=200
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User Login Api Views
class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                email=serializer.validated_data['email']
            )
            token, _created = Token.objects.get_or_create(
                user = user
            )
            user.last_login = timezone.datetime.now()
            user.save()
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Login Success.",
                    'token': token.key,
                    'data': UserProfileSerializer(user).data
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# Forget User Password Api Views
class ForgetPasswordView(viewsets.ModelViewSet):
    serializer_class = ForgetPasswordSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Otp sent on email, please verify..",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )




# Forget User Password Api Views
class ConfirmForgetPasswordView(viewsets.ModelViewSet):
    serializer_class = ConfirmForgetPasswordSerializer
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "OK",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User Change Password
class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = ChangePasswordSerializer
    http_method_names = ('post',)
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        email = user.email
        try:
            request.data['email'] = email
        except:
            request.data._mutable = True
            request.data['email'] = email
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            try:
                request.user.auth_token.delete()
            except:
                pass
            return Response(
                {   'status': status.HTTP_200_OK,
                    'message': "Success.",
                }
            )
        errors = serializer.errors
        error_message = ""
        for key in list(errors):
            error_message += f"{errors[key][0]}"
            break
        return Response(
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# User logout api view - here we delete user auth token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'status': 200, 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 500, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" User Profile View. """
class ProfileView(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance = request.user,
            data = request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "OK",
                }
            )
        return Response(
            status = status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )



"""
    Sign in with google View
"""
@api_view(['POST'])
def googleAuth(request):
    id_token = request.data.get('id_token', None)
    if not id_token:
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "BAD REQUEST",
                'errors': {
                    'id_token': "This field is required"
                }
            },
            status=400
        )
    url = "https://oauth2.googleapis.com/tokeninfo"
    params = {'id_token': f'{id_token}'}

    r = requests.get(url, params=params)

    try:
        result = r.json()
        userid = result['sub']
        email = result['email']
        # profile_picture = result['picture']
        f_name = result['given_name']
        l_name = result['family_name']

        if email:
            user_objects = User.objects.filter(email=email)
            if user_objects:
                user = user_objects.first()
                # user.image = profile_picture
                user.name = f"{f_name} {l_name}"
                user.login_method = "GOOGLE"
                user.social_id = userid
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                user.last_login = timezone.datetime.now()
                user.save()
                return Response(
                    data = {
                        'status': status.HTTP_200_OK,
                        'message': "Login Success.",
                        'token': token.key,
                        'data': UserProfileSerializer(user).data
                    }
                )

            else:
                user = User(
                    email = email,
                    name = f"{f_name} {l_name}",
                    # image = profile_picture,
                    login_method = "GOOGLE",
                    social_id = userid,
                    is_active = True
                )
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                user.last_login = timezone.datetime.now()
                user.save()
                return Response(
                    data = {
                        'status': status.HTTP_200_OK,
                        'message': "Login Success.",
                        'token': token.key,
                        'data': UserProfileSerializer(user).data
                    }
                )
        else:
            return Response(
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Please Input Valid Token"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        raise InvaliedToken()
    


# Facebook auth
@api_view(['POST'])
def facebookAuth(request):
    access_token = request.data.get('access_token', None)
    if not access_token:
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "BAD REQUEST",
                'errors': {
                    'access_token': "This field is required"
                }
            },
            status=400
        )
    try:
        url = "https://graph.facebook.com/me"
        params = {'access_token': f'{access_token}'}

        r = requests.get(url, params=params)
        result = r.json()
        data_details = {}
        data_details['name'] = result['name']
        data_details['id'] = result['id']

        # return Response({"data": data_details, "status": "success"})

    except Exception as ex:
        raise InvaliedToken()

    try:
        url = f"https://graph.facebook.com/{result['id']}"
        params = {'fields': 'id,name,email,picture', 'access_token': f'{access_token}'}

        p = requests.get(url, params=params)

        result2 = p.json()
        name = result2['name']
        email = result2['email']
        id = result2['id']
        # login_type = "facebook"

        if email:
            user_objects = User.objects.filter(email=email)
            if user_objects:
                user = user_objects.first()
                user.name = name
                user.login_method = "FACEBOOK"
                user.social_id = id
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                user.last_login = timezone.datetime.now()
                user.save()
                return Response(
                    data = {
                        'status': status.HTTP_200_OK,
                        'message': "Login Success.",
                        'token': token.key,
                        'data': UserProfileSerializer(user).data
                    }
                )
            else:
                user = User(
                    email = email,
                    name = name,
                    login_method = "FACEBOOK",
                    social_id = id,
                    is_active = True
                )
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                user.last_login = timezone.datetime.now()
                user.save()
                return Response(
                    data = {
                        'status': status.HTTP_200_OK,
                        'message': "Login Success.",
                        'token': token.key,
                        'data': UserProfileSerializer(user).data
                    }
                )
        else:
            raise InvaliedToken()
    except Exception as ex:
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"{ex}"
            }
        )



""" Country Code List View. """
class CountryCodeView(viewsets.ModelViewSet):
    http_method_names = ("get",)
    serializer_class = CountryCodeSerializer
    queryset = CountryCode.objects.all()
    
    def list(self, request, *args, **kwargs):
        return Response(
            data={
                'status': 200,
                'message': "OK",
                "data": self.serializer_class(self.queryset, many=True).data
            }
        )
