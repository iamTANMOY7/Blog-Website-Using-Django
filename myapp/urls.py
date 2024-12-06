from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="index"),
    path("blog",views.blog,name="blog"),
    path("signin",views.signin,name="signin"),
    path("signup",views.signup,name="signup"),
    path("logout",views.logout,name="logout"),
    path("create",views.create,name="create"),
    path("increaselikes/<int:id>",views.increaselikes,name='increaselikes'),
    path("profile",views.profile,name='profile'),
    path("profile/edit",views.profileedit,name='profileedit'),
    path("post/<int:id>",views.post,name="post"),
    path("post/comment/<int:id>",views.savecomment,name="savecomment"),
    path("post/comment/delete/<int:id>",views.deletecomment,name="deletecomment"),
    path("post/edit/<int:id>",views.editpost,name="editpost"),
    path("post/delete/<int:id>",views.deletepost,name="deletepost"),
    path("contact",views.contact_us,name="contact"),
    path("forget",views.forget,name="forget"),
    path("resetpassword/<str:token>",views.resetpassword,name="resetpassword"),
    path('category/<str:category_name>/', views.category, name='category'),
    path('toggle_status/<int:post_id>/', views.toggle_post_status, name='toggle_status'),
]
