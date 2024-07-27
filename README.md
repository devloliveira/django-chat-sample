Sample app that uses django channels and redis to allow real time communication between clients.

### Installation
> sudo docker-compose build


### Running the Migrations
> sudo docker-compose run backend ./django_chat/manage.py migrate


### Running the tests
> sudo docker-compose run backend pytest


### Running the project
> docker-compose up

The app will run on localhost:5000
