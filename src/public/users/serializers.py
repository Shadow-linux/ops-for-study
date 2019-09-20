# coding: utf-8

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UsersAccount


class UsersRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        label='用户名(邮箱)',
        validators=[UniqueValidator(queryset=UsersAccount.objects.all(), message='用户已经存在')],
        help_text='str: 用户名',
        style={'input_type': 'email'}
    )
    password = serializers.CharField(required=True, label='密码', help_text='str: 密码', style={'input_type': 'password'})
    real_name = serializers.CharField(required=True, label='真实姓名', help_text='str: 真实姓名')
    position = serializers.CharField(required=True, help_text='str: 职位', label='职位')
    department = serializers.CharField(required=True, help_text='str: 部门', label='部门')
    mobile = serializers.CharField(required=True, help_text='str; 手机号')

    class Meta:
        model = UsersAccount
        fields = ('username', 'password', 'real_name', 'position', 'department', 'email', 'mobile')


class UsersLoginSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField(label="用户名", help_text="用户名", required=True)
    password = serializers.CharField(
        label="密码",
        style={'input_type': 'password'},
        required=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersAccount
        fields = ('id', 'username')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')


class UsersOperationsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    username = serializers.CharField(read_only=True, style={'input_type': 'email'})
    gid = serializers.IntegerField(write_only=True, help_text='int: 权限组ID')

    class Meta:
        model = UsersAccount
        fields = (
            'id',
            'username',
            'email',
            'real_name',
            'position',
            'department',
            'groups',
            'gid',
            'mobile',
            'is_staff',
            'is_superuser')


class UsersChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, help_text='密码')
    password_check = serializers.CharField(write_only=True, required=True, help_text='确认密码')

    def validate(self, attrs):
        password_check = attrs.get('password_check')
        password = attrs.get('password')

        if password != password_check:
            raise serializers.ValidationError(detail='两次的密码不一致')
        return attrs

    class Meta:
        model = UsersAccount
        fields = ('password', 'password_check')


class UsersAddSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        label='用户名(邮箱)',
        validators=[UniqueValidator(queryset=UsersAccount.objects.all(), message='用户已经存在')],
        help_text='str: 用户名',
        style={'input_type': 'email'}
    )
    password_check = serializers.CharField(write_only=True, help_text='确认密码')
    gid = serializers.IntegerField(write_only=True, help_text='int: 权限组ID')

    def validate(self, attrs):
        password_check = attrs.get('password_check')
        password = attrs.get('password')

        if password != password_check:
            raise serializers.ValidationError(detail='两次的密码不一致')
        return attrs

    class Meta:
        model = UsersAccount
        fields = ('username',
                  'email',
                  'password',
                  'password_check',
                  'position',
                  'real_name',
                  'department',
                  'position',
                  'is_staff',
                  'mobile',
                  'is_superuser',
                  'gid'
                  )


class UsersGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text='int: 用户组id')
    name = serializers.CharField(
        required=True,
        label='用户组',
        validators=[UniqueValidator(queryset=Group.objects.all(), message='用户组已经存在')],
        help_text='str: 用户组'
    )
    users = serializers.SerializerMethodField(
        help_text='关联 users 列表',
        method_name='return_users',
        read_only=True
    )
    def return_users(self, obj):
        return [ UserSerializer(user_obj).data for user_obj in obj.user_set.all()]

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')


class PersonalInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, help_text='str; 用户名')
    groups = GroupSerializer(many=True, read_only=True, help_text='str; 权限组')
    is_staff = serializers.BooleanField(read_only=True, help_text='int; 是否是员工')
    is_superuser = serializers.BooleanField(read_only=True, help_text='int; 是否是超级管理员')

    class Meta:
        model = UsersAccount
        fields = ('username', 'real_name', 'email', 'department', 'position', 'is_staff', 'is_superuser', 'groups')


class PersonalChangePasswordSerializer(serializers.ModelSerializer):
    origin_password = serializers.CharField(required=True, help_text='str; 原始密码')

    class Meta:
        model = UsersAccount
        fields = ('origin_password', 'password', 'groups')
