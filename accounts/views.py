from django.shortcuts import render
from django.shortcuts import redirect
import requests
from config.settings import SOCIAL_OUTH_CONFIG

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


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
    print(res.text)

    return Response(res.text)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])  # 로그인된 사용자만 접근 가능하도록 설정
# def update_user(request):
#     user = request.user
#     serializer = UserSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'User information updated successfully.'})
#     return Response(serializer.errors, status=400)

@api_view(['GET'])  # POST 요청으로 로그아웃 처리
@permission_classes([IsAuthenticated])  # 로그인된 사용자만 로그아웃 가능
def kakao_logout(request):
    def kakao_logout(request):

    access_token = request.query_params.get('access_token')  # 클라이언트에서 전달한 토큰
    
    if not access_token:
        return Response({'message': 'Access token is missing.'}, status=status.HTTP_400_BAD_REQUEST)
    
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        # 로그아웃 성공 처리
        return Response({'message': 'Kakao logout successful.'}, status=status.HTTP_200_OK)
    else:
        # 로그아웃 실패 처리
        return Response({'message': 'Kakao logout failed.'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def kakao_logout(request):
#     pass









#     # user = request.user
#     # url = "https://kapi.kakao.com/v1/user/logout"

#     # print(user)

#     # if user.kakao_id:
#     #     headers = {
#     #         "Authorization": f"Bearer {user.kakao_access_token}"
#     #     }
#     #     response = requests.post(url, headers=headers)

#     #     if response.status_code == status.HTTP_200_OK:
#     #         # 카카오 로그아웃 성공
#     #         user.kakao_id = None
#     #         user.kakao_access_token = None
#     #         user.save()
#     #         return Response({"detail": "Kakao logout successful."}, status=status.HTTP_200_OK)
#     #     else:
#     #         # 카카오 로그아웃 실패
#     #         return Response({"detail": "Failed to logout from Kakao."}, status=status.HTTP_400_BAD_REQUEST)
#     # else:
#     #     # 사용자가 카카오 로그인을 하지 않은 경우
#     #     return Response({"detail": "User is not logged in with Kakao."}, status=status.HTTP_400_BAD_REQUEST)