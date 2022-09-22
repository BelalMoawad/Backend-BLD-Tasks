import imp
import re
from django.http import JsonResponse
from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from courses import serializers 
#get all the courses
#serialize them
#return json

@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        Courses = Course.objects.all()
        serializer = CourseSerializer(Courses, many = True)
        return Response( serializer.data) 

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)   



@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, id):
    try: 
       course =  Course.objects.get(pk=id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
