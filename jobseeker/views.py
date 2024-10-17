from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,TemplateView,DetailView,UpdateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages

from jobseeker.forms import RegistrationForm,ProfileForm
from myapp.models import StudentPofile,Jobs,Applications,Category

# Create your views here.


def signinrequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Signin required")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


dex=[signinrequired,never_cache]





class SignUpView(CreateView):
    
    template_name="jobseeker/register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")


@method_decorator(dex,name="dispatch")
class StudentIndexView(ListView):

    template_name="jobseeker/index.html"
    context_object_name="data"
    model=Jobs

    def get_queryset(self):
        my_applications=Applications.objects.filter(student=self.request.user).values_list("job",flat=True)
        qs=Jobs.objects.exclude(id__in=my_applications).order_by("-created_date")
        # localhost:8000/seeker/index?category=frontend
        if "category" in self.request.GET:
            category_value=self.request.GET.get("category")
            print(category_value)
            qs=qs.filter(category__name=category_value)
        return qs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        qs=Category.objects.all()
        context["categories"]=qs
        return context


@method_decorator(dex,name="dispatch")
class ProfileCreateView(CreateView):

    template_name="jobseeker/profile_add.html"
    form_class=ProfileForm
    success_url=reverse_lazy("seeker-index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    

@method_decorator(dex,name="dispatch")
class ProfileDetailView(DetailView):

    template_name="jobseeker/profile_detail.html"
    context_object_name="data"
    model=StudentPofile


@method_decorator(dex,name="dispatch")
class ProfileEditView(UpdateView):
    
    template_name="jobseeker/profile_edit.html"
    form_class=ProfileForm
    model=StudentPofile
    success_url=reverse_lazy("seeker-index")


@method_decorator(dex,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


# class JobListView(ListView):

#     template_name="jobseeker/job_list.html"
#     context_object_name="jobs"
#     model=Jobs


# localhost:8000/seeker/jobs/<int:pk>/
class JobDetailView(DetailView):

    template_name="jobseeker/job_detail.html"
    model=Jobs
    context_object_name="data"


class ApplyJobView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        sudent_object=request.user
        Applications.objects.create(job=job_object,student=sudent_object)
        return redirect("seeker-index")


class ApplicationListView(ListView):

    template_name="jobseeker/applications.html"
    model=Applications
    context_object_name="data"

    def get_queryset(self):
        qs=Applications.objects.filter(student=self.request.user)
        return qs
    

class JobSaveView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        action=request.POST.get("action")
        if action=="save":
            request.user.profile.saved_jobs.add(job_object)
        elif action=="unsave":
            request.user.profile.saved_jobs.remove(job_object)
        return redirect("seeker-index")


class SavedJobListView(View):
    
    template_name="jobseeker/saved_jobs.html"
    
    def get(self,request,*args,**kwargs):
        qs=request.user.profile.saved_jobs.all()
        return render(request,self.template_name,{"data":qs})


