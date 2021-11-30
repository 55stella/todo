from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import FutureSerializer, TodoSerializers
from .models import Todos
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone





@swagger_auto_schema(methods=['POST'], request_body=TodoSerializers())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def todo(request):
    if request.method == 'GET':
        objs = Todos.objects.filter(user=request.user)
        serializer = TodoSerializers(objs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer =  TodoSerializers(data=request.data)
        if serializer.is_valid():
            
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
                
            object = Todos.objects.create(**serializer.validated_data, user=request.user)#here we are using unpaking to create data. using key word arguments
            serializer = TodoSerializers(object)# this is converting the data to a querrry set so that we can store it in our databe
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        







@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=TodoSerializers())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
    """
    Takes in a student id and returns the http response depending on the http method.
    Args:
    student_id:integer


    Allowed methods:
    GET- get the detail of a single student
    PUT- allows students details to be edited
    DELETE: this logic deletes the students record from the database.
    """
    
    try:
        obj = Todos.objects.get(id = todo_id)# this would return a querry set.Not only a querry set, it would return the id of a particular user
    except Todos.DoesNotExist:
            error ={
                 "message": "failed",
                 "error":f"book with id{todo_id} does not exist"
            }
            return  Response(error, status=status.HTTP_400_BAD_REQUEST) 
    if obj.user != request.user:
     raise PermissionDenied(detail='You do not have permission to perform this action')

    if request.method == 'GET':
        serializer = TodoSerializers(obj)
        data = {
            "message":"sucess",
            "data":serializer.data
            #prepare the response
        }
        return Response(data, status= status.HTTP_200_OK)#send the response
    elif request.method =="PUT":
        serializer = TodoSerializers(obj, data = request.data, partial = True)#here we are trying to convert the querry set to jason by passing it into the erializer class
        

        if serializer.is_valid():
            
            
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
        obj.delete()
        return Response({"message":"success"}, status= status.HTTP_204_NO_CONTENT)

@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def mark_complete(request, todo_id):
   
    try:
        obj = Todos.objects.get(id = todo_id)
    
    except Todos.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user != request.user:#here we want to know if the user who is trying to access the todo is the one who created it. obj.user will give us the user who created this todo.#request.user will give us the user who is currently looged i                                             
        raise PermissionDenied(detail='You do not have permission to perform this action')
    
    
    if request.method == 'GET':
        if obj.completed == False:
            obj.completed=True
            obj.save()
                  
            data = {
                    'status'  : True,
                    'message' : "Successful"
                }

            return Response(data, status=status.HTTP_200_OK)
        else:
                  
            data = {
                    'status'  : False,
                    'message' : "Already marked complete"
                }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def today_list(request):
    if request.method == 'GET':
        today_date = timezone.now().date()
        objects = Todos.objects.filter(date=today_date, user=request.user)
        
        serializer = TodoSerializers(objects, many=True)
        data = {
            'status'  : True,
            'message' : "Successful",
            'data' : serializer.data,
        }

        return Response(data, status = status.HTTP_200_OK)




@swagger_auto_schema(method='post', request_body=FutureSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def future_list(request):
    if request.method == 'POST':
        serializer = FutureSerializer(data=request.data)#here the data that the user is entering is passing through a serializer
        if serializer.is_valid():
            objects = Todos.objects.filter(date=serializer.validated_data['date'], user=request.user)
            #it then filters where the date the user is entering is equals to the future date that a person entered when they were creating their todo in the todo model.
            #Serializer.validated_data['date'] means that it would filter where the data you entered in the post method serializer matches with the date in the todo model
            serializer = TodoSerializers(objects, many=True)# if it finds the data, it then passes it into the Todoserializer 
                  
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,#which the displays all the information contained in that todo model. ie. the todo written in that day
            }
            
               
            return Response(data, status = status.HTTP_200_OK)
        else:
            error = {
                'status'  : False,
                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(error, status = status.HTTP_200_OK)
















    # if request.method =="GET":
    #     Todo = Todos.objects.values_list('day',flat=True).distinct()#we wamt our data to be represemted in the dictionary
    #     # the dictinct function would selct a particular cohort of the same month instead of listing the entire cohort
    #     print(Todo)# what flat = true does is that it converts the value list into a list and removes the tuple. if you print cohort
    #     #without value list you will see list of tuple. but flat woould remove that. 

    #     data = {cohort:{
    #         # this code would loop throuh all the cohorts then select a particular
    #     #     #then selects all the students objects that registered in that same cohort. so it filters all the students 
    #     #     # then counts all the student that shares the same cohort.
    #          "data":Todos.objects.filter(day=cohort).values()}# this would return the values of all the student in that cohort
    #          for cohort in Todo
    #     }
    #     return Response(data, status= status.HTTP_200_OK)


    