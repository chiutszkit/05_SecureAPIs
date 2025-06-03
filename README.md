<h1>HW_05_SecureAPI</h1>

<h3>This is a Python Project to serve API Requests With API Key Authentication</h3>

## How To Use Python

### Create Environment (For First Time)

```
python3 -m venv .venv
```

### Create .env file (For First Time)
```
Create a .env file in this project root folder

Add the following line to the .env file
API_KEY=your_api_key_here  //any strings will do
```

### Setup Proxy
```
pip config set global.proxy http://proxy.my-proxy-domain.com:my-proxy-port
pip config set global.trusted-host pypi.python.org\npypi.org\nfiles.pythonhosted.org
```

## Run 

### Run Virtual Environment
```
source .venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run the App
```
python3 api_server.py
```
The Flask App is configured for you. Running it on http://127.0.0.1:5000

## Sample Requests

### Method 1: Using Swagger UI
```
http://127.0.0.1:5000/api/docs
```

### Method 2: Using curl (Please make sure to replace your_api_key_here with your actual API key)

### Create a new todo:
```
curl -X POST http://localhost:5000/todos -H "Content-Type: application/json" -H "X-API-Key: your_api_key_here" -d '{"title": "Learn Flask", "description": "Study Flask documentation"}'
```

### Get all todos:
```
curl http://localhost:5000/todos -H "X-API-Key: your_api_key_here"
```

### Update a todo:
```
curl -X PUT http://localhost:5000/todos/1 -H "Content-Type: application/json" -H "X-API-Key: your_api_key_here" -d '{"completed": true}'
``` 

### Delete a todo:
```
curl -X DELETE http://localhost:5000/todos/1 -H "X-API-Key: your_api_key_here"
```