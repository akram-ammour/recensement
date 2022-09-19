from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# add json area test
def jsontest(request):
    return render(request,"json.html",{})