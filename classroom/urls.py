from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.new, name="new"),
    path('logout', views.logout_view, name="logout"),
    path('join', views.join, name="join"),
    path('search', views.search, name='search'),
    path('login', views.login_view, name='login'),
    path('create', views.new_classroom, name='new_classroom'),
    path('class/<str:id>', views.class_view, name='class'),
    path('reset/<str:email>', views.reset_email),
    path('reset_password/<str:hash>', views.reset_view),
    path('work/<int:class_id>/<int:hw_id>', views.work, name="work"),
    # API
    path('api/user', views.get_user),
    path('api/create/<int:id>', views.create_assignment),
    path('api/leave/<int:id>', views.leave_or_delete)
   # path('/api/class', "")
]

