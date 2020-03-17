# 集群内部署则设置为True，会自动从/etc目录加载token
IN_CLUSTER = False
# 打印Kubernetse客户端调试日志
DEBUG = False

# base64的bearer token
BEARER_TOKEN = 'ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkltcHVjRWxZWVZBeGRqRktNbU4xY0VwWk9YbFBjWFpuWVdSV09UQkJkMGN3UnkxTVUxQjBWa2hqY1dzaWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxjblpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZVzFsYzNCaFkyVWlPaUp0YjI1cGRHOXlhVzVuSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXpaV055WlhRdWJtRnRaU0k2SW10MVltVnlibVYwWlhNdFpYWmxiblJ6TFdOdmJHeGxZM1J2Y2kxMGIydGxiaTAyT1hoMlp5SXNJbXQxWW1WeWJtVjBaWE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWeWRtbGpaUzFoWTJOdmRXNTBMbTVoYldVaU9pSnJkV0psY201bGRHVnpMV1YyWlc1MGN5MWpiMnhzWldOMGIzSWlMQ0pyZFdKbGNtNWxkR1Z6TG1sdkwzTmxjblpwWTJWaFkyTnZkVzUwTDNObGNuWnBZMlV0WVdOamIzVnVkQzUxYVdRaU9pSTVPV1kyWWpOaFl5MHlNV1JqTFRReU9UTXRPRGs1TnkwM1pUZ3paR1JtT0RVNFpHSWlMQ0p6ZFdJaU9pSnplWE4wWlcwNmMyVnlkbWxqWldGalkyOTFiblE2Ylc5dWFYUnZjbWx1WnpwcmRXSmxjbTVsZEdWekxXVjJaVzUwY3kxamIyeHNaV04wYjNJaWZRLmk0ZEdVTENMNkd1OGtaUDdza1I2WXVQbTkwLWxjVjM0RWEyeVF0M3BHMnZJaUpROWthRm5DUTNMc3pieWlrbU1WUHV2dGRrZkNibnV6NmxYYndfNzhQLVkwT29MNWJXenZwbHg3VnZYSW9YMG5nWV9jemRxczAtalZQSnlWeklrNnpWZU1zTkhfZzBVRDhHdFBKVWJjSFFvdTRBdGpiVkVQV0I0SUp4TDNWVXlTRmtMMDZUZUZfcm1NUThpU1BRNXpUbl8ta2F1UHVEUmh2RW4xUWNqUWU3eTFJMGxNdzZESEdhU2VFS0NZWi1Tb01uaW1aczNLOVltY2pqWVM5cVd0bUhIbFdTVG5hN1ZrR0lxUk1faGstbHdKN3hJeC12OG5wWTd2YmhtQW1McWlvaWxyMHZBa2hGc0FHSTN6d2dhT2JFMWxQUnJFeG1ES1Q4VDFtWndhUQ=='
# 集群访问地址
API_SERVER_HOST = 'https://localhost:8443'
# 是否校验apiserver证书
API_VERIFY_SSL = False
# 如果校验apiserver身份，则配置一下apiserver的CA
API_SSL_CA = ''

# 发布超时时间
PUBLISH_TIMEOUT = 30 # 30秒