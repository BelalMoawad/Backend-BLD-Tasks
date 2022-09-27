from telnetlib import STATUS
from unicodedata import name
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import uuid
import json
from .forms import CourseForm,UserForm
from .models import Course, User


class CourseView(View) :
    
    def get(self, request, *args, **kwargs) :
        AllCoursesData = list(Course.objects.values())  # wrap in list(), because QuerySet is not JSON serializable
        return JsonResponse({'Courses' : AllCoursesData}, safe=False)  # JsonResponse(data)

    def Creating_Course(self, name_of_course, description_of_course):
        Course_To_Post = {
            "name" : name_of_course,
            "description" : description_of_course,
        }
        return Course_To_Post

    def post(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Course_To_Post = Course(name = Body["name"], description = Body["description"])
        New_Course = self.Creating_Course(Body["name"], Body["description"])
        valitationState = CourseForm(New_Course)
        if valitationState.is_valid():
            Course_To_Post.save()
            return HttpResponse(status = 200) #Ok
        else:
            return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity

class SingleCourseView(View) :
    def get(self, request, *args,  **kwargs):
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            return JsonResponse(Get_Course, status = 302, safe = False)   
        else:
            return HttpResponse(status = 404)

    def delete(self, request, *args, **kwargs):
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            Course.objects.filter(id=kwargs["id"]).delete()
            return HttpResponse(status = 200)
        else :
            return HttpResponse(status = 404)

    def Creating_Course(self, name_of_course, description_of_course):
        Course_To_Validate = {
            "name" : name_of_course,
            "description" : description_of_course,
        }
        return Course_To_Validate

    def put(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            # Validating course
            To_Validate_Course = self.Creating_Course(Body["name"], Body["description"])
            valitationState = CourseForm(To_Validate_Course)
            if valitationState.is_valid():
                pass # Updating with body attributes
                Course.objects.filter(id=kwargs["id"]).update(name = Body["name"], description=Body["description"])
                return HttpResponse(status = 200)
            else:
                return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity    

class UserQueriesView(View) :
    def get(self, request, *args, **kwargs) :
        AllUsers = User.objects.all()
        AllUsersList = list(User.objects.values())
        Body = json.loads(request.body)
        UsersGreatherThanCertainAge = []
        UserIndex = 0 
        for SingleUser in AllUsers:
            if SingleUser.age > int (Body["age"]) :
                UsersGreatherThanCertainAge.append(AllUsersList[UserIndex])
                print(SingleUser.password)
            UserIndex += 1
        return JsonResponse({'Filtered Users' : UsersGreatherThanCertainAge}, status = 200, safe = False)    

class UserView(View) :
    def get(self, request, *args, **kwargs) :
        AllUsersData = list(User.objects.values())  # wrap in list(), because QuerySet is not JSON serializable
        return JsonResponse({'Users' : AllUsersData}, safe=False)  # JsonResponse(data)

    def Registering_User(self, firstName, lastName, birthDate, userEmail, Password):
        User_To_Resgiser = {
            "first_name" : firstName,
            "last_name" : lastName, 
            "birth_date" : birthDate,
            "user_email" : userEmail, 
            "password" : Password
        }
        return User_To_Resgiser

    def post(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        User_To_Register = User(
            first_name = Body["first_name"], last_name = Body["last_name"],birth_date =  Body["birth_date"], 
            user_email = Body["user_email"], password = Body["password"]
        )
        New_User = self.Registering_User(
            Body["first_name"], Body["last_name"], Body["birth_date"], Body["user_email"], Body["password"]
        )
        valitationState = UserForm(New_User)
        if valitationState.is_valid():
            User_To_Register.save()
            return HttpResponse(status = 200) #Ok
        else:
            return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity

class SingleUserView(View) :
    def get(self, request, *args,  **kwargs):
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            return JsonResponse(Get_User, status = 302, safe = False)  
        else:
            return HttpResponse(status = 404)

    def delete(self, request, *args, **kwargs):
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            User.objects.filter(id=kwargs["id"]).delete()
            return HttpResponse(status = 200)
        else :
            return HttpResponse(status = 404)

    def Registering_User(self, firstName, lastName, birthDate, userEmail, Password):
        User_To_Resgiser = {
            "first_name" : firstName,
            "last_name" : lastName, 
            "birth_date" : birthDate,
            "user_email" : userEmail, 
            "password" : Password
        }
        return User_To_Resgiser

    def put(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            # Validating user
            To_Validate_User = self.Registering_User(
                Body["first_name"], Body["last_name"], Body["birth_date"], Body["user_email"], Body["password"]
            )
            valitationState = UserForm(To_Validate_User)
            if valitationState.is_valid():
                # Updating with body attributes
                User.objects.filter(id=kwargs["id"]).update(
                    first_name = Body["first_name"], last_name = Body["last_name"],birth_date =  Body["birth_date"], 
                    user_email = Body["user_email"], password = Body["password"]
                )
                return HttpResponse(status = 200) # OK
            else:
                return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity 


                       