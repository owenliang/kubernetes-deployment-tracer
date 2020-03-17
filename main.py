from deployment_tracer import *
import time

# 业务注册回调函数
def my_callback(deployment, track, notify):
    # 基础信息
    basic_info = '部署: {}\t状态: {}\t通知: {}\t'.format(get_deployment_fullname(deployment), track['status'], notify)

    # 根据notify追加信息
    ext_info = ''
    if notify == DEPLOYMENT_NOTIFY_PUBLISH_DOING: # 开始发布
        ext_info = '开始时间: {}'.format(track['begin_time'])
    elif notify == DEPLOYMENT_NOTIFY_PUBLISH_TIMEOUT:  # 发布超时
        ext_info = '持续时间: {}'.format(time.time() - track['begin_time'])
    elif notify == DEPLOYMENT_NOTIFY_PUBLISH_DONE: # 发布成功
        ext_info = '持续时间: {}'.format(track['end_time'] - track['begin_time'])
    elif notify == DEPLOYMENT_NOTIFY_RUNNING_ERROR: # 运行异常
        ext_info = '开始时间: {}'.format(track['error_time'])
    elif notify == DEPLOYMENT_NOTIFY_RUNNING_RECOVER: # 运行恢复
        ext_info = '持续时间: {}'.format(track['recover_time'] - track['error_time'])

    print(basic_info + ext_info)

if __name__ == '__main__':
    tracer(my_callback)