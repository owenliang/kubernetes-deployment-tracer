from kubernetes import client
import settings

def new_client():
    conf = client.Configuration()
    conf.host = settings.API_SERVER_HOST
    conf.verify_ssl = settings.API_VERIFY_SSL
    conf.api_key['authorization'] = settings.BEARER_TOKEN
    conf.api_key_prefix['authorization'] = 'Bearer'
    conf.debug = True
    return client.ApiClient(conf)