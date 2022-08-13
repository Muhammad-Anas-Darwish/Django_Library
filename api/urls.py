from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # مؤلفين الكتب
    path('authors/', AuthorsView.as_view()),
    path('authors/<str:pk>/', AuthorView.as_view()),

    # الكتب
    path('books/', BooksView.as_view()),
    path('books/<str:pk>', BookView.as_view()),

    # الاستعارات
    path('metaphors/', MetaphorsView.as_view()),

    # الموظفين
    path('customers/', CustomersView.as_view()),
    path('customers/<str:pk>/', CustomerView.as_view()),

    # التصنيف
    path('categories/', CategoriesView.as_view()),
    path('categories/<str:pk>/', CategoryView.as_view()),

    # تسجيل الدخول والخروج
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', obtain_auth_token, name="obtain_auth_token"),

    #  الموظفين
    path('users/', UsersView.as_view(), name="users"),
    path('users/<str:pk>/', UserView.as_view(), name="users"),

    # مجموعات الموظفين
    path('groups/', GroupsView.as_view()),
    path('groups/<str:pk>/', GroupView.as_view()),
]
