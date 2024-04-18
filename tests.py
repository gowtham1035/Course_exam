import unittest
from App import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dashboard_route_authenticated_student(self):
        response = self.app.post('/dashboard', data=dict(username='student123', password='password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Dashboard', response.data)

    def test_dashboard_route_authenticated_teacher(self):
        response = self.app.post('/dashboard', data=dict(username='teacher456', password='password456'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teacher Dashboard', response.data)

    def test_dashboard_route_unauthenticated(self):
        response = self.app.post('/dashboard', data=dict(username='invalid', password='invalid'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
    unittest.main()
