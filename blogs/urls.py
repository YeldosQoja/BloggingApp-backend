from django.urls import path
from blogs import views

app_name = "blogs"

urlpatterns = [
    path("home/", views.HomeBlogListView.as_view(), name="home"),
    path("<int:pk>/", views.BlogRetrieveView.as_view(), name="blog"),
    path("", views.BlogListCreateView.as_view(), name="blog-list"),
    path("update/<int:pk>/", views.BlogUpdateView.as_view(), name="update-blog"),
    path("delete/<int:pk>/", views.BlogDeleteView.as_view(), name="delete-blog"),
    path("<int:fk>/like/", views.like_blog, name="like-blog"),
    path("<int:fk>/comments/", views.CommentCreateListView.as_view(), name="comment-list"),
    path("comments/delete/<int:pk>/", views.CommentDeleteView.as_view(), name="delete-comment"),
]