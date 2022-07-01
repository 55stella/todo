from django.db.models import fields
from rest_framework import serializers
from account.models import CustomUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","email","date_joined","username","address","password","is_active","id"]
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300)
    password = serializers.CharField(max_length=200)


class ChangePasswordSerializer(serializers.Serializer):
      old_password = serializers.CharField(max_length=500)#here we are creating serializers from scratch. these serializers doesnt have a model that it comes with.
      new_password = serializers.CharField(max_length=500)
      re_password = serializers.CharField(max_length=500)



    # def password_validate(self):
     #     if self.initial_data['new_password'] != self.initial_data['re_password']:
     #         raise serializers.ValidationError("Please enter matching passwords")
     #     return True


      def validate_new_password(self, value):
         if value != self.initial_data['re_password']:#initial data isa data that has not been validated
             raise serializers.ValidationError("Please enter matching passwords")
         return value
