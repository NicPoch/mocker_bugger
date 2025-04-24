# mocker_bugger

## Description

A code snippet that base on a yaml file generates a fast api mock. Grabs the data from the yaml, renders it on some jinja3 templates, and writes the output under generated_apis.

## Example yaml

```yaml
endpoints:
  - path: /users
    method: GET
    response:
      status_code: 200
      body:
        users: [{ id: 1, name: "Alice" }]
  - path: /users/1
    method: GET
    delay: 5
    response:
      status_code: 200
      body: { id: 1, name: "Alice" }
  - path: /users/2
    method: GET
    response:
      status_code: 400
      body: {error: "Some error"}
app:
  cors:
    origins: ["http://localhost","http://localhost:8080"]
    credentials: True
    methods: ["*"]
    headers: ["*"]
  metadata:
    title: "Example Api"
    description: "Example Description"
    summary: "Example Summary"
    version: "1"
requirements:
  - annotated-types==0.7.0
  - anyio==4.5.2
  - black==24.8.0
  - click==8.1.8
  - colorama==0.4.6
  - exceptiongroup==1.2.2
  - fastapi==0.115.12
  - flake8==7.1.2
  - h11==0.14.0
  - idna==3.10
  - iniconfig==2.1.0
  - isort==5.13.2
  - jinja2==3.1.6
  - MarkupSafe==2.1.5
  - mccabe==0.7.0
  - mypy-extensions==1.1.0
  - packaging==25.0
  - pathspec==0.12.1
  - platformdirs==4.3.6
  - pluggy==1.5.0
  - pycodestyle==2.12.1
  - pydantic==2.10.6
  - pydantic-core==2.27.2
  - pyflakes==3.2.0
  - pytest==8.3.5
  - PyYAML==6.0.2
  - sniffio==1.3.1
  - starlette==0.44.0
  - tomli==2.2.1
  - typing-extensions==4.13.2
  - uvicorn==0.33.0
```

## Parameters

### endpoints

Defines the endpoints to mock by listing the paths

#### path

the path to be mocked and the response/error to return
allows for:
- delays
- http method definition
- the path
- the response body
- the response status

*Bear in mind that any status code different to 2\*\* will raise a HttpException*

example of paths
```yaml
- path: /users
  method: GET
  response:
    status_code: 200
    body:
      users: [{ id: 1, name: "Alice" }]
- path: /users/1
  method: GET
  delay: 5
  response:
    status_code: 200
    body: { id: 1, name: "Alice" }
- path: /users/2
  method: GET
  response:
    status_code: 400
    body: {error: "Some error"}
```

### app

Defines the app configuration and metadata (havent implemented metadata yet)

#### cors

the cors parameter to be used by the mock api
the implementation handles the parameters
```yaml
origins: ["http://localhost","http://localhost:8080"]
credentials: True
methods: ["*"]
headers: ["*"]
```
map to 
```python
origins= ['http://localhost', 'http://localhost:8080']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

### metadata (to be implemented)
Information regarding the api metadata based on the fastapi documentation

expected yaml
```yaml
title: "Example Api"
description: "Example Description"
summary: "Example Summary"
version: "1"
```

### requirements
the libraries required to run the api, it is a list of libraries and version
example yaml
```yaml
- annotated-types==0.7.0
- anyio==4.5.2
- black==24.8.0
- click==8.1.8
- colorama==0.4.6
- exceptiongroup==1.2.2
- fastapi==0.115.12
- flake8==7.1.2
- h11==0.14.0
- idna==3.10
- iniconfig==2.1.0
- isort==5.13.2
- jinja2==3.1.6
- MarkupSafe==2.1.5
- mccabe==0.7.0
- mypy-extensions==1.1.0
- packaging==25.0
- pathspec==0.12.1
- platformdirs==4.3.6
- pluggy==1.5.0
- pycodestyle==2.12.1
- pydantic==2.10.6
- pydantic-core==2.27.2
- pyflakes==3.2.0
- pytest==8.3.5
- PyYAML==6.0.2
- sniffio==1.3.1
- starlette==0.44.0
- tomli==2.2.1
- typing-extensions==4.13.2
- uvicorn==0.33.0
```