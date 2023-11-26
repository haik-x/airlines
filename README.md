# airlines


## MongoDB

### Setup a python virtual env with python cassandra installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r requirements.txt
```

### To run the API service
```
python3 -m uvicorn main:app --reload
```


### To load data
Ensure you have a running mongodb instance
i.e.:
```
docker run --name mongodbl -d -p 27017:27017 mongo
```
Once your API service is running (see step above), run the populate script
```
cd data/
python3 populate.py
```
### To run the client

```
python3 client.py search
```

## DGraph

### Setup a python virtual env with python cassandra installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r requirements.txt
```

### To load data
Ensure you have a running dgraph instance
i.e.:
```
docker run --name dgraph_project -d -p 8081:8080 -p 9081:9080  dgraph/standalone
```

### To run the client

```
python3 main.py
```

```
Option 1 to always load the data
```


