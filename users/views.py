from django.views.generic import View
from django.http import JsonResponse
import json
from .forms import UserForm
from .models import User

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

    def Registering_User(self, Body):
        User_To_Resgiser = {
            "first_name" : Body["first_name"],
            "last_name" : Body["last_name"], 
            "birth_date" : Body["birth_date"],
            "user_email" : Body["user_email"], 
            "password" : Body["password"]   
        }
        return User_To_Resgiser

    def Create_User(self, Body) :
        return User(
            first_name = Body["first_name"],
            last_name = Body["last_name"],
            birth_date =  Body["birth_date"], 
            user_email = Body["user_email"],
            password = Body["password"]
        )

    def post(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        User_To_Register = self.Create_User(Body)
        New_User = self.Registering_User(Body)
        valitationState = UserForm(New_User)
        if valitationState.is_valid():
            User_To_Register.save()
            return JsonResponse({'User added' : New_User}, status = 200, safe = False) #Ok
        else:
            return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity

class SingleUserView(View) :
    def get(self, request, *args,  **kwargs):
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            return JsonResponse(Get_User, status = 302, safe = False) # Found 
        else:
            return JsonResponse(data = "User Not Found", status = 404, safe = False) # Not Found

    def delete(self, request, *args, **kwargs):
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            User.objects.filter(id=kwargs["id"]).delete()
            return JsonResponse(data = "User is deleted", status = 200, safe = False) # OK
        else :
            return JsonResponse(data = "User Not Found", status = 404, safe = False) # Not Found

    def Registering_User(self, Body):
        User_To_Resgiser = {
            "first_name" : Body["first_name"],
            "last_name" : Body["last_name"], 
            "birth_date" : Body["birth_date"],
            "user_email" : Body["user_email"], 
            "password" : Body["password"]   
        }
        return User_To_Resgiser

    def Update_User(self, Body, id) :
        return User.objects.filter(id=id).update(
            first_name = Body["first_name"],
            last_name = Body["last_name"],
            birth_date =  Body["birth_date"], 
            user_email = Body["user_email"],
            password = Body["password"]
        )

    def put(self, request, *args, **kwargs):
        Body = json.loads(request.body)
        Get_User = list(User.objects.filter(id=kwargs["id"]).values())
        if len(Get_User) != 0:
            # Validating user
            To_Validate_User = self.Registering_User(Body)
            valitationState = UserForm(To_Validate_User)
            if valitationState.is_valid():
                # Updating with body attributes
                self.Update_User(Body, kwargs["id"])
                return JsonResponse("User is Updated", status = 200, safe = False) # OK
            else:
                return JsonResponse(data = json.loads(valitationState.errors.as_json()), status = 422) # 422 Unprocessable Entity 

