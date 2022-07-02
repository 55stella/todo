from django.shortcuts import render

# Create your views here.


from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from copy import error
from rest_framework import serializers, status

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models import CustomUser
from account.serializers import UserSerializers, ChangePasswordSerializer, LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.signals import user_logged_in
from drf_yasg import openapi









User = get_user_model()

@swagger_auto_schema(methods=['POST'], request_body= UserSerializers())
@api_view(['POST'])
def signup(request):
    
    if request.method =="POST":
        
            serializer=UserSerializers(data = request.data)#creates an instance of serializer class. it al

            if serializer.is_valid():
                serializer.validated_data['password']=make_password(serializer.validated_data['password'])#hash/encrypt the password
                user = User.objects.create(**serializer.validated_data)#dictionary unpackin
                #here we are unpacking. we save a new password by starting to create the serializer by name, password etc
                user_serializer = UserSerializers(user)#after hashingn the password we still need to pass into serializer to convert to jason
                data={
                    "message":"success",
                    "data": user_serializer.data
                }
                
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                error ={
                    'message': 'failed',
                    "error": serializer.errors
                }
                return Response(error, status= status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
     user = request.user# here we are trying to request for that particuar user
     # print(user.password)
     if request.method == "POST":
         serializer = ChangePasswordSerializer(data=request.data)

         if serializer.is_valid():
             old_password = serializer.validated_data['old_password']
             if check_password(old_password, user.password):#this check_password function tries to check two passwords if they are the same
                  #user.password will try to get the password belonging to that particular userv mayb saved somewhere innthe system.
                 user.set_password(serializer.validated_data['new_password'])#the set password function tries to replace the old password with the new one

                 user.save()

                 # print(user.password)

                 return Response({"message":"success"}, status=status.HTTP_200_OK)

             else:
                 error = {
                 'message':'failed',
                 "errors":"Old password not correct"
             }

             return Response(error, status=status.HTTP_400_BAD_REQUEST) 

         else:
             error = {
                 'message':'failed',
                 "errors":serializer.errors
             }

             return Response(error, status=status.HTTP_400_BAD_REQUEST)  


# @swagger_auto_schema(methods=['POST'], request_body=LoginSerializer())
# @api_view(['POST'])
# def login(request):
#     if request.method =="POST":
#         serializer = LoginSerializer(data= request.data)
#         if serializer.is_valid():
#             user = authenticate(request, username= serializer.validated_data['username'], password = serializer.validated_data['password'])
#             if user:
#                 if user.is_active:
#                     serializer= UserSerializers(user)
#                     data={
#                         'message':'login successful',
#                         'data':serializer.data
#                     }
#                     return Response(data, status= status.HTTP_200_OK)
#                 else:
#                     error ={
#                         'message': 'please activate your account'
#                     }
#                     return Response(error, status =  status.HTTP_401_UNAUTHORIZED)
#             else:
#                 error={
#                     'error':serializer.errors
#                 }        


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    }
))
@api_view(['POST'])



def user_login(request):

     """Allows users to log in to the platform. Sends the jwt refresh and access tokens. Check settings for token life time."""

     if request.method == "POST":
         user = authenticate(request, username = request.data['username'], password = request.data['password'])
         if user is not None:
             if user.is_active==True:

                 try:

                     user_detail = {}
                     user_detail['id']   = user.id
                     user_detail['first_name'] = user.first_name
                     user_detail['last_name'] = user.last_name
                     user_detail['email'] = user.email
                     user_detail['username'] = user.username

                     user_logged_in.send(sender=user.__class__,
                                         request=request, user=user)#to signal django to take record of the time the user is logging in.

                     data = {
                     'status'  : True,
                     'message' : "Successful",
                     'data' : user_detail,
                     }
                     return Response(data, status=status.HTTP_200_OK)



                 except Exception as e:
                     raise e
             else:
                 data = {
                 'status'  : False,
                 'error': 'This account has not been activated'
                 }
             return Response(data, status=status.HTTP_403_FORBIDDEN)

         else:
             data = {
                 'status'  : False,
                 'error': 'Please provide a valid username and a password'
                 }
             return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserSerializers())
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def profile(request):
    """
    Takes in a student id and returns the http response depending on the http method.
    Args:
    student_id:integer


    Allowed methods:
    GET- get the detail of a single student
    PUT- allows students details to be edited
    DELETE: this logic deletes the students record from the database.
    """
    
    # try:
    user = User.objects.all()

    #     # this would return a querry set.Not only a querry set, it would return the id of a logged in user
                                               
    # except User.DoesNotExist:
    #         error ={
    #              "message": "failed",
    #              "error":f"profile  with id{id} does not exist"
    #         }
    #         return  Response(error, status=status.HTTP_400_BAD_REQUEST) 
    if request.method == 'GET':
        serializer = UserSerializers(user)
        data = {
            "message":"sucess",
            "data":serializer.data
            #prepare the response
        }
        return Response(data, status= status.HTTP_200_OK)#send the response
    elif request.method =="PUT":
        serializer = UserSerializers(user, data = request.data, partial = True)#here we are trying to convert the querry set to jason by passing it into the erializer class
        

        if serializer.is_valid():
            print(serializer.validated_data)
            if 'password' in serializer.validated_data.keys():

                raise ValidationError('unable to change password')
                    #if serializer.validated_data['password']!= serializer['password']:
                    #error ={
                        #"message":"failed",
                        #"#errors":serializer.errors
                    #}
                    #return Response(error, status =status.HTTP_403_FORBIDDEN)
                
                    
                   # else:   
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
            }
            return Response(data, status = status.HTTP_202_ACCEPTED)
        else:
            error = {
                "message":"failes",
                "errors":serializer.errors
            }
            return Response(error, status = status.HTTP_400_BAD_REQUEST)

    elif request.method=="DELETE":
        user.is_active=False
        user.save()
        data ={
            'status':True,
            'message':'Successfully deleted' 
        }
        return Response({"message":"success"}, status= status.HTTP_204_NO_CONTENT)




@swagger_auto_schema(methods=['DELETE'], request_body=UserSerializers())
@api_view(['GET', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
def user_detail(request, user_id):
    """"""
    
    try:
        user = User.objects.get(id=user_id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializers(user)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)