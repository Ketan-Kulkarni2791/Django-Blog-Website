from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog_home_url = reverse('blog-home')
        self.blog_about_url = reverse('blog-about')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.logout_url = reverse('logout')
        self.blog_post_detail_url = reverse('post-detail', kwargs={'pk': 1})
        self.blog_create_new_post_url = reverse('post-create')
        # User data to register.
        self.user = {
            'username': 'TestUser1',
            'email': 'TestUser@gmail.com',
            'password1': 'test@123',
            'password2': 'test@123'
        }
        # User data for login credentials
        self.user_login_credentials = {
            'username': 'TestUser1',
            'password': 'test@123'
        }

    def test_home_GET(self):
        response = self.client.get(self.blog_home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_about_GET(self):
        response = self.client.get(self.blog_about_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

    def test_post_detail_GET(self):
        response = self.client.get(self.blog_post_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_form_GET(self):
        response = self.client.get(self.blog_create_new_post_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_profile_GET(self):
        # Here we are creating a user to log in
        self.client.post(self.register_url, self.user, format='text/html')
        # Here we are making that user an active in database
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        # Here we are trying to log in with that user
        response = self.client.post(self.login_url, self.user_login_credentials, format='text/html')
        self.assertEqual(response.status_code, 302)
        # After login successfully, try to access profile page.
        response1 = self.client.get(self.profile_url)
        self.assertEquals(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'users/profile.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')







