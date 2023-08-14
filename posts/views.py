from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Report
from .serializers import PostListRetrieveModelSerializer, PostCreateModelSerializer


# Create your views here.
# 단어 리스트보기
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListRetrieveModelSerializer

# 단어 총 개수 가져오기
class PostCountView(APIView):
    def get(self, request):
        post_count = Post.objects.all().count()
        return Response({'post_count': post_count}, status=status.HTTP_200_OK)

# 단어 상세보기
class PostRetrieveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListRetrieveModelSerializer

# 단어 생성하기
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateModelSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            Post.objects.get(word=request.data['word'])
            return Response({'result': 'Already Existed'})
        except Post.DoesNotExist:
            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            prev_post = Post.objects.latest('id')
            prev_id = prev_post.id
            next_id = Post.objects.only('id').earliest('id').id
        except Post.DoesNotExist:
            # 처음 단어 생성하는 경우
            prev_post = None
            prev_id = None
            next_id = None

        # 로그인 O
        # serializer.save(writer=request.user)
        
        # 로그인 X
        if request.user.is_authenticated:
            serializer.save(writer=request.user, prev_id=prev_id, next_id=next_id)
        else:
            serializer.save(prev_id=prev_id, next_id=next_id)

        # 처음/이전 단어 업데이트하기
        cur_post = Post.objects.only('id').latest('id')
        if prev_post:
            post_count = Post.objects.all().count()
            cur_id = cur_post.id

            # 처음 단어 업데이트하기
            first_post = Post.objects.earliest('id')
            first_post.prev_id = cur_id

            # 이전 단어 업데이트하기
            if post_count == 2:
                first_post.next_id = cur_id
            else:
                prev_post.next_id = cur_id
                prev_post.save()

            first_post.save()
        else:
            # 처음 단어 생성하는 경우
            cur_post.prev_id = cur_post.id
            cur_post.next_id = cur_post.id
            cur_post.save()

        # # 이전/다음 단어 업데이트하기
        # if prev_post:
        #     cur_id = Post.objects.only('id').latest('id').id

        #     # 처음 단어 업데이트하기
        #     first_post = Post.objects.earliest('id')
        #     first_post.prev_id = cur_id
        #     first_post.save()

        # if Post.objects.all().count() > 2:
        #     # 이전 단어 업데이트하기
        #     prev_post.next_id = cur_id
        #     prev_post.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# 단어 신고하기
class PostReportView(APIView):
    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset = Report.objects.filter(post=post)

        # 로그인 O
        # # 이미 신고한 사용자 → 신고 X
        # for query in queryset:
        #     if query.writer == request.user:
        #         return Response({'detail': 'Already Reported'}, status=status.HTTP_400_BAD_REQUEST)
        # # 신고
        # report = Report(post=post, writer=request.user)
        # report.save()

        # 로그인 X
        # 신고
        report = Report(post=post)
        report.save()

        # 신고 3번 → 단어 삭제
        if queryset.count() == 3:
            prev_id = post.prev_id
            next_id = post.next_id

            post.delete()

            # 이전/다음 단어 업데이트하기
            post_count = Post.objects.all().count()
            if post_count == 1:
                # 남은 단어 업데이트하기
                post = Post.objects.get()
                post.prev_id = post.id
                post.next_id = post.id
                post.save()
            elif post_count > 1:
                # 이전 단어 업데이트하기
                prev_post = Post.objects.get(id=prev_id)
                prev_post.next_id = next_id
                prev_post.save()
                
                # 다음 단어 업데이트하기
                next_post = Post.objects.get(id=next_id)
                next_post.prev_id = prev_id
                next_post.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_201_CREATED)