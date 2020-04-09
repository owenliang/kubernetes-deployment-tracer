from kubernetes import watch, client
from k8s_client import new_client
import time
import settings

# deployment状态
DEPLOYMENT_STATUS_PUBLISH_DOING = '发布中'  # 发布中
DEPLOYMENT_STATUS_RUNNING_HEALTHY = '运行中' # 运行中
DEPLOYMENT_STATUS_PUBLISH_TIMEOUT = '发布超时' # 发布超时
DEPLOYMENT_STATUS_RUNNING_ERROR = '运行异常' # 运行异常

# deployment通告
DEPLOYMENT_NOTIFY_PUBLISH_DOING = '开始发布'
DEPLOYMENT_NOTIFY_PUBLISH_DONE = '发布成功'
DEPLOYMENT_NOTIFY_PUBLISH_TIMEOUT = '发布超时'
DEPLOYMENT_NOTIFY_PUBLISH_RECOVER = '发布恢复'
DEPLOYMENT_NOTIFY_RUNNING_ERROR = '运行异常'
DEPLOYMENT_NOTIFY_RUNNING_RECOVER = '运行恢复'

# 状态追踪表
deployment_track = {}

# 判断deployment是否正常运行
def is_deployment_healthy(deployment):
    # 新提交的YAML，generation字段是空的，这时候需要认定为不健康
    if  deployment['status']['observed_generation'] and \
            deployment['metadata']['generation'] and \
            deployment['status']['observed_generation'] == deployment['metadata']['generation'] and \
            deployment['status']['updated_replicas'] == deployment['spec']['replicas'] and \
            deployment['status']['replicas'] == deployment['spec']['replicas'] and \
            deployment['status']['available_replicas'] == deployment['spec']['replicas']:
        return True
    return False

# 获取deploymnet预期的generation
def get_deployment_expected_generation(deployment):
    return deployment['metadata']['generation']

# 获取deployment的fullname
def get_deployment_fullname(deployment):
    namespace = deployment['metadata']['namespace']
    name = deployment['metadata']['name']
    return '{}/{}'.format(namespace, name)

# 生成新track记录
def insert_deployment_track(info, deployment):
    now = time.time()
    track = {'generation': info['generation'], 'begin_time': now, 'end_time': now, 'error_time': now, 'recover_time': now}

    notify = ''

    if info['healthy']:
        track['status'] = DEPLOYMENT_STATUS_RUNNING_HEALTHY
    else:
        # 新插入的不健康都认为是发布中
        notify = DEPLOYMENT_NOTIFY_PUBLISH_DOING
        track['status'] = DEPLOYMENT_STATUS_PUBLISH_DOING

    # 对本轮发布是否成功过做一个猜测
    if track['status'] == DEPLOYMENT_STATUS_RUNNING_HEALTHY:
        track['succeed_before'] = True
    else:
        track['succeed_before'] = False

    deployment_track[info['fullname']] = track

    return track, notify

# 部署健康的状态机处理
def proc_deployment_track_on_healthy(track, info, deployment):
    prev_status = track['status']
    track['status'] = DEPLOYMENT_STATUS_RUNNING_HEALTHY

    now = time.time()
    notify = ''
    if prev_status == DEPLOYMENT_STATUS_PUBLISH_DOING: # 发布中 -> 健康
        track['end_time'] = now # 发布结束时间
        notify = DEPLOYMENT_NOTIFY_PUBLISH_DONE  # 发布成功
    elif prev_status == DEPLOYMENT_STATUS_PUBLISH_TIMEOUT: # 发布超时 -> 健康
        track['end_time '] = track['recover_time'] = now # 发布结束时间
        notify = DEPLOYMENT_NOTIFY_PUBLISH_RECOVER # 发布恢复
    elif prev_status == DEPLOYMENT_STATUS_RUNNING_ERROR: # 运行异常 -> 健康
        track['recover_time'] = now
        notify = DEPLOYMENT_NOTIFY_RUNNING_RECOVER # 运行恢复

    return notify

# 部署不健康的状态机驱动
def proc_deployment_track_on_unhealthy(track, info, deployment):
    prev_status = track['status']

    now = time.time()
    notify = ''
    if prev_status == DEPLOYMENT_STATUS_PUBLISH_DOING: # 发布中 -> 发布超时
        if now - track['begin_time'] > settings.PUBLISH_TIMEOUT:
            track['status'] = DEPLOYMENT_STATUS_PUBLISH_TIMEOUT # 发布超时
            notify = DEPLOYMENT_NOTIFY_PUBLISH_TIMEOUT # 公告发布超时
    elif prev_status == DEPLOYMENT_STATUS_RUNNING_HEALTHY:  # 运行中 -> 运行异常
        track['status'] = DEPLOYMENT_STATUS_RUNNING_ERROR
        track['error_time'] = now
        notify = DEPLOYMENT_NOTIFY_RUNNING_ERROR # 公告运行异常

    return notify

def handle_deplyment_track(cb, event_obj):
    # 操作类型
    op_type = event_obj['type']
    # 部署对象
    deployment = event_obj['object'].to_dict()

    deployment_fullname = get_deployment_fullname(deployment)
    deployment_healthy = is_deployment_healthy(deployment)
    deployment_generation = get_deployment_expected_generation(deployment)
    deployment_info = {
        'fullname': deployment_fullname, # 部署名
        'healthy': deployment_healthy,   # 是否部署完成
        'generation': deployment_generation, # 期望版本
    }

    # 删除处理
    if op_type == 'DELETED':
        if deployment_fullname in deployment_track:
            del deployment_track[deployment_fullname]
        return

    notify = ''
    if deployment_fullname not in deployment_track:  # 不存在则记录
        track, notify = insert_deployment_track(deployment_info, deployment)
    else:
        track = deployment_track[deployment_fullname]
        if track['generation'] != deployment_generation: # 版本不一致, 则意味着新一轮的部署
            track, notify =  insert_deployment_track(deployment_info, deployment) # 重新插入
        else:
            if deployment_healthy:  # 部署健康, 状态机驱动
                notify = proc_deployment_track_on_healthy(track, deployment_info, deployment)
            else: # 部署不健康，状态机驱动
                notify = proc_deployment_track_on_unhealthy(track, deployment_info, deployment)

    cb(deployment, track, notify)

def tracer(cb):
    api_client = new_client()
    apps_v1 = client.AppsV1Api(api_client)

    w = watch.Watch()
    for event_obj in w.stream(apps_v1.list_deployment_for_all_namespaces):
        handle_deplyment_track(cb, event_obj)
