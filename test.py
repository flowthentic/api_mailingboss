from mailboss import *
import aiohttp, asyncio
import os

async def main():
  async with aiohttp.ClientSession() as httpClient:
    api = Mailboss(os.environ['api_key'], httpClient)
    
    #lists = await api.get_lists()
    #print(lists[0])
    
    testing_list = '63b2c7f813b5b'
    #print(await api.search_by_email(testing_list, 'test@mail.com'))
    
    subscriber_to_be_added = MailbossSubscriber(api, testing_list)
    subscriber_to_be_added.set_email('test@mail.com')
    subscriber_to_be_added.add_tags(['testmt'])
    #print(await subscriber_to_be_added.add())

    dummy_subscriber_cleanup = MailbossSubscriber(api, testing_list, '63fba8b20e1d7')
    print(await dummy_subscriber_cleanup.delete())
if __name__ == '__main__':
  asyncio.run(main())
