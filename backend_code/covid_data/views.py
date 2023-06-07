from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions,generics,views
from django.contrib.auth import login,logout
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json

# Create your views here.
class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

@csrf_exempt
def covid_data_api(request,date1=''):
    if request.method == "GET" and request.user.is_authenticated:
        with open('./Pakistan.json') as file:
            json_obj = json.load(file)
        return JsonResponse(json_obj,safe=False)

    elif request.method == "POST"and request.user.is_authenticated:
        new_data = JSONParser().parse(request)
        with open('./Pakistan.json','r+') as file:
            file_data = json.load(file)
            file_data.append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
        return JsonResponse("Added Data Successfully!",safe=False)

    elif request.method == "PUT" and request.user.is_authenticated:
        new_data = JSONParser().parse(request)
        obj  = json.load(open("./Pakistan.json"))                                       
        for i in range(len(obj)):
            if obj[i]["date"] == date1:
                obj[i]["location"] = new_data['location']
                obj[i]["vaccine"] = new_data['vaccine']
                obj[i]["source_url"] = new_data['source_url']
                obj[i]["total_vaccinations"] = new_data['total_vaccinations']
                obj[i]["people_vaccinated"] = new_data['people_vaccinated']
                obj[i]["people_fully_vaccinated"] = new_data['people_fully_vaccinated']
                obj[i]["total_boosters"] = new_data['total_boosters']
                obj[i]["people_partly_vaccinated"] = new_data['people_partly_vaccinated']
                break                               
        open("./Pakistan.json", "w").write(
            json.dumps(obj, indent=4, separators=(',', ': '))
        )
        return JsonResponse("Editted Data Successfully!",safe=False)

    elif request.method == "DELETE" and request.user.is_authenticated:  
        obj  = json.load(open("./Pakistan.json"))                                       
        for i in range(len(obj)):
            if obj[i]["date"] == date1:
                obj.pop(i)
                break                               
        open("./Pakistan.json", "w").write(
            json.dumps(obj, indent=4, separators=(',', ': '))
        )
        return JsonResponse("Deleted Data Successfully!",safe=False)

    else:
        return JsonResponse("Invalid Request!",safe=False)