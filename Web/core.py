from time import strftime, gmtime

import requests
from pprint import pprint
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

# from nornir.plugins.functions.text import print_result
# #from Web import nr, myclient, mydb, Rcol, Scol, Vcol, Pcol, db
# import nornir
# from nornir import InitNornir
# from nornir.plugins.tasks.networking import napalm_get, netmiko_send_command, netmiko_send_config, tcp_ping
# from nornir.core.filter import F
# from netmiko import NetMikoTimeoutException, NetmikoTimeoutException
# import yaml
# import pymongo
# import pyodbc
# import jinja2
# import copy
# import time
#
# from Web.Database import Notificacion, Servicio
#
#
# def router():
#     hosts = nr.filter(F(groups__contains="router_group"))
#     hosts = hosts.inventory.hosts
#     hostsDB = []
#     router = {
#         "_id": 0,
#         "hostname": "",
#         "type": "",
#         "model": "",
#         "int": {},
#         "location": "",
#         "username": "",
#         "pass": "",
#         "config": ""
#     }
#     for i in hosts:
#         for x in Rcol.find({}, {"_id": 0, "hostname": 1}):
#             hostsDB.append(x["hostname"])
#         if i not in hostsDB:
#             router["_id"] = len(hostsDB) + 1
#             router["hostname"] = i
#             router["type"] = nr.inventory.hosts[i].data["typ"]
#             router["location"] = nr.inventory.hosts[i].data["location"]
#             router["username"] = nr.inventory.hosts[i].username
#             router["pass"] = nr.inventory.hosts[i].password
#             print(i)
#             host = nr.filter(F(name=i))
#             results = host.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
#             print(results)
#             print(results[i][0].result)
#             router["model"] = results[i][0].result[0]["hardware"][0]
#             results = host.run(task=netmiko_send_command, command_string="show interfaces", use_textfsm=True)
#             dic = results[i][0].result
#             print(dic)
#             for j in dic:
#                 intf = j["interface"]
#                 intf = intf.replace(".", ",")
#                 router["int"][intf] = {
#                     "link_status": j["link_status"],
#                     "protocol_status": j["protocol_status"],
#                     "ip": j["ip_address"],
#                     "bandwidth": int(j["bandwidth"].replace(' Kbit', ''))
#                 }
#             results = host.run(task=netmiko_send_command, command_string="show run")
#             router["config"] = results[i][0].result
#             Rcol.insert_one(router)
#         else:
#             print(i, "Ya existe en la base de datos")
#         hostsDB.clear()
#
# def switch():
#     hosts = nr.filter(F(groups__contains="switch_group"))
#     hosts = hosts.inventory.hosts
#     hostsDB = []
#     switch = {
#         "_id": 0,
#         "hostname": "",
#         "type": "",
#         "model": "",
#         "int": {},
#         "location": "",
#         "username": "",
#         "pass": "",
#         "config": ""
#     }
#
#     for i in hosts:
#         for x in Scol.find({}, {"_id": 0, "hostname": 1}):
#             hostsDB.append(x["hostname"])
#         if i not in hostsDB:
#             switch["_id"] = len(hostsDB) + 1
#             switch["hostname"] = i
#             switch["type"] = nr.inventory.hosts[i].data["typ"]
#             switch["location"] = nr.inventory.hosts[i].data["location"]
#             switch["username"] = nr.inventory.hosts[i].username
#             switch["pass"] = nr.inventory.hosts[i].password
#             print(i)
#             host = nr.filter(F(name=i))
#             results = host.run(task=netmiko_send_command, command_string="show version", use_textfsm=True)
#             print(results)
#             print(results[i])
#             print(results[i][0])
#             print(results[i][0].result)
#             print(results[i][0].result[0])
#             switch["model"] = results[i][0].result[0]["serial"][0]
#             results = host.run(task=netmiko_send_command, command_string="show interfaces", use_textfsm=True)
#             dic = results[i][0].result
#             for j in dic:
#                 intf = j["interface"]
#                 intf = intf.replace(".", ",")
#                 switch["int"][intf] = {
#                     "available": True,
#                     "link_status": j["link_status"],
#                     "protocol_status": j["protocol_status"],
#                     "ip": j["ip_address"],
#                     "bandwidth": int(j["bandwidth"].replace(' Kbit', ''))
#                 }
#             results = host.run(task=netmiko_send_command, command_string="show run")
#             switch["config"] = results[i][0].result
#             Scol.insert_one(switch)
#         else:
#             print(i, "Ya existe en la base de datos")
#         hostsDB.clear()
#
# def update_l2vpn_service(id_servicio, cursor, location, new_bw):
#   cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   #location = ''
#   up=0
#   down=0
#   tp=''
#   ide=0
#   for m in cursor:
#     #location = m[3]
#     up=m[5]
#     down=m[6]
#     tp=m[2]
#     ide=m[1]
#   #print(location)
#   myquery = {"location": location}
#   hosts = nr.filter(F(groups__contains="switch_group") & F(location='{}'.format(location)))
#   for a in hosts.inventory.hosts:
#     host = a
#   print("Validando disponibilidad de ancho de banda")
#   # se buscan los vecinos de ese switch y se guardan las interfaces que lo conectan
#   results = hosts.run(task=netmiko_send_command, command_string="show cdp neighbors", use_textfsm=True)
#   intl = ''
#   intn = ''
#   for c in results[host][0].result:
#     if c['neighbor'] == hosts.inventory.hosts[host].data["neighbor"] + '.prueba.com':
#       intl = c['local_interface']
#       intn = c['neighbor_interface']
#       break
#   intl = intl.replace('Eth ', 'Ethernet')
#   intn = intn.replace('Gig ', 'GigabitEthernet')
#   int_trunk_switch = intl
#   # Se busca la interfaz del vecino que conecta al switch, en router se guarda el documento de dicho vecino
#   neighbor = hosts.inventory.hosts[host].data["neighbor"]
#   router_name = neighbor
#   neighbordict = {'hostname': neighbor}
#   router = Rcol.find(neighbordict, {'int': 1})
#   # se busca y guarda el ancho de banda de la interfaz del vecino para comparar
#   bwr = 0
#   for g in router:
#       bwr = g['int'][intn]['bandwidth']
#   dwbw = False
#   if bwr > int(new_bw - down ):
#       dwbw = True
#   # se busca y se guarda el ancho de banda de la interfaz lcoal y se compara con el servicio
#   bws = 0
#   switchhostname = Scol.find(myquery, {'hostname': 1})
#   for h in switchhostname:
#       switch_name = h["hostname"]
#   switch = Scol.find(myquery, {'int': 1})
#   for x in switch:
#       intf = x
#   for c in intf['int'].items():
#       if c[0] == intl:
#           bws = c[1]['bandwidth']
#   upbw = False
#   if bws > int(new_bw - up):
#       upbw = True
#   if dwbw == False or upbw == False:
#       print("No existe ancho de banda disponible para brindar el servicio")
#       return False
#   bw_switch = new_bw
#   bw_router = new_bw
#   # se edita el archivo del switch
#   swfile = "configs" + str(id_servicio) + location + ".txt"
#   with open(swfile, "r") as f:
#       lines = f.readlines()
#   line = lines[5].split(" ")
#   line[2] = str(new_bw) + " \n"
#   lines[5] = " ".join(line)
#   new_lines = ""
#   for i in lines:
#       new_lines += i
#   with open(swfile, "w") as f:
#       f.write(new_lines)
#   # Se edita el archivo del router ce
#   rcefile = "configce" + str(id_servicio) + location + ".txt"
#   with open(rcefile, "r") as f:  #####
#       lines = f.readlines()
#   line = lines[2].split(" ")
#   line[2] = str(new_bw) + " \n"
#   lines[2] = " ".join(line)
#   new_lines = ""
#   lines[2] = " ".join(line)
#   new_lines = ""
#   for i in lines:
#       new_lines += i
#   with open(rcefile, "w") as f:
#       f.write(new_lines)
#   host = nr.filter(F(name=switch))
#   r = hosts.run(task=netmiko_send_config, config_file=swfile)
#   host = nr.filter(F(service_id=id_servicio) & F(location=location))
#   t = host.run(task=netmiko_send_config, config_file=rcefile)
#   print("############Su servicio ya se ha actualizado!!##############")
#   # Actualizacion de la base de datos
#   myquery = {"hostname": '{}'.format(router_name)}
#   # busca el router de la localidad y se actualiza la informacion en Mongo
#   routerint = Rcol.find(myquery, {'int': 1})
#   for h in routerint:
#       oldintf = h
#   newintf = copy.deepcopy(oldintf)
#   newbw = (oldintf['int'][intn[0:18]]['bandwidth'] + int(down)) - int(new_bw)
#   newintf['int'][intn[0:18]]['bandwidth'] = newbw
#   Rcol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=router_name))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[router_name][0].result
#   Rcol.update({'hostname': router_name}, {"$set": {'config': newconf}})
#
#   oldintf.clear()
#   newintf.clear()
#   # busca el switch de la localidad y se actualiza la informacion en Mongo
#   myquery = {"hostname": switch_name}
#   switchint = Scol.find(myquery, {'int': 1})
#   for a in switchint:
#       oldintf = a
#   newintf = copy.deepcopy(oldintf)
#   newbw = (oldintf['int'][intl]['bandwidth'] + int(up)) - int(new_bw)
#   newintf['int'][intl]['bandwidth'] = newbw
#   Scol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=switch_name))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[switch_name][0].result
#   Scol.update({'hostname': switch_name}, {"$set": {'config': newconf}})
#   # actualizando el registro en sql
#   cursor.execute("update Base_de_datos_proyecto.[dbo].[servicio] set up_bw = '{}', dw_bw='{}' where id = '{}'".format(new_bw, new_bw,
#                                                                                                         id_servicio))
#   cursor.commit()
#   return
#
# def update_service(id_servicio, cursor, up_bw, dw_bw):
#   print(id_servicio)
#   new_upbw= up_bw
#   new_dwbw= dw_bw
#   cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   #new_dwbw = input("Digite el nuevo ancho de banda de bajada (1M= 1000 Kbps): ")
#   #cursor.execute("SELECT * FROM proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   location = ''
#   up = 0
#   down = 0
#   tp = ''
#   ide = 0
#   for m in cursor:
#       location = m[3]
#       up = m[5]
#       down = m[6]
#       tp = m[2]
#       ide = m[1]
#   print(location)
#   myquery = {"location": location}
#   hosts = nr.filter(F(groups__contains="switch_group") & F(location='{}'.format(location)))
#   for a in hosts.inventory.hosts:
#       host = a
#   print("Validando disponibilidad de ancho de banda")
#   # se buscan los vecinos de ese switch y se guardan las interfaces que lo conectan
#   results = hosts.run(task=netmiko_send_command, command_string="show cdp neighbors", use_textfsm=True)
#   intl = ''
#   intn = ''
#   for c in results[host][0].result:
#       if c['neighbor'] == hosts.inventory.hosts[host].data["neighbor"] + '.prueba.com':
#           intl = c['local_interface']
#           intn = c['neighbor_interface']
#           break
#   intl = intl.replace('Fas ', 'FastEthernet')
#   intn = intn.replace('Fas ', 'FastEthernet')
#   int_trunk_switch = intl
#   # Se busca la interfaz del vecino que conecta al switch, en router se guarda el documento de dicho vecino
#   neighbor = hosts.inventory.hosts[host].data["neighbor"]
#   router_name = neighbor
#   neighbordict = {'hostname': neighbor}
#   router = Rcol.find(neighbordict, {'int': 1})
#   # print("Buscando ancho de banda del vecino")
#   # se busca y guarda el ancho de banda de la interfaz del vecino para comparar
#   bwr = 0
#   for g in router:
#       bwr = g['int'][intn[0:15]]['bandwidth']
#   dwbw = False
#   if bwr > int(new_dwbw - down):
#       dwbw = True
#   # se busca y se guarda el ancho de banda de la interfaz lcoal y se compara con el servicio
#   bws = 0
#   switchhostname = Scol.find(myquery, {'hostname': 1})
#   routerhostname= Rcol.find(myquery, {'hostname': 1})
#   for h in switchhostname:
#       switch_name = h["hostname"]
#   for f in routerhostname:
#       router_name = f["hostname"]
#   switch = Scol.find(myquery, {'int': 1})
#   for x in switch:
#       intf = x
#   for c in intf['int'].items():
#       intf = x
#   for c in intf['int'].items():
#       if c[0] == intl:
#           bws = c[1]['bandwidth']
#   upbw = False
#   if bws > int(new_upbw - up):
#       upbw = True
#   if dwbw == False or upbw == False:
#       print("No existe ancho de banda disponible para brindar el servicio")
#       return False
#   bw_switch = new_upbw
#   bw_router = new_dwbw
#   # se edita el archivo del switch
#   swfile = "configs" + str(id_servicio) + location + ".txt"
#   with open(swfile, "r") as f:
#       lines = f.readlines()
#   line = lines[5].split(" ")
#   line[1] = str(new_upbw * 1000)
#   lines[5] = " ".join(line)
#   new_lines = ""
#   for i in lines:
#       new_lines += i
#   with open(swfile, "w") as f:
#       f.write(new_lines)
#   # Se edita el archivo del router pe
#   rfile = "configr" + str(id_servicio) + location + ".txt"
#   with open(rfile, "r") as f:
#       lines = f.readlines()
#   line = lines[2].split(" ")
#   line[1] = str(new_dwbw * 1000)
#   lines[2] = " ".join(line)
#   new_lines = ""
#   for i in lines:
#       new_lines += i
#   with open(rfile, "w") as f:
#       f.write(new_lines)
#   host = nr.filter(F(name=switch))
#   r = hosts.run(task=netmiko_send_config, config_file=swfile)
#   print(router_name, location)
#   host = nr.filter(F(name=router_name) & F(location=location))
#   print(hosts.inventory.hosts.keys())
#   print(host.inventory.hosts.keys())
#   t = host.run(task=netmiko_send_config, config_file=rfile)
#   # # Se edita el archivo del router ce
#   # rcefile = "configce" + str(id_servicio) + location + ".txt"
#   # with open(rcefile, "r") as f:
#   #     lines = f.readlines()
#   # line = lines[2].split(" ")
#   # line[2] = str(new_upbw) + " \n"
#   # lines[2] = " ".join(line)
#   # new_lines = ""
#   # for i in lines:
#   #     new_lines += i
#   # with open(rcefile, "w") as f:
#   #     f.write(new_lines)
#   # host = nr.filter(F(name=switch))
#   # r = hosts.run(task=netmiko_send_config, config_file=swfile)
#   # host = nr.filter(F(service_id=id_servicio) & F(location=location))
#   # t = host.run(task=netmiko_send_config, config_file=rcefile)
#   print("############Su servicio ya esta configurado!!##############")
#   # Actualizacion de la base de datos
#   myquery = {"hostname": '{}'.format(router_name)}
#   # busca el router de la localidad y se actualiza la informacion en Mongo
#   routerint = Rcol.find(myquery, {'int': 1})
#   for h in routerint:
#       oldintf = h
#   newintf = copy.deepcopy(oldintf)
#   newbw = (oldintf['int'][intn[0:15]]['bandwidth'] + int(down)) - int(new_dwbw)
#   newintf['int'][intn[0:15]]['bandwidth'] = newbw
#   Rcol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=router_name))
#   Rcol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=router_name))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[router_name][0].result
#   Rcol.update({'hostname': router_name}, {"$set": {'config': newconf}})
#
#   oldintf.clear()
#   newintf.clear()
#   # busca el switch de la localidad y se actualiza la informacion en Mongo
#   myquery = {"hostname": switch_name}
#   switchint = Scol.find(myquery, {'int': 1})
#   for a in switchint:
#       oldintf = a
#   newintf = copy.deepcopy(oldintf)
#   newbw = (oldintf['int'][intl]['bandwidth'] + int(up)) - int(new_upbw)
#   newintf['int'][intl]['bandwidth'] = newbw
#   Scol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=switch_name))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[switch_name][0].result
#   Scol.update({'hostname': switch_name}, {"$set": {'config': newconf}})
#   # actualizando el registro en sql
#   cursor.execute(
#       "update Base_de_datos_proyecto.[dbo].[servicio] set up_bw = '{}', dw_bw='{}' where id = '{}'".format(new_upbw, new_dwbw,
#                                                                                              id_servicio))
#   cursor.commit()
#   notificacion = Notificacion(id_servicio= id_servicio, tipo_not="Servicio",
#                               des="Se ha completado el upgrade del servicio con id: " + str(id_servicio),
#                               checked=False,
#                               fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   return "se actualizo"
#
# def delete_l2vpn_service(id_servicio, cursor, location):
#   cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   #location=''
#   ide=id_servicio
#   tp= ''
#   upbw=0
#   dwbw=0
#   for m in cursor:
#    # location = m[3]
#     tp= m[2]
#     upbw=m[5]
#     dwbw=m[6]
#   #para cada location repetir todo
#   myquery = {"location": location}
#   mypoolquery= {"location": location, "service": tp}
#   #busca el switch de la localidad
#   switchhostname = Scol.find(myquery, {'hostname': 1})
#   swname=''
#   rname=''
#   for i in switchhostname:
#     swname = i['hostname']
#   routerhostname = Rcol.find(myquery, {'hostname': 1})
#   for j in routerhostname:
#     rname= j['hostname']
#   rfile= "configr"+str(id_servicio)+str(location) + ".txt"
#   sfile= "configs"+str(id_servicio)+str(location) + ".txt"
#   #print(swname, rname)
#   rintf = ''
#   if tp == "L2vpn":
#       # print(swname, rname)
#       if tp == "L2vpn":
#           with open(sfile, "r") as f:
#               lines = f.readlines()
#           count = 0
#           newfile = ''
#           for line in lines:
#               if count in [0, 3, 7, 8, 9]:
#                   newfile += "no " + line
#               elif count in [2, 10]:
#                   newfile += line.replace("add", "remove")
#               elif count in [4, 5]:
#                   pass
#               else:
#                   newfile += line
#               count += 1
#           with open("delete_" + sfile, "w") as f:
#               f.write(newfile)
#           host = nr.filter(F(name=swname))
#           r = host.run(task=netmiko_send_config, config_file="delete_" + sfile)
#           newfile2 = ''
#           with open(rfile, "r") as f:
#               lines = f.readlines()
#           newfile2 += "no " + lines[0]
#           # borrando el vc_id de mongo
#           vc = int(lines[2].split(" ")[2])
#           lastid = Vcol.find({}, {'vc_id': 1})
#           all_id = []
#           olddic = []
#           for f in lastid:
#               all_id = f["vc_id"]
#               olddic = copy.deepcopy(all_id)
#           all_id[vc] = 0
#           Vcol.update_one({"vc_id": olddic}, {"$set": {"vc_id": all_id}})
#
#           rintf = lines[0].split(" ")[-1].replace(".", ",").strip()
#           with open("delete_" + rfile, "w") as f:
#               f.write(newfile2)
#           host = nr.filter(F(name=rname))
#           r = host.run(task=netmiko_send_config, config_file="delete_" + rfile)
#       # querys
#       pool = Pcol.find(mypoolquery, {'pool': 1})
#       rints_objects = Rcol.find({'hostname': rname}, {'int': 1})
#       rints = []
#       for x in pool:
#           thispool = x
#       for d in rints_objects:
#           rints = d
#       # aqui se libera el pool
#       for a, b in thispool['pool'].items():
#           if (b['id_service'] == str(id_servicio)):
#               finalpool = a
#               olddic = thispool
#               finalpool = a
#               olddic = thispool
#               newdic = copy.deepcopy(olddic)
#               newdic['pool'][finalpool]['available'] = True
#               newdic['pool'][finalpool]['id_service'] = ''
#               Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#               break
#       # aqui se actualiza el ancho de banda de subida y se elimina la subinterfaz
#       for y in rints['int'].items():
#           if (y[0] == rintf[0:18]):
#               bw = y[1]['bandwidth'] + dwbw
#               newintf = copy.deepcopy(rints)
#               newintf['int'][rintf[0:18]]['bandwidth'] = bw
#               Rcol.update_one({'int': rints['int']}, {"$set": {'int': newintf['int']}})
#           if (rintf == y[0]):
#               Rcol.update({'hostname': rname}, {"$unset": {"int." + rintf: 1}})
#       swints_objects = Scol.find({'hostname': swname}, {'int': 1})
#       for t in swints_objects:
#           swints = t
#       newintf = copy.deepcopy(swints)
#       with open("delete_" + sfile, "r") as f:
#           lines = f.readlines()
#       swintf = lines[1].split(" ")[-1].strip()
#       sw_client_int = lines[4].split(" ")[-1].strip()
#       for i in swints['int'].items():
#           if (i[0] == swintf):
#               bw = i[1]['bandwidth'] + upbw
#               newintf['int'][swintf]['bandwidth'] = bw
#           if (i[0] == sw_client_int):
#               newintf['int'][sw_client_int]['available'] = True
#       Scol.update_one({'int': swints['int']}, {"$set": {'int': newintf['int']}})
#       # actualizar el registro a inactivo en sql
#       cursor.execute("update Base_de_datos_proyecto.[dbo].[servicio] set active='{}' where id = '{}'".format(False, id_servicio))
#       cursor.commit()
#       return
#
# def delete_service(id_servicio, cursor):
#   cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   location=''
#   ide=id_servicio
#   tp= ''
#   upbw=0
#   dwbw=0
#   for m in cursor:
#     print(m)
#     location = m[3]
#     tp= m[2]
#     upbw=m[5]
#     dwbw=m[6]
#   #para cada location repetir todo
#   myquery = {"location": location}
#   mypoolquery= {"location": location, "service": tp}
#   #busca el switch de la localidad
#   switchhostname = Scol.find(myquery, {'hostname': 1})
#   swname=''
#   rname=''
#   for i in switchhostname:
#     swname = i['hostname']
#   routerhostname = Rcol.find(myquery, {'hostname': 1})
#   for j in routerhostname:
#     rname= j['hostname']
#   rfile="configr"+str(id_servicio)+str(location) + ".txt"
#   sfile= "configs"+str(id_servicio)+str(location) + ".txt"
#   rintf = ''
#   #print(swname, rname)
#   if tp == "Internet":
#     with open(sfile, "r") as f:
#       lines = f.readlines()
#     count=0
#     newfile=''
#     for line in lines:
#       if count in [0,3,8,9]:
#         newfile += "no "+ line
#       elif count == 2:
#         newfile+=line.replace("add", "remove")
#       elif count in [4,5,7]:
#         pass
#       else:
#         newfile+=line
#       count+= 1
#     with open("delete_"+sfile, "w") as f:
#         count += 1
#         with open("delete_" + sfile, "w") as f:
#             f.write(newfile)
#         host = nr.filter(F(name=swname))
#         r = host.run(task=netmiko_send_config, config_file="delete_" + sfile)
#         newfile2 = ''
#         with open(rfile, "r") as f:
#             lines = f.readlines()
#         newfile2 += "no " + lines[0]
#         newfile2 += "no " + lines[3]
#         rintf = lines[3].split(" ")[-1].replace(".", ",").strip()
#         with open("delete_" + rfile, "w") as f:
#             f.write(newfile2)
#         host = nr.filter(F(name=rname))
#         r = host.run(task=netmiko_send_config, config_file="delete_" + rfile)
#     # querys
#   pool = Pcol.find(mypoolquery, {'pool': 1})
#   rints_objects = Rcol.find({'hostname': rname}, {'int': 1})
#   rints = []
#   thispool=[]
#   for x in pool:
#       print(x)
#       thispool = x
#   for d in rints_objects:
#       rints = d
#   print(thispool)
#   # aqui se libera el pool
#   for a, b in thispool['pool'].items():
#       if (b['id_service'] == str(id_servicio)):
#           finalpool = a
#           olddic = thispool
#           newdic = copy.deepcopy(olddic)
#           newdic['pool'][finalpool]['available'] = True
#           newdic['pool'][finalpool]['id_service'] = ''
#           Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#           break
#   # aqui se actualiza el ancho de banda de subida y se elimina la subinterfaz
#   print(rintf)
#   for y in rints['int'].items():
#       if (y[0] == rintf[0:15]):
#           bw = y[1]['bandwidth'] + dwbw
#           newintf = copy.deepcopy(rints)
#           newintf['int'][rintf[0:15]]['bandwidth'] = bw
#           Rcol.update_one({'int': rints['int']}, {"$set": {'int': newintf['int']}})
#       if (rintf == y[0]):
#           Rcol.update({'hostname': rname}, {"$unset": {"int." + rintf: 1}})
#   swints_objects = Scol.find({'hostname': swname}, {'int': 1})
#   for t in swints_objects:
#       swints = t
#   newintf = copy.deepcopy(swints)
#   with open("delete_" + sfile, "r") as f:
#       lines = f.readlines()
#   swintf = lines[1].split(" ")[-1].strip()
#   sw_client_int = lines[4].split(" ")[-1].strip()
#   print(sw_client_int)
#   print(swints['int'])
#
#   for i in swints['int'].items():
#       # if (i[0] == swintf):
#       #   bw = i[1]['bandwidth'] + upbw
#       if (i[0] == swintf):
#           bw = i[1]['bandwidth'] + upbw
#           newintf['int'][swintf]['bandwidth'] = bw
#       if (i[0] == sw_client_int):
#           print(newintf['int'][sw_client_int]['available'])
#           newintf['int'][sw_client_int]['available'] = True
#           print(newintf['int'][sw_client_int]['available'])
#   print(newintf['int'])
#   Scol.update_one({'int': swints['int']}, {"$set": {'int': newintf['int']}})
#   # actualizar el registro a inactivo en sql
#   cursor.execute("update Base_de_datos_proyecto.[dbo].[servicio] set active='{}' where id = '{}'".format(False, id_servicio))
#   cursor.commit()
#   return
#
# def adddevice(name,ip,location, id_servicio):
#   with open('/home/ubuntu/Desktop/Proyecto_final/Web/hosts.yaml') as f:
#       data = yaml.load(f, Loader=yaml.FullLoader)
#   data[name]={
#   "hostname":ip,
#   "platform":'ios',
#   "username":'admin',
#   "password":'cisco',
#   "groups":['cisco_group', 'router_group'],
#   "data":{"domain": 'prueba.com',
#           "location":location,
#           "typ":'ce',
#           "ip":ip,
#           "service_id":id_servicio}
#   }
#   with open('/home/ubuntu/Desktop/Proyecto_final/Web/hosts.yaml', 'w') as f:
#       yaml.dump(data, f, explicit_start=True)
#
# def validatel2vpn(id_servicio, cursor, loc):
#     notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Servicio",
#                                 des="Ha comenzado el proceso de validacion del servicio con id: " + str(id_servicio),
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#     db.session.add(notificacion)
#     # Servicio.query.filter_by(id=services[id].id).delete()
#     db.session.commit()
#     dic = {
#         "id_servicio": "",
#         "switch": "",
#         "int_switch": "",
#         "int_trunk_switch": "",
#         "bw_switch": "",
#         "servicevlan": "",
#         "router": "",
#         "routerce": "",
#         "int_router": "",
#         "bw_router": "",
#         "vc_id": "",
#         "ip_adm_loc": "",
#         "ip_ce": ""}
#     dic["id_servicio"] = id_servicio
#     cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#     tp = ''
#     for m in cursor:
#         tp = m[2]
#     location = loc
#     myquery = {"location": location}
#     mypoolquery = {"location": location, "service": tp}
#     print("Validando interfaces")
#     # busca el switch de la localidad
#     switchhostname = Scol.find(myquery, {'hostname': 1})
#     int_av = False
#     # print(switchhostname)
#     for h in switchhostname:
#         dic["switch"] = h["hostname"]
#     switch = Scol.find(myquery, {'int': 1})
#     for x in switch:
#         intf = x
#     for y, j in intf['int'].items():
#         if (j['available'] == True):
#             interfaz = y
#             int_av = True
#             dic["int_switch"] = interfaz
#             break
#     if int_av == False:
#         print("No hay interfaces disponibles para dar el servicio")
#         return False
#     print("Validando vlans")
#     # se conecta al switch y se busca una vlan disponible
#     vlan_av = False
#     hosts = nr.filter(F(groups__contains="switch_group") & F(location='{}'.format(location)))
#     host=''
#     for a in hosts.inventory.hosts:
#         host = a
#     results = hosts.run(task=netmiko_send_command, command_string="show vlan", use_textfsm=True)
#     vlans = []
#     for b in results[host][0].result:
#         try:
#             vlans.append(b["vlan_id"])
#         except (TypeError):
#             return "No se pudo conectar al switch de la zona"
#     vlanid = ''
#     for i in range(2, 4095):
#         if str(i) not in vlans:
#             vlanid = str(i)
#             vlan_av = True
#             break
#     if vlan_av == False:
#         print("No existen vlan's disponibles para dar el servicio")
#         return False
#     print("Validando ancho de banda")
#     # print("Buscando sus vecinos")
#     # se buscan los vecinos de ese switch y se guardan las interfaces que lo conectan
#     results = hosts.run(task=netmiko_send_command, command_string="show cdp neighbors", use_textfsm=True)
#     intl = ''
#     intn = ''
#     for c in results[host][0].result:
#         if c['neighbor'] == hosts.inventory.hosts[host].data["neighbor"] + '.prueba.com':
#             intl = c['local_interface']
#             intn = c['neighbor_interface']
#             break
#     intl = intl.replace('Eth ', 'Ethernet')
#     intn = intn.replace('Gig ', 'GigabitEthernet')
#     dic["int_trunk_switch"] = intl
#     dic["int_router"] = intn + "." + vlanid
#     dic["servicevlan"] = vlanid
#     # Se busca la interfaz del vecino que conecta al switch, en router se guarda el documento de dicho vecino
#     neighbor = hosts.inventory.hosts[host].data["neighbor"]
#     dic["router"] = neighbor
#     neighbordict = {'hostname': neighbor}
#     router = Rcol.find(neighbordict, {'int': 1})
#     # print("Buscando ancho de banda del vecino")
#     # se busca y guarda el ancho de banda de la interfaz del vecino para comparar
#     bwr = 0
#     for g in router:
#         bwr = g['int'][intn]['bandwidth']
#     dwbw = False
#     if bwr > m[6]:
#         dwbw = True
#     # print("Buscando ancho de banda local")
#     # se busca y se guarda el ancho de banda de la interfaz lcoal y se compara con el servicio
#     bws = 0
#     for c in intf['int'].items():
#         if c[0] == intl:
#             bws = c[1]['bandwidth']
#     upbw = False
#     if bws > m[5]:
#         upbw = True
#     if dwbw == False or upbw == False:
#         print("No existe ancho de banda disponible para brindar el servicio")
#         return False
#     # print("Si, se puede dar el servicio con id: {} ".format(m[0]))
#     dic["bw_switch"] = m[5]
#     dic["bw_router"] = m[6]
#     # Busca un circuito virtual disponible
#     hosts = nr.filter(F(groups__contains="router_group") & F(location='{}'.format(location)))
#     for d in hosts.inventory.hosts:
#         hosts_a_name = d
#     dic["ip_adm_loc"] = nr.inventory.hosts[hosts_a_name]['ip']
#     # Se busca la disponibilidad de Ip's
#     print("Validando disponibilidad de ip's")
#     pool = Pcol.find(mypoolquery, {'pool': 1})
#     for x in pool:
#         thispool = x
#     ip_av = False
#     # print(thispool)
#     for a, b in thispool['pool'].items():
#         if (b['available'] == True):
#             finalpool = a
#             ip_av = True
#             dic["ip_ce"] = b['ip1']
#             dic["mask"] = b['mask']
#             olddic = thispool
#             newdic = copy.deepcopy(olddic)
#             newdic['pool'][finalpool]['available'] = False
#             newdic['pool'][finalpool]['id_service'] = str(id_servicio)
#             # print(olddic)
#             # print('#######')
#             # print(newdic)
#             Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#             break
#         # dic['ip_loc'] = input(
#         #      "Ingrese la ip y mascara que desea utilizar para la localidad " + location + "ej: X.X.X.X X.X.X.X ")
#     #dic['ip_loc'] = "10.0.0.2 255.255.255.0"
#     dic['routerce'] = dic['router'].replace('P', 'C') + "_" + dic['int_switch'][-3:]
#     print(dic)
#     adddevice(dic['router'].replace('P', 'C') + "_" + dic['int_switch'][-3:], dic['ip_ce'], location, id_servicio)
#     notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Servicio",
#                                 des="El proceso de configuracion del servicio con id: " + str(id_servicio) + " ha terminado",
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#     db.session.add(notificacion)
#     # Servicio.query.filter_by(id=services[id].id).delete()
#     db.session.commit()
#     return dic
#
# def validateint(id_servicio, cursor):
#   notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Servicio",
#                                 des="Ha comenzado el proceso de validacion del servicio " + str(id_servicio),
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   dic = {
#   "id_servicio": "",
#   "switch": "",
#   "int_switch": "",
#   "int_trunk_switch": "",
#   "bw_switch": "",
#   "servicevlan": "",
#   "router": "",
#   "routerce":"",
#   "int_router": "",
#   "bw_router": "",
#   "ip_pe":"",
#   "ip_ce":"",
#   "mask":""}
#   dic["id_servicio"] = id_servicio
#   cursor.execute("SELECT * FROM Base_de_datos_proyecto.[dbo].[servicio] WHERE id = '{}'".format(id_servicio))
#   location = ''
#   up=0
#   down=0
#   tp=''
#   ide=0
#   for m in cursor:
#     location = m[3]
#     up=m[5]
#     down=m[6]
#     tp=m[2]
#     ide=m[1]
#     print(" ")
#     print(" ")
#     print("      El cliente con id " +str(ide))
#     print("      desea contratar y configurar un servicio de " + tp )
#     print("      en la zona " + location )
#     print("      con una velocidad de subida de " + str(up) + "Kbps")
#     print("      y con una velocidad de bajada de " + str(down)+ "Kbps")
#     print(" ")
#     print(" ")
#   #print("El cliente con id " +str(ide)+ " desea contratar y configurar un servicio de " + tp + " en la zona "+ location+ " con una velocidad de " + str(up) +" Kbps de subida y "+ str(down) + " Kbps de bajada.")
#   myquery = {"location": location}
#   mypoolquery = {"location": location, "service": tp}
#   print("Validando interfaces")
#   # busca el switch de la localidad
#   switchhostname = Scol.find(myquery, {'hostname': 1})
#   int_av = False
#   print(switchhostname)
#   for h in switchhostname:
#       dic["switch"] = h["hostname"]
#   switch = Scol.find(myquery, {'int': 1})
#   for x in switch:
#       intf = x
#   for y, j in intf['int'].items():
#       if (j['available'] == True):
#           interfaz = y
#           int_av = True
#           dic["int_switch"] = interfaz
#           break
#   if int_av == False:
#       notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existen interfaces disponibles",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y"))+" "+str(time.strftime("%I:%M:%S")))
#       db.session.add(notificacion)
#       db.session.commit()
#       skwargs = {'id': dic["id_servicio"]}
#       services = Servicio.query.filter_by(**skwargs).first()
#       services.in_progress = False
#       print("No hay interfaces disponibles para dar el servicio")
#       return False
#   print("Validando vlans")
#   # se conecta al switch y se busca una vlan disponible
#   vlan_av = False
#   host=''
#   hosts = nr.filter(F(groups__contains="switch_group") & F(location='{}'.format(location)))
#   for a in hosts.inventory.hosts:
#       host = a
#       print(host)
#   try:
#       results = hosts.run(task=netmiko_send_command, command_string='show vlan', use_textfsm=True)
#       #nr.close_connections()
#   except(NetMikoTimeoutException) as e:
#       notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existe comunicacion con el switch" + str(
#                                       host) + "de la zona ",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#       db.session.add(notificacion)
#       db.session.commit()
#       skwargs = {'id': dic["id_servicio"]}
#       services = Servicio.query.filter_by(**skwargs).first()
#       services.in_progress = False
#       return "Fallo la conexion a los equipos: " + str(host)
#   vlans = []
#   if host not in results:
#       skwargs = {'id': dic["id_servicio"]}
#       services = Servicio.query.filter_by(**skwargs).first()
#       services.in_progress = False
#       notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existe comunicacion con el switch" + str(
#                                       host) + "de la zona ",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#       db.session.add(notificacion)
#       db.session.commit()
#       return "Fallo la conexion a los equipos: " + str(host)
#   for b in results[host][0].result:
#       try:
#           vlans.append(b["vlan_id"])
#       except (TypeError):
#           notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Recurso",
#                                       des="no se pudo configurar debido a que no se ha podido establecer conexión con el switch la zona",
#                                       checked=False,
#                                       fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#           db.session.add(notificacion)
#           db.session.commit()
#           skwargs = {'id': dic["id_servicio"]}
#           services = Servicio.query.filter_by(**skwargs).first()
#           services.in_progress = False
#           return "No se pudo conectar al switch de la zona"
#   vlanid = ''
#   for i in range(2, 4095):
#       if str(i) not in vlans:
#           vlanid = str(i)
#           vlan_av = True
#           break
#   if vlan_av == False:
#       notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existen vlans disponibles en la zona",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#       db.session.add(notificacion)
#       db.session.commit()
#       skwargs = {'id': dic["id_servicio"]}
#       services = Servicio.query.filter_by(**skwargs).first()
#       services.in_progress = False
#       print("No existen vlan's disponibles para dar el servicio")
#       return False
#   print("Validando disponibilidad de ancho de banda")
#   # se buscan los vecinos y se verifican las interfaces
#   try:
#       results = hosts.run(task=netmiko_send_command, command_string="show cdp neighbors", use_textfsm=True)
#       #nr.close_connections()
#   except(NetMikoTimeoutException) as e:
#       notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existe comunicacion con el switch" + str(
#                                       host) + "de la zona ",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#       db.session.add(notificacion)
#       db.session.commit()
#       skwargs = {'id': dic["id_servicio"]}
#       services = Servicio.query.filter_by(**skwargs).first()
#       services.in_progress = False
#       return "Fallo la conexion a los equipos: " + str(host)
#   intl = ''
#   intn = ''
#   for c in results[host][0].result:
#       if c['neighbor'] == hosts.inventory.hosts[host].data["neighbor"] + '.prueba.com':
#           intl = c['local_interface']
#           intn = c['neighbor_interface']
#   intl = intl.replace('Fas ', 'FastEthernet')
#   intn = intn.replace('Fas ', 'FastEthernet')
#   dic["int_trunk_switch"] = intl
#   dic["int_router"] = intn + "." + vlanid
#   dic["servicevlan"] = vlanid
#   #Se busca la interfaz del vecino que conecta al switch, en router se guarda el documento de dicho vecino
#   neighbor = hosts.inventory.hosts[host].data["neighbor"]
#   dic["router"] = neighbor
#   neighbordict = {'hostname': neighbor}
#   router = Rcol.find(neighbordict, {'int': 1})
#   # se busca y guarda el ancho de banda de la interfaz del vecino para comparar
#   bwr = 0
#   for g in router:
#     bwr = g['int'][intn]['bandwidth']
#   dwbw = False
#   if bwr > m[6]:
#    dwbw = True
#   #se busca y se guarda el ancho de banda de la interfaz local y se compara con el servicio
#   bws = 0
#   for c in intf['int'].items():
#     if c[0] == intl:
#       bws = c[1]['bandwidth']
#   upbw = False
#   if bws > m[5]:
#     upbw = True
#   if dwbw == False or upbw == False:
#     notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Recurso",
#                                   des="no se pudo configurar debido a que no existe ancho de banda disponible en la zona ",
#                                   checked=False,
#                                   fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#     db.session.add(notificacion)
#     db.session.commit()
#     skwargs = {'id': dic["id_servicio"]}
#     services = Servicio.query.filter_by(**skwargs).first()
#     services.in_progress = False
#     print("No existe ancho de banda disponible para brindar el servicio")
#     return False
#   dic["bw_switch"] = m[5]
#   dic["bw_router"] = m[6]
#   print("Validando disponibilidad de ip's")
#   pool = Pcol.find(mypoolquery, {'pool': 1})
#   for x in pool:
#     thispool = x
#   ip_av=False
#   for a, b in thispool['pool'].items():
#     if (b['available'] == True):
#       finalpool = a
#       ip_av = True
#       dic["ip_pe"] = b['ip1']
#       dic["ip_ce"] = b['ip2']
#       dic["mask"] = b['mask']
#       olddic = thispool
#       newdic = copy.deepcopy(olddic)
#       newdic['pool'][finalpool]['available'] = False
#       newdic['pool'][finalpool]['id_service'] = str(id_servicio)
#       Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#       break
#     else:
#         notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Recurso",
#                                     des="No existen IPs disponibles para dar el servicio en la zona ",
#                                     checked=False,
#                                     fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#         db.session.add(notificacion)
#         db.session.commit()
#         skwargs = {'id': dic["id_servicio"]}
#         services = Servicio.query.filter_by(**skwargs).first()
#         services.in_progress = False
#         print("No existen IPs disponibles para dar el servicio")
#         return False
#   dic['routerce']=dic['router'].replace('P','C')+ "_" + dic['int_switch'][-3:]
#   #adddevice(dic['router'].replace('P','C')+ "_" + dic['int_switch'][-3:],dic['ip_ce'],location, id_servicio)
#   notificacion = Notificacion(id_servicio=id_servicio, tipo_not="Servicio",
#                               des="El proceso de validacion del servicio con id: " + str(id_servicio) + " ha sido completado",
#                               checked=False,
#                               fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   return dic
#
# def configint(side,cursor, **dic):
#   notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Servicio",
#                                 des="El proceso de configuracion del servicio con id: " + str(dic['id_servicio']) + " ha comenzado",
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   global oldintf
#   #nr=InitNornir(config_file="config.yaml")
#   mypoolquery= {"location": side, "service": "internet"}
#   dic["bw_router"] = int(dic["bw_router"]) * 1000
#   dic["bw_switch"] = int(dic["bw_switch"]) * 1000
#
#   #burst size
#   rburst_size=round((int(dic["bw_router"])/1000) * 5)
#   sburst_size = round((int(dic["bw_switch"])/1000) * 5)
#   print(rburst_size)
#   print(sburst_size)
#   templatesw = jinja2.Template(
#                             "vlan {{a['servicevlan']}}\n"
#                             "interface {{a['int_trunk_switch']}}\n"
#                             "switchport trunk allowed vlan add {{a['servicevlan']}}\n"
#                             "policy-map {{ a['id_servicio'] }} \n"
#                             "class class-default \n"
#                             "police {{ a['bw_switch'] }} " + str(sburst_size) + "\n"
#                             "interface {{ a['int_switch'] }}\n"
#                             "service-policy input {{ a['id_servicio'] }}\n"
#                             "switchport mode access \n"
#                             "switchport access vlan {{a['servicevlan']}}\n")
#
#   templater = jinja2.Template("policy-map {{ a['id_servicio'] }} \n"
#                               "class class-default \n"
#                               "police {{ a['bw_router'] }} " + str(rburst_size) + "\n"
#                               "interface {{ a['int_router'] }}\n"
#                               "encapsulation dot1Q {{a['servicevlan']}} \n"
#                               "ip address {{a['ip_pe']}} {{a['mask']}} \n"
#                               "service-policy output {{ a['id_servicio'] }}\n")
#
# ##########ESTO CREEEEO QUE SE PUEDE QUITAR##########
#   templatece = jinja2.Template("policy-map {{ a['id_servicio'] }} \n"
#                               "class class-default \n"
#                               "shape average {{ a['bw_switch'] }} \n"
#                               "interface FastEthernet 0/0 \n"
#                               "service-policy output {{ a['id_servicio'] }}\n")
#
#   output = templatesw.render(a = dic)
#   swfile="configs" +str(dic['id_servicio']) + side + ".txt"
#   file= open(swfile,"w+")
#   file.write(output)
#   file.close()
#   output = templater.render(a = dic)
#   rfile="configr" + str(dic['id_servicio']) + side + ".txt"
#   file= open(rfile,"w+")
#   file.write(output)
#   file.close()
#   output = templatece.render(a = dic)
#   #rcefile= "configce"+ str(dic['id_servicio']) + side + ".txt"
#   #file= open(rcefile,"w+")
#   #file.write(output)
#   #file.close()
#   print(" ")
#   print(" ")
#   print("      Aviso para el administrador: se esta configurando un servicio ")
#   print("      favor correr el siguiente script y enviar al cliente su equipo de borde." )
#   print("      el script solo contiene la configuracion de habilitar SSH y la siguiente IP en la interfaz G0/0: " + dic["ip_ce"] )
#   print("      Nota: el equipo de borde va conectado a la interfaz "+ dic["int_switch"])
#   print(" ")
#   print(" ")
#   print('####Cliente: Conectar el equipo y encenderlo##########')
#   print(" ")
#   trigg= 'ya'
#   if trigg == 'ya':
#       # se configura el router del side correspondiente
#       hostr = nr.filter(F(name=dic['router']))
#       hosts = nr.filter(F(name=dic['switch']))
#       hostce = nr.filter(F(name=dic['routerce']))
#       try:
#           r = hostr.run(task=netmiko_send_config, config_file=rfile)
#           #nr.close_connections()
#           print("se configuro el p")
#       except(NetMikoTimeoutException) as e:
#           notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Recurso",
#                                       des="no se pudo configurar debido a que no existe comunicacion con el router" + str(dic["router"])+ "de la zona ",
#                                       checked=False,
#                                       fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#           db.session.add(notificacion)
#           db.session.commit()
#           skwargs = {'id': dic["id_servicio"]}
#           services = Servicio.query.filter_by(**skwargs).first()
#           services.in_progress = False
#           return "Fallo la conexion a los equipos: " + str(dic["router"])
#       try:
#           r = hosts.run(task=netmiko_send_config, config_file=swfile)
#           #nr.close_connections()
#           print("se configuro el sw")
#       except (NetMikoTimeoutException) as e:
#           newfile2 = ''
#           with open(rfile, "r") as f:
#               lines = f.readlines()
#           newfile2 += "no " + lines[0]
#           rintf = lines[0].split(" ")[-1].replace(".", ",").strip()
#           with open("delete_" + rfile, "w") as f:
#               f.write(newfile2)
#           r = hostr.run(task=netmiko_send_config, config_file="delete_" + rfile)
#           #nr.close_connections()
#           pool = Pcol.find(mypoolquery, {'pool': 1})
#           for x in pool:
#               thispool = x
#           for a, b in thispool['pool'].items():
#               if (b['id_service'] == str(dic['id_servicio'])):
#                   finalpool = a
#                   olddic = thispool
#                   newdic = copy.deepcopy(olddic)
#                   newdic['pool'][finalpool]['available'] = True
#                   newdic['pool'][finalpool]['id_service'] = ''
#                   Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#           notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Recurso",
#                                       des="no se pudo configurar debido a que no existe comunicacion con el router" + str(dic["switch"]) + "de la zona ",
#                                       checked=False,
#                                       fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#           db.session.add(notificacion)
#           db.session.commit()
#           skwargs = {'id': dic["id_servicio"]}
#           services = Servicio.query.filter_by(**skwargs).first()
#           services.in_progress = False
#           return "Fallo la conexion a los equipos: " + str(dic["switch"])
#       #time.sleep(3)
#       #try:
#       #    t = hostce.run(task=netmiko_send_config, config_file=rcefile)
#       #    print("se configuro el ce")
#       #except (NetmikoTimeoutException) as e:
#           # with open(swfile, "r") as f:
#           #     lines = f.readlines()
#           # count = 0
#           # newfile = ''
#           # for line in lines:
#           #     if count in [0, 3, 8, 9]:
#           #         newfile += "no " + line
#           #     elif count == 2:
#           #         newfile += line.replace("add", "remove")
#           #     elif count in [4, 5, 7]:
#           #         pass
#           #     else:
#           #         newfile += line
#           #         count += 1
#           #     with open("delete_" + swfile, "w") as f:
#           #         f.write(newfile)
#           #     r = hosts.run(task=netmiko_send_config, config_file="delete_" + swfile)
#           #     newfile2 = ''
#           #     with open(rfile, "r") as f:
#           #         lines = f.readlines()
#           #     newfile2 += "no " + lines[0]
#           #     rintf = lines[0].split(" ")[-1].replace(".", ",").strip()
#           #     with open("delete_" + rfile, "w") as f:
#           #         f.write(newfile2)
#           #     r = hostr.run(task=netmiko_send_config, config_file="delete_" + rfile)
#           #     pool = Pcol.find(mypoolquery, {'pool': 1})
#           #     for x in pool:
#           #         thispool = x
#           #     for a, b in thispool['pool'].items():
#           #         if (b['id_service'] == str(dic['id_servicio'])):
#           #             finalpool = a
#           #             olddic = thispool
#           #             newdic = copy.deepcopy(olddic)
#           #             newdic['pool'][finalpool]['available'] = True
#           #             newdic['pool'][finalpool]['id_service'] = ''
#           #             Pcol.update_one({'pool': olddic['pool']}, {"$set": {'pool': newdic['pool']}})
#           #     return "Fallo la conexion a los equipos: " + str(dic["switch"])
#   notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Servicio",
#                               des="Se debe configurar la siguiente ip en el router del cliente:"+ dic["ip_ce"]+ "/30 " + "GW: " + dic["ip_pe"] +  " y enviar el equipo." + "\n                                El equipo de borde va conectado en la interfaz: " + dic["int_switch"] + "\n                                se ha configurado exitosamente el servicio con id " + str(dic['id_servicio']),
#                               checked=False,
#                               fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   db.session.commit()
#   print("############Su servicio ya esta configurado!!##############")
#   myquery = {"hostname": dic['router']}
#   # busca el router de la localidad y se actualizan las interfaces
#   routerint = Rcol.find(myquery, {'int': 1})
#   print("antes de entrar")
#   for h in routerint:
#       print("dentro")
#       oldintf = h
#       newintf = copy.deepcopy(oldintf)
#       print(newintf)
#       print(oldintf)
#       newintf['int'][dic['int_router'].replace(".", ",")] = {'link_status': 'up', 'protocol_status': 'up',
#                                                                  'ip': dic['ip_pe'], 'bandwidth': 100000}
#       newbw = oldintf['int'][dic['int_router'][0:15]]['bandwidth'] - (dic['bw_router']/1000)
#       newintf['int'][dic['int_router'][0:15]]['bandwidth'] = newbw
#       Rcol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#       # se busca el router y se actualiza la configuracion
#       host = nr.filter(F(name=dic['router']))
#       r = host.run(task=netmiko_send_command, command_string="show run")
#       nr.close_connections()
#       newconf = r[dic['router']][0].result
#       Rcol.update({'hostname': dic['router']}, {"$set": {'config': newconf}})
#       oldintf.clear()
#       newintf.clear()
#       myquery = {"hostname": dic['switch']}
#       # busca el switch de la localidad
#       switchint = Scol.find(myquery, {'int': 1})
#       for a in switchint:
#           oldintf = a
#   newintf = copy.deepcopy(oldintf)
#   print(newintf)
#   newintf['int'][dic['int_switch']]['available'] = False
#   newbw = oldintf['int'][dic['int_trunk_switch']]['bandwidth'] - (dic['bw_switch']/1000)
#   newintf['int'][dic['int_trunk_switch']]['bandwidth'] = newbw
#   Scol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=dic['switch']))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[dic['switch']][0].result
#   Scol.update({'hostname': dic['switch']}, {"$set": {'config': newconf}})
#   # Actualizando el registro del servicio en sql
#   cursor.execute(
#       "update Base_de_datos_proyecto.[dbo].[servicio] set active='{}' where id = '{}'".format(True, dic['id_servicio']))
#   cursor.commit()
#   notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Servicio",
#                               des="El proceso de configuracion del servicio con id: " + str(dic[
#                                   'id_servicio']) + " ha terminado",
#                               checked=False,
#                               fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   return "se configuró"
#
# def configl2vpn(vc, side, cursor,remote_ip,ip_loc, **dic):
#   notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Servicio",
#                                 des="El proceso de configuracion del servicio con id: " + str(dic[
#                                     'id_servicio']) + " ha comenzado",
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   dic["vc_id"]= vc
#   dic["remote_ip"]= remote_ip
#   dic['ip_loc'] = ip_loc
#   print(dic)
#   templatesw_a = jinja2.Template(
#                             "vlan {{a['servicevlan']}}\n"
#                             "interface {{a['int_trunk_switch']}}\n"
#                             "switchport trunk allowed vlan add {{a['servicevlan']}}\n"
#                             "policy-map {{ a['id_servicio'] }} \n"
#                             "class class-default \n"
#                             "shape average {{ a['bw_router'] }}\n"
#                             "interface {{ a['int_switch'] }}\n"
#                             "service-policy output {{ a['id_servicio'] }}\n"
#                             "switchport trunk encapsulation dot1q \n"
#                             "switchport mode trunk \n"
#                             "switchport trunk allowed vlan add {{a['servicevlan']}}\n")
#
#   templater_a = jinja2.Template("interface {{a['int_router']}}\n"
#                               "encapsulation dot1Q {{a['servicevlan']}} \n"
#                               "xconnect {{a['remote_ip']}} {{a['vc_id']}} encap mpls \n")
#
#   templatece_a = jinja2.Template("policy-map {{ a['id_servicio'] }} \n"
#                               "class class-default \n"
#                               "shape average {{ a['bw_switch'] }} \n"
#                               "interface {{ a['int_router'][0:18] }} \n"
#                               "service-policy output {{ a['id_servicio'] }}\n"
#                               "interface {{ a['int_router'] }} \n"
#                               "encapsulation dot1Q {{a['servicevlan']}} \n"
#                               "ip address {{a['ip_loc']}} \n")
#
#   output = templatesw_a.render(a = dic)
#   swfile="configs" +str(dic['id_servicio']) + side + ".txt"
#   file= open(swfile,"w+")
#   file.write(output)
#   file.close()
#   #print(output)
#   output = templater_a.render(a = dic)
#   rfile="configr" + str(dic['id_servicio']) + side + ".txt"
#   file= open(rfile,"w+")
#   file.write(output)
#   file.close()
#   # print(output)
#   output = templatece_a.render(a=dic)
#   rcefile = "configce" + str(dic['id_servicio']) + side + ".txt"
#   file = open(rcefile, "w+")
#   file.write(output)
#   file.close()
#   print(" ")
#   print(" ")
#   print("      Aviso para el administrador: se esta configurando un servicio ")
#   print("      favor correr el siguiente script y enviar al cliente su equipo de borde.")
#   print("      el script solo contiene la configuracion de habilitar SSH y la siguiente IP en la interfaz G1/0: " + dic[
#       "ip_ce"])
#   print("      Nota: el equipo de borde va conectado a la interfaz " + dic["int_switch"])
#   print(" ")
#   print(" ")
#   print('####Cliente: Conectar el equipo y encenderlo##########')
#   print(" ")
#   trigg = 'ya'
#   if trigg == 'ya':
#       # if lo 3 archivos existen configuralo
#       # se configura el router del side correspondiente
#       hostr = nr.filter(F(name=dic['router']))
#       hosts = nr.filter(F(name=dic['switch']))
#       hostce = nr.filter(F(name=dic['routerce']))
#       try:
#           r = hostr.run(task=netmiko_send_config, config_file=rfile)
#           print_result(r)
#       except (NetMikoTimeoutException) as e:
#           return "Fallo la conexion a los equipos: " + str(dic["router"])
#       try:
#           r = hosts.run(task=netmiko_send_config, config_file=swfile)
#           print_result(r)
#       except (NetMikoTimeoutException) as e:
#           newfile2 = ''
#           with open(rfile, "r") as f:
#               lines = f.readlines()
#           newfile2 += "no " + lines[0]
#           rintf = lines[0].split(" ")[-1].replace(".", ",").strip()
#           with open("delete_" + rfile, "w") as f:
#               f.write(newfile2)
#           r = hostr.run(task=netmiko_send_config, config_file="delete_" + rfile)
#           return "Fallo la conexion a los equipos: " + str(dic["switch"])
#       time.sleep(3)
#       try:
#           r = hostce.run(task=netmiko_send_config, config_file=rcefile)
#           print_result(r)
#       except (NetMikoTimeoutException) as e:
#           with open(swfile, "r") as f:
#               lines = f.readlines()
#           count = 0
#           newfile = ''
#           for line in lines:
#               if count in [0, 3, 7, 8, 9]:
#                   newfile += "no " + line
#               elif count in [2, 10]:
#                   newfile += line.replace("add", "remove")
#               elif count in [4, 5]:
#                   pass
#               else:
#                   newfile += line
#               count += 1
#           with open("delete_" + swfile, "w") as f:
#               f.write(newfile)
#           r = hosts.run(task=netmiko_send_config, config_file="delete_" + swfile)
#           newfile2 = ''
#           with open(rfile, "r") as f:
#               lines = f.readlines()
#           newfile2 += "no " + lines[0]
#           rintf = lines[0].split(" ")[-1].replace(".", ",").strip()
#           with open("delete_" + rfile, "w") as f:
#               f.write(newfile2)
#           r = hostr.run(task=netmiko_send_config, config_file="delete_" + rfile)
#           return "Fallo la conexion a los equipos: " + str(dic["routerce"])
#   print("############Su servicio ya esta configurado!!##############")
#   myquery = {"hostname": dic['router']}
#   # busca el router de la localidad y se actualizan las interfaces
#   routerint = Rcol.find(myquery, {'int': 1})
#   for h in routerint:
#       oldintf = h
#   newintf = copy.deepcopy(oldintf)
#   newintf['int'][dic['int_router'].replace(".", ",")] = {'link_status': 'up', 'protocol_status': 'up', 'ip': "",
#                                                          'bandwidth': 1000000}
#   newbw = oldintf['int'][dic['int_router'][0:18]]['bandwidth'] - dic['bw_router']
#   newintf['int'][dic['int_router'][0:18]]['bandwidth'] = newbw
#   Rcol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   # se busca el router y se actualiza la configuracion
#   host = nr.filter(F(name=dic['router']))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   print(r)
#   print(r[dic['router']])
#   newconf = r[dic['router']][0].result
#   Rcol.update({'hostname': dic['router']}, {"$set": {'config': newconf}})
#   oldintf.clear()
#   newintf.clear()
#   myquery = {"hostname": dic['switch']}
#   # busca el switch de la localidad
#   switchint = Scol.find(myquery, {'int': 1})
#   for a in switchint:
#       oldintf = a
#   newintf = copy.deepcopy(oldintf)
#   newintf['int'][dic['int_switch']]['available'] = False
#   newbw = oldintf['int'][dic['int_trunk_switch']]['bandwidth'] - dic['bw_switch']
#   newintf['int'][dic['int_trunk_switch']]['bandwidth'] = newbw
#   Scol.update_one({'int': oldintf['int']}, {"$set": {'int': newintf['int']}})
#   host = nr.filter(F(name=dic['switch']))
#   r = host.run(task=netmiko_send_command, command_string="show run")
#   newconf = r[dic['switch']][0].result
#   Scol.update({'hostname': dic['switch']}, {"$set": {'config': newconf}})
#   cursor.execute("update Base_de_datos_proyecto.[dbo].[servicio] set active='{}' where id = '{}'".format(True, dic['id_servicio']))
#   cursor.commit()
#   notificacion = Notificacion(id_servicio=dic['id_servicio'], tipo_not="Servicio",
#                               des="El proceso de configuracion del servicio con id: " + str(dic[
#                                   'id_servicio']) + " ha terminado",
#                               checked=False,
#                               fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#   db.session.add(notificacion)
#   # Servicio.query.filter_by(id=services[id].id).delete()
#   db.session.commit()
#   return True
#
#
#
#
#
#
#
#
