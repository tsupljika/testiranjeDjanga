from django.urls import path
from . import views

app_name='polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerView, name="register"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/report/', views.ReportView.as_view(), name='report'),
    path('<int:question_id>/pdfView/', views.pdfView, name='pdfView'),
]