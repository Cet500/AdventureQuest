import requests

base_url = 'http://127.0.0.1:8001'

response = requests.post( base_url + '/user/Pavel/100/10/5' )

print( response )