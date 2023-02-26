import aiohttp

class Mailboss:
  url = 'https://member.mailingboss.com'
  
  def __init__(self, user_token, aioClient):
    self.token = user_token
    self.client = aioClient
    
  async def get_lists(self):
    return await self.get('/integration/index.php/lists/')
  
  async def search_by_email(self, list_uid, email):
    return await self.post( \
        '/integration/index.php/lists/subscribers/search-by-email/', \
        {'list_uid':list_uid, 'email':email})
    
    
  async def post(self, params, data):
    async with self.client.post(Mailboss.url+params+self.token, json=data) \
        as request:
      return await self.handle_response(request)
    
  async def get(self, params):
    async with self.client.get(Mailboss.url+params+self.token) as request:
      return await self.handle_response(request)
    
  async def handle_response(self, request):
    response = await request.json()
    if request.status != 200:
      request.raise_for_status()
    elif len(response) == 0:
      request.status = 401
      request.message = 'Unauthorized'
      request.raise_for_status()
    elif response['status'] == 'success':
      #print(response)
      return response.get('data', None)
    else: return False
  
class MailbossSubscriber:
    
  def __init__(self, user_connector, list_uid = '', subscriber_uid = ''):
    assert isinstance(list_uid, str)
    assert isinstance(subscriber_uid, str)
    if len(list_uid) == 0: raise ValueError("list_uid must be specified")
    self.connector = user_connector
    self.data = {'email':'', 'taginternals':'', 'taginternals_remove':'', \
      'list_uid':list_uid, 'subscriber_uid':subscriber_uid}
    
  async def add(self):
    #if self.data.subscriber_uid
    response = await self.connector.post( \
        '/integration/index.php/lists/subscribers/create/', self.data)
    if response == None:
      return False  #Subscriber already existed and was updated
    self.data = response
    return response
    
  async def update(self):
    raise NotImplemented()
    return await self.connector.post( \
        '/integration/index.php/lists/subscribers/update/', self.data)
  
  async def unsubscribe(self):
    raise NotImplemented()
    return await self.connector.post( \
        '/integration/index.php/lists/subscribers/unsubscribe/', self.data)
  
  async def delete(self):
    return None == await self.connector.post( \
        '/integration/index.php/lists/subscribers/delete/', self.data)
    
    
  def set_email(self, email):
    self.data['email'] = email
    
  def add_tags(self, new_tags):
    present_tags = self.data['taginternals'].split(',')
    present_tags = [ \
      next(iter(filter(None, tag)), '') for tag in zip(present_tags, new_tags)]
    self.data['taginternals'] = ','.join(present_tags)
  
  def remove_tags(self, tags):
    raise NotImplemented()
    
