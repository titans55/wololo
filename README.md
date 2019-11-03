# Wololo

Browser based strategy game

## Getting Started

Pull the develop (will be created) branch, install prerequisites and requierments.

### Prerequisites

Install virtualenv: (pip3 install virtualenv) and create your env. (virtualenv yourenvname)

Install rabbitMQ: [Docs](http://www.dropwizard.io/1.0.2/docs/)

Install docker: [Docs](https://docs.docker.com/install/)

Install postgresql: [Docs](https://www.postgresql.org/download/)

### Installing

Follow these instructions after installing prerequisites.

Go in to your virtual environment :

```
virtualenv yourenvname
```
Install modules:

```
pip3 install requierments.txt
```

Log in to your psql and create database for migration:

```
sudo -u postgres -i
psql
CREATE DATABASE "wololoDjango"
```

After this, your db is ready for running migrations. so do it.

```
python3 manage.py migrate
```

You will find wololopostgres.sh file on the project. change the paths according to your file system. then run it.

```
sudo ./wololopostgres.sh
```

Check opened terminals and give permission to the rabbitMQ and Docker if neccessary. 


That's all.

## Running the tests

Will be added ASAP.


### And coding style tests

Use VSCode and install python extension.

## Deployment

Will be discussed.


