"""
Django settings for ops project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import datetime
import pymysql
import configparser
import urllib3

# 关掉ssl warning
urllib3.disable_warnings()
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'private'))
sys.path.insert(0, os.path.join(BASE_DIR, 'public'))
sys.path.insert(0, BASE_DIR)

# 读取 deploy.conf
DEPLOY_CONF = configparser.ConfigParser()
DEPLOY_CONF.read(os.path.join(BASE_DIR, 'deploy.conf'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u)zall!ag&mci+ja5u&-6*1e^ufyu)l4i8+^=mw$845@k!ie+3.txt'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = True if DEPLOY_CONF.get('ops_backend', 'debug') == 'true' else False

ALLOWED_HOSTS = ['*']

# 重载User Model需要指定auth user model
AUTH_USER_MODEL = 'users.UsersAccount'

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'rest_framework',
    'users',
    'permission',
    'operation',
    'common',
    'message',
    'openapi',
    'apps',
    'cmdb.cloud',
    'cmdb.native',
    'cmdb.cmdb_common',
    'code_publish',
    'monitor',
    'activity.business',
]

MIDDLEWARE = [
    # 跨域请求
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 全局操作记录
    'operation.middleware.GlobalOperatingLogMiddleware',
    # 处理异常
    'operation.middleware.RequestExceptionMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'PATCH',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'pp'
)

ROOT_URLCONF = 'ops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, './templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ops.wsgi.application'
# src.ops.settings

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DEPLOY_CONF.get('mysql', 'schema'),
        'USER': DEPLOY_CONF.get('mysql', 'username'),
        "PORT": DEPLOY_CONF.get('mysql', 'port'),
        "PASSWORD": DEPLOY_CONF.get('mysql', 'password'),
        "HOST": DEPLOY_CONF.get('mysql', 'host')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 设置时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   # 默认是True, 时间是UTC时间,由于我们要用本地时间,所以要改为False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(name)s:%(lineno)d [%(levelname)s]: %(message)s'}
        # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, './log/error.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 1,
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, './log/ops.log'),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 1,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, './log/access.log'),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 1,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False
        },
        'ops': {
            'handlers': ['console', 'gunicorn', 'default'],
            'level': DEPLOY_CONF.get('ops_backend', 'log_level'),
            'propagate': False
        },
        'gunicorn.access': {
            'handlers': ['console', 'gunicorn'],
            'level': DEPLOY_CONF.get('ops_backend', 'log_level'),
        },
        'gunicorn.error': {
            'handlers': ['error'],
            'level': DEPLOY_CONF.get('ops_backend', 'log_level'),
        }

    }
}

# 计划任务
CRONTAB_COMMAND_SUFFIX = '>/dev/null 2>&1'
CRONJOBS = [
    # 业务它们的nginx access 监控
    ('*/1 * * * *', 'activity.business.cron.ngx_access_cron'),
    # 阿里云每半个小时更新状态
    ('*/30 * * * *', 'cmdb.cmdb_common.cron.aliyun_ecs_update_cron'),
    # 需要使用ansible更新 status
    ('*/30 * * * *', 'cmdb.cmdb_common.cron.ansible_host_update_status_cron'),
    # 更新阿里云RDS status
    ('*/60 * * * *', 'cmdb.cmdb_common.cron.aliyun_rds_update_cron'),
    # 第三方监控信息每一个小时更新状态，及监控图表信息
    ('*/60 * * * *', 'monitor.cron.monitor_third_party_cron'),
    # 删除发布数据
    ('0 0 * * *', 'code_publish.cron.delete_code_publish_record_cron'),
    # 释放发布环境锁
    ('*/1 * * * *', 'code_publish.cron.release_env_lock_cron'),
    # app alive collect
    ('59 23 * * *', 'common.cron.collect_app_alive_failed_point_cron'),
    # app alive brief statistics
    ('1 0 * * *', 'common.cron.category_app_alive_brief_cron'),
    # remain 7 days log
    ('2 0 * * *', 'message.cron.remain_7_days_log_cron'),
    ('2 0 * * *', 'operation.cron.remain_7_days_log_cron')
]


# 常量
CLONE_DIR = DEPLOY_CONF.get('ops_backend', 'clone_dir')