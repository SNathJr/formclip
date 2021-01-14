import os
import json

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
    
    def post(self, request):
        try:
            DataStore.objects.create(
                header_data=json.dumps(dict(request.META)), 
                form_data=json.dumps(dict(request.POST))
            )
        except:
            return JsonResponse({"success": False})
        else:
            return JsonResponse({"success": True})
