import urllib3
from faker import Faker
import requests
from Comment.login import Login

f = Faker()
Host: str = "https://sit-beijing.nhcbs.5i5j.com"

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "User-Agent": "Mozilla/5.0",
           "Content-Type": "application/json"}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def createNewProject(creator: str = "15077", projectName: str = "TEST_" + f.pystr()[:5], handle: int = 3):
    """
    项目立项
    :param creator: 创建人id
    :param projectName: 项目名称
    :param handle: 审批中 1、审批驳回2 、审批完成3
    :return:
    """
    token: str = Login("sit").getToken(creator)
    # 先拿token
    headers["Authorization"] = token
    body = {"projectApproval": {"belongerByName": "", "belongerFramework": "", "projectPkid": None, "cityCode": "",
                                "cityName": "", "projectName": f"{projectName}", "projectAlias": f"{projectName}",
                                "projectAliasNew": "",
                                "projectScale": "10", "salesType": "", "roomNumber": "2", "initialCycle": "2",
                                "signCycle": "2", "downPaymentPolicy": "2", "areaId": 8, "areaName": "东单",
                                "bizCityCode": "110100000000", "bizCityName": "北京", "districtCode": "110101000000",
                                "districtName": "东城", "estateAddress": "公主坟普惠北里小区", "latitude": 39.920653,
                                "longitude": 116.314564, "provinceCode": "110000000000", "provinceName": "北京",
                                "regionalType": "1", "trader": 10550}, "buildingSourcePkid": "",
            "projectDeveloper": {"companyAddress": "", "developerName": "", "trademark": "", "developerAddress": "",
                                 "contactsName": "", "contactsPhone": "", "contactsPosition": "",
                                 "balanceCondition": "", "commissionIncome": "", "paymentCycle": "",
                                 "isCheckoutCommission": "", "otherMsg": "", "initialPayment": ""},
            "projectProperties": [{"propertyType": "COMMON_HOUSE", "minPrice": "1", "maxPrice": "2"}],
            "projectCooperation": {"commissionIncomeType": "1", "commissionIncomeStart": "1",
                                   "commissionIncomeEnd": "2", "businessChargeCompanyOther": "",
                                   "advanceInstallment": "1", "projectType": "1102", "pkid": "", "isStartHjh": "1",
                                   "trademark": "", "cooperativeCompany": "甲方名称公司111", "cooperationType": "5",
                                   "commissionIncome": "", "dealType": "INITIAL_SIGN", "projectPkid": "",
                                   "dealTypeInput": "", "chosePayType": "FIRST_PAY", "baseRatioSettlement": "",
                                   "isBusiness": "1", "businessChargeCompany": "1", "settlementRatioInput": "",
                                   "initialPayment": "1", "isAccountPayment": "", "isCheckoutCommission": "",
                                   "otherMsg": "", "notCooperationReason": "", "notCooperationReasonType": "",
                                   "receptionSalesCompany": "", "trademarks": [{"id": ""}]},
            "projectProxys": [{"proxyCompanyName": "", "isSales": "1", "isReceptionCustomer": ""}],
            "projectOnelevelChannels": [],
            "projectTwolevelChannel": {"channelType": "1", "companyName": "开发商名称111", "trademark": "",
                                       "dealType": "",
                                       "dealTypeInput": "", "initialPayment": "", "chosePayType": "",
                                       "baseRatioSettlement": "", "settlementRatioInput": "", "companyAddress": "",
                                       "contacts": "", "contactsPhone": "", "contactsPosition": "",
                                       "paymentCycle": "",
                                       "paymentTerm": "", "commissionRatio": "",
                                       "isContractDeadlineStart": "2022-08-18",
                                       "isContractDeadlineEnd": "2022-08-31",
                                       "differenceMsg": "", "isCheckoutCommission": "", "isAccountPayment": "",
                                       "isContract": "1", "isContractDeadline": "", "receptionSalesCompany": "",
                                       "cooperationMode": "CHANNEL_ALL_SELL", "notCooperationReasonType": "",
                                       "notCooperationReason": "", "trademarks": [{"id": 10550}]},
            "isAgainApproval": "0", "attachments": [
            {"attNode": "项目立项", "attType": "甲方分销权证明", "createByName": "李嵩", "createTime": "2022-08-18 15:30:19",
             "cnt": 1, "baseAttachments": [
                {"fileId": "3223a72df45f4b5da1e6e3abac3211ed", "fileName": "微信图片_20220104140537.jpg",
                 "fileUrl": "https://sit-beijing.nhcbs.5i5j.com/filesvr-web/JQeryUpload/getfile?fileId=3223a72df45f4b5da1e6e3abac3211ed",
                 "fileCat": "jpg", "status": "待确认", "remark": "", "attType": "甲方分销权证明", "attNode": "项目立项"}]}]}
    url = "/nhapigw/ys-api//projectApproval/add"
    res = requests.post(Host + url, headers=headers, json=body,
                        verify=False)
    pkid = res.json()['content'].get("pkid", None)
    print(f'create success pkid={pkid}')
    # 获取审批人info
    if handle == 1:
        return "ok"
    elif handle == 2:
        r = get_approve_info(pkid)
        r['action'] = False
        return handleTask(**r)
    else:
        return approve(pkid)


