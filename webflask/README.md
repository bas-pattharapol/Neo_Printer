# Uniliver PreWeight API

This is API for PreWieght Client and PreWeight Center

# Install Package

```bash
$ pip install -r requirements.txt
```

# How to run

Command

```bash
$ python app.py
```

Result

```bash
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

# Endpoint

Host: http://localhost:5000

| No. | Endpoint                                 | Method | Header                                              | Body                                        | Response                                           |
| --- | ---------------------------------------- | ------ | --------------------------------------------------- | ------------------------------------------- | -------------------------------------------------- |
| 1   | /login                                   | POST   | -                                                   | {"username": username, "password": password | {"exp": 3600, "token" token}                       |
| 2   | /register                                | POST   | -                                                   | {"username": username, "password": password | {'message': 'registered, successfully' }           |
| 3   | /user                                    | GET    | {"x-access-tokens": token}                          | -                                           | {"sec_public_id": user_id,"sec_username": username |
| 4   | /preweight/{wsid}/{batchid}/{materialid} | GET    | {"x-access-tokens": token}                          | -                                           | JSON Format                                        |
| 5   | /campaign/{start}/{end}                  | GET    | {"x-access-tokens": token}                          | -                                           | JSON Format                                        |
| 6   | /batch/{id}                              | GET    | {"x-access-tokens": token}                          | -                                           | JSON Format                                        |
| 7   | /preweight/barcode/{barcode}             | GET    | {"x-access-tokens": token, "x-access-scaleID": id } | -                                           | JSON Format                                        |

<!-- # Docker

build image
docker build -t flaskapp .

run
docker run -it -p 5000:5000 --rm --name flaskapp flaskapp -->


MesloLGS NF, 'Courier New', monospace