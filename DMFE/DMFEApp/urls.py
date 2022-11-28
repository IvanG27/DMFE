from django.urls import path
from DMFEApp import views

urlpatterns = [
    path('home.html', views.home, name="Home"),
    path('instructions.html', views.instructions, name="Instructions"),
    path('eda.html', views.eda, name="EDA"),
    path('pca.html', views.pca, name="PCA"),
]
