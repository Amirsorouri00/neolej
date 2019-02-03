from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import Role, User
from commons import serializers as cserializers


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
        instance.id = validated_data.get('id', instance.id)
        # instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.username = validated_data.get('email', instance.email)
        instance.set_password(validated_data['password'])
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
