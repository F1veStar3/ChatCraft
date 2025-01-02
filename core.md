
1. DevOps:
 - github (tests, env) + deploy on AWS/buket
 - sub domains  

2. Frontend (d)
   - React
   - tailwind
 
3. App
   + auth + google
   - login/register/logout
   - smtp/forgot_password 
   - chat ws (d)
   - AI (d)
  
```python3 -m venv .venv```

```source .venv/bin/activate```

```pip install -r requirements.txt```

```docker-compose up -d```

```pip freeze > requirements.txt```

---
+ rework auth(django-allauth)
+ crete dev branch
+ create .env-exampels 

- create pytest
- create git Actions (env)
- fix google auth
- add smtp 
- add celery
