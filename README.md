# TFM-EnriqueVillarrubia

The project is organised into the following directories, structured depending on their purpose:

* __backend.__ Main backend responsible for the users, games and matches management and data persistence.
* __backend_match.__ Real-time match backend implemented using the WebSocket communication protocol.
* __backend_players.__ The core of this Bachelor of Computer Science, where the general board game and the AlphaZero algorithm for creation of the players are located. Employing a multiprocessing backend for their creation and verification of movements.
* __frontend.__ Web application designed in Vue.js.

The requirements and installation of the application are covered in the next sections.

## Requirements

The whole project has been carried out with the Python3 and JavaScript programming language with their respective package management systems and PostgreSQL for the data persistence. The exact versions are enumerated below.

* Python3, 3.8.6.
* Pip, 21.1.2.
* Node, 14.5.5.
* Npm, 6.14.11.
* PostgreSQL, 12.7.

## Installation

First, it is necessary to clone the repository.

```
git clone https://github.com/Kinrre/TFG-EnriqueVillarrubia.git
```

After that, in each backend directory, there is a requirements file containing all the requisites with the exact versions. They are divided into each subproject to facilitate its installation in different virtual environments. So, it is necessary to execute the following command:

```
pip install -r requirements.txt
```

Regarding the frontend, its installation is equivalent to the backend. Instead of installing the packages using pip, as it is developed in JavaScript, npm must be employed. So, navigate to the frontend directory TFG-EnriqueVillarrubia/frontend/ and run:

```
npm install
```

With respect to the database running in PostgreSQL, the database name and a randomly generated user and password are included in the file TFG-EnriqueVillarrubia/backend/core/config.py. It is necessary to create the database, the user and then grant the permissions to the new user, instead of using the root one. First, ensure the PostgreSQL process is running:

```
sudo service start postgresql start
```

Then, in order to create the database, open a SQL shell:

```
sudo -u postgres psql
```

Create the database:

```
CREATE DATABASE db;
```

Once created the database, connect to it:

```
\c db;
```

After that, the user must be created:

```
CREATE USER jhtw6nsf WITH ENCRYPTED PASSWORD '475fa74c47d1';
```

Finally, the user must have all the privileges in that database.

```
GRANT ALL PRIVILEGES ON DATABASE db to jhtw6nsf;
```

Now, the installation has finished and the application is ready to be executed.

## Running the main backend

All the backends developed are running using the uvicorn server. In order to execute the main backend, it is necessary to execute the following command in the root of the project:

```
uvicorn backend.main:app
```

## Running the real-time match backend

The execution of the real-time match backend is equal to the previous one, except the port of the server must be changed to 8001. So, the command to execute is:

```
uvicorn backend.main:app --port 8001
```

## Running the players backend

The players backend is using the 8002 port. In this case, run the following command:

```
uvicorn backend.main:app --port 8002
```

## Running the frontend

Finally, a server is required to provide the frontend files. So, the command to execute in the TFG-EnriqueVillarrubia/frontend/ directory is:

```
npm run serve
```

It is also possible to compile the web application minifying the files that will be located in the \directory{TFG-EnriqueVillarrubia/frontend/build/} directory, and then use another server running:

```
npm run build
```

Lastly, to use the application it is necessary to open a web browser and navigate to http://localhost:8080/. The documentation of the backend is located in http://localhost:8000/docs.
