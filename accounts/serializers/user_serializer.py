'''
 .d8888b.  888          888               888      8888888                                         888             
d88P  Y88b 888          888               888        888                                           888             
888    888 888          888               888        888                                           888             
888        888  .d88b.  88888b.   8888b.  888        888   88888b.d88b.  88888b.   .d88b.  888d888 888888 .d8888b  
888  88888 888 d88""88b 888 "88b     "88b 888        888   888 "888 "88b 888 "88b d88""88b 888P"   888    88K      
888    888 888 888  888 888  888 .d888888 888        888   888  888  888 888  888 888  888 888     888    "Y8888b. 
Y88b  d88P 888 Y88..88P 888 d88P 888  888 888        888   888  888  888 888 d88P Y88..88P 888     Y88b.       X88 
 "Y8888P88 888  "Y88P"  88888P"  "Y888888 888      8888888 888  888  888 88888P"   "Y88P"  888      "Y888  88888P' 
                                                                         888                                       
                                                                         888                                       
                                                                         888                                       
'''    
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import Role, User
from commons import serializers as cserializers


'''
888     888  .d8888b.  8888888888 8888888b.        .d8888b.  8888888888 8888888b.  8888888        d8888 888      8888888 8888888888P 8888888888 8888888b.  
888     888 d88P  Y88b 888        888   Y88b      d88P  Y88b 888        888   Y88b   888         d88888 888        888         d88P  888        888   Y88b 
888     888 Y88b.      888        888    888      Y88b.      888        888    888   888        d88P888 888        888        d88P   888        888    888 
888     888  "Y888b.   8888888    888   d88P       "Y888b.   8888888    888   d88P   888       d88P 888 888        888       d88P    8888888    888   d88P 
888     888     "Y88b. 888        8888888P"           "Y88b. 888        8888888P"    888      d88P  888 888        888      d88P     888        8888888P"  
888     888       "888 888        888 T88b              "888 888        888 T88b     888     d88P   888 888        888     d88P      888        888 T88b   
Y88b. .d88P Y88b  d88P 888        888  T88b       Y88b  d88P 888        888  T88b    888    d8888888888 888        888    d88P       888        888  T88b  
 "Y88888P"   "Y8888P"  8888888888 888   T88b       "Y8888P"  8888888888 888   T88b 8888888 d88P     888 88888888 8888888 d8888888888 8888888888 888   T88b 
                                                                                                                                                                                                                                     
'''

class RoleField(serializers.Field):
    def to_representation(self, instance):
        ret = []
        # print(instance['email'])
        for value in instance.roles.all():
            # print(value)
            tmp = {
                "role_id": value.role_id,
                "role_name": value.get_id_display()
            }
            ret.append(tmp)
        return ret

    def to_internal_value(self, data):
        # print(list(data))
        data = data.strip('[').rstrip(']')
        roles = {'roles': [Role(role_id = int(val)) for val in data.split(',')]}
        return roles

class UserSerializer(cserializers.DynamicFieldsModelSerializer):
    roles = RoleField(source='*')
    
    class Meta:
        model = User
        fields = ('id', 'uuid', 'email', 'username', 'password', 'cell_phone', 'last_login', 'is_superuser', 'first_name', 'last_name',
                   'is_staff', 'is_active', 'date_joined', 'roles', 'popularity')
        read_only_fields = ('id', 'uuid','is_active','is_superuser','is_staff','date_joined', 'roles', 'popularity')
        extra_kwargs = {'password': {'write_only': True}, 'cell_phone': {'required': True}, 'username': {'required': False}}
        # exclude = ['uuid']

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        for role in roles:
            role.save()
            user.roles.add(role)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.cell_phone = validated_data.get('cell_phone', instance.cell_phone)
        # instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def get_excluder(self, obj):
        # return obj.id :Example
        return 'excluder'

    def get_exclud(self, obj):
        # return ''
        return 'exclud'
    
    def _includer():
        return '_includer'
