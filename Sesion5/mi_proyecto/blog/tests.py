from django.test import TestCase, Client
from django.urls import reverse

class CSRFTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_with_csrf(self):
        # Suponiendo que tienes una vista llamada 'mi_vista_post'
        # y que acepta un campo 'dato'
        response = self.client.post(
            reverse('mi_vista_post'),
            {'dato': 'valor'},
            follow=True
        )
        # Solo comprobamos que no sea 403
        self.assertNotEqual(response.status_code, 403)
