from django.urls import path

from jobseeker import views
urlpatterns = [

    path("register/",views.SignUpView.as_view(),name="signup"),
    path("index",views.StudentIndexView.as_view(),name="seeker-index"),
    path("profile/add",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile/<int:pk>/",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:pk>/change",views.ProfileEditView.as_view(),name="profile-edit"),
    path("signout/",views.SignOutView.as_view(),name="signout"),
    path("jobs/<int:pk>",views.JobDetailView.as_view(),name="job-detail"),
    path("jobs/<int:pk>/apply",views.ApplyJobView.as_view(),name="job-apply"),
    path("application/all",views.ApplicationListView.as_view(),name="my-applications"),
    path("jobs/<int:pk>/save",views.JobSaveView.as_view(),name="job-save"),
    path("jobs/saved/all",views.SavedJobListView.as_view(),name="saved-jobs"),
    

]