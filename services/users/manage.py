from flask.cli import FlaskGroup
import unittest
import coverage
import sys

from project import create_app,db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

coverage_obj = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
coverage_obj.start()

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(tests)
    if result.wasSuccessful():
        coverage_obj.stop()
        coverage_obj.save()
        print('Converage Report')
        coverage_obj.report()
        coverage_obj.html_report()
        coverage_obj.erase()
        return 0
    sys.exit(result)

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(tests)
    if result.wasSuccessful():
        coverage_obj.stop()
        coverage_obj.save()
        print('Coverage Summary:')
        coverage_obj.report()
        coverage_obj.html_report()
        coverage_obj.erase()
        return 0
    sys.exit(result)

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='kamal', email='kamal.s@gc.com'))
    db.session.add(User(username='kamal1', email='kamal.s1@gc.com'))
    db.session.commit()

if __name__ == "__main__":
    cli()
