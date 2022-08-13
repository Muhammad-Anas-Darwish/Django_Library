from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from api.permissions import EmployeePermissions
from api.serializers import *
from .models import *
# from base.views import book

# المؤلفين
class AuthorsView(generics.ListCreateAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# المؤلف
class AuthorView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    # من اجل تصفية المؤلفين
    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['pk']
        )

    # تحديث المؤلف
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    
    # حذف المؤلف
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# الكتب
class BooksView(generics.ListCreateAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookSerializer
        return BooksSerializer

# كتاب
class BookView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    # البحث عن المستخدم
    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])
    # تعديل بياناتت الكتاب
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.serializer_class = BookSerializer
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    # حذف الكتاب
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# الاستعارات
class MetaphorsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Metaphor.objects.all()

    # تحديد الحقول
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MetaphorSerializer
        return MetaphorsSerializer

    # استعارة أو إرجاع الاستعارة
    def perform_create(self, serializer):
        if serializer.validated_data.get('event') == 'metaphor':
            book = Book.objects.get(id=serializer.validated_data.get('book').id)
            if book.number_of_borrowed_books >= book.number_of_books:
                return Response({"message": "failed", "details": "No books available!"})
        else:
            metaphor = Metaphor.objects.filter(
                book=serializer.validated_data.get('book'),
                customer=serializer.validated_data.get('customer'),
                borrowed=True,
                )[0]
            if metaphor:
                metaphor.borrowed = False
                metaphor.save()
            else:
                return Response({"message": "failed", "details": "This book has not been borrowed"})

        serializer.save(employee=self.request.user)

# الزبائن
class CustomersView(generics.ListCreateAPIView):
    permission_classes = [EmployeePermissions]
    serializer_class = CustomersSerializer
    queryset = Customer.objects.all()

# الزبون
class CustomerView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Customer.objects.all()
    serializer_class = CustomersSerializer

    # البحث عن الزيون
    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])
    # تعديل الزبون
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    # حذف الزبون
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# التصنيفات
class CategoriesView(generics.ListCreateAPIView):
    permission_classes = [EmployeePermissions]
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()

# التصنيف
class CategoryView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [EmployeePermissions]
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# تسجيل خروج
class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# المستخدمين
class UsersView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer

# المستخدم
class UserView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        return super().get_queryset().filter(username=self.kwargs['pk'])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# المجموعات
class GroupsView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

# المجموعة
class GroupView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
    def delete(self,request,*args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)