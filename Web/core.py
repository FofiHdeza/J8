import datetime
from time import strftime, gmtime

import requests
from pprint import pprint

from bs4 import BeautifulSoup
from tabulate import tabulate


def show_devices():
    device_id = []
    device_stats = []
    device_casn = []
    device_account = []
    acctable = []
    device_publicid=[]
    device_created=[]
    device_modified=[]
    device_actstatus=[]
    response = requests.get('http://172.16.11.244/ALT49DLA/adm/v1/devices').json()
    json_response = response['resourceSet']

    for accounts in json_response:
        ids = accounts.get('_id')
        account = accounts.get('accountUid')
        casn = accounts.get('caSN')
        publicid= accounts.get('publicId')
        status = accounts.get('status')
        created = accounts.get('created')
        modified = accounts.get('modified')
        actstatus = accounts.get('activationStatus')
        device_id.append(ids)
        device_account.append(account)
        device_casn.append(casn)
        device_publicid.append(publicid)
        device_stats.append(status)
        device_created.append(created)
        device_modified.append(modified)
        device_actstatus.append(actstatus)
    for i in range(0, (len(device_id))):
        tableacc = [device_id[i], device_account[i], device_casn[i], device_publicid[i], device_stats[i], device_created[i], device_modified[i], device_actstatus[i]]
        acctable.append(tableacc)
        tableofacc = tabulate(acctable, headers=['ID', 'CA_SN', 'Account', 'Status'], tablefmt='fancy_grid')
    return acctable

def show_devices_fromacc(accnumber):
    device_id = []
    device_stats = []
    device_casn = []
    device_account = []
    acctable = []

    response = requests.get("http://172.16.11.244/ALT49DLA/adm/v1/devices?filter={'accountUid':'"+accnumber+"'}").json()
    json_response = response['resourceSet']

    for accounts in json_response:
        ids = accounts.get('_id')
        status = accounts.get('activationStatus')
        casn = accounts.get('caSN')
        account = accounts.get('accountUid')
        device_id.append(ids)
        device_stats.append(status)
        device_casn.append(casn)
        device_account.append(account)

    for i in range(0, (len(device_id))):
        tableacc = [device_id[i], device_casn[i], device_account[i], device_stats[i]]
        acctable.append(tableacc)

    return acctable


def show_one_device(id):
    device_id = []
    device_stats = []
    device_casn = []
    device_account = []
    acctable = []
    device_publicid=[]
    device_created=[]
    device_modified=[]
    device_actstatus=[]
    url='http://172.16.11.244/ALT49DLA/adm/v1/devices/' + str(id)
    response = requests.get(url).json()
    json_response = [response]
    for accounts in json_response:
        ids = accounts.get('_id')
        account = accounts.get('accountUid')
        casn = accounts.get('caSN')
        publicid= accounts.get('publicId')
        status = accounts.get('status')
        created = accounts.get('created')
        modified = accounts.get('modified')
        actstatus = accounts.get('activationStatus')
        device_id.append(ids)
        device_account.append(account)
        device_casn.append(casn)
        device_publicid.append(publicid)
        device_stats.append(status)
        device_created.append(created)
        device_modified.append(modified)
        device_actstatus.append(actstatus)
    for i in range(0, (len(device_id))):
        tableacc = [device_id[i], device_account[i], device_casn[i], device_publicid[i], device_stats[i], device_created[i], device_modified[i], device_actstatus[i]]
        acctable.append(tableacc)
        tableofacc = tabulate(acctable, headers=['ID', 'CA_SN', 'Account', 'Status'], tablefmt='fancy_grid')
    return acctable


def add_device(ide,casn,account):
    device_data = {'_id': ide,
                   'accountUid': account,
                   'activationStatus': 'ACTIVE',
                   'caSN': casn,
                   'deviceProfileId': 'DEFAULT',
                   'deviceType': 'MANAGED',
                   'status': 'ENABLED'}
    new_device = requests.post('http://172.16.11.244/ALT49DLA/adm/v1/devices', json=device_data)


