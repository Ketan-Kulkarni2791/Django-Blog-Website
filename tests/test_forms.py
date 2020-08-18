from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# To test Register and login form
class TestForms(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.home_url = reverse('blog-home')
        self.logout_url = reverse('logout')
        self.create_new_post_url = reverse('post-create')
        self.blog_post_detail_url = reverse('post-detail', kwargs={'pk': 1})
        self.blog_post_update_url = reverse('post-update', kwargs={'pk': 1})
        # User data to register.
        self.user = {
            'username': 'TestUser1',
            'email': 'TestUser@gmail.com',
            'password1': 'test@123',
            'password2': 'test@123'
        }
        # User data with short length password
        self.user_with_short_password = {
            'username': 'TestUser2',
            'email': 'TestUser@gmail.com',
            'password1': 'tes',
            'password2': 'tes'
        }
        # User data with mismatched length password
        self.user_with_mismatched_password = {
            'username': 'TestUser2',
            'email': 'TestUser@gmail.com',
            'password1': 'test',
            'password2': 'tes'
        }
        # User data with invalid email
        self.user_with_invalid_email = {
            'username': 'TestUser2',
            'email': 'TestUser-gmail.com',
            'password1': 'test',
            'password2': 'tes'
        }
        # User data for login credentials
        self.user_login_credentials = {
            'username': 'TestUser1',
            'password': 'test@123'
        }
        # Data for new post creation
        self.new_post_creation_data = {
            'title': 'Test Post 1',
            'content': 'My Post with Unit testing.'
        }
        # Data for post update
        self.new_post_updation_data = {
            'title': 'Test Post 1 Update',
            'content': 'My Post with Unit testing for update.'
        }

    # region  Register Form Validations

    # To test whether registration is working fine.
    def test_register_POST(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEquals(response.status_code, 302)

    # To test whether password validation is working with short length password
    def test_register_with_short_password_POST(self):
        response = self.client.post(self.register_url, self.user_with_short_password, format='text/html')
        self.assertEquals(response.status_code, 200)  # Since we are staying on the same page.
        self.assertTemplateUsed(response, 'users/register.html')

    # To test whether password validation is working with short length password
    def test_register_with_mismatched_password_POST(self):
        response = self.client.post(self.register_url, self.user_with_mismatched_password, format='text/html')
        self.assertEquals(response.status_code, 200)  # Since we are staying on the same page.
        self.assertTemplateUsed(response, 'users/register.html')

    # To test whether email validation is working with invalid email format
    def test_register_with_invalid_email_POST(self):
        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')
        self.assertEquals(response.status_code, 200)  # Since we are staying on the same page.
        self.assertTemplateUsed(response, 'users/register.html')

    # To test whether email validation is working with invalid email format
    def test_register_with_taken_email_POST(self):
        # We have created one user with an email id.
        self.client.post(self.register_url, self.user, format='text/html')
        # Then we have created another user with same email id
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEquals(response.status_code, 200)  # Since we are staying on the same page.
        self.assertTemplateUsed(response, 'users/register.html')

    # endregion

    # region Login and logout Form Validations

    # To test whether login is working fine.
    def test_login_POST(self):
        # Here we are creating a user to log in
        self.client.post(self.register_url, self.user, format='text/html')
        # Here we are making that user an active in database
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        # Here we are trying to log in with that user
        response = self.client.post(self.login_url, self.user_login_credentials, format='text/html')
        self.assertEqual(response.status_code, 302)

    # To test whether logout is working fine.
    def test_logout_POST(self):
        # Here we are creating a user to log in
        self.client.post(self.register_url, self.user, format='text/html')
        # Here we are making that user an active in database
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        # Here we are trying to log in with that user
        response = self.client.post(self.login_url, self.user_login_credentials, format='text/html')
        self.assertEqual(response.status_code, 302)
        # Let's see whether we get home page
        response1 = self.client.get(self.home_url)
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'blog/home.html')
        # Now let's logout.
        response2 = self.client.get(self.logout_url)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'users/logout.html')

    # To test whether login validation is working fine with empty username fields.
    def test_login_with_empty_Username_fields_POST(self):
        response = self.client.post(self.login_url, {'username': '', 'password': 'password'}, format='text/html')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    # To test whether login validation is working fine with empty password fields.
    def test_login_with_empty_Password_fields_POST(self):
        response = self.client.post(self.login_url, {'username': 'username', 'password': ''}, format='text/html')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    # endregion

    # To test whether new post creation is working or not
    def test_new_post_creation_POST(self):
        # Here we are creating a user to log in
        self.client.post(self.register_url, self.user, format='text/html')
        # Here we are making that user an active in database
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        # Here we are trying to log in with that user
        response = self.client.post(self.login_url, self.user_login_credentials, format='text/html')
        self.assertEqual(response.status_code, 302)
        # After login successfully, try to create a new post.
        response1 = self.client.post(self.create_new_post_url, self.new_post_creation_data, format='text/html')
        self.assertEqual(response1.status_code, 302)
        # After creating post successfully, let's see whether the post detail page is accessible.
        response2 = self.client.get(self.blog_post_detail_url)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'blog/post_detail.html')

    # To test whether new post creation validation working or not if user tries to post without login
    def test_new_post_creation_without_login_POST(self):
        # Without login, try to create a new post.
        response1 = self.client.post(self.create_new_post_url, self.new_post_creation_data, format='text/html')
        self.assertEqual(response1.status_code, 302)
        response2 = self.client.get(self.login_url)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'users/login.html')

    # To test whether post updation is working or not
    def test_post_update_POST(self):
        # Here we are creating a user to log in
        self.client.post(self.register_url, self.user, format='text/html')
        # Here we are making that user an active in database
        user = User.objects.filter(username=self.user['username']).first()
        user.is_active = True
        user.save()
        # Here we are trying to log in with that user
        response = self.client.post(self.login_url, self.user_login_credentials, format='text/html')
        self.assertEqual(response.status_code, 302)
        # After login successfully, try to create a new post.
        response1 = self.client.post(self.create_new_post_url, self.new_post_creation_data, format='text/html')
        self.assertEqual(response1.status_code, 302)
        # After creating post successfully, let's see whether the post detail page is accessible.
        response2 = self.client.get(self.blog_post_detail_url)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'blog/post_detail.html')
        # After accessing post detail, let's update that post with new data.
        response3 = self.client.post(self.blog_post_update_url, self.new_post_updation_data, format='text/html')
        self.assertEqual(response3.status_code, 302)
        # After updating post successfully, let's see whether the post detail page is accessible.
        response4 = self.client.get(self.blog_post_detail_url)
        self.assertEqual(response4.status_code, 200)
        self.assertTemplateUsed(response4, 'blog/post_detail.html')
