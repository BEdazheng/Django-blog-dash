from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import BlogPostModelForm
from .models import BlogPost
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def blog_post_list_view(request):
    #list out objects
    #could be search view qs = BlogPost.objects.filter(title__contains='hello')
    qs = BlogPost.objects.all() #published()
    title = 'Lists of blog posts'
    template_name = 'blog/list.html'
    context = {'object_list' : qs, 'title' : title}
    return render(request, template_name, context)

@staff_member_required
def blog_post_create_view(request):
    #create objects using forms
    form = BlogPostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False) #Allows us to alter the data before saving
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name = 'blog/form.html'
    title = 'Create new Blog Post'
    context = {'form' : form, 'title':title}
    return render(request, template_name, context)

def blog_post_detail_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {'object' : obj}
    return render(request, template_name, context) 

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(f"/blog/{obj.slug}")
    template_name = 'blog/form.html'
    context = {'form': form, 'title': f"Update '{obj.title}'"}
    return render(request, template_name, context) 

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {'objec' : obj}
    return render(request, template_name, context)  

