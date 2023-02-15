from django.urls import path, include
from .views import CategoryView, TagView


urlpatterns = [
    path('categories/', CategoryView.as_view({'get': 'list'}), name='category'),
    path('categories/<int:pk>/', CategoryView.as_view({'get':'retrieve',
                                                       'put':'update', 
                                                       'patch':'partial_update',
                                                       'delete':'destroy'}), name='category'),
    path('tags/', TagView.as_view({'get':'list'}), name='tags'),
    path('tags/<int:pk>/', TagView.as_view({'get':'retrieve','put':'update',
                                   'patch':'partial_update','delete':'destroy'}), name='tags'),
]