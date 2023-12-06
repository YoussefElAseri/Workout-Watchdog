import datetime
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base, Exercise, Set, Workout, User, UserWeight


class TestModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_exercise(self):
        exercise = Exercise(name='Test Exercise', body_weight=True)
        self.session.add(exercise)
        self.session.commit()

        exercise = self.session.query(Exercise).filter_by(name='Test Exercise').first()
        self.assertIsNotNone(exercise)

    def test_set(self):
        set_ = Set(set_id=1, reps=5, weight=None, exercise_name='Test Exercise')
        self.session.add(set_)
        self.session.commit()

        set_ = self.session.query(Set).filter_by(set_id=1).first()
        self.assertIsNotNone(set_)

    def test_workout(self):
        workout = Workout(workout_id=1, user_id='Test User', date=datetime.date.today())
        self.session.add(workout)
        self.session.commit()

        workout = self.session.query(Workout).filter_by(workout_id=1).first()
        self.assertIsNotNone(workout)

    def test_user(self):
        user = User(name='Test User')
        self.session.add(user)
        self.session.commit()

        user = self.session.query(User).filter_by(name='Test User').first()
        self.assertIsNotNone(user)

    def test_user_weight(self):
        user_weight = UserWeight(id=1, user_name='Test User', weight=50.0, date=datetime.date.today())
        self.session.add(user_weight)
        self.session.commit()

        user_weight = self.session.query(UserWeight).filter_by(id=1).first()
        self.assertIsNotNone(user_weight)


if __name__ == '__main__':
    unittest.main()
