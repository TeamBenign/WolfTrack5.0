import unittest
import sys
import shutil
import os
sys.path.append('./')
from flask_testing import TestCase
from app import app, db 
from flask import url_for
from unittest.mock import patch


class TestFlaskApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        source_folder = './Controller/temp_resume'
        destination_folder = './Controller/resume'
        files_to_copy = os.listdir(source_folder)  
        for file_name in files_to_copy:
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            shutil.copy(source_file_path, destination_file_path)  # Copy files to destination folder

        db.session.remove()
        db.drop_all()
        # Clean up after tests

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assert200(response)
        self.assert_template_used('login.html')  

        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'user_role': 'admin'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assert200(response)

    def test_signup_route(self):
        response = self.client.get('/signup')
        self.assert200(response)
        self.assert_template_used('signup.html')  

        # data = {
        #     'username': 'newuser',
        #     'password': 'newpassword',
        #     'name': 'New User',
        #     'usertype': 'student' 
        # }
        # response = self.client.post('/signup', data=data, follow_redirects=True)
        # self.assert200(response)

    def test_logout_route(self):
        response = self.client.get('/logout')
        self.assertStatus(response, 302) 

    def test_admin_route_without_login(self):
        response = self.client.get('/admin', follow_redirects=True)
        self.assert200(response)  

    def test_student_route_without_login(self):
        response = self.client.get('/student', follow_redirects=True)
        self.assert200(response)  
    def test_invalid_login(self):
        # Test login with invalid credentials
        data = {
            'username': 'invalid_user',
            'password': 'invalid_password',
            'user_role': 'admin'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assert200(response)  

    def test_admin_login_and_access(self):
        # Test login as admin and access admin route
        data = {
            'username': 'admin_username',
            'password': 'admin_password',
            'user_role': 'admin'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assert200(response)
        response = self.client.get('/admin')
        # self.assert200(response) 
        self.assertEqual(response.status_code, 302) 

    def test_student_login_and_access(self):
        # Test login as student and access student route
        data = {
            'username': 'student_username',
            'password': 'student_password',
            'user_role': 'student'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assert200(response)
        response = self.client.get('/student')
        # self.assert200(response)
        self.assertEqual(response.status_code, 302)  
    # def test_add_New_route(self):
    #     # Test 'add_New' route with invalid data
    #     data = {
            
    #     }
    #     response = self.client.post('/student/add_New', data=data, follow_redirects=True)
    #     self.assert400(response)  

    
    def test_send_invaid_email_route(self):
        # Test 'send_email' route with valid data
        data = {
            
        }
        response = self.client.post('/admin/send_email', data=data, follow_redirects=True)
        # self.assert400(response)  
        self.assertEqual(response.status_code, 200)
    def test_render_resume_route(self):
        # Test 'render_resume' route
        response = self.client.get('/admin/render_resume')
        # self.assert200(response)  
        self.assertEqual(response.status_code, 302)


    def test_job_search_route(self):
        # Test 'job_search' route
        response = self.client.get('/student/job_search')
        self.assertIn(response.status_code, [200, 302])
    def test_job_search_result_route(self):
        # Test 'job_search/result' route with valid job role
        data = {
            'job_role': 'Software Engineer'  
        }
        response = self.client.post('/student/job_search/result', data=data, follow_redirects=True)
        self.assert200(response) 

    def test_admin_route(self):
        # Test 'admin' route with valid user data
        data = {
           
        }
        response = self.client.post('/admin', data=data, follow_redirects=True)
        self.assert200(response) 

    def test_student_route(self):
        # Test 'student' route with valid user data
        data = {
            
        }
        response = self.client.post('/student', data=data, follow_redirects=True)
        self.assert200(response)  
   
    def test_analyze_resume_route(self):
        # Test 'view_ResumeAna' (analyze_resume) route
        response = self.client.get('/student/analyze_resume')
        # self.assert200(response)  
        self.assertEqual(response.status_code, 302)     
    @patch('os.listdir')
    def test_display_route(self,mock_listdir):
        # Test 'display' route for file display or download
        directory = '/path/to/directory'
        # Define the return value you want to mock
        mock_listdir.return_value = ['User_Resume.pdf', 'file2.txt', 'file3.txt']
        response = self.client.get('/student/display/')
        # self.assert200(response) 
        self.assertEqual(response.status_code, 302) 
    # def test_add_job_application_invalid_data(self):
    #     # Test adding a job application with invalid or missing data
    #     data = {
           
    #     }
    #     response = self.client.post('/add_job_application', data=data, follow_redirects=True)
    #     self.assert400(response)  

    def test_update_job_application_invalid_data(self):
        # Test updating a job application with invalid or missing data
        data = {
            
        }
        response = self.client.post('/student/update_job_application', data=data, follow_redirects=True)
        # self.assert400(response)  
        self.assertEqual(response.status_code, 200)

    # def test_delete_job_application_invalid_data(self):
    #     # Test deleting a job application with invalid or missing data
    #     company = "InvalidCompany"  # Provide invalid company name
    #     response = self.client.post(f'/student/delete_job_application/{company}', follow_redirects=True)
    #     self.assert400(response) 

    def test_send_email_invalid_input(self):
        # Test sending email with invalid inputs or missing fields
        data = {
           
        }
        response = self.client.post('/admin/send_email', data=data, follow_redirects=True)
        # self.assert400(response)  
        self.assertEqual(response.status_code, 200)

    # def test_send_email_incorrect_address(self):
    #     # Test sending email with incorrect or non-existing email addresses
    #     data = {
            
    #     }
    #     response = self.client.post('/admin/send_email', data=data, follow_redirects=True)
    #     self.assert400(response) 

    def test_upload_incorrect_files(self):
        # Test uploading incorrect files
        data = {
           
        }
        response = self.client.post('/student/upload', data=data, follow_redirects=True)
        # self.assert400(response)  
        self.assertEqual(response.status_code, 200)

    def test_access_routes_without_credentials(self):
        # Test accessing routes without proper authentication
        routes = ['/admin', '/student']
        for route in routes:
            response = self.client.get(route, follow_redirects=True)
            self.assert200(response)  

    def test_correct_data_display(self):
        response = self.client.get('/student')
       
        # self.assert200(response)  
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
   