def edit_device(account):

    device_data = {'accountUid': account}
    new_device = requests.put('http://172.16.11.244/ALT49DLA/adm/v1/devices', data=device_data)


def delete_device(ide):
    del_device = requests.delete('http://172.16.11.244/ALT49DLA/adm/v1/devices/' + ide)


def filter_entitlements(account):
    ent_id = []
    accounts = []
    create_date = []
    expiration_date = []
    modified_date = []
    product_id = []
    status = []
    enttable = []

    show_ents = requests.get('http://172.16.11.244/ALT49DLA/rmg/v1/operator/entitlements/').json()
    json_response = show_ents['resourceSet']

    for entitlements in json_response:
        ent_account = entitlements.get('accountId')

        if ent_account == account:
            ids = entitlements.get('_id')
            accts = entitlements.get('accountId')
            creation = entitlements.get('created')
            expiration = entitlements.get('expiryDate')
            modified = entitlements.get('modified')
            productid = entitlements.get('productId')
            entstatus = entitlements.get('status')

            ent_id.append(ids)
            accounts.append(accts)
            create_date.append(creation)
            expiration_date.append(expiration)
            modified_date.append(modified)
            product_id.append(productid)
            status.append(entstatus)

    for i in range(0, (len(ent_id))):
        tableacc = [ent_id[i], accounts[i], create_date[i], expiration_date[i], modified_date[i], product_id[i],
                    status[i]]
        enttable.append(tableacc)

        tableofents = tabulate(enttable, headers=['Entitlement ID', 'Account', 'Creation Date', 'Expiration Date',
                                                  'Modification Date', 'Product ID', 'Status'], tablefmt='fancy_grid')

    return enttable


def add_entitlement(productid, accountid, producttype):
    current_datetime = strftime("%Y-%m-%dT%H:%M:%S" + "0Z", gmtime())
    entitlement_data = {
        "productId": productid,
        "accountId": accountid,
        "validityType": "ABSOLUTE",
        "productType": producttype,
        "validFrom": current_datetime,
        "expiryDate": "2038-12-01T01:00:00Z"
    }

    new_entitlement = requests.post('http://172.16.11.244/ALT49DLA/rmg/v1/operator/entitlements/',
                                    json=entitlement_data).json()

    print(new_entitlement)


def update_entitlement(productid, accountid):
    entitlement_data = {
        "productId": productid,
        "accountId": accountid,
        "validityType": "ABSOLUTE",
        "productType": "SUBSCRIPTION",
    }

    new_entitlement = requests.put('http://172.16.11.244/ALT49DLA/rmg/v1/operator/entitlements/',
                                   json=entitlement_data).json()

    print(new_entitlement)


def delete_entitlement(entitlementid):

    new_entitlement = requests.delete('http://172.16.11.244/ALT49DLA/rmg/v1/operator/entitlements/'
                                      + entitlementid).json()

    print(new_entitlement)


def ssp_addaccount(accountId):
    account_data = {
        "status": "ACTIVE",
        "accountProfileId": "DEFAULT",
        "pvrStatus": "ENABLED",
        "geoBlockExempt": 'false',
        "_id": accountId}
    new_account = requests.post('http://172.16.11.244/ALT49DLA/adm/v1/accounts', json=account_data).json()
    return new_account


def ssp_deleteaccount(accountId):
    delete_account = requests.delete('http://172.16.11.244/ALT49DLA/adm/v1/accounts/actions/purgeAccount/' + accountId).json()
    return delete_account


