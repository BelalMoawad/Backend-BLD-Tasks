from django.views.generic import View
from django.http import JsonResponse 
import json
from .forms import CourseForm
from .models import Course


class CourseView(View) :
    
    def get(self, request, *args, **kwargs) :
        AllCoursesData = list(Course.objects.values())  # wrap in list(), because QuerySet is not JSON serializable
        return JsonResponse({'Courses' : AllCoursesData}, safe=False) 

    def Creating_Course(self, Body):
        Course_To_Post = {
            "name" : Body["name"],
            "description" : Body["description"],
        }
        return Course_To_Post

    def To_Save_Course(self, Body) :
        return Course(
            name = Body["name"],
            description = Body["description"]
        )

    def post(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Course_To_Post = self.To_Save_Course(Body)
        New_Course = self.Creating_Course(Body)
        valitationState = CourseForm(New_Course)
        if valitationState.is_valid():
            Course_To_Post.save()
            return JsonResponse(data = New_Course, status = 200) #Ok
        else:
            return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity

class SingleCourseView(View) :
    def get(self, request, *args,  **kwargs):
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            return JsonResponse(Get_Course, status = 302, safe = False)   
        else:
            return JsonResponse(data = "Course not found", status = 404, safe = False)

    def delete(self, request, *args, **kwargs):
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            Course.objects.filter(id=kwargs["id"]).delete()
            return JsonResponse(data = "Course is deleted", status = 200, safe = False)
        else :
            return JsonResponse(data = "Course not found", status = 404, safe = False)

    def Creating_Course(self, Body):
        Course_To_Post = {
            "name" : Body["name"],
            "description" : Body["description"],
        }
        return Course_To_Post

    def Updating_Course(self, Body, id) :
        return Course.objects.filter(id=id).update(
            name = Body["name"],
            description=Body["description"]
        )

    def put(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Get_Course = list(Course.objects.filter(id=kwargs["id"]).values())
        if len(Get_Course) != 0:
            # Validating course
            valitationState = CourseForm(self.Creating_Course(Body))
            if valitationState.is_valid():
                # Updating with body attributes
                self.Updating_Course(Body, kwargs["id"])
                return JsonResponse(data = "Course is Update", status = 200, safe = False)
            else:
                return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity                    