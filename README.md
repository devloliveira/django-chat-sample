Sample app that uses django channels and redis to allow real time communication between clients.

### Installation
> sudo docker-compose build


### Running the Migrations
> sudo docker-compose run backend ./django_chat/manage.py migrate


### Running the tests
> sudo docker-compose run backend pytest


### Create some users
> sudo docker-compose run backend ./django_chat/manage.py populate_db
The above command will create three different users.(their password are set to `123`)

### Running the project
> sudo docker-compose up

The app will run on localhost:5000
