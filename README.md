# Messaging System with RabbitMQ/Celery and Python Flask Application

Deploying a Python application behind Nginx that interacts with RabbitMQ/Celery for email sending and logging functionality.

### Setup

### Prerequisites

- Python 3.8 or higher
- PIP
- Celery
- Rabbit MQ

### Running App locally
Clone the [repository](https://github.com/sodiadrhain/python-rabbit-nginx.git) and proceed with the instructions below.

Install all requirements and dependancies

```
pip install -r requirements.txt
```

Then run

```
python -m flask run
```

Running Celery

```
python -m celery -A app.celery worker --loglevel=info
```

Note: if you have `python3` command installed use python3 instead of `python`