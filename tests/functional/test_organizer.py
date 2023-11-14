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
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def signup_user(self):
        response = self.client.post('/user/signup', data={
                "name": 'Test anotherUser',
                'email': 'existing@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'faculty': "Engineering",
                'major': "Testmajor",
                'year_of_study': '1st',
                'submit': 'Submit',
            })
        return response
        
    def signup_organizer(self): 
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
        }) # Signup as organizer
        return response
        
    def create_event(self): 
        response = self.client.post('/organizer/create/event', data={
                "event_name": 'Test Event', 
                "organizer_id": '0', 
                "image": None, 
                'description': 'Test Description', 
                'date': '2023-01-01', 
                'time': '12:00', 
                'location': 'St. George', 
                "google_map_link": "https://map.google.com", 
                'fee': '10', 
                'has_rsvp': '1'
        })
        return response

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

    def test_signup_successful_user(self):
        response = self.client.get('/user/signup')
        response = self.client.post('/user/signup', data={
                "name": 'Test User',
                'email': 'test@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'faculty': "Engineering",
                'major': "Testmajor",
                'year_of_study': '1st',
                'submit': 'Submit',
            })
        print(response.data)
        self.assert200
        assert(response.headers['location'] == '/signup/interests')

            # Assert that the user has been added to the database
        user = User.query.filter_by(email='test@utoronto.ca').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')

    def test_duplicate_email_user(self):
        # Add a test organizer to the database with a known email
        existing_user = User(
            id=str(uuid.uuid4()),
            name='Existing User',
            email='existing@utoronto.ca',
            password='existingpassword',
            campus= 'St. George',
            faculty= 'Engineering',
            major= 'Testmajor',
            year_of_study='1st',
        )
        db.session.add(existing_user)
        db.session.commit()

        # Attempt to sign up with the existing email
        response = self.client.get('/user/signup')
        response = self.client.post('/user/signup', data={
                "name": 'Test anotherUser',
                'email': 'existing@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'faculty': "Engineering",
                'major': "Testmajor",
                'year_of_study': '1st',
            })

        # Additional assertions based on the expected behavior when email is already registered
        print(response.data)
        assert b"Account with this email address already exists!" in response.data

    def test_invalid_email_domain_user(self):
        response = self.client.post('/user/signup', data={
                "name": 'Test anotherUser',
                'email': 'existing@gmail.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'faculty': "Engineering",
                'major': "Testmajor",
                'year_of_study': '1st',
        })

        assert response.status_code == 200
        assert b'You may only register with your UofT email' in response.data

    def test_incomplete_form_user(self):
        response = self.client.post('/user/signup', data={
                "name": 'Test anotherUser',
                'email': 'existing@gmail.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'year_of_study': '1st',
            'submit': 'Submit',
        })
        assert response.status_code == 200
        assert b'This field is required.' in response.data  # Expect an error message for missing confirm_password

    def test_user_login(self):
        self.client.post('/user/signup', data={
                "name": 'Test anotherUser',
                'email': 'existing@utoronto.ca',
                'password': 'testpassword',
                'confirm': 'testpassword',
                'campus': 'St. George',
                'faculty': "Engineering",
                'major': "Testmajor",
                'year_of_study': '1st',
                'submit': 'Submit',
            })
        self.client.post('/logout')
        response = self.client.post('/', data={'email': 'existing@utoronto.ca', 'password': 'testpassword', 'role': 'user'})
        self.assert200
        assert(response.headers['location'] == '/user/myAccount')
        self.assertTrue(current_user.is_authenticated)
        self.assertTrue(current_user.role == "user")
        self.assertEqual(current_user.name, 'Test anotherUser')

    def test_invalid_login_organizer(self):
        response = self.client.post('/', data={'email': 'invalid@example.com', 'password': 'wrongpassword', 'role': 'organizer'})
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
        
        event = Event.query.filter_by(event_name='Test Event').first()
        
        self.assertEqual(event.organizer_id, current_user.id)

    def test_organizer_create_event_failure(self):
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
                                        data={ "event_name": '', 
                                            "organizer_id": organizer.id, 
                                            "image": None, 
                                            'description': 'Test Description', 
                                            'date': '2023-01-01', 
                                            'time': '12:00', 
                                            'location': 'St. George', 
                                            "google_map_link": "https://map.google.com", 
                                            'fee': '10', 
                                            'has_rsvp': '1' })
            
            
            self.assertIn(b'This field is required.', response.data)
        
    def test_organizer_appears_webpage(self):
        self.signup_organizer()
        response = self.client.get('/organizer/list')
         
        assert b'href="/organizer/details/' in response.data # Check if webpage updated
        
    def test_organizer_not_appears_webpage(self):
        self.signup_user()
        response = self.client.get('/organizer/list')
        
        assert b'href="/organizer/details/' not in response.data # Check if webpage updated (it shouldn't)
        
    def test_event_is_created_on_webpage(self):
        self.signup_organizer()
        response = self.client.get('/discover')
        
        assert b'event-row-component-container event-row-component-root-class-name' not in response.data # Check if no events yet
        
        self.create_event()
        
        response = self.client.get('/discover')
        
        assert b'event-row-component-container event-row-component-root-class-name' in response.data # Check if events added in webpage
