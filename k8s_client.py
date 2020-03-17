from kubernetes import client
import settings
import base64

def new_client():
    conf = client.Configuration()

    if settings.IN_CLUSTER:
        conf.host = 'https://kubernetes.default.svc:443'
        conf.verify_ssl = False
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as fp:
            conf.api_key['authorization'] = fp.read()
    else:
        conf.host = settings.API_SERVER_HOST
        conf.verify_ssl = False # settings.API_VERIFY_SSL
        conf.api_key['authorization'] = base64.b64decode(settings.BEARER_TOKEN).decode('utf-8')

    conf.api_key_prefix['authorization'] = 'Bearer'
    conf.debug = settings.DEBUG
    return client.ApiClient(conf)