def ssp_getallaccounts():
    accnumber = []
    accid = []
    accreated = []
    accmod = []
    pvrstatus = []
    accstatus = []
    accstable = []

    response = requests.get('http://172.16.11.244/ALT49DLA/adm/v1/accounts').json()
    json_response = response['resourceSet']

    for stuff in json_response:
        acnumber = stuff.get('accountNumber')
        acid = stuff.get('_id')
        acreated = stuff.get('created')
        acmod = stuff.get ('modified')
        pvr = stuff.get('pvrStatus')
        acstatus = stuff.get('status')
        accnumber.append(acnumber)
        accid.append(acid)
        accreated.append(acreated)
        accmod.append(acmod)
        pvrstatus.append(pvr)
        accstatus.append(acstatus)

    for i in range(0, (len(accnumber))):
        tableacc = [accnumber[i], accid[i], accreated[i], accmod[i], pvrstatus[i], accstatus[i]]
        accstable.append(tableacc)

    return accstable


def ssp_getoneaccount(accountNumber):
    accnumber = []
    accid = []
    accreated = []
    accmod = []
    pvrstatus = []
    accstatus = []
    accstable = []

    response = requests.get("http://172.16.11.244/ALT49DLA/adm/v1/accounts?filter={'accountNumber':'"+accountNumber+"'}").json()
    json_response = response['resourceSet']

    for stuff in json_response:
        acnumber = stuff.get('accountNumber')
        acid = stuff.get('_id')
        acreated = stuff.get('created')
        acmod = stuff.get ('modified')
        pvr = stuff.get('pvrStatus')
        acstatus = stuff.get('status')
        accnumber.append(acnumber)
        accid.append(acid)
        accreated.append(acreated)
        accmod.append(acmod)
        pvrstatus.append(pvr)
        accstatus.append(acstatus)

    for i in range(0, (len(accnumber))):
        tableacc = [accnumber[i], accid[i], accreated[i], accmod[i], pvrstatus[i], accstatus[i]]
        accstable.append(tableacc)

    return accstable

####################SDP-ML########################

def sdp_account_getbycasn(casn):
    finalaccount = []
    url = "http://172.16.11.247/ws-gateway/gateway/ws/deviceservice"
    headers = {'content-type': 'text/xml'}
    body_casn = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dev="http://quative.tv/DeviceServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <dev:getDeviceByCASN>
            <!--Optional:-->
            <casn>"""+casn+"""</casn>
        </dev:getDeviceByCASN>
    </soapenv:Body>
