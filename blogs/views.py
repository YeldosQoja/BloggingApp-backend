from django.contrib.auth.models import User
from .models import Blog, Like, Comment
from .serializers import (
    UserSerializer,
    BlogSerializer,
    CommentSerializer,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def user_login(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed(
                "No active account found with the given credentials"
            )
        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    except (KeyError, AuthenticationFailed) as error:
        match error:
            case KeyError():
                return Response(
                    {"error": {"message": "Username or(and) password not provided!"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            case AuthenticationFailed():
                return Response(
                    {"error": {"message": error.detail}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class HomeBlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]


class BlogListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class BlogRetrieveView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]


class BlogUpdateView(generics.UpdateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)


class BlogDeleteView(generics.DestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)


class CommentCreateListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blog_id = self.kwargs["fk"]
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        blog_id = self.kwargs["fk"]
        if serializer.is_valid():
            serializer.save(author=self.request.user, blog_id=blog_id)
        else:
            print(serializer.errors)


class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def like_blog(request, fk):
    """
    Like a blog, or delete a like from a blog
    """
    if request.method == "POST":
        like = Like.objects.get_or_create(user=request.user, blog_id=fk)
        return Response(status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        like = get_object_or_404(Like, user=request.user, blog_id=fk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def user_list(request):
    """
    List all users, or create a new user
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT"])
def user_detail(request, pk):
    """
    Retrieve, update, delete a user
    """
    user = get_object_or_404(User, pk=pk)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
