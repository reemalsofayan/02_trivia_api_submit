import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:root@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        
        self.new_question = {
            'question': 'Name the two holy cities of Saudi Arabia?',
            'answer': 'Mecca, Almadenah Almonawara',
            'difficulty': 3,
            'category': '3'
        }

    def tearDown(self):
        pass    

    def test_get_paginated_questions(self):
        
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that total_questions 
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))    
    
    def test_404_request_beyond_valid_page(self):
        
        # request unexist page
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        # check status code 
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        #select an question to delete
        res = self.client().delete('/questions/33')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 33).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],33)
        self.assertEqual(question, None) 

    def test_create_new_question(self):
        # query all questions before insertion
        questions_before_newquestion = Question.query.all()

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        # query all questions after insertion
        questions_After_newquestion = Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # if number of  questions is incresing mean we habe successfull insertion
        self.assertTrue( len(questions_before_newquestion) < len(questions_After_newquestion)        )

    def test_get_questions_by_category(self):
        
        #select questions of art category with id 2
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Art')

    def test_play_quiz_game(self):
        
        res = self.client().post('/quizzes',json={'previous_questions': [10, 11],
                                      'quiz_category': {'type': 'Sports', 'id': '6'}})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
  
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 6)
        self.assertNotEqual(data['question']['id'], 10)
        self.assertNotEqual(data['question']['id'], 11)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
