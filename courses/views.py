from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import uuid
import json
from .forms import CourseForm

DB = settings.DB_FILE
from db import readDB, writeDB

class CourseView(View) :
    def get(self, request, *args, **kwargs) :
        AllCoursesData = readDB(filename=DB)
        return JsonResponse(data=AllCoursesData, status=200, safe=False) # 200 is OK

    def Creating_Course(self, name_of_course, description_of_course):
        Course_To_Post = {
            "id" : str(uuid.uuid1()),
            "name" : name_of_course,
            "description" : description_of_course,
        }
        return Course_To_Post

    def post(self, request, *args, **kwargs):
        AllCoursesData = readDB(filename=DB)
        Body = json.loads(request.body)
        Course_To_Post = self.Creating_Course(Body["name"], Body["description"])
        valitationState = CourseForm(Course_To_Post)
        if valitationState.is_valid():
            AllCoursesData.append(Course_To_Post)
            writeDB(AllCoursesData , filename=DB)
            return JsonResponse(data=Course_To_Post, status=201, safe=False) # 201 created
        else:
            return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity

class SingleCourseView(View) :
    def Search_Course_withId(self, courseId, coursesData):
        for courseIdx in range(len(coursesData)):
            if coursesData[courseIdx]["id"] == courseId:
                return courseIdx
        return -1

    def get(self, request, *args,  **kwargs):
        AllCoursesData = readDB(filename=DB)
        courseIdx = self.Search_Course_withId(kwargs["id"], AllCoursesData)
        Course = {} 
        CourseStatus = 404 # Not Found
        if courseIdx != -1:
            Course = AllCoursesData[courseIdx]
            CourseStatus = 302 # Found    
        return JsonResponse(data = Course, status = CourseStatus, safe=False)


    def Update_Course(self, courseIdx, courseName, courseDescrition, coursesData):
        coursesData[courseIdx]["name"] = courseName
        coursesData[courseIdx]["description"] = courseDescrition

    def put(self, request, *args, **kwargs):
        AllCoursesData = readDB(filename=DB)
        Body = json.loads(request.body)
        courseIdx = self.Search_Course_withId(
            kwargs["id"], AllCoursesData
            )
        Course = {}    
        courseStatues = 404 # Not Found 
        if courseIdx != -1:
            courseStatues = 200 # Ok
            valitationState = CourseForm(
                {"name": Body["name"], "description": Body["description"]}
            )
            if valitationState.is_valid():
                self.Update_Course(
                    courseIdx, Body["name"], Body["description"], AllCoursesData
                )
                Course = AllCoursesData[courseIdx]
                writeDB(AllCoursesData, filename=DB)
            else:
                return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity
        return JsonResponse(data=Course, status = courseStatues)


    def delete(self, request, *args, **kwargs):
        AllCoursesData = readDB(filename=DB)
        courseIdx = self.Search_Course_withId(kwargs["id"], AllCoursesData)
        courseStatues = 404 # Not Found
        if courseIdx != -1:
           AllCoursesData.pop(courseIdx)
           courseStatues = 200 # Ok
        writeDB(AllCoursesData, filename=DB)   
        return HttpResponse(status = courseStatues)        