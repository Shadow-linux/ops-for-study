# coding: utf-8


from rest_framework_jwt.settings import api_settings
# from rest_framework_jwt.utils import jwt_decode_handler

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


## 解析JWT
def parseJWT(token):
    # return token
    return (jwt_decode_handler(token.encode()))