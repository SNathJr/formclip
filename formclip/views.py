import os
import json
from datetime import datetime

from django.views import View
from django.middleware import csrf
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse

from .models import *

class IndexView(View):
    def get(self, request):
        return HttpResponse('Use post method to save your data!')

class SignupView(View):
    def post(self, request):
        # if they do not pass email id, give error
        if 'first_name' not in request.POST or 'last_name' not in request.POST:
            return JsonResponse({'success': False, 'message': 'first_name and last_name are required for signup!'}, status=400)
        # if they do not pass email id, give error
        if 'email' not in request.POST:
            return JsonResponse({'success': False, 'message': 'email id is required for signup!'}, status=400)
        # if they do not pass password, give error
        if 'password' not in request.POST:
            return JsonResponse({'success': False, 'message': 'password is required for signup!'}, status=400)
        # get data from request.post
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            # create an user and mark it as active
            user = User.objects.create_user(first_name = first_name, 
                                        last_name = last_name, 
                                        username = email,
                                        email = email,
                                        is_active = True)
            user.set_password(password)
            user.save()
        except:
            return JsonResponse(status=404, data={
                'success': False,'message':'Try again, email already used in another account.'
            })
        else:
            return JsonResponse({"success": True, "message": "Your account has been created!"})


class SigninView(View):
    def post(self, request):
        if request.user.is_authenticated:
            return JsonResponse({"success": True, "message": "You are already logged in!"})
        # if they do not pass email id, give error
        if 'email' not in request.POST:
            return JsonResponse({'success': False, 'message': 'email id is required for signing in!'}, status=400)
        # if they do not pass password, give error
        if 'password' not in request.POST:
            return JsonResponse({'success': False, 'message': 'password is required for signing in!'}, status=400)
        email = request.POST['email']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # log the user in
            login(request, user)
            return JsonResponse({"success": True, "message": "Logged in successfully!"})
        else:
            # try to find the user model
            user = User.objects.filter(username = email).first()
            # if the user exists
            if user:
                # and the user is active, password was incorrect
                if user.is_active:
                    return JsonResponse(
                        status=401, 
                        data={'success': False, 'message': 'Incorrect password, please try again.'}
                    )
                # otherwise, account is inactive
                else:
                    return JsonResponse(
                        status=401, 
                        data={'success': False, 'message':'Your account is inactive, please send us an email.'}
                    )
            # if user does not exist
            else:
                return JsonResponse(status=404, data={'success': False, 'message':'This account does not exist, please signup.'})

class SignoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({'success': True, 'message':'You have successfully signed out.'})

class FormSubmitView(View):
    def post(self, request, username):
        metaItemsToCatch = [
            'HTTP_HOST', 'HTTP_USER_AGENT', 'HTTP_ACCEPT_ENCODING', 
            'REMOTE_HOST', 'REMOTE_ADDR'
        ]
        print(request.META)
        user = User.objects.filter(username = username, is_active=True).first()
        if user:
            user_url = UserUrlMap.objects.filter(user=user, url=request.get_host()).first()
            if user_url:
                if user_url.is_active:
                    try:
                        DataStore.objects.create(
                            user=user,
                            url=user_url,
                            created_at=datetime.now(),
                            header_data=json.dumps({item: request.META[item] for item in metaItemsToCatch}), 
                            form_data=json.dumps(dict(request.POST))
                        )
                    except:
                        return JsonResponse(status=400, data={"success": False, "message": "Could not submit, try again!"})
                    else:
                        return JsonResponse({"success": True, "message": "Form submitted successfully!"})
                else:
                    return JsonResponse(
                        status=400, 
                        data={"success": False, "message": f"Form not submitted, you need to activate the originating domain {request.get_host()} first!"}
                    )
            else:
                UserUrlMap.objects.create(user=user, url=request.get_host())
                return JsonResponse(
                    status=400, 
                    data={"success": False, "message": f"Form not submitted, you need to verify the originating domain {request.get_host()} first!"}
                )
        else:
            return JsonResponse(
                status=403, 
                data={'success': False, 'message': 'This form is not active yet, signup or activate to submit data!'}
            )
