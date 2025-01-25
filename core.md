
1. DevOps:
 - github (tests, env) + deploy AWS
 - sub domains

2. Frontend (d)
   - React/tailwind
 
3. App
   + auth
   + chat ws /AI
   - user profile + AWS s3
 

```python3 -m venv .venv```

```source .venv/bin/activate```

```pip install -r requirements.txt```

```docker-compose up -d```

```pip freeze > requirements.txt```

```npm install -g wscat```
```wscat -c ws://localhost:8000/ws/chat/```

```daphne core.asgi:application```

{"user_message": "hello"}



