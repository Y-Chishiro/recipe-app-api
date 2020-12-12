from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successfull"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # このresの中身は、
        # res.status_code
        # res.data←ほぼpayloadの内容

        # 何を期待するか？というと、
        # まずは201ステータスコード。リクエストが成功してリソースが生成されたことを返す。
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # 本当にオブジェクトが生成されたか確認する
        user = get_user_model().objects.get(**res.data)

        # パスワードが正しいか確認する。
        self.assertTrue(user.check_password(payload['password']))

        # パスワードがデータの中に入っていないことを確認する
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test',
        }
        create_user(**payload)  # 先に、内部的にユーザ生成しておく。

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'pw',
            'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test'
        }
        create_user(**payload)

        # TOKEN_URLにメールアドレスとパスワードを投げる
        # 成功すれば200コードと、Tokenが含まれたValueがresponseに入っている。
        res = self.client.post(TOKEN_URL, payload)

        # Tokenがデータに入っているかチェックする。
        self.assertIn('token', res.data)
        # ステータスコードをチェックする
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'wrong',
            'name': 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        # 存在しないユーザのTokenを取得しようとしたときもエラーを出すように。
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
