from requests import get

try:
    print(get('http://localhost:5000/api/v2/users').json()['users'])
except Exception:
    print('Get http://localhost:5000/api/v2/users not work')
try:
    print(get('http://localhost:5000/api/v2/users/1').json()['user'])
except Exception:
    print('Get http://localhost:5000/api/v2/users/1 not work')
try:
    print(get('http://localhost:5000/api/v2/users/a').json()['users'])
except Exception:
    print('Get http://localhost:5000/api/v2/users/a not work')
try:
    print(get('http://localhost:5000/api/v2/users/b').json()['user'])
except Exception:
    print('Get http://localhost:5000/api/v2/users/b not work')
try:
    print(get('http://localhost:5000/api/v2/user').json()['user'])
except Exception:
    print('Get http://localhost:5000/api/v2/user not work')
print('')


try:
    print(get('http://localhost:5000/api/v2/jobs').json()['jobs'])
except Exception:
    print('Get http://localhost:5000/api/v2/users not work')
try:
    print(get('http://localhost:5000/api/v2/jobs/1').json()['jobs'])
except Exception:
    print('Get http://localhost:5000/api/v2/jobs/1 not work')
try:
    print(get('http://localhost:5000/api/v2/jobs/a').json()['jobs'])
except Exception:
    print('Get http://localhost:5000/api/v2/jobs/a not work')
try:
    print(get('http://localhost:5000/api/v2/jobs/b').json()['jobs'])
except Exception:
    print('Get http://localhost:5000/api/v2/jobs/b not work')
try:
    print(get('http://localhost:5000/api/v2/job').json()['jobs'])
except Exception:
    print('Get http://localhost:5000/api/v2/job not work')