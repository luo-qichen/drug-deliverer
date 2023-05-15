#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import threading

# Future warning 不知道是干什么的
# sys.path.append("/home/ncut/scheduler_ws/devel/lib/python2.7/dist-packages")
import rospy
from scheduler import NeedToChangeStatus, RequestType, Scheduler, TargetStatus

from deliver_scheduler.srv import (
    ChangeTimeResult,
    ChangeTimeResultResponse,
    DestinationMsg,
    DestinationMsgResponse,
)

DEBUG = 0


def SchedulerServerMain():
    rospy.spin()


def HandleRequests(req):
    response = DestinationMsgResponse()

    if req.request_type == RequestType.GetNewRequest.value:
        rospy.loginfo("[scheduler]收到新的目标板信息!")
        # 将药物类型数字转换为字符"A","B","C"
        stringRequestDrugType = requestDrugTypeToString[req.request_drug_type]
        rospy.loginfo(
            "[scheduler] 新的药物需求类型:%s, 配送终点: %d",
            stringRequestDrugType,
            req.request_deliver_destination,
        )
        scheduler.GetNewRequest(stringRequestDrugType, req.request_deliver_destination)
        return emptyResponse

    if req.request_type == RequestType.GetNextTarget.value:
        rospy.loginfo("[scheduler] 收到获取新目标请求!")
        # FUTURE WARNING: Service的requestType和scheduler的requestType含义不同，之后可能会统一
        rospy.loginfo(
            "[scheduler] 当前药物剩余: A:%d, B:%d, C:%d",
            scheduler.GetRemainDrug("A"),
            scheduler.GetRemainDrug("B"),
            scheduler.GetRemainDrug("C"),
        )
        currentQueue = scheduler.GetRequestStatus()
        rospy.loginfo("[scheduler] 当前配送需求:")
        for item in currentQueue:
            rospy.loginfo("[scheduler] %c -> %d", item[0], item[1])

        schedulerResponse, status = scheduler.GetNextTarget()

        # schedulerResponse的requestType字段为请求药物的类型，为字符，需要将其转换为整数
        response.drug_location = requestDrugTypeToInt[schedulerResponse["requestType"]]
        response.deliver_destination = schedulerResponse["deliverDestination"]

        # 对于当前无目标的情形，schedulerResponse的两个字段均为None, 在这里用-1表示None
        if response.drug_location is None or response.deliver_destination is None:
            response.drug_location = -1
            response.deliver_destination = -1
            if status == TargetStatus.NO_DRUG_REMAIN.value:
                rospy.loginfo("[scheduler] 当前没有目标! 因为药品没有库存")
            elif status == TargetStatus.NO_MORE_REQUEST.value:
                rospy.loginfo("[scheduler] 当前没有目标! 因为没有配送需求")

        rospy.loginfo("[scheduler] 对 actuator 的回复:")
        rospy.loginfo(response)
        return response

    # 对于DrugLoaded和Delivered信息，返回空信息
    if req.request_type == RequestType.DrugLoaded.value:
        rospy.loginfo("Got DrugLoaded!")
        scheduler.DrugLoaded()
        return emptyResponse

    if req.request_type == RequestType.Delivered.value:
        rospy.loginfo("Got Delivered!")
        scheduler.Delivered()
        return emptyResponse


def DrugCoolingTimeHandlerMain():
    needToChangeService = rospy.ServiceProxy("changetime", ChangeTimeResult)
    needToChangeService.wait_for_service()
    while not rospy.is_shutdown():
        need = scheduler.GetNeedToChangeStatus()
        if need != NeedToChangeStatus.DONT_CHANGE.value:
            response = needToChangeService.call(need)
            if need != scheduler.GetNeedToChangeStatus():
                # 可能存在到达手写数字点后，已经不需要更新配送时间的情况
                rospy.logwarn("[scheduler] 更新时间需求与发出请求时不同!")
            if response.success:
                scheduler.UpdateDrugCoolingTime(need)


if __name__ == "__main__":
    scheduler = Scheduler()
    emptyResponse = DestinationMsgResponse()
    emptyResponse.drug_location = -1
    emptyResponse.deliver_destination = -1

    # 将数字编码类型请求转换为GetNewRequest方法接受的字符类型"A","B","C"
    requestDrugTypeToString = {0: "A", 1: "B", 2: "C"}
    requestDrugTypeToInt = {"A": 0, "B": 1, "C": 2, None: -1}

    rospy.init_node("scheduler_server")
    s = rospy.Service("mission", DestinationMsg, HandleRequests)
    print("[scheduler] 调度器就绪!")

    drugCoolingTimeHandlerThread = threading.Thread(target=DrugCoolingTimeHandlerMain)
    drugCoolingTimeHandlerThread.setDaemon(True)
    drugCoolingTimeHandlerThread.start()

    SchedulerServerMain()
