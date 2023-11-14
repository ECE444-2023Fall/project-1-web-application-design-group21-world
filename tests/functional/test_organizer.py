import pytest
from flask import Flask
from flask_testing import TestCase
from flask_login import login_user, current_user
from app import create_app, db, login_manager
from flask_migrate import Migrate
from app.models import Organizer, User, Event 
from bs4 import BeautifulSoup
import io
import uuid

class FunctionalTests(TestCase):
    def create_app(self):
        app = create_app("testing")
        migrate = Migrate(app, db)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        organizer = Organizer.query.get(user_id)
        if user:
            return user
        elif organizer:
            return organizer
        return None


    def test_signup_successful(self):
        response = self.client.get('/organizer/signup')
        response = self.client.post('/organizer/signup', data={
                "organization_name": 'Test Organization',
                'organization_email': 'test@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'organization_campus': 'St. George',
                'image': None,
                'organization_description': 'Test organization description.',
                'organization_website_link': 'https://www.testorganization.com',
                'organization_instagram_link': 'https://www.instagram.com/testorganization',
                'organization_linkedin_link': 'https://www.linkedin.com/testorganization',
                'submit': 'Submit'
            })
        print(response.data)
        self.assert200
        assert(response.headers['location'] == '/organizer/myAccount')

            # Assert that the organizer has been added to the database
        organizer = Organizer.query.filter_by(organizer_email='test@utoronto.ca').first()
        self.assertIsNotNone(organizer)
        self.assertEqual(organizer.organizer_name, 'Test Organization')



    def test_duplicate_email(self):
        # Add a test organizer to the database with a known email
        existing_organizer = Organizer(
            id=str(uuid.uuid4()),
            organizer_name='Existing Organization',
            organizer_email='existing@utoronto.ca',
            password='existingpassword',
            campus='UTSC',
            description='Another test organization.',
            image_link=None,
            website='http://www.anotherorganization.com',
            instagram='http://www.instagram.com/anotherorganization',
            linkedin='http://www.linkedin.com/anotherorganization'
        )
        db.session.add(existing_organizer)
        db.session.commit()

        # Attempt to sign up with the existing email
        response = self.client.get('/organizer/signup')
        response = self.client.post('/organizer/signup', data={
                "organization_name": 'Test Organization',
                'organization_email': 'existing@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'organization_campus': 'St. George',
                'image': None,
                'organization_description': 'Test organization description.',
                'organization_website_link': 'https://www.testorganization.com',
                'organization_instagram_link': 'https://www.instagram.com/testorganization',
                'organization_linkedin_link': 'https://www.linkedin.com/testorganization',
                'submit': 'Submit'
            })

        # Additional assertions based on the expected behavior when email is already registered
        print(response.data)
        assert b"Account with this email address already exists!" in response.data
        # Add more assertions if needed


    def test_invalid_email_domain(self):
        response = self.client.post('/organizer/signup', data={
            "organization_name": 'Test Organization',
                'organization_email': 'testorganization@gmail.com',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'organization_campus': 'St. George',
                'image': None,
                'organization_description': 'Test organization description.',
                'organization_website_link': 'https://www.testorganization.com',
                'organization_instagram_link': 'https://www.instagram.com/testorganization',
                'organization_linkedin_link': 'https://www.linkedin.com/testorganization',
                'submit': 'Submit'
        })

        assert response.status_code == 200
        assert b'You may only register with your UofT email' in response.data


    def test_incomplete_form(self):
        response = self.client.post('/organizer/signup', data={
            'organization_name': '',
            'organization_email': '',
            'password': '',
            'confirm_password': '',  # Leaving confirm_password blank
            'campus': '',
            'image': None,
            'description': ' ',
            'website': 'http://www.testorganization.com',
            'instagram': 'http://www.instagram.com/testorganization',
            'linkedin': 'http://www.linkedin.com/testorganization',
            'submit': 'Submit',
        })
        assert response.status_code == 200
        assert b'This field is required.' in response.data  # Expect an error message for missing confirm_password


    def test_organizer_login(self):
        self.client.post('/organizer/signup', data={
                "organization_name": 'Test Organization',
                'organization_email': 'test@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'organization_campus': 'St. George',
                'image': None,
                'organization_description': 'Test organization description.',
                'organization_website_link': 'https://www.testorganization.com',
                'organization_instagram_link': 'https://www.instagram.com/testorganization',
                'organization_linkedin_link': 'https://www.linkedin.com/testorganization',
                'submit': 'Submit'
            })
        self.client.post('/logout')
        response = self.client.post('/', data={'email': 'test@utoronto.ca', 'password': 'testpassword', 'role': 'organizer'})
        self.assert200
        assert(response.headers['location'] == '/organizer/myAccount')
        self.assertTrue(current_user.is_authenticated)
        self.assertTrue(current_user.role == "organizer")
        self.assertEqual(current_user.organizer_name, 'Test Organization')


    def test_invalid_login(self):
        response = self.client.post('/', data={'email': 'invalid@example.com', 'password': 'wrongpassword', 'role': 'user'})
        self.assertMessageFlashed('Invalid email or password')
        self.assertFalse(current_user.is_authenticated)

    def test_organizer_details(self):
        # Add a test organizer to the database with a known email
        existing_organizer = Organizer(
            id=str(1),
            organizer_name='Test Organizer',
            organizer_email='existing@utoronto.ca',
            password='existingpassword',
            campus='UTSC',
            description='Another test organization.',
            image_link=None,
            website='http://www.anotherorganization.com',
            instagram='http://www.instagram.com/anotherorganization',
            linkedin='http://www.linkedin.com/anotherorganization'
        )
        db.session.add(existing_organizer)
        db.session.commit()

        # send a GET request to the route with the organizer_id parameter
        response = self.client.get('/organizer/details/1')
        self.assertEqual(response.status_code, 200)
        # print(response.data)
        self.assertIn(b'Test Organizer', response.data)

    def test_organizer_details_route_not_found(self):
        # Add a test organizer to the database with a known email
        existing_organizer = Organizer(
            id=str(1),
            organizer_name='Test Organizer',
            organizer_email='existing@utoronto.ca',
            password='existingpassword',
            campus='UTSC',
            description='Another test organization.',
            image_link=None,
            website='http://www.anotherorganization.com',
            instagram='http://www.instagram.com/anotherorganization',
            linkedin='http://www.linkedin.com/anotherorganization'
        )
        db.session.add(existing_organizer)
        db.session.commit()

        # send a GET request to the route with invalid organizer_id parameter
        response = self.client.get('/organizer/details/999')

        # assert that the response status code is 404
        self.assertEqual(response.status_code, 404)
        # print(response.data)
        self.assertIn(b'Page Not Found', response.data)

    def test_organizer_create_event_success(self):
        self.client.post('/organizer/signup', 
                         data={ "organization_name": 'Test Organization', 
                               'organization_email': 'test@utoronto.ca', 
                               'password': 'testpassword', 
                               'confirm': 'testpassword', 
                               'organization_campus': 'St. George', 
                               'image': None, 
                               'organization_description': 'Test organization description.', 
                               'organization_website_link': 'https://www.testorganization.com', 
                               'organization_instagram_link': 'https://www.instagram.com/testorganization', 
                               'organization_linkedin_link': 'https://www.linkedin.com/testorganization', 
                               'submit': 'Submit' })

        self.client.post('/logout') 
        response = self.client.post('/', data={
            'email': 'test@utoronto.ca', 
            'password': 'testpassword', 
            'role': 'organizer'}) 
        organizer = Organizer.query.filter_by(organizer_email='test@utoronto.ca').first() 
        response = self.client.post('/organizer/create/event', 
                                    data={ "event_name": 'Test Event', 
                                          "organizer_id": organizer.id, 
                                          "image": None, 
                                          'description': 'Test Description', 
                                          'date': '2023-01-01', 
                                          'time': '12:00', 
                                          'location': 'St. George', 
                                          "google_map_link": "https://map.google.com", 
                                          'fee': '10', 
                                          'has_rsvp': '1' })
        
       
        # Assert that the response status code is 200 (OK) or 302 (redirect)
        self.assertIn(response.status_code, {200, 302})
        
        # Optionally, you can add assertions to check if the event is added to the database
        event = Event.query.filter_by(event_name='Test Event').first()
        
        # self.assertIsNotNone(event)
        self.assertEqual(event.organizer_id, current_user.id)
