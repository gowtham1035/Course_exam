import unittest
from App import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_login_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_teacher_dashboard_route(self):
        response = self.client.get('/teacher/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_student_dashboard_route(self):
        response = self.client.get('/student/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_create_course_route(self):
        data = {'name': 'Math', 'teacher': 'John Doe'}
        response = self.client.post('/create_course', data=data)
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_drop_course_route(self):
        response = self.client.post('/drop_course/1')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_enroll_route(self):
        data = {'course': 'Math'}
        response = self.client.post('/enroll', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)  # Check for success message in response

    def test_dashboard_route_authenticated(self):
        data = {'username': 'student123', 'password': 'password123'}
        response = self.client.post('/dashboard', data=data)
        self.assertEqual(response.status_code, 302)  # Redirect status code

def test_dashboard_route_unauthenticated(self):
    response = self.client.post('/dashboard', data=dict(username='invalid', password='invalid'), follow_redirects=True)
    self.assertIn(b'Invalid username or password', response.data)  # Check for error message in response
  # Check for error message in response

if __name__ == '__main__':
    unittest.main()
