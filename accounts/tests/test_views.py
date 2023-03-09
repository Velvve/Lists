from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token
import accounts.views


class SendLoginEmailViewTest(TestCase):
    """тест представления, которое отправляет
       сообщение для входа в систему"""

    def test_redirect_to_home_page(self):
        """тест: переадресуется на домашнюю страницу"""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'velwe-beck@mail.ru'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """тест: отправляет сообщение на адрес из метода post"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'velwe-beck@mail.ru'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'velwe-beck@mail.ru')
        self.assertEqual(to_list, ['velwe-beck@mail.ru'])

    def test_adds_success_message(self):
        """тест: добавляется сообщение об успехе"""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'velwe-beck@mail.ru'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            'Check your email, мы отправили Вам ссылку, \
            которую можно использовать для входа на сайт'
        )
        self.assertEqual(message.tags, 'success')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_email):
        """тест: отсылается ссылка на вход в систему, используя uid маркера"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'velwe-beck@mail.ru'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_email.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """тест представления входа в систему"""

    def test_redirects_to_home_page(self, mock_auth):
        """тест: переадресуется на домашнюю страницу"""
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self, mock_auth):
        """тест: создается маркер, связанный с электронной почтой"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'velwe-beck@mail.ru'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'velwe-beck@mail.ru')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """тест: вызывается authenticate с uid из GET-запроса"""
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """тест: вызывает auth_login с пользователем, если такой имеется"""
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        """тест: не регистрируется в системе, если пользователь не аунтентифицирован"""
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)