def approve(pkid: str):
    # token: str = Login("sit").getToken("8051602")
    # headers["Authorization"] = token
    while True:
        r = get_approve_info(pkid)
        if isinstance(r, bool):
            return "ok"
        else:
            handleTask(**r)


def get_approve_info(pkid: str) -> bool | dict:
    """
    获取审批流
    :param pkid:
    :return:
    """

    # token: str = Login("sit").getToken("15077")
    # headers["Authorization"] = token
    url = "/nhapigw/chanjue-activiti/wfProcessInstHistories/getProcessInstHistoryListNew"
    body = {"businessId": pkid, "modelCode": "t_pj_project_audit", "rows": 100, "page": 1}
    resp = requests.post(Host + url, json=body, verify=False, headers=headers)
    lastItems: dict = resp.json().get("items")[-1]
    appInfo = {
        "approveUser": lastItems.get("actUserName").split("/")[0],
        "procInstId": lastItems.get("processInstId"),
        "result": lastItems.get("result")
    }
    if appInfo['result'] == "审批通过":
        return True
    print(appInfo)
    return appInfo


def getTaskId(procInstId: str, headers) -> str | None:
    url: str = "/nhapigw/chanjue-activiti/wfTodoTask/getPagedList"
    body = {"page": 1, "rows": 10, "createTime": ""}
    resp = requests.post(Host + url, json=body, headers=headers, verify=False)
    items: list[dict] = resp.json().get("items")
    for item in items:
        if item.get("procInstId") == procInstId:
            return item.get("taskId")
    return None


def handleTask(approveUser: str, procInstId: str, action: bool = True, **kwargs):
    """
    :return:
    """
    token: str = Login("sit").getToken(approveUser)
    headers["Authorization"] = token
    taskId: str = getTaskId(procInstId, headers)
    url = "/nhapigw/chanjue-activiti/wfWorkflow/handleTask"
    body = {"action": "approve" if action else "decline", "claim": True, "dataFields": {}, "docId": "",
            "isClaim": False,
            "result": "审批通过" if action else "审批驳回",
            "taskId": taskId, "taskRemark": "test"}
    resp = requests.post(Host + url, json=body, verify=False, headers=headers)
    print(resp.text)


def addPan(creator, name):
    url = "https://sit-beijing.nhcbs.5i5j.com/nhapigw/ys-api/buildingSource/addBuildingSource"

    headers[
        'Authorization'] = Login("sit").getToken(creator)
    body = {"buildingSourceDto": {"sourceName": name, "sourceAlias": "别名_" + name, "regionalType": "2",
                                  "provinceCode": "110000000000", "bizCityCode": "110100000000",
                                  "districtCode": "110101000000", "areaId": 8, "developerBrands": "10550",
                                  "scalp": 10550, "developerName": f.pystr(), "raceCooperation": "10",
                                  "provinceName": "北京", "bizCityName": "北京", "districtName": "东城", "areaName": "东单"},
            "buildingProjectDto": [
                {"projectPropertyType": "APARTMENT", "saleSataus": "SALEING", "saleAreaMin": "1", "saleAreaMax": "2",
                 "saleAvgPrice": "1", "restBulidNum": "1", "saleBulidNum": "1"}]}
    res = requests.post(url, headers=headers, json=body,
                        verify=False)

    print(res.text)
