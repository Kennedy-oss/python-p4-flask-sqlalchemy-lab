from datetime import datetime
import re

from app import app, db
from server.models import Animal, Enclosure, Zookeeper

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        # Convert string to datetime.date object for the birthday
        z = Zookeeper(name='John Doe', birthday=datetime.strptime('2000-01-01', '%Y-%m-%d').date())
        db.session.add(z)
        db.session.commit()  # Commit here to ensure Zookeeper gets an ID
        
        # Assuming Enclosure requires an environment
        e = Enclosure(environment='grass', open_to_visitors=True)
        db.session.add(e)
        db.session.commit()  # Commit here to ensure Enclosure gets an ID
        
        # Assuming Animal requires a name, species, zookeeper_id, and enclosure_id
        a_1 = Animal(name='Lion', species='Panthera leo', zookeeper_id=z.id, enclosure_id=e.id)
        a_2 = Animal(name='Tiger', species='Panthera tigris', zookeeper_id=z.id, enclosure_id=e.id)
        db.session.add_all([a_1, a_2])
        db.session.commit()

    def test_animal_route_has_attrs(self):
        '''displays attributes in animal route in <ul> tags called Name, Species.'''
        name_li = re.compile(r'\<li\>Name: .+?\</li\>')
        species_li = re.compile(r'\<li\>Species: .+?\</li\>')
        
        response = app.test_client().get('/animal/1')

        assert len(name_li.findall(response.data.decode())) >= 1
        assert len(species_li.findall(response.data.decode())) >= 1

    def test_animal_route_has_many_to_one_attrs(self):
        '''displays attributes in animal route in <ul> tags called Zookeeper, Enclosure.'''
        zookeeper_li = re.compile(r'\<li\>Zookeeper: .+?\</li\>')
        enclosure_li = re.compile(r'\<li\>Enclosure: .+?\</li\>')
        
        response = app.test_client().get('/animal/1')

        assert len(zookeeper_li.findall(response.data.decode())) >= 1
        assert len(enclosure_li.findall(response.data.decode())) >= 1

    def test_zookeeper_route_has_attrs(self):
        '''displays attributes in zookeeper route in <ul> tags called Name, Birthday.'''
        name_li = re.compile(r'\<li\>Name: .+?\</li\>')
        birthday_li = re.compile(r'\<li\>Birthday: .+?\</li\>')
        
        response = app.test_client().get('/zookeeper/1')

        assert len(name_li.findall(response.data.decode())) >= 1
        assert len(birthday_li.findall(response.data.decode())) >= 1

    def test_enclosure_route_has_attrs(self):
        '''displays attributes in enclosure route in <ul> tags called Environment, Open to Visitors.'''
        environment_li = re.compile(r'\<li\>Environment: .+?\</li\>')
        open_li = re.compile(r'\<li\>Open to Visitors: .+?\</li\>')
        
        response = app.test_client().get('/enclosure/1')

        assert len(environment_li.findall(response.data.decode())) >= 1
        assert len(open_li.findall(response.data.decode())) >= 1
