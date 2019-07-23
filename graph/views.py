from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .form import UploadFileForm
from .handle_uploaded_file import from_csv_to_db

def graph_analyze(request):
    template_name = 'graph/graph_analyze.html'
    context = {}
    return render(request, template_name, context)

def graph_rtcm(request):
    template_name = 'graph/graph_rtcm.html'
    context = {}
    return render(request, template_name, context)

def upload_file(request):
    print("test")
    template_name = 'graph/upload.html'
    title = 'Upload'
    message = 'Upload a csv forecasting file'
    if request.method == 'POST':
        print("test2")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("test3")
            from_csv_to_db(request.FILES['file'])
            message = 'You successfuly uploaded the db'
            form = UploadFileForm()
    else:
        print("test4")
        form = UploadFileForm()
    context = {'form':form, 'message':message, 'title':title}
    return render(request, template_name, context)