</soapenv:Envelope>"""
    response_casn = requests.post(url, data=body_casn, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse_casn = BeautifulSoup(response_casn.content, 'xml')
    account_uid = beautifulresponse_casn.find('accountUID').contents[0]

    url_accounts = "http://172.16.11.247/ws-gateway/gateway/ws/accountservice"
    body_uid = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:acc="http://quative.tv/AccountServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <acc:getByUID>
            <!--Optional:-->
            <uid>"""+account_uid+"""</uid>
        </acc:getByUID>
    </soapenv:Body>
</soapenv:Envelope>"""
    response_uid = requests.post(url_accounts, data=body_uid, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse_uid = BeautifulSoup(response_uid.content, 'xml')
    account_number = beautifulresponse_uid.find('accountNumber').contents[0]
    account_status = beautifulresponse_uid.find('status').contents[0]
    account_firstname = beautifulresponse_uid.find('firstName').contents[0]
    account_lastname = beautifulresponse_uid.find('lastName').contents[0]
    account_password = beautifulresponse_uid.find('password').contents[0]
    account_npvrprof = beautifulresponse_uid.find('npvrProfile').contents[0]
    account_credlimit = beautifulresponse_uid.find('creditLimit').contents[0]
    account_credspent = beautifulresponse_uid.find('creditSpent').contents[0]
    finalaccount = [account_number,account_status,account_firstname,account_lastname,account_password,
                    account_password,account_npvrprof,account_credlimit,account_credspent,account_uid]
    return finalaccount


def sdp_devices_getbyaccount(account_uid):
    finalaccount = []
    url = "http://172.16.11.247/ws-gateway/gateway/ws/deviceservice"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dev="http://quative.tv/DeviceServiceNamespace">
       <soapenv:Header/>
       <soapenv:Body>
          <dev:getSetTopBoxByAccountUID>
             <!--Optional:-->
             <accountUID>""" + account_uid + """</accountUID>
          </dev:getSetTopBoxByAccountUID>
       </soapenv:Body>
    </soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    device_casn = (
        str(beautifulresponse.find_all('caSN')).replace('<caSN>', '').replace('</caSN>', '').replace('[', '').replace(
            ']', '')).split(',')
    device_status = (
        str(beautifulresponse.find_all('status')).replace('<status>', '').replace('</status>', '').replace('[',
                                                                                                           '').replace(
            ']', '')).split(',')
    device_enabled = (
        str(beautifulresponse.find_all('deviceEnabled')).replace('<deviceEnabled>', '').replace('</deviceEnabled>',
                                                                                                '').replace('[',
                                                                                                            '').replace(
            ']', '')).split(',')
    device_uid = (
        str(beautifulresponse.find_all('UID')).replace('<UID>', '').replace('</UID>',
                                                                            '').replace('[',
                                                                                        '').replace(
            ']', '')).split(',')
    for a,b,c,d in zip(device_casn,device_enabled,device_status,device_uid):
        finalaccount.append([a,b,c,d])
    for i in finalaccount:
        if i[0][0] == ' ':
            i[0] = i[0][1:]
        if i[3][0] == ' ':
            i[3] = i[3][1:]
    print(finalaccount)
    return finalaccount
    # for i in range(0, len(device_casn)):
    #     print(device_casn[i], device_status[i], device_enabled[i])


def sdp_account_getbyaccnumber(acc_number):
    finalaccount = []
    url = "http://172.16.11.247/ws-gateway/gateway/ws/accountservice"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:acc="http://quative.tv/AccountServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <acc:getByAccountNumber>
            <!--Optional:-->
            <accountNumber>"""+acc_number+"""</accountNumber>
        </acc:getByAccountNumber>
    </soapenv:Body>
</soapenv:Envelope>"""

    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    account_number = beautifulresponse.find('accountNumber').contents[0]
    account_status = beautifulresponse.find('status').contents[0]
    account_firstname = beautifulresponse.find('firstName').contents[0]
    account_lastname = beautifulresponse.find('lastName').contents[0]
    account_password = beautifulresponse.find('password').contents[0]
    account_npvrprof = beautifulresponse.find('npvrProfile').contents[0]
    account_credlimit = beautifulresponse.find('creditLimit').contents[0]
    account_credspent = beautifulresponse.find('creditSpentRst').contents[0]
    # print(beautifulresponse)
    # if beautifulresponse.find('creditSpent').contents[0] == None:
    #     account_credspent = str('0')
    # else:
    #     account_credspent = beautifulresponse.find('creditSpent').contents[0]
    account_uid = beautifulresponse.find('UID').contents[0]

    finalaccount = [account_number, account_status, account_firstname, account_lastname, account_password,
                    account_password, account_npvrprof, account_credlimit, account_credspent,account_uid]
    return finalaccount


def sdp_account_createnewacc(accNumber, lastName, firstName, password, status, ppvStatus, locality, npvrProfile,
                             credLimit):
    # En los campos opcionales, se puede enviar un '?' en vez de algo concreto.
    # PpvStatus es true o false

    url = "http://172.16.11.247/ws-gateway/gateway/ws/accountservice"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:acc="http://quative.tv/AccountServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <acc:create>
            <!--Optional:-->
            <model>
                <!--Zero or more repetitions:-->
                <changeLog>?</changeLog>
                <!--Optional:-->
                <creationDate>?</creationDate>
                <!--Optional:-->
                <exportID>?</exportID>
                <!--Optional:-->
                <modifiedDate>?</modifiedDate>
                <!--Optional:-->
                <originID>?</originID>
                <!--Optional:-->
                <originKey>?</originKey>
                <!--Optional:-->
                <serviceProviderID>?</serviceProviderID>
                <!--Optional:-->
                <UID>?</UID>
                <!--Optional:-->
                <accessPointUID>?</accessPointUID>
                <!--Optional:-->
                <accountNumber>""" + accNumber + """</accountNumber>
                <!--Optional:-->
                <accountProfileUID>?</accountProfileUID>
                <!--Optional:-->
                <address1>?</address1>
                <!--Optional:-->
                <address2>?</address2>
                <!--Optional:-->
                <city>?</city>
                <!--Optional:-->
                <country>?</country>
                <!--Optional:-->
                <county>?</county>
                <!--Optional:-->
                <creditLimit>""" + credLimit + """</creditLimit>
                <!--Optional:-->
                <creditSpent>?</creditSpent>
                <!--Optional:-->
                <creditSpentRst>?</creditSpentRst>
                <!--Optional:-->
                <firstName>""" + firstName + """</firstName>
                <!--Optional:-->
                <lastActivityTime>?</lastActivityTime>
                <!--Optional:-->
                <lastName>""" + lastName + """</lastName>
                <!--Optional:-->
                <locality>""" + locality + """</locality>
                <!--Optional:-->
                <maxMPDeviceAllowed>?</maxMPDeviceAllowed>
                <!--Optional:-->
                <maxMPDeviceDate>?</maxMPDeviceDate>
                <!--Optional:-->
                <maxMPDeviceDelete>?</maxMPDeviceDelete>
                <!--Optional:-->
                <maxUserAllowed>?</maxUserAllowed>
                <!--Optional:-->
                <npvrProfile>""" + npvrProfile + """</npvrProfile>
                <!--Optional:-->
                <password>""" + password + """</password>
                <!--Optional:-->
                <postCode>?</postCode>
                <!--Optional:-->
                <ppvStatus>""" + ppvStatus + """</ppvStatus>
                <!--Optional:-->
                <rolloutProfileUid>?</rolloutProfileUid>
                <!--Optional:-->
                <status>""" + status + """</status>
                <!--Optional:-->
                <statusCode>?</statusCode>
                <!--Optional:-->
                <title>?</title>
            </model>
        </acc:create>
    </soapenv:Body>
</soapenv:Envelope>"""

    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    new_account_uid = beautifulresponse.find('return').contents[0]
    print(new_account_uid)


def sdp_account_deleteacc(account_number, account_uid):
    # Se puede utilizar acc UID y/o acc number, si se usa 1, poner ? en el otro.

    url = "http://172.16.11.247/ws-gateway/gateway/ws/accountservice"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:acc="http://quative.tv/AccountServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <acc:purgeAccount>
            <!--Optional:-->
            <accountSpecification>
                <!--Optional:-->
                <accountNumber>""" + account_number + """</accountNumber>
                <!--Optional:-->
                <accountUid>""" + account_uid + """</accountUid>
                <!--Optional:-->
                <originSpecification>
                    <!--Optional:-->
                    <originId>?</originId>
                    <!--Optional:-->
                    <originKey>?</originKey>
                </originSpecification>
            </accountSpecification>
        </acc:purgeAccount>
    </soapenv:Body>
</soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    del_acc_resp = beautifulresponse.find('return').contents[0]
    print(del_acc_resp)
    if del_acc_resp == '1':
        print("Account deleted")
    else:
        print("Update failed")


def sdp_account_updateacc(acc_uid, lastName, firstName, password, status, ppvStatus, npvrProfile, locality,
                          mpDeviceAllowed, profileUID, creditLimit, creditSpent):
    # Se tienen que mandar todos los campos que requiere el def, aunque sea un ?
    # Se puede subir el form con los datos que la cuenta ya tiene, asi no hay que agregar todo de nuevo.

    url = "http://172.16.11.247/ws-gateway/gateway/ws/accountservice"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:acc="http://quative.tv/AccountServiceNamespace">
    <soapenv:Header/>
    <soapenv:Body>
        <acc:update>
            <!--Optional:-->
            <model>
                <!--Zero or more repetitions:-->
                <changeLog>?</changeLog>
                <!--Optional:-->
                <creationDate>?</creationDate>
                <!--Optional:-->
                <exportID>?</exportID>
                <!--Optional:-->
                <modifiedDate>?</modifiedDate>
                <!--Optional:-->
                <originID>?</originID>
                <!--Optional:-->
                <originKey>?</originKey>
                <!--Optional:-->
                <serviceProviderID>?</serviceProviderID>
                <!--Optional:-->
                <UID>""" + acc_uid + """</UID>
                <!--Optional:-->
                <accessPointUID>?</accessPointUID>
                <!--Optional:-->
                <accountNumber>?</accountNumber>
                <!--Optional:-->
                <accountProfileUID>""" + profileUID + """</accountProfileUID>
                <!--Optional:-->
                <address1>?</address1>
                <!--Optional:-->
                <address2>?</address2>
                <!--Optional:-->
                <city>?</city>
                <!--Optional:-->
                <country>?</country>
                <!--Optional:-->
                <county>?</county>
                <!--Optional:-->
                <creditLimit>""" + creditLimit + """</creditLimit>
                <!--Optional:-->
                <creditSpent>""" + creditSpent + """</creditSpent>
                <!--Optional:-->
                <creditSpentRst>?</creditSpentRst>
                <!--Optional:-->
                <firstName>""" + firstName + """</firstName>
                <!--Optional:-->
                <lastActivityTime>?</lastActivityTime>
                <!--Optional:-->
                <lastName>""" + lastName + """</lastName>
                <!--Optional:-->
                <locality>""" + locality + """</locality>
                <!--Optional:-->
                <maxMPDeviceAllowed>""" + mpDeviceAllowed + """</maxMPDeviceAllowed>
                <!--Optional:-->
                <maxMPDeviceDate>?</maxMPDeviceDate>
                <!--Optional:-->
                <maxMPDeviceDelete>?</maxMPDeviceDelete>
                <!--Optional:-->
                <maxUserAllowed>?</maxUserAllowed>
                <!--Optional:-->
                <npvrProfile>""" + npvrProfile + """</npvrProfile>
                <!--Optional:-->
                <password>""" + password + """</password>
                <!--Optional:-->
                <postCode>?</postCode>
                <!--Optional:-->
                <ppvStatus>""" + ppvStatus + """</ppvStatus>
                <!--Optional:-->
                <rolloutProfileUid>?</rolloutProfileUid>
                <!--Optional:-->
                <status>""" + status + """</status>
                <!--Optional:-->
                <statusCode>?</statusCode>
                <!--Optional:-->
                <title>?</title>
            </model>
        </acc:update>
    </soapenv:Body>
</soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    update_acc_resp = beautifulresponse.find('return').contents[0]
    print(update_acc_resp)
    if update_acc_resp == '1':
        print("Account updated")
    else:
        print("Update failed")


def sdp_device_createstb(casn, banned, devEnabled, accuid, smcardtype, status, statuscode):
    url = "http://172.16.11.247/api/smsservice_2.2"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sms="http://nagra.com/xmlns/she/sdp/SMSDomain_v2.2">
    <soapenv:Header/>
    <soapenv:Body>
        <sms:CreateSetTopBox>
            <stb>
                <!--Optional:-->
                <caSN>""" + casn + """</caSN>
                <!--Optional:-->
                <banned>""" + banned + """</banned>
                <deviceEnabled>""" + devEnabled + """</deviceEnabled>
                <!--Optional:-->
                <account>
                    <uid>""" + accuid + """</uid>
                </account>
                <!--Optional:-->
                <smartcardType>""" + smcardtype + """</smartcardType>
                <!--Optional:-->
                <status>""" + status + """</status>
                <!--Optional:-->
                <statusCode>""" + statuscode + """</statusCode>
            </stb>
        </sms:CreateSetTopBox>
    </soapenv:Body>
</soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))
    beautifulresponse = BeautifulSoup(response.content, 'xml')
    create_stb_casn = beautifulresponse.find('caSN').contents[0]
    create_stb_uid = beautifulresponse.find('uid').contents[0]

    if create_stb_casn:
        print("Device created with CASN " + create_stb_casn + " and deviceUID " + create_stb_uid)

    else:
        print("Device creation failed")


