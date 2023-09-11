from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import my_user
from .serializers import MyUserSerializer


#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")



class UserListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        
        users_list = my_user.objects.filter(user = request.user.id)
        serializer = MyUserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the user with given data
        '''
        

        if isinstance(request.data, list):

            obl_list = []


            for obj in request.data:
                obl_list.append(
                    {
                        'user': request.user.id,
                        'name': obj.get('name'), 
                        'salary': obj.get('salary'), 
                        'percentage': obj.get('percentage')
                    }
                )

            serializer = MyUserSerializer(data=obl_list, many=True)
        else:
            data = {
                'user': request.user.id,
                'name': request.data.get('name'), 
                'salary': request.data.get('salary'), 
                'percentage': request.data.get('percentage')
                }
            serializer = MyUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#############################################################

class UserSearchLikeApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. search all
    def get(self, request, *args, **kwargs):
        
        users_list = my_user.objects.filter(user = request.user.id,
                                            #name = request.data.get('name'),
                                            name__contains = request.data.get('name'))
        serializer = MyUserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

###########################################################

class UserSearchExactlyApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated] #application/json

    # 1. search all
    def get(self, request, *args, **kwargs):
        
        users_list = my_user.objects.filter(user = request.user.id, name = request.data.get('name'))
        serializer = MyUserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
############################################################


class uploadApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    parser_classes = (MultiPartParser, FormParser,)#multipart/form-data; boundary=<calculated when request is sent>

    # 2. Create
    def post(self, request, *args, **kwargs):

        if request.FILES['excel_file'] is None:
            return Response({"error": "No File Found"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        excel_file = request.data.get('excel_file')


        df = pd.read_excel(excel_file,names=["Name","Salery","percentage"])
        df['Name'].fillna("")
        df['Salery'].fillna(0)
        df['percentage'].fillna(0)


        obj_list = []
        for row_index in df.index:
            if df['Name'][row_index] != "":
                obj_list.append(
                    {
                        'user': request.user.id,
                        'name': df['Name'][row_index], 
                        'salary': df['Salery'][row_index], 
                        'percentage': df['percentage'][row_index]
                    }
                )
        serializer = MyUserSerializer(data=obj_list, many=True)
    

        if serializer.is_valid():
            serializer.save()
            return Response({"Response": "Success"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

####################################################################
'''

class UserListApiView2(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        
        print("--- name = "+str(request.data.get('Name')))
        users_model = user.objects.filter(Name__contains = request.data.get('Name'))
        serializer = UserSerializer(users_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        
        data = {
            'Name': request.data.get('Name'), 
            'salary': request.data.get('salary'), 
            'percentage': request.data.get('percentage')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    


class TodoDetailApiView(APIView):

    def get_object(self, user_name):
        
        try:
            return user.objects.get(Name=user_name)
        except user.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, user_name, *args, **kwargs):
        
        user_instance = self.get_object(user_name)
        if not user_instance:
            return Response(
                {"res": "Object with user name does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, user_name, *args, **kwargs):
        
        user_instance = self.get_object(user_name)
        if not user_instance:
            return Response(
                {"res": "Object with user name does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'Name': request.data.get('Name'), 
            'salary': request.data.get('salary'), 
            'percentage': request.data.get('percentage')
        }
        serializer = UserSerializer(instance = user_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, user_name, *args, **kwargs):
        
        user_instance = self.get_object(user_name)
        if not user_instance:
            return Response(
                {"res": "Object with user name does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        user_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )'''