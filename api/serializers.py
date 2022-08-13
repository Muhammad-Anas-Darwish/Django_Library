from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import *
import uuid

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

# امكانية رؤية  الكتب
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# امكانية تعديل او اضافة كتب
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['metaphors', 'number_of_borrowed_books']

class MetaphorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metaphor
        fields = '__all__'

class MetaphorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metaphor
        exclude = ['employee', 'borrowed']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        # exclude = ['groups', 'user_permissions']
        exclude = ['user_permissions']
    
    def create(self, validated_data):
        validated_data['username'] = str(uuid.uuid4())
        return MyUser.objects.create_user(**validated_data)

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
