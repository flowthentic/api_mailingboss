import json
from requests_futures.sessions import FuturesSession

class Mailboss:
  url = 'https://member.mailingboss.com'
  async_timeout = 1
  connector = FuturesSession()
  
  def __init__(self, token):
    self.token = token
    self.futures = []
  
  def add_subscriber(self, email, list_uid):
    self.post('/integration/index.php/lists/subscribers/create/'+self.token \
      , json.dumps({'email':email, 'list_uid':list_uid}))
    
  def post(self, params, data):
    self.futures.append(Mailboss.connector.post(Mailboss.url+params \
      , data=json.dumps(data), timeout=Mailboss.async_timeout))
    
  def get(self, params):
    self.futures.append(Mailboss.connector.get(Mailboss.url+params \
      , timeout=Mailboss.async_timeout))
    
    
