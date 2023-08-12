from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
import requests
from config.settings import SOCIAL_OUTH_CONFIG

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView

from django.contrib.auth import logout

from .models import KakaoUser
from .serializers import KaKaoUserSerializer
from rest_framework import generics

import json

class KakaoUserCreateView(generics.CreateAPIView):
    queryset = KakaoUser.objects.all()
    serializer_class = KaKaoUserSerializer

class KakaoUserListView(ListAPIView):
    queryset = KakaoUser.objects.all()
    serializer_class = KaKaoUserSerializer

kakao_id = ["0",]

@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakao_get_login(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRECT_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRECT_URL)
    res = redirect(url)
    print(res)
    return res

@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_user_info(request):
    CODE = request.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
        'grant_type': 'authorization_code',
        'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
        'code': CODE
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    token_json = response.json()
    user_url = "https://kapi.kakao.com/v2/user/me"
    auth = "Bearer " + token_json['access_token']
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(user_url, headers=HEADER)
    print(response.json())

    print(response)
    print("내용",res.text)

    # json 추출

    response_text = res.text
    response_data = json.loads(response_text)

    kakao_id[0] = response_data["id"]
    nickname = response_data["properties"]["nickname"]

    print("kakao_id : ", kakao_id[0])
    print(nickname)

    # Serialized
    kakao_user_data = {
        'kakao_id': kakao_id[0],
        'nickname': nickname,
        'post_count': 0  # 예시로 초기값 설정
    }
    
    # Create an instance of HttpRequest and set the method to POST
    
    serializer = KaKaoUserSerializer(data=kakao_user_data)

    if serializer.is_valid():
        serializer.save()
        print("Add Data")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("error")
    
    
    return Response(res.text)

#@api_view(['POST'])
#@permission_classes([IsAuthenticated, ])
def kakao_logout(request):
    print(kakao_id[0])
    
    kakao_admin_key = SOCIAL_OUTH_CONFIG['KAKAO_ADMIN_KEY']
    logout_url = "https://kapi.kakao.com/v1/user/logout"
    target_id = kakao_id[0]

    print(target_id)

    target_id = int(target_id)
    headers = {"Authorization": f"KakaoAK {kakao_admin_key}"}
    data = {"target_id_type": "user_id", "target_id": target_id}
    logout_res = requests.post(
        logout_url, headers=headers, data=data
    ).json()
    response = logout_res.get("id")
    if target_id != response:
        return Exception("Kakao Logout failed")
    else:
        print(str(response) + "Kakao Logout successed")
       
    logout(request)
    return redirect("/accounts/kakao/logout_with_kakao/")

def logout_with_kakao(request):
    """
    카카오톡과 함께 로그아웃 처리
    """
    kakao_rest_api_key = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    logout_redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_LOGOUT_REDIRECT_URI']
    state = "none"
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"

    print("kakao Logout")

    print(kakao_id[0])

    return redirect(
        f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}"
    )