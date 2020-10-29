from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import UploadFile
from django.views.generic import View 
from django.urls import reverse_lazy

from .models import UserFile
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class FileUploadView(LoginRequiredMixin,View):
    form_class = UploadFile
    success_url = reverse_lazy('index')
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        key_word = request.GET.get('search',None)

        if key_word:
            files = UserFile.objects.filter(
            (Q(content_key_words__contains=key_word)|
            Q(file__contains=key_word)), user=user)
        else:
            files = UserFile.objects.filter(user=user)
        return render(request, self.template_name, {'files' :files})

    def post(self, request, *args, **kwargs):
        user = request.user
        if 'upload' in request.POST:
            UserFile.objects.create(user=user,file=request.FILES['file'])
            return redirect(self.success_url)
        else:
            return render(request, self.template_name)