def sdp_device_deletestb(casn, devuid):
    url = "http://172.16.11.247/api/smsservice_2.2"
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sms="http://nagra.com/xmlns/she/sdp/SMSDomain_v2.2">
   <soapenv:Header/>
   <soapenv:Body>
      <sms:DeleteSetTopBox>
         <deviceSpecification>
            <!--Optional:-->
            <casn>"""+casn+"""</casn>
            <!--Optional:-->
            <uid>"""+devuid+"""</uid>
            <!--Optional:-->
            <originSpecification>
               <originKey>?</originKey>
               <originId>?</originId>
            </originSpecification>
            <!--Optional:-->
            <nuID>?</nuID>
         </deviceSpecification>
      </sms:DeleteSetTopBox>
   </soapenv:Body>
</soapenv:Envelope>"""
    response = requests.post(url, data=body, headers=headers, auth=('administrator', 'quative'))

    if str(response) == '<Response [200]>':
        print("Device with CASN " + casn + " and deviceUID " + devuid + ' deleted')

    else:
        print("Device delete failed")


def get_nagratoken(casn):
    new_token = requests.get(
        'http://172.16.11.247/hue-gateway/gateway/http/js/signonService/signonByCASN?arg0=' + casn).json()
    token = new_token.get('token')
    return token


#######VOD#######

def vod_getnodes(tkn):
    titles = []
    ids = []
    children = []
    parents = []
    isroot = []
    nodestable = []
    token = get_nagratoken(tkn)
    get_services = requests.get('http://172.16.11.247:80/metadata/delivery/GLOBAL/vod/nodes?token=' + token).json()
    metadata = get_services['nodes']

    # for stuff in metadata:
    #     title = stuff.get('Title')
    #     id = stuff.get('id')
    #     child = stuff.get('children')
    #     parent = stuff.get('ancestors')
    #     root = stuff.get('isRoot')
    #     titles.append(title)
    #     ids.append(id)
    #     children.append(child)
    #     parents.append(parent)
    #     isroot.append(root)
    #
    # for i in range(0, (len(titles))):
    #     tablenode = [titles[i], ids[i], children[i], parents[i], isroot[i]]
    #     nodestable.append(tablenode)

    return metadata


def vod_geteditorials():
    titles = []
    ids = []
    technicals = []
    products = []
    startdate = []
    enddate = []
    items = []
    cleid = []
    noderefs = []
    editorialstable = []

    token = get_nagratoken('0000065536')
    get_services = requests.get('http://172.16.37.115/metadata/delivery/GLOBAL/vod/editorials?token=' + token).json()
    metadata = get_services['editorials']

    for stuff in metadata:
        title = stuff.get('Title')
        id = stuff.get('id')
        technical = stuff.get('technicals')
        titles.append(title)
        ids.append(id)
        technicals.append(technical)

    for vainas in range(0, len(technicals)):
        techs = technicals[vainas]
        product = techs[0]['products']
        products.append(product)

    for cosas in range(0, len(products)):
        prods = products[cosas]
        start = datetime.datetime.fromtimestamp(prods[0]['startPurchase']).strftime('%c')
        end = datetime.datetime.fromtimestamp(prods[0]['endValidity']).strftime('%c')
        voditem = prods[0]['voditems']
        startdate.append(start)
        enddate.append(end)
        items.append(voditem)

    for khe in range(0, len(items)):
        item = items[khe]
        cle = item[0]['contentRef']
        noderef = item[0]['nodeRefs']
        cleid.append(cle)
        noderefs.append(noderef)

    for i in range(0, (len(titles))):
        tableeditorial = [titles[i], ids[i], cleid[i], startdate[i], enddate[i], noderefs[i]]
        editorialstable.append(tableeditorial)

    return editorialstable