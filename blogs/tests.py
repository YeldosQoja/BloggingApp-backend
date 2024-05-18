from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

client = Client()


def register_user(username, password):
    response = client.post(
        reverse("register-user"), {"username": username, "password": password}
    )
    return response


def register_user_and_get_access_token(username, password):
    register_user_response = register_user(username, password)
    response = client.post(
        reverse("token"), {"username": username, "password": password}
    )
    return (response.data["access"], register_user_response)


def create_blog(access_token, data):
    response = client.post(
        reverse("blogs:blog-list"),
        data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response.data


# Create your tests here.
class CreateUserViewTests(TestCase):
    def test_register_user(self):
        response = register_user("Tester", "test123")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BlogListCreateViewTests(TestCase):
    def test_no_blog(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        response = self.client.get(
            reverse("blogs:blog-list"),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_blog_list_with_blog(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        response = self.client.get(
            reverse("blogs:blog-list"),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.data, [blog])

    def test_blog_list_with_two_blogs(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        blog2 = create_blog(
            access_token,
            {
                "title": "Test blog 2",
                "content": "Content text 2",
                "tagline": "one two three",
            },
        )
        response = self.client.get(
            reverse("blogs:blog-list"),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.data, [blog, blog2])


class BlogRetrieveViewTestCase(TestCase):
    def test_get_blog(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        response = self.client.get(
            reverse("blogs:blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, blog)


class BlogDeleteViewTests(TestCase):
    def test_delete_blog(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        response = self.client.delete(
            reverse("blogs:delete-blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(
            reverse("blogs:blog-list"),
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.data, [])


class BlogLikeViewTests(TestCase):
    def test_increment_num_likes(self):
        # Create a user
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        # Create a blog
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        # Create an another user
        access_token_2, user_response = register_user_and_get_access_token(
            "User", "user123"
        )
        # Like a blog with the new user created by the first user
        response = self.client.post(
            reverse("blogs:like-blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Get the liked blog
        response = self.client.get(
            reverse("blogs:blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        self.assertEqual(response.data["num_likes"], 1)

    def test_decrement_num_likes(self):
        # Create a user
        access_token_1, user_response_1 = register_user_and_get_access_token(
            "Tester", "test123"
        )
        # Create a blog
        blog = create_blog(
            access_token_1,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        # Create an another user
        access_token_2, user_response_2 = register_user_and_get_access_token(
            "User", "user123"
        )
        # Like a blog with the first user created by the first user
        response = self.client.post(
            reverse("blogs:like-blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        # Like a blog with the new user created by the first user
        response = self.client.post(
            reverse("blogs:like-blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        # Delete a like by the second user
        response = self.client.delete(
            reverse("blogs:like-blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Get the liked blog
        response = self.client.get(
            reverse("blogs:blog", args=(blog["id"],)),
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        self.assertEqual(response.data["num_likes"], 1)


class CommentCreateDeleteTests(TestCase):
    def test_create_comment(self):
        access_token, user_response = register_user_and_get_access_token(
            "Tester", "test123"
        )
        blog = create_blog(
            access_token,
            {
                "title": "Test blog",
                "content": "Content text",
                "tagline": "blog python django",
            },
        )
        response = self.client.post(
            reverse("blogs:comment-list", args=(blog["id"],)),
            {"text": "Comment text"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        comments = Comment.objects.filter(blog=blog["id"]).all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, [response.data])