<<<<<<< HEAD
    
    def test_event_details(self):
        existing_event = Event(
            id=str(1),
            event_name='Test Event',
            organizer_id=str(2),
            description='A test Event.',
            image_link= None,
            date='2023-11-14',
            time='12pm',
            location='Test Location',
            google_map_link=None,
            fee='10',
            external_registration_link=None
        )
        db.session.add(existing_event)
        db.session.commit()

        response = self.client.get('/event_details/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Event', response.data)

    def test_event_details_route_not_found(self):
        existing_event = Event(
            id=str(1),
            event_name='Test Event',
            organizer_id=str(2),
            description='A test Event.',
            image_link= None,
            date='2023-11-14',
            time='12pm',
            location='Test Location',
            google_map_link=None,
            fee='10',
            external_registration_link=None
        )
        db.session.add(existing_event)
        db.session.commit()

        response = self.client.get('/event_details/100000')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        

        
=======


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
        
        event = Event.query.filter_by(event_name='Test Event').first()
        
        self.assertEqual(event.organizer_id, current_user.id)

    def test_organizer_create_event_failure(self):
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
                                        data={ "event_name": '', 
                                            "organizer_id": organizer.id, 
                                            "image": None, 
                                            'description': 'Test Description', 
                                            'date': '2023-01-01', 
                                            'time': '12:00', 
                                            'location': 'St. George', 
                                            "google_map_link": "https://map.google.com", 
                                            'fee': '10', 
                                            'has_rsvp': '1' })
            
            
            self.assertIn(b'This field is required.', response.data)
            
         
    def test_registration(self):
            event = Event(
                event_name="Test Event",
                organizer_id="1",
                description="Lorem Ipsum",
                date="01/01/1960",
                time="00:00",
                location="Toronto, Ontario, Canada",
                google_map_link="https://test.com",
                fee="1",
                external_registration_link="https://test.com",
            )
            db.session.add(event)
            db.session.commit()

            assert event in Event.query.all()

            event = Event.query.filter(Event.event_name == "Test Event").first()

            self.signup_user()
            self.client.post("/logout")
            response = self.client.post(
                "/",
                data={
                    "email": "existing@utoronto.ca",
                    "password": "testpassword",
                    "role": "user",
                },
            )
            self.assert200
            self.assertTrue(current_user.is_authenticated)

            response = self.client.post(f"/register_for_event/{event.id}")
            assert event in current_user.events
            assert current_user in event.users

            response = self.client.post(f"/unregister_for_event/{event.id}")
            assert event not in current_user.events
            assert current_user not in event.users
>>>>>>> 40e963f8cf883c0c540a6b62999f79a3ddecb3c5
