from django.urls import path
from .import views
urlpatterns = [
    


    path('todo/<int:todo_id>', views.todo_detail),
    path('todo/', views.todo),
    path('todo/mark_complete/<int:todo_id>', views.mark_complete),
    path('todo/today', views.today_list),
    path('todo/future', views.future_list)
    
]