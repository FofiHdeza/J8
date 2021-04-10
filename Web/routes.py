import time
import datetime
from flask import render_template, flash, url_for, redirect, request
from Web import app
from Web.Data import posts
from Web.forms import AdddeviceForm, UpdateDeviceForm, DeviceForm, AddproductForm, AccountMLForm
#from Web.Database import User, Servicio, Notificacion
from flask_login import login_user, current_user, logout_user, login_required
from Web import core
import random
#from Web import Vcol, nr
import copy
#from nornir.core.filter import F
#from uwsgidecorators import *
#import uwsgi

# def systemsummary(zone):
#     router = mongo.db.Routers.find({"location": zone})
#     switch = mongo.db.Switches.find({"location": zone})
#     l2vpn_ips = mongo.db.Ippool.find({"location": zone, "service": "L2vpn"})
#     internet_ips = mongo.db.Ippool.find({"location": zone, "service": "Internet"})
#
#     up_bw_taken = 0  #######
#     up_bw_total = 10  #######
#     int_dict = []
#     for up_bw in switch:
#         print(up_bw)
#         up_bw_taken = 100 - up_bw["int"]["Ethernet0/1"]["bandwidth"] / 1000
#         int_dict = up_bw["int"]
#
#     int_total = 28
#     taken_int = 0
#     for intf, av in int_dict.items():
#         if av["available"] == False:
#             taken_int += 1
#
#     dw_bw_taken = 0  #######
#     dw_bw_total = 100  ######
#     for dw_bw in router:
#         print(dw_bw)
#         dw_bw_taken = 100 - dw_bw["int"]["GigabitEthernet1/0"]["bandwidth"] / 1000
#
#     total_internet_ips = 0  ########
#     thispool = []
#     for ip in internet_ips:
#         total_internet_ips = len(ip["pool"].keys())
#         thispool = ip["pool"]
#
#     taken_internet_ips = 0  ########
#     for i, av in thispool.items():
#         if av["available"] == False:
#             taken_internet_ips += 1
#
#     total_l2vpn_ips = 0  ########
#     thispool1 = []
#     for ip in l2vpn_ips:
#         total_l2vpn_ips = len(ip["pool"].keys())
#         thispool1 = ip["pool"]
#
#     taken_l2vpn_ips = 0  ########
#     for i, av in thispool1.items():
#         if av["available"] == False:
#             taken_l2vpn_ips += 1
#     info = {}
#     up_bw_percent = round((up_bw_taken * 20) / up_bw_total)
#     dw_bw_percent = round((dw_bw_taken * 20) / dw_bw_total)
#     intf_percent = round((taken_int * 20) / int_total)
#     internet_ips_percent = round((taken_internet_ips * 20) / total_internet_ips)
#     l2vpn_ips_percent = round((taken_l2vpn_ips * 20) / total_l2vpn_ips)
#     zone_percent= up_bw_percent + dw_bw_percent + intf_percent + internet_ips_percent + l2vpn_ips_percent
#     return zone_percent


# def coloresrandom():
#     color ="(" + str(random.randrange(255)) + "," + str(random.randrange(255)) + "," + str(random.randrange(255)) + "," + "0.7" + ")"
#     return "rgba" + color


# @spoolraw(pass_arguments=True)
# def serviceedit(id,upbw,dwbw,l2vpn_bw):
#     notificacion = Notificacion(id_servicio=id, tipo_not="Servicio",
#                                 des="Ha comenzado el upgrade del servicio con id: " + str(id),
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#     db.session.add(notificacion)
#     # Servicio.query.filter_by(id=services[id].id).delete()
#     db.session.commit()
#     this_service = Servicio.query.filter_by(id=id).first()
#     print(this_service)
#     if this_service.tipo_servicio == "Internet":
#         core.update_service(id, c, upbw, dwbw)
#         return uwsgi.SPOOL_OK
#     else:
#         core.update_l2vpn_service(id,c,this_service.location_a,l2vpn_bw)
#         core.update_l2vpn_service(id, c, this_service.location_b,l2vpn_bw)
#         return uwsgi.SPOOL_OK




# @spoolraw(pass_arguments=True)
# def configservice(id, **kwargs):
#     services = Servicio.query.filter_by(**kwargs).all()
#     notificacion = Notificacion(id_servicio=services[id].id, tipo_not="Servicio",
#                                 des="Ha comenzado la configuracion del servicio con id: " + str(services[id].id),
#                                 checked=False,
#                                 fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#     db.session.add(notificacion)
#     # Servicio.query.filter_by(id=services[id].id).delete()
#     db.session.commit()
#     if services[id].active == False:
#         if services[id].tipo_servicio == 'Internet':
#             dic1 = core.validateint(services[id].id, c)
#             if type(dic1) is dict:
#                 result = core.configint(services[id].location_a, c, **dic1)
#                 print(result)
#                 id_del_servicio = services[id].id
#                 skwargs = {'id': id_del_servicio}
#                 services = Servicio.query.filter_by(**skwargs).first()
#                 services.in_progress = False
#                 db.session.commit()
#                 redirect(url_for('serviceinfo'))
#                 return uwsgi.SPOOL_OK
#         elif services[id].tipo_servicio == 'L2vpn':
#             hosts = nr.filter(F(groups__contains="router_group") & F(location='{}'.format(services[id].location_a)))
#             host_a = ""
#             host_b = ""
#             for a in hosts.inventory.hosts:
#                 host_a = a
#             ip_host_a = hosts.inventory.hosts[host_a].data["ip"]
#             hosts = nr.filter(F(groups__contains="router_group") & F(location='{}'.format(services[id].location_b)))
#             for a in hosts.inventory.hosts:
#                 host_b = a
#             ip_host_b = hosts.inventory.hosts[host_b].data["ip"]
#             vc = 0
#             lastid = Vcol.find({}, {'vc_id': 1})
#             all_id = []
#             olddic = []
#             for f in lastid:
#                 all_id = f["vc_id"]
#                 olddic = copy.deepcopy(all_id)
#             final_id = 0
#             if len(olddic) < 101:
#                 for ids in range(1, len(all_id)):
#                     if all_id[ids] == 0:
#                         final_id = ids
#                         all_id[ids] = 1
#                         break
#                 if final_id == 0:
#                     all_id.append(1)
#                     final_id = len(all_id) - 1
#                 vc = final_id
#             else:
#                 print("Ya no existen circuitos virtuales disponibles para proveer el servicio")
#                 # notificacion
#                 return uwsgi.SPOOL_OK
#             dic1 = core.validatel2vpn(services[id].id, c, services[id].location_a)
#             print(dic1)
#             dic2 = core.validatel2vpn(services[id].id, c, services[id].location_b)
#             print(dic2)
#             if type(dic1) is dict and type(dic2) is dict:
#                 print('####################CONFIGURACION PARA EL PRIMER SIDE########################')
#                 result = core.configl2vpn(vc, services[id].location_a, c, ip_host_b,services[id].ip_loc_a, **dic1)
#                 if result == True:
#                     print('####################CONFIGURACION PARA EL SEGUNDO SIDE########################')
#                     result = core.configl2vpn(vc, services[id].location_b, c, ip_host_a,services[id].ip_loc_b, **dic2)
#                     if result != True:
#                         print(core.delete_l2vpn_service(services[id].id, c, services[id].location_a))
#             else:
#                 print("1-No se pudo dar el servicio, no existen recursos disponibles")
#                 # notificacion
#                 return uwsgi.SPOOL_OK
#             id_del_servicio = services[id].id
#             skwargs = {'id': id_del_servicio}
#             services = Servicio.query.filter_by(**skwargs).first()
#             services.in_progress = False
#             db.session.commit()
#             print("Si, es L2vpn")
#         return uwsgi.SPOOL_OK
#     else:
#         return uwsgi.SPOOL_OK

# @spoolraw(pass_arguments=True)
# def deleteservice(id,usuario, **kwargs):
#     if usuario == "prueba@final.com":
#         services = Servicio.query.all()
#     else:
#         services = Servicio.query.filter_by(**kwargs).all()
#     print(services)
#     if services[id].active == True:
#         if services[id].tipo_servicio == 'Internet':
#             core.delete_service(services[id].id, c)
#         #kwargs = {'id_cliente': 1}
#             notificacion = Notificacion(id_servicio=services[id].id, tipo_not="Servicio",
#                                         des="Se ha eliminado un servicio de " + services[id].tipo_servicio,
#                                         checked=False,
#                                         fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#             db.session.add(notificacion)
#             #Servicio.query.filter_by(id=services[id].id).delete()
#             db.session.commit()
#             id_del_servicio = services[id].id
#             skwargs = {'id': id_del_servicio}
#             services = Servicio.query.filter_by(**skwargs).first()
#             services.in_progress = False
#             db.session.commit()
#             return uwsgi.SPOOL_OK
#         elif services[id].tipo_servicio == 'L2vpn':
#             notificacion = Notificacion(id_servicio=services[id].id, tipo_not="Servicio",
#                                         des="Se ha eliminado un servicio de " + services[id].tipo_servicio,
#                                         checked=False,
#                                         fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#             db.session.add(notificacion)
#             core.delete_l2vpn_service(services[id].id, c, services[id].location_a)
#             core.delete_l2vpn_service(services[id].id, c, services[id].location_b)
#             id_del_servicio = services[id].id
#             skwargs = {'id': id_del_servicio}
#             services = Servicio.query.filter_by(**skwargs).first()
#             services.in_progress = False
#             db.session.commit()
#             print("Si, tambien es L2vpn")
#         return uwsgi.SPOOL_OK
#     else:
#         #flash('El servicio no puede eliminarse si no esta configurado', 'danger')
#         return uwsgi.SPOOL_OK


def products(id):
    device = core.show_one_device(id)
    products = core.filter_entitlements(device[0][1])
    return products

@app.route('/')
@app.route('/HomePage')
def HomePage():
    return render_template("HomePage.html", posts=posts)


@app.route('/Devices',methods=['GET', 'POST'])
def Devices():
    form=DeviceForm()
    devices = []
    if request.method == 'POST':
        if form.filter.data == '':
            #devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE'], ['vm-gos-133', 'Account_01', 'vm-gos-133', '5f55f9394a6d86754ee1a4cf', 'ENABLED', '2020-09-07T09:11:21.404Z', '2020-09-07T09:11:21.407Z', 'ACTIVE'], ['0000123456', 'Account_01', '0000123456', '5f55fa8e4a6d86754ee1a4d0', 'ENABLED', '2020-09-07T09:17:02.625Z', '2020-09-14T10:13:57.026Z', 'ACTIVE'], ['0000138147', 'Account_Wiztivi', '0000138147', '5f8eaa1b45f48c4ef284f292', 'ENABLED', '2020-10-20T09:12:59.797Z', '2020-10-20T09:12:59.798Z', 'ACTIVE'], ['0000138286', 'Account_Wiztivi', '0000138286', '5f8eaa3c45f48c4ef284f294', 'ENABLED', '2020-10-20T09:13:32.295Z', '2020-10-20T09:13:32.299Z', 'ACTIVE'], ['0000138301', 'Account_Wiztivi', '0000138301', '5f8ebb7645f48c4ef284f295', 'ENABLED', '2020-10-20T10:27:02.756Z', '2020-10-20T10:27:02.760Z', 'ACTIVE'], ['0000138300', 'Account_Wiztivi', '0000138300', '5f8ebb8845f48c4ef284f296', 'ENABLED', '2020-10-20T10:27:20.988Z', '2020-10-20T10:27:20.989Z', 'ACTIVE'], ['0000138283', 'Account_Wiztivi', '0000138283', '5f8ebba245f48c4ef284f297', 'ENABLED', '2020-10-20T10:27:46.667Z', '2020-10-20T10:27:46.669Z', 'ACTIVE'], ['0000138293', 'Account_Sagem', '0000138293', '5f9022bb45f48c4ef284f298', 'ENABLED', '2020-10-21T11:59:55.678Z', '2020-10-21T11:59:55.680Z', 'ACTIVE'], ['0000138297', 'Account_Sagem', '0000138297', '5f9022c745f48c4ef284f299', 'ENABLED', '2020-10-21T12:00:07.109Z', '2020-10-21T12:00:07.112Z', 'ACTIVE'], ['0000138298', 'Account_Sagem', '0000138298', '5f9022de45f48c4ef284f29a', 'ENABLED', '2020-10-21T12:00:30.500Z', '2020-10-21T12:00:30.502Z', 'ACTIVE'], ['2153121438', 'Account_ADO', '2153121438', '5fda61ab45f48c4ef284f2b4', 'ENABLED', '2020-12-16T19:36:11.217Z', '2020-12-16T19:36:11.219Z', 'ACTIVE'], ['2153121415', 'Account_ADO', '2153121415', '5fda61b645f48c4ef284f2b5', 'ENABLED', '2020-12-16T19:36:22.678Z', '2020-12-16T19:36:22.679Z', 'ACTIVE'], ['2153121422', 'Account_ADO', '2153121422', '5fda61c145f48c4ef284f2b6', 'ENABLED', '2020-12-16T19:36:33.897Z', '2020-12-16T19:36:33.898Z', 'ACTIVE'], ['2153121428', 'Account_ADO', '2153121428', '5fda61cf45f48c4ef284f2b7', 'ENABLED', '2020-12-16T19:36:47.424Z', '2020-12-16T19:36:47.425Z', 'ACTIVE'], ['2153121435', 'Account_ADO', '2153121435', '5fda61da45f48c4ef284f2b8', 'ENABLED', '2020-12-16T19:36:58.700Z', '2020-12-16T19:36:58.701Z', 'ACTIVE'], ['2153121423', 'Account_ADO', '2153121423', '5fda61e645f48c4ef284f2b9', 'ENABLED', '2020-12-16T19:37:10.638Z', '2020-12-16T19:37:10.640Z', 'ACTIVE'], ['2153121392', 'Account_ADO', '2153121392', '5fda61f245f48c4ef284f2ba', 'ENABLED', '2020-12-16T19:37:22.239Z', '2020-12-16T19:37:22.240Z', 'ACTIVE'], ['2153121421', 'Account_ADO', '2153121421', '5fda61fe45f48c4ef284f2bb', 'ENABLED', '2020-12-16T19:37:34.376Z', '2020-12-16T19:37:34.377Z', 'ACTIVE'], ['2153121393', 'Account_ADO', '2153121393', '5fda621045f48c4ef284f2bc', 'ENABLED', '2020-12-16T19:37:52.241Z', '2020-12-18T11:13:17.389Z', 'ACTIVE'], ['2153121441', 'Account_ADO', '2153121441', '5fdb2f4645f48c4ef284f2bd', 'ENABLED', '2020-12-17T10:13:26.727Z', '2020-12-17T10:13:26.729Z', 'ACTIVE'], ['2153121446', 'Account_ADO', '2153121446', '5fdb2f5345f48c4ef284f2be', 'ENABLED', '2020-12-17T10:13:39.569Z', '2020-12-17T10:13:39.571Z', 'ACTIVE'], ['2153121457', 'Account_ADO', '2153121457', '5fdb2f5b45f48c4ef284f2bf', 'ENABLED', '2020-12-17T10:13:47.248Z', '2020-12-17T10:13:47.249Z', 'ACTIVE'], ['2153121467', 'Account_ADO', '2153121467', '5fdb2f6345f48c4ef284f2c0', 'ENABLED', '2020-12-17T10:13:55.009Z', '2020-12-17T10:13:55.011Z', 'ACTIVE'], ['2153121416', 'Account_ADO', '2153121416', '5fdb2f6b45f48c4ef284f2c1', 'ENABLED', '2020-12-17T10:14:03.126Z', '2020-12-17T10:14:03.129Z', 'ACTIVE'], ['2153121411', 'Account_ADO', '2153121411', '5fdb2f7245f48c4ef284f2c2', 'ENABLED', '2020-12-17T10:14:10.772Z', '2020-12-17T10:14:10.775Z', 'ACTIVE'], ['2153121407', 'Account_ADO', '2153121407', '5fdb2f7c45f48c4ef284f2c3', 'ENABLED', '2020-12-17T10:14:20.585Z', '2020-12-17T10:14:20.586Z', 'ACTIVE'], ['2153121447', 'Account_ADO', '2153121447', '5fdb2f8445f48c4ef284f2c4', 'ENABLED', '2020-12-17T10:14:28.537Z', '2020-12-17T10:14:28.538Z', 'ACTIVE'], ['2153121475', 'Account_ADO', '2153121475', '5fe1b32345f48c4ef284f2c5', 'ENABLED', '2020-12-22T08:49:39.269Z', '2020-12-22T08:49:39.270Z', 'ACTIVE'], ['2153121455', 'Account_ADO', '2153121455', '5fe1b36945f48c4ef284f2c6', 'ENABLED', '2020-12-22T08:50:49.996Z', '2020-12-22T08:50:49.998Z', 'ACTIVE'], ['2153121427', 'Account_ADO', '2153121427', '5fe2064045f48c4ef284f2c7', 'ENABLED', '2020-12-22T14:44:16.700Z', '2020-12-22T14:44:16.701Z', 'ACTIVE'], ['2153121417', 'Account_ADO', '2153121417', '5fe2064b45f48c4ef284f2c8', 'ENABLED', '2020-12-22T14:44:27.125Z', '2020-12-22T14:44:27.126Z', 'ACTIVE'], ['2153121436', 'Account_ADO', '2153121436', '5fe2065a45f48c4ef284f2c9', 'ENABLED', '2020-12-22T14:44:42.028Z', '2020-12-22T14:44:42.029Z', 'ACTIVE'], ['2153121429', 'Account_ADO', '2153121429', '5fe2066845f48c4ef284f2ca', 'ENABLED', '2020-12-22T14:44:56.132Z', '2020-12-22T14:44:56.136Z', 'ACTIVE'], ['2153121425', 'Account_ADO', '2153121425', '5fe2067245f48c4ef284f2cb', 'ENABLED', '2020-12-22T14:45:06.767Z', '2020-12-22T14:45:06.768Z', 'ACTIVE'], ['2313212156', 'Account_ADO_TEST', '2313212156', '5fe22ace45f48c4ef284f2cc', 'ENABLED', '2020-12-22T17:20:14.383Z', '2020-12-22T17:20:14.384Z', 'ACTIVE'], ['098765432112', 'Account_Wiztivi', '098765432112', '5fe38f6045f48c4ef284f2ce', 'ENABLED', '2020-12-23T18:41:36.819Z', '2020-12-23T18:41:36.821Z', 'ACTIVE']]
            devices = core.show_devices()
            return render_template("Devices.html", posts=posts, devices=devices, form=form)
        elif form.filtertype.data == 'CaSN':
            devices = core.show_one_device(form.filter.data)
            #devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z','2020-08-25T08:06:06.294Z', 'ACTIVE']]
            return render_template("Devices.html", posts=posts, devices=devices, form=form)
        elif form.filtertype.data == 'AccountId':
            device = form.filter.data
            alldevices = core.show_devices()
            #alldevices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE'], ['vm-gos-133', 'Account_01', 'vm-gos-133', '5f55f9394a6d86754ee1a4cf', 'ENABLED', '2020-09-07T09:11:21.404Z', '2020-09-07T09:11:21.407Z', 'ACTIVE'], ['0000123456', 'Account_01', '0000123456', '5f55fa8e4a6d86754ee1a4d0', 'ENABLED', '2020-09-07T09:17:02.625Z', '2020-09-14T10:13:57.026Z', 'ACTIVE'], ['0000138147', 'Account_Wiztivi', '0000138147', '5f8eaa1b45f48c4ef284f292', 'ENABLED', '2020-10-20T09:12:59.797Z', '2020-10-20T09:12:59.798Z', 'ACTIVE'], ['0000138286', 'Account_Wiztivi', '0000138286', '5f8eaa3c45f48c4ef284f294', 'ENABLED', '2020-10-20T09:13:32.295Z', '2020-10-20T09:13:32.299Z', 'ACTIVE'], ['0000138301', 'Account_Wiztivi', '0000138301', '5f8ebb7645f48c4ef284f295', 'ENABLED', '2020-10-20T10:27:02.756Z', '2020-10-20T10:27:02.760Z', 'ACTIVE'], ['0000138300', 'Account_Wiztivi', '0000138300', '5f8ebb8845f48c4ef284f296', 'ENABLED', '2020-10-20T10:27:20.988Z', '2020-10-20T10:27:20.989Z', 'ACTIVE'], ['0000138283', 'Account_Wiztivi', '0000138283', '5f8ebba245f48c4ef284f297', 'ENABLED', '2020-10-20T10:27:46.667Z', '2020-10-20T10:27:46.669Z', 'ACTIVE'], ['0000138293', 'Account_Sagem', '0000138293', '5f9022bb45f48c4ef284f298', 'ENABLED', '2020-10-21T11:59:55.678Z', '2020-10-21T11:59:55.680Z', 'ACTIVE'], ['0000138297', 'Account_Sagem', '0000138297', '5f9022c745f48c4ef284f299', 'ENABLED', '2020-10-21T12:00:07.109Z', '2020-10-21T12:00:07.112Z', 'ACTIVE'], ['0000138298', 'Account_Sagem', '0000138298', '5f9022de45f48c4ef284f29a', 'ENABLED', '2020-10-21T12:00:30.500Z', '2020-10-21T12:00:30.502Z', 'ACTIVE'], ['2153121438', 'Account_ADO', '2153121438', '5fda61ab45f48c4ef284f2b4', 'ENABLED', '2020-12-16T19:36:11.217Z', '2020-12-16T19:36:11.219Z', 'ACTIVE'], ['2153121415', 'Account_ADO', '2153121415', '5fda61b645f48c4ef284f2b5', 'ENABLED', '2020-12-16T19:36:22.678Z', '2020-12-16T19:36:22.679Z', 'ACTIVE'], ['2153121422', 'Account_ADO', '2153121422', '5fda61c145f48c4ef284f2b6', 'ENABLED', '2020-12-16T19:36:33.897Z', '2020-12-16T19:36:33.898Z', 'ACTIVE'], ['2153121428', 'Account_ADO', '2153121428', '5fda61cf45f48c4ef284f2b7', 'ENABLED', '2020-12-16T19:36:47.424Z', '2020-12-16T19:36:47.425Z', 'ACTIVE'], ['2153121435', 'Account_ADO', '2153121435', '5fda61da45f48c4ef284f2b8', 'ENABLED', '2020-12-16T19:36:58.700Z', '2020-12-16T19:36:58.701Z', 'ACTIVE'], ['2153121423', 'Account_ADO', '2153121423', '5fda61e645f48c4ef284f2b9', 'ENABLED', '2020-12-16T19:37:10.638Z', '2020-12-16T19:37:10.640Z', 'ACTIVE'], ['2153121392', 'Account_ADO', '2153121392', '5fda61f245f48c4ef284f2ba', 'ENABLED', '2020-12-16T19:37:22.239Z', '2020-12-16T19:37:22.240Z', 'ACTIVE'], ['2153121421', 'Account_ADO', '2153121421', '5fda61fe45f48c4ef284f2bb', 'ENABLED', '2020-12-16T19:37:34.376Z', '2020-12-16T19:37:34.377Z', 'ACTIVE'], ['2153121393', 'Account_ADO', '2153121393', '5fda621045f48c4ef284f2bc', 'ENABLED', '2020-12-16T19:37:52.241Z', '2020-12-18T11:13:17.389Z', 'ACTIVE'], ['2153121441', 'Account_ADO', '2153121441', '5fdb2f4645f48c4ef284f2bd', 'ENABLED', '2020-12-17T10:13:26.727Z', '2020-12-17T10:13:26.729Z', 'ACTIVE'], ['2153121446', 'Account_ADO', '2153121446', '5fdb2f5345f48c4ef284f2be', 'ENABLED', '2020-12-17T10:13:39.569Z', '2020-12-17T10:13:39.571Z', 'ACTIVE'], ['2153121457', 'Account_ADO', '2153121457', '5fdb2f5b45f48c4ef284f2bf', 'ENABLED', '2020-12-17T10:13:47.248Z', '2020-12-17T10:13:47.249Z', 'ACTIVE'], ['2153121467', 'Account_ADO', '2153121467', '5fdb2f6345f48c4ef284f2c0', 'ENABLED', '2020-12-17T10:13:55.009Z', '2020-12-17T10:13:55.011Z', 'ACTIVE'], ['2153121416', 'Account_ADO', '2153121416', '5fdb2f6b45f48c4ef284f2c1', 'ENABLED', '2020-12-17T10:14:03.126Z', '2020-12-17T10:14:03.129Z', 'ACTIVE'], ['2153121411', 'Account_ADO', '2153121411', '5fdb2f7245f48c4ef284f2c2', 'ENABLED', '2020-12-17T10:14:10.772Z', '2020-12-17T10:14:10.775Z', 'ACTIVE'], ['2153121407', 'Account_ADO', '2153121407', '5fdb2f7c45f48c4ef284f2c3', 'ENABLED', '2020-12-17T10:14:20.585Z', '2020-12-17T10:14:20.586Z', 'ACTIVE'], ['2153121447', 'Account_ADO', '2153121447', '5fdb2f8445f48c4ef284f2c4', 'ENABLED', '2020-12-17T10:14:28.537Z', '2020-12-17T10:14:28.538Z', 'ACTIVE'], ['2153121475', 'Account_ADO', '2153121475', '5fe1b32345f48c4ef284f2c5', 'ENABLED', '2020-12-22T08:49:39.269Z', '2020-12-22T08:49:39.270Z', 'ACTIVE'], ['2153121455', 'Account_ADO', '2153121455', '5fe1b36945f48c4ef284f2c6', 'ENABLED', '2020-12-22T08:50:49.996Z', '2020-12-22T08:50:49.998Z', 'ACTIVE'], ['2153121427', 'Account_ADO', '2153121427', '5fe2064045f48c4ef284f2c7', 'ENABLED', '2020-12-22T14:44:16.700Z', '2020-12-22T14:44:16.701Z', 'ACTIVE'], ['2153121417', 'Account_ADO', '2153121417', '5fe2064b45f48c4ef284f2c8', 'ENABLED', '2020-12-22T14:44:27.125Z', '2020-12-22T14:44:27.126Z', 'ACTIVE'], ['2153121436', 'Account_ADO', '2153121436', '5fe2065a45f48c4ef284f2c9', 'ENABLED', '2020-12-22T14:44:42.028Z', '2020-12-22T14:44:42.029Z', 'ACTIVE'], ['2153121429', 'Account_ADO', '2153121429', '5fe2066845f48c4ef284f2ca', 'ENABLED', '2020-12-22T14:44:56.132Z', '2020-12-22T14:44:56.136Z', 'ACTIVE'], ['2153121425', 'Account_ADO', '2153121425', '5fe2067245f48c4ef284f2cb', 'ENABLED', '2020-12-22T14:45:06.767Z', '2020-12-22T14:45:06.768Z', 'ACTIVE'], ['2313212156', 'Account_ADO_TEST', '2313212156', '5fe22ace45f48c4ef284f2cc', 'ENABLED', '2020-12-22T17:20:14.383Z', '2020-12-22T17:20:14.384Z', 'ACTIVE'], ['098765432112', 'Account_Wiztivi', '098765432112', '5fe38f6045f48c4ef284f2ce', 'ENABLED', '2020-12-23T18:41:36.819Z', '2020-12-23T18:41:36.821Z', 'ACTIVE']]
            devices = []
            for i in alldevices:
                if device in i:
                    devices.append(i)
            # devices = core.show_one_device(form.filter.data)
            # devices = [['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED',
            #             '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE']]
            return render_template("Devices.html", posts=posts, devices=devices, form=form)
        #print(devices)
        #devices=[]
    return render_template("Devices.html", posts=posts, devices=devices, form=form)

@app.route('/Adddevice',methods=['GET', 'POST'])
def Adddevice():
    form= AdddeviceForm()
    if form.validate_on_submit():
        if form.account.data == "Account_ADO":
            print(form.ide.data,form.casn.data,form.account.data)
            core.add_device(form.ide.data,form.casn.data,form.account.data)
            flash('Device Added', 'success')
            return redirect(url_for('Devices'))
        elif form.account.data == "Account_Sagem":
            print(form.ide.data,form.casn.data,form.account.data)
            core.add_device(form.ide.data,form.casn.data,form.account.data)
            flash('Device Added', 'success')
            return redirect(url_for('Devices'))
        else:
            flash('Account does not exist, please verify or create it', 'danger')
            return redirect(url_for('Devices'))
    return render_template("AddDevice.html", posts=posts, form=form)

@app.route('/Deletedevice/<string:id>',methods=['GET', 'POST'])
def Deletedevice(id):
    core.delete_device(id)
    flash('Device emilinated', 'success')
    return redirect(url_for('Devices'))


@app.route('/Editdevice/<string:id>',methods=['GET', 'POST'])
def Editdevice(id):
    form= UpdateDeviceForm()
    device = core.show_one_device(id)
    if form.validate_on_submit():
        if form.account.data == "Account_ADO":
            core.edit_device(form.account.data)
            flash('Device Added', 'success')
            return redirect(url_for('Devices'))
        else:
            flash('Account does not exist, please verify or create it', 'danger')
            return redirect(url_for('Devices'))
    return render_template("EditDevice.html", posts=posts, form=form,device=device)


@app.route('/Addproduct/<string:id>',methods=['GET', 'POST'])
def Addproduct(id):
    form= AddproductForm()
    device = core.show_one_device(id)
    products= core.filter_entitlements(device[0][1])
    productscreated=[
        ["100092","Basico Digital 2"],
        ["32787",	"HBO"],
        ["400126",	"HBO HD"],
        ["32790",	"Playboy"],
        ["32789",	"Venus"],
        ["32798",	"Noti Plus"],
        ["110",	    "TEST DLK"],
        ["52",	    "Training 90"],
        ["662331",	"Playboy HD"],
        ["10096	",	"GINX"],
        ["100162",	"MLB Extraining"],
        ["400046",	"MLB HD"],
        ["662895",	"Golden"],
        ["662817",	"Stingray Music"],
        ["100092",	"Basico Digital 2"],
        ["100093",	"Channel Pack C"],
        ["32800",	"Sport Plus"],
        ["1",       "PAQUETE NUEVO DE PRUEBA"],
        ["100090",	"Compacto DIG"],
        ["32788	",	"Moviepack"],
        ["660549",	"Moviecity HD"],
        ["100136",	"PAQUETE SUPER VIP"],
        ["101",	    "Training 88"],
        ["102",	    "Training 91"],
        ["50",	    "Training 97"],
        ["1000031",	"UFC"],
        ["1000230",	"MLB Mini Extraining"],
        ["32799",	"Movie Plus"],
        ["32801",	"Family Plus"],
        ["100094",	"Basico Plus"],
        ["777777",	"PAQUETE VIP"],
        ["2",       "Training 95"],
        ["51",	    "Training 96"],
        ["32791",	"Private"],
        ["32793",	"Digital"],
        ["660102",	"Comercial HD"],
        ["100095",	"Basico Plus Regional"],
        ["1000233",	"mini MLB HD"],
        ["16777220","PlanJulio2019"],
        ["100",	    "Training 93"],
        ["100083",	"Basico Digital"],
        ["100091",	"Compacto Digital 2"],
        ["100137",	"Basico HD"],
        ["10097",	"FOODNETW"],
        ["661721",	"CCampo"],
        ["662920",	"Retencion"]


    ]
    devices = core.show_devices()
    acc_devices= []
    for i in devices:
        if device[0][1] in i:
            acc_devices.append(i)
    if form.validate_on_submit():
        core.add_entitlement(form.product.data, device[0][1], form.producttype.data)
        products = core.filter_entitlements(device[0][1])
        flash('Entitlement Added', 'success')
        return render_template("addproduct.html", posts=posts,products=products, form=form,id=id,
                           productscreated=productscreated,acc_devices=acc_devices, len_devices=len(acc_devices))
    return render_template("addproduct.html", posts=posts,products=products, form=form,id=id,
                           productscreated=productscreated,acc_devices=acc_devices,len_devices=len(acc_devices))

@app.route('/Deleteproduct/<string:id>',methods=['GET', 'POST'])
def Deleteproduct(id):
    core.delete_entitlement(id)
    return redirect(url_for('Devices'))


@app.route("/VOD")
def VOD():

    return render_template("VOD.html", posts=posts)


@app.route("/BTV")
def BTV():

    return render_template("BTV.html", posts=posts)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         return redirect(url_for('system'))
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(correo=form.correo.data).first()
#         if user and bcrypt.check_password_hash(user.passw, form.passw.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             if(user.correo != 'prueba@final.com'):
#                 return redirect(next_page) if next_page else redirect(url_for('account'))
#             else:
#                 return redirect(next_page) if next_page else redirect(url_for('system'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template("Login.html", posts=posts, form=form)


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('homepage'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
#         if form.validate_email(form.correo.data):
#             flash('That email is taken. Please choose another','danger')
#         else:
#             user = User(nombre_empresa= form.nombre_empresa.data, rnc=form.rnc.data ,direccion=form.direccion.data
#                         , correo = form.correo.data, passw = hashed_password, telefono=form.telefono.data,createdon=datetime.datetime.now().strftime("%Y-%m-%d"))
#             db.session.add(user)
#             db.session.registry()
#             db.session.commit()
#             db.session.flush()
#             notificacion  = Notificacion(id_servicio=user.id_cliente,tipo_not="Usuario",des="Se ha agregado un nuevo usuario: ",checked=False, fecha=str(time.strftime("%d/%m/%y"))+" "+str(time.strftime("%I:%M:%S")))
#             db.session.add(notificacion)
#             db.session.commit()
#             flash('Su cuenta fue creada, ya puede iniciar sesión', 'success')
#             return redirect(url_for('login'))
#     return render_template('Register.html', title='Register', form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('homepage'))


# @app.route("/options/<string:option>")
# def options(option):
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         if option == "users":
#             users = User.query.all()
#             users_dic = {}
#             for i in users:
#                 users_dic[users.index(i)] = {
#                     'id_cliente': i.id_cliente,
#                     'nombre_empresa': i.nombre_empresa,
#                     'rnc': i.rnc,
#                     'direccion': i.direccion,
#                     'correo': i.correo,
#                     'telefono': i.telefono,
#                 }
#             ids = []
#             for i in users_dic:
#                 ids.append(i)
#             return render_template("userinfo.html", posts=users_dic, len_dict=len(users_dic), ids=ids,notification=notification)
#         elif option == "services":
#             # kwargs={'id_cliente': 1}
#             services = Servicio.query.all()
#             services_dic = {}
#             for i in services:
#                 services_dic[services.index(i)] = {
#                     'id': i.id,
#                     'id_cliente': i.id_cliente,
#                     'tipo_servicio': i.tipo_servicio,
#                     'location_a': i.location_a,
#                     'location_b': i.location_b,
#                     'up_bw': i.up_bw,
#                     'dw_bw': i.dw_bw,
#                     'active': i.active
#                 }
#             ids = []
#             for i in services_dic:
#                 ids.append(i)
#             return render_template("serviceinfo.html", posts=services_dic, len_dict=len(services_dic), ids=ids,notification=notification)
#         elif option == "router":
#             core.router()
#             return option
#         elif option == "switch":
#             core.switch()
#             return option
#         return render_template("Options.html")
#     else:
#         return redirect(url_for('homepage'))


# @app.route('/deleteuser/<int:id>')
# def deleteuser(id):
#     users = Servicio.query.all()
#     #User.query.filter_by(id=users[id].id).delete()
#     #db.session.commit()
#     ###hay que buscar todos los servicios que tiene ese usuario y desconfigurarlos##
#     print(id)
#     return redirect(url_for('homepage'))


@app.route("/AccountML",methods=['GET', 'POST'])
def AccountML():
    form = AccountMLForm()
    accounts = []
    if request.method == 'POST':
        # if form.filter.data == '':
        #     # devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE'], ['vm-gos-133', 'Account_01', 'vm-gos-133', '5f55f9394a6d86754ee1a4cf', 'ENABLED', '2020-09-07T09:11:21.404Z', '2020-09-07T09:11:21.407Z', 'ACTIVE'], ['0000123456', 'Account_01', '0000123456', '5f55fa8e4a6d86754ee1a4d0', 'ENABLED', '2020-09-07T09:17:02.625Z', '2020-09-14T10:13:57.026Z', 'ACTIVE'], ['0000138147', 'Account_Wiztivi', '0000138147', '5f8eaa1b45f48c4ef284f292', 'ENABLED', '2020-10-20T09:12:59.797Z', '2020-10-20T09:12:59.798Z', 'ACTIVE'], ['0000138286', 'Account_Wiztivi', '0000138286', '5f8eaa3c45f48c4ef284f294', 'ENABLED', '2020-10-20T09:13:32.295Z', '2020-10-20T09:13:32.299Z', 'ACTIVE'], ['0000138301', 'Account_Wiztivi', '0000138301', '5f8ebb7645f48c4ef284f295', 'ENABLED', '2020-10-20T10:27:02.756Z', '2020-10-20T10:27:02.760Z', 'ACTIVE'], ['0000138300', 'Account_Wiztivi', '0000138300', '5f8ebb8845f48c4ef284f296', 'ENABLED', '2020-10-20T10:27:20.988Z', '2020-10-20T10:27:20.989Z', 'ACTIVE'], ['0000138283', 'Account_Wiztivi', '0000138283', '5f8ebba245f48c4ef284f297', 'ENABLED', '2020-10-20T10:27:46.667Z', '2020-10-20T10:27:46.669Z', 'ACTIVE'], ['0000138293', 'Account_Sagem', '0000138293', '5f9022bb45f48c4ef284f298', 'ENABLED', '2020-10-21T11:59:55.678Z', '2020-10-21T11:59:55.680Z', 'ACTIVE'], ['0000138297', 'Account_Sagem', '0000138297', '5f9022c745f48c4ef284f299', 'ENABLED', '2020-10-21T12:00:07.109Z', '2020-10-21T12:00:07.112Z', 'ACTIVE'], ['0000138298', 'Account_Sagem', '0000138298', '5f9022de45f48c4ef284f29a', 'ENABLED', '2020-10-21T12:00:30.500Z', '2020-10-21T12:00:30.502Z', 'ACTIVE'], ['2153121438', 'Account_ADO', '2153121438', '5fda61ab45f48c4ef284f2b4', 'ENABLED', '2020-12-16T19:36:11.217Z', '2020-12-16T19:36:11.219Z', 'ACTIVE'], ['2153121415', 'Account_ADO', '2153121415', '5fda61b645f48c4ef284f2b5', 'ENABLED', '2020-12-16T19:36:22.678Z', '2020-12-16T19:36:22.679Z', 'ACTIVE'], ['2153121422', 'Account_ADO', '2153121422', '5fda61c145f48c4ef284f2b6', 'ENABLED', '2020-12-16T19:36:33.897Z', '2020-12-16T19:36:33.898Z', 'ACTIVE'], ['2153121428', 'Account_ADO', '2153121428', '5fda61cf45f48c4ef284f2b7', 'ENABLED', '2020-12-16T19:36:47.424Z', '2020-12-16T19:36:47.425Z', 'ACTIVE'], ['2153121435', 'Account_ADO', '2153121435', '5fda61da45f48c4ef284f2b8', 'ENABLED', '2020-12-16T19:36:58.700Z', '2020-12-16T19:36:58.701Z', 'ACTIVE'], ['2153121423', 'Account_ADO', '2153121423', '5fda61e645f48c4ef284f2b9', 'ENABLED', '2020-12-16T19:37:10.638Z', '2020-12-16T19:37:10.640Z', 'ACTIVE'], ['2153121392', 'Account_ADO', '2153121392', '5fda61f245f48c4ef284f2ba', 'ENABLED', '2020-12-16T19:37:22.239Z', '2020-12-16T19:37:22.240Z', 'ACTIVE'], ['2153121421', 'Account_ADO', '2153121421', '5fda61fe45f48c4ef284f2bb', 'ENABLED', '2020-12-16T19:37:34.376Z', '2020-12-16T19:37:34.377Z', 'ACTIVE'], ['2153121393', 'Account_ADO', '2153121393', '5fda621045f48c4ef284f2bc', 'ENABLED', '2020-12-16T19:37:52.241Z', '2020-12-18T11:13:17.389Z', 'ACTIVE'], ['2153121441', 'Account_ADO', '2153121441', '5fdb2f4645f48c4ef284f2bd', 'ENABLED', '2020-12-17T10:13:26.727Z', '2020-12-17T10:13:26.729Z', 'ACTIVE'], ['2153121446', 'Account_ADO', '2153121446', '5fdb2f5345f48c4ef284f2be', 'ENABLED', '2020-12-17T10:13:39.569Z', '2020-12-17T10:13:39.571Z', 'ACTIVE'], ['2153121457', 'Account_ADO', '2153121457', '5fdb2f5b45f48c4ef284f2bf', 'ENABLED', '2020-12-17T10:13:47.248Z', '2020-12-17T10:13:47.249Z', 'ACTIVE'], ['2153121467', 'Account_ADO', '2153121467', '5fdb2f6345f48c4ef284f2c0', 'ENABLED', '2020-12-17T10:13:55.009Z', '2020-12-17T10:13:55.011Z', 'ACTIVE'], ['2153121416', 'Account_ADO', '2153121416', '5fdb2f6b45f48c4ef284f2c1', 'ENABLED', '2020-12-17T10:14:03.126Z', '2020-12-17T10:14:03.129Z', 'ACTIVE'], ['2153121411', 'Account_ADO', '2153121411', '5fdb2f7245f48c4ef284f2c2', 'ENABLED', '2020-12-17T10:14:10.772Z', '2020-12-17T10:14:10.775Z', 'ACTIVE'], ['2153121407', 'Account_ADO', '2153121407', '5fdb2f7c45f48c4ef284f2c3', 'ENABLED', '2020-12-17T10:14:20.585Z', '2020-12-17T10:14:20.586Z', 'ACTIVE'], ['2153121447', 'Account_ADO', '2153121447', '5fdb2f8445f48c4ef284f2c4', 'ENABLED', '2020-12-17T10:14:28.537Z', '2020-12-17T10:14:28.538Z', 'ACTIVE'], ['2153121475', 'Account_ADO', '2153121475', '5fe1b32345f48c4ef284f2c5', 'ENABLED', '2020-12-22T08:49:39.269Z', '2020-12-22T08:49:39.270Z', 'ACTIVE'], ['2153121455', 'Account_ADO', '2153121455', '5fe1b36945f48c4ef284f2c6', 'ENABLED', '2020-12-22T08:50:49.996Z', '2020-12-22T08:50:49.998Z', 'ACTIVE'], ['2153121427', 'Account_ADO', '2153121427', '5fe2064045f48c4ef284f2c7', 'ENABLED', '2020-12-22T14:44:16.700Z', '2020-12-22T14:44:16.701Z', 'ACTIVE'], ['2153121417', 'Account_ADO', '2153121417', '5fe2064b45f48c4ef284f2c8', 'ENABLED', '2020-12-22T14:44:27.125Z', '2020-12-22T14:44:27.126Z', 'ACTIVE'], ['2153121436', 'Account_ADO', '2153121436', '5fe2065a45f48c4ef284f2c9', 'ENABLED', '2020-12-22T14:44:42.028Z', '2020-12-22T14:44:42.029Z', 'ACTIVE'], ['2153121429', 'Account_ADO', '2153121429', '5fe2066845f48c4ef284f2ca', 'ENABLED', '2020-12-22T14:44:56.132Z', '2020-12-22T14:44:56.136Z', 'ACTIVE'], ['2153121425', 'Account_ADO', '2153121425', '5fe2067245f48c4ef284f2cb', 'ENABLED', '2020-12-22T14:45:06.767Z', '2020-12-22T14:45:06.768Z', 'ACTIVE'], ['2313212156', 'Account_ADO_TEST', '2313212156', '5fe22ace45f48c4ef284f2cc', 'ENABLED', '2020-12-22T17:20:14.383Z', '2020-12-22T17:20:14.384Z', 'ACTIVE'], ['098765432112', 'Account_Wiztivi', '098765432112', '5fe38f6045f48c4ef284f2ce', 'ENABLED', '2020-12-23T18:41:36.819Z', '2020-12-23T18:41:36.821Z', 'ACTIVE']]
        #     accounts = core.show_devices()
        #     return render_template("Devices.html", posts=posts, devices=accounts, form=form)
        # if form.filtertype.data == 'SSP':
        #     accounts = core.show_one_device(form.filter.data)
        #     # devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z','2020-08-25T08:06:06.294Z', 'ACTIVE']]
        #     return render_template("Devices.html", posts=posts, devices=accounts, form=form)
        if form.filtertype.data == 'CASN':
            casn = str(form.filter.data)
            allaccounts = core.sdp_account_getbycasn(casn)
            devices = core.sdp_devices_getbyaccount((core.sdp_account_getbycasn(casn))[9])
            return render_template("AccountML.html", posts=posts, devices=allaccounts,acc_devices=devices,len_devices=len(devices), form=form)
        elif form.filtertype.data == 'Acc Num':
            acnum = str(form.filter.data)
            allaccounts = core.sdp_account_getbyaccnumber(acnum)
            devices = core.sdp_devices_getbyaccount((core.sdp_account_getbyaccnumber(acnum))[9])
            return render_template("AccountML.html", posts=posts, devices=allaccounts,acc_devices=devices,len_devices=len(devices), form=form)
    return render_template("AccountML.html", posts=posts, devices=accounts, form=form)




# @app.route('/serviceinfo')
# def serviceinfo():
#     nkwargs = {'checked': False}
#     notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#     notification = False
#     if not notificaciones:
#         notification = False
#         print('ta vacia')
#     else:
#         notification = True
#         print('no ta vacia')
#     kwargs={'id_cliente': current_user.id_cliente}
#     #kwargs={'id_cliente': 1}
#     services= Servicio.query.filter_by(**kwargs).all()
#     services_dic={}
#     for i in services:
#         services_dic[services.index(i)]={
#             'id': i.id,
#             'id_cliente': i.id_cliente,
#             'tipo_servicio': i.tipo_servicio,
#             'location_a': i.location_a,
#             'location_b': i.location_b,
#             'up_bw': i.up_bw,
#             'dw_bw': i.dw_bw,
#             'ip_loc_a': i.ip_loc_a,
#             'ip_loc_b': i.ip_loc_b,
#             'in_progress':i.in_progress,
#             'active': i.active
#         }
#     ids=[]
#     for i in services_dic:
#         ids.append(i)
#     return render_template("serviceinfo.html", posts=services_dic, len_dict=len(services_dic), ids=ids,notification=notification)


# @app.route('/configservice/<int:id>')
# def configservice_background(id):
#     kwargs = {'id_cliente': current_user.id_cliente}
#     services = Servicio.query.filter_by(**kwargs).all()
#     id_del_servicio= services[id].id
#     skwargs = {'id': id_del_servicio}
#     services = Servicio.query.filter_by(**skwargs).first()
#     services.in_progress = True
#     db.session.commit()
#     print(services)
#     configservice.spool(id, **kwargs)
#     return redirect(url_for('serviceinfo'))
#
#
# @app.route('/deleteservice/<int:id>')
# def deleteservice_background(id):
#     if current_user.correo == "prueba@final.com":
#         usuario = "prueba@final.com"
#         kwargs = {'id_cliente': current_user.id_cliente}
#         services = Servicio.query.all()
#         id_del_servicio = services[id].id
#         skwargs = {'id': id_del_servicio}
#         services = Servicio.query.filter_by(**skwargs).first()
#         services.in_progress = True
#         db.session.commit()
#         deleteservice.spool(id,usuario, **kwargs)
#         return redirect(url_for('system'))
#     else:
#         usuario=''
#         kwargs = {'id_cliente': current_user.id_cliente}
#         services = Servicio.query.filter_by(**kwargs).all()
#         id_del_servicio = services[id].id
#         skwargs = {'id': id_del_servicio}
#         services = Servicio.query.filter_by(**skwargs).first()
#         services.in_progress = True
#         db.session.commit()
#         deleteservice.spool(id,usuario, **kwargs)
#         return redirect(url_for('serviceinfo'))
#
#
# @app.route('/new_l2vpn_service', methods=['GET', 'POST'])
# def new_l2vpn_service():
#     nkwargs = {'checked': False}
#     notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#     notification = False
#     if not notificaciones:
#         notification = False
#         print('ta vacia')
#     else:
#         notification = True
#         print('no ta vacia')
#     if current_user.correo == "prueba@final.com":
#         return redirect(url_for('homepage'))
#     kwargs={'id_cliente': current_user.id_cliente}
#     services= Servicio.query.filter_by(**kwargs).all()
#     services_dic={}
#     form = Newl2vpnServiceForm()
#     if form.validate_on_submit():
#         servicio = Servicio(id_cliente=current_user.id_cliente,tipo_servicio="L2vpn", location_a=form.location_a.data,
#                                 location_b=form.location_b.data, up_bw=form.up_bw.data*1000, dw_bw=form.up_bw.data*1000,
#                             active=0,in_progress=0,createdon=datetime.datetime.now().strftime("%Y-%m-%d"),
#                             ip_loc_a=form.ip_loc_a.data,ip_loc_b=form.ip_loc_b.data)
#         db.session.add(servicio)
#         db.session.commit()
#         flash('Su servicio ya fue creado', 'success')
#         return redirect(url_for('serviceinfo'))
#     return render_template("new_l2vpn_service.html", posts=services_dic,form=form,notification=notification)
#
#
# @app.route('/new_internet_service', methods=['GET', 'POST'])
# def new_internet_service():
#     nkwargs = {'checked': False}
#     notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#     notification = False
#     if not notificaciones:
#         notification = False
#         print('ta vacia')
#     else:
#         notification = True
#         print('no ta vacia')
#     if current_user.correo == "prueba@final.com":
#         return redirect(url_for('homepage'))
#     kwargs={'id_cliente': current_user.id_cliente}
#     services= Servicio.query.filter_by(**kwargs).all()
#     services_dic={}
#     form = NewInternetServiceForm()
#     if form.validate_on_submit():
#         servicio = Servicio(id_cliente=current_user.id_cliente,tipo_servicio="Internet", location_a=form.location_a.data,
#                                 up_bw=form.up_bw.data*1000, dw_bw=form.dw_bw.data*1000, active=0, in_progress=0,createdon=datetime.datetime.now().strftime("%Y-%m-%d"))
#         db.session.add(servicio)
#         db.session.commit()
#         db.session.flush()
#         notificacion = Notificacion(id_servicio=servicio.id, tipo_not="Servicio",
#                                     des="Se ha creado un nuevo servicio de " +servicio.tipo_servicio,
#                                     checked=False,
#                                     fecha=str(time.strftime("%d/%m/%y")) + " " + str(time.strftime("%I:%M:%S")))
#         db.session.add(notificacion)
#         db.session.commit()
#         flash('Su servicio ya fue creado', 'success')
#         return redirect(url_for('serviceinfo'))
#     return render_template("new_internet_service.html", posts=services_dic,form=form,notification=notification)
#
#
# @app.route('/upgradeservice/<int:id>',methods=['GET', 'POST'])
# def serviceedit_background(id):
#     nkwargs = {'checked': False}
#     notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#     notification = False
#     if not notificaciones:
#         notification = False
#     else:
#         notification = True
#     if current_user.correo == "prueba@final.com":
#         return redirect(url_for('homepage'))
#     form = UpdateServiceForm()
#     kwargs = {'id_cliente': current_user.id_cliente}
#     services = Servicio.query.filter_by(**kwargs).all()
#     this_service = Servicio.query.filter_by(id=services[id].id).first()
#     tipo_servicio= this_service.tipo_servicio
#     print('SUBMIT 1')
#     print(tipo_servicio)
#     if this_service.active == True:
#         print('SUBMIT 2')
#         if form.validate_on_submit():
#             print('SUBMIT 3')
#             if tipo_servicio == "Internet":
#                 serviceedit.spool(services[id].id,form.up_bw.data * 1000, form.dw_bw.data * 1000)
#             else:
#                 serviceedit.spool(services[id].id, 1, 1,form.l2vpn_bw.data * 1000)
#             return redirect(url_for('serviceinfo'))
#         return render_template("upgradeservice.html",form=form, up_baw=services[id].up_bw, dw_baw=services[id].dw_bw,
#                                notification=notification, tipo_servicio=tipo_servicio)
#     else:
#         return redirect(url_for('serviceinfo'))
#
#
# @app.route('/system',methods=['GET', 'POST'])
# def system():
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         if current_user.correo == "prueba@final.com":
#             zone_percents={}
#             zone_percents= {
#                 "norte": systemsummary("Norte")
#
#             }
#             print(zone_percents)
#             services = Servicio.query.all()
#             services_dic = {}
#             for i in services:
#                 kwargs = {'id_cliente': i.id_cliente}
#                 #nombre = User.query.filter_by(**kwargs).first()
#                 #print(nombre.nombre_empresa)
#                 services_dic[services.index(i)] = {
#                     'nombre_cliente': User.query.filter_by(**kwargs).first().nombre_empresa,
#                     'id': i.id,
#                     'id_cliente': i.id_cliente,
#                     'tipo_servicio': i.tipo_servicio,
#                     'location_a': i.location_a,
#                     'location_b': i.location_b,
#                     'up_bw': i.up_bw,
#                     'dw_bw': i.dw_bw,
#                     'active': i.active
#                 }
#             ids = []
#             for i in services_dic:
#                 ids.append(i)
#             return render_template("system.html", posts=services_dic, len_dict=len(services_dic), ids=ids,zone_percents=zone_percents,notification=notification)
#         return redirect(url_for('homepage'))
#     else:
#         return redirect(url_for('homepage'))
#
#
# @app.route('/zonedetails/<string:zone>',methods=['GET', 'POST'])
# def zonedetails(zone):
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         if current_user.correo == "prueba@final.com":
#             router = mongo.db.Routers.find({"location": zone})
#             switch = mongo.db.Switches.find({"location": zone})
#             l2vpn_ips = mongo.db.Ippool.find({"location": zone, "service": "L2vpn"})
#             internet_ips = mongo.db.Ippool.find({"location": zone, "service": "Internet"})
#
#             up_bw_taken = 0 #######
#             up_bw_total= 10 #######
#             int_dict=[]
#             for up_bw in switch:
#                 up_bw_taken= 10 - up_bw["int"]["Ethernet0/1"]["bandwidth"]/1000
#                 int_dict=up_bw["int"]
#
#             int_total=24
#             taken_int=0
#             taken_int_list=[]
#             for intf, av in int_dict.items():
#                if av["available"] == False:
#                   taken_int+=1
#                   if intf[0:4] != "Vlan":
#                     taken_int_list.append(intf)
#
#             dw_bw_taken=0 #######
#             dw_bw_total = 100 ######
#             for dw_bw in router:
#                 dw_bw_taken=100 - dw_bw["int"]["GigabitEthernet1/0"]["bandwidth"]/1000
#
#             total_internet_ips=0 ########
#             thispool=[]
#             for ip in internet_ips:
#                 total_internet_ips= len(ip["pool"].keys())
#                 thispool=ip["pool"]
#
#             taken_internet_ips=0 ########
#             internet_ips_list=[]
#             for i,av in thispool.items():
#                 if av["available"] == False:
#                     taken_internet_ips+=1
#                     i = i.replace(',', '.')
#                     internet_ips_list.append(i)
#
#             total_l2vpn_ips = 0  ########
#             thispool1 = []
#             for ip in l2vpn_ips:
#                 total_l2vpn_ips = len(ip["pool"].keys())
#                 thispool1 = ip["pool"]
#
#             taken_l2vpn_ips = 0  ########
#             l2vpn_ips_list=[]
#             for i, av in thispool1.items():
#                 if av["available"] == False:
#                     taken_l2vpn_ips += 1
#                     i = i.replace(',', '.')
#                     l2vpn_ips_list.append(i)
#             info={}
#             up_bw_percent = round((up_bw_taken*100)/up_bw_total)
#             dw_bw_percent= round((dw_bw_taken*100)/dw_bw_total)
#             intf_percent= round((taken_int*100)/int_total)
#             internet_ips_percent= round((taken_internet_ips*100)/total_internet_ips)
#             l2vpn_ips_percent= round((taken_l2vpn_ips*100)/total_l2vpn_ips)
#
#             info= {
#                 'up_bw_av': up_bw_percent,
#                 'dw_bw_av':dw_bw_percent,
#                 'int_av':intf_percent,
#                 'taken_internet_ips':internet_ips_percent,
#                 'taken_l2vpn_ips':l2vpn_ips_percent
#             }
#
#             return render_template("zonedetails.html", zone=zone, info=info, up_bw_taken=up_bw_taken,up_bw_total=up_bw_total,
#                                    dw_bw_taken=dw_bw_taken,dw_bw_total=dw_bw_total,taken_int_list=taken_int_list,
#                                    internet_ips_list=internet_ips_list,l2vpn_ips_list=l2vpn_ips_list,notification=notification)
#         return redirect(url_for('homepage'))
#     else:
#         return redirect(url_for('system'))
#
#
#
# @app.route('/notifications')
# def notifications():
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         ukwargs = {'tipo_not': "Usuario"}
#         user_notifications = Notificacion.query.filter_by(**ukwargs).all()
#         skwargs = {'tipo_not': "Servicio"}
#         service_notifications = Notificacion.query.filter_by(**skwargs).all()
#         rkwargs = {'tipo_not': "Recurso"}
#         resource_notifications = Notificacion.query.filter_by(**rkwargs).all()
#         user_notifications_dic = {}
#         user_unchecked=[]
#         for i in user_notifications:
#             if i.checked == False:
#                 user_unchecked.append(i)
#             user_notifications_dic[user_notifications.index(i)] = {
#                 'id': i.id,
#                 'id_servicio': i.id_servicio,
#                 'tipo_not': i.tipo_not,
#                 'des': i.des,
#                 'checked': i.checked,
#                 'fecha': i.fecha
#             }
#
#         ids = []
#         for i in user_notifications_dic:
#             ids.append(i)
#         #####################################################################
#         service_notifications_dic = {}
#         service_unchecked = []
#         for j in service_notifications:
#             if j.checked == False:
#                 service_unchecked.append(j)
#             service_notifications_dic[service_notifications.index(j)] = {
#                 'id': j.id,
#                 'id_servicio': j.id_servicio,
#                 'tipo_not': j.tipo_not,
#                 'des': j.des,
#                 'checked': j.checked,
#                 'fecha': j.fecha
#             }
#         ids1 = []
#         for j in service_notifications_dic:
#             ids1.append(j)
#         #####################################################################
#         resource_notifications_dic = {}
#         resource_unchecked = []
#         for k in resource_notifications:
#             if k.checked == False:
#                 resource_unchecked.append(k)
#             resource_notifications_dic[resource_notifications.index(k)] = {
#                 'id': k.id,
#                 'id_servicio': k.id_servicio,
#                 'tipo_not': k.tipo_not,
#                 'des': k.des,
#                 'checked': k.checked,
#                 'fecha': k.fecha
#             }
#         ids2 = []
#         for j in resource_notifications_dic:
#             ids2.append(j)
#         return render_template("notifications.html", posts=user_notifications_dic, posts_service=service_notifications_dic,
#                                posts_resource=resource_notifications_dic, len_user_dict=len(user_unchecked),
#                                len_service_dict=len(service_unchecked),
#                                len_resource_dict=len(resource_unchecked), ids=ids,notification=notification)
#     else:
#         return redirect(url_for('homepage'))
#
#
# @app.route('/notifications/detail/<int:id>')
# def notificationdetail(id):
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         notificacion = Notificacion.query.filter_by(id=id).first()
#         notificacion_dic={
#             'id': notificacion.id,
#             'id_servicio': notificacion.id_servicio,
#             'tipo_not': notificacion.tipo_not,
#             'des': notificacion.des,
#             'checked': notificacion.checked,
#             'fecha': notificacion.fecha
#         }
#         id_x= notificacion.id_servicio
#         tp= notificacion.tipo_not
#         ser_servicio_dic={}
#         ser_usuario_dic = {}
#         if tp == "Servicio":
#             notificacion.checked = True
#             db.session.commit()
#             kwargs = {'id': id_x}
#             servicio = Servicio.query.filter_by(**kwargs).all()
#             ser_servicio_dic={}
#             for i in servicio:
#                 ser_servicio_dic={
#                     'id': i.id,
#                     'id_cliente': i.id_cliente,
#                     'tipo_servicio': i.tipo_servicio,
#                     'location_a': i.location_a,
#                     'location_b': i.location_b,
#                     'up_bw': i.up_bw,
#                     'dw_bw': i.dw_bw,
#                     'active': i.active
#                 }
#             kwargs = {'id_cliente': int(ser_servicio_dic['id_cliente'])}
#             usuario = User.query.filter_by(**kwargs).all()
#             ser_usuario_dic={}
#             for j in usuario:
#                 ser_usuario_dic={
#                     'id_cliente': j.id_cliente,
#                     'nombre_empresa': j.nombre_empresa,
#                     'rnc': j.rnc,
#                     'direccion': j.direccion,
#                     'correo': j.correo,
#                     'telefono': j.telefono,
#                 }
#             return render_template("notificationdetail.html", ser_usuario_dic=ser_usuario_dic,
#                                    ser_servicio_dic=ser_servicio_dic, notificacion_dic=notificacion_dic,notification=notification)
#         elif tp == "Usuario":
#             notificacion.checked = True
#             db.session.commit()
#             kwargs = {'id_cliente': id_x}
#             usuario = User.query.filter_by(**kwargs).all()
#             usuario_dic = {}
#             for j in usuario:
#                 usuario_dic = {
#                     'id_cliente': j.id_cliente,
#                     'nombre_empresa': j.nombre_empresa,
#                     'rnc': j.rnc,
#                     'direccion': j.direccion,
#                     'correo': j.correo,
#                     'telefono': j.telefono,
#                 }
#             return render_template("notificationdetail.html", usuario_dic=usuario_dic,notification=notification)
#         elif tp == "Recurso":
#             notificacion.checked = True
#             db.session.commit()
#             kwargs = {'id': id_x}
#             servicio = Servicio.query.filter_by(**kwargs).all()
#             res_servicio_dic = {}
#             for i in servicio:
#                 res_servicio_dic = {
#                     'id': i.id,
#                     'id_cliente': i.id_cliente,
#                     'tipo_servicio': i.tipo_servicio,
#                     'location_a': i.location_a,
#                     'location_b': i.location_b,
#                     'up_bw': i.up_bw,
#                     'dw_bw': i.dw_bw,
#                     'active': i.active
#                 }
#             kwargs = {'id_cliente': int(res_servicio_dic['id_cliente'])}
#             usuario = User.query.filter_by(**kwargs).all()
#             res_usuario_dic = {}
#             for j in usuario:
#                 res_usuario_dic = {
#                     'id_cliente': j.id_cliente,
#                     'nombre_empresa': j.nombre_empresa,
#                     'rnc': j.rnc,
#                     'direccion': j.direccion,
#                     'correo': j.correo,
#                     'telefono': j.telefono,
#                 }
#             return render_template("notificationdetail.html", res_usuario_dic=res_usuario_dic,
#                                    res_servicio_dic=res_servicio_dic, notificacion_dic=notificacion_dic,notification=notification)
#         return render_template("system.html")
#     else:
#         return redirect(url_for('homepage'))
#
#
#
# @app.route('/statics')
# def statics():
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#         else:
#             notification = True
#         today = datetime.date.today()
#         week_dates=[]
#         real_week_dates=[]
#         for i in reversed(range(7)):
#             week_ago = today - datetime.timedelta(days=i)
#             week_dates.append(str(week_ago))
#             real_week_dates.append(week_ago)
#         legend = 'Servicios creados'
#         legend1 = 'Servicios configurados'
#         legend2 = 'Servicios'
#         legend3= 'Servicios configurados totales'
#         labels = [week_dates[0], week_dates[1], week_dates[2], week_dates[3], week_dates[4], week_dates[5], week_dates[6]]
#         values = []
#         values1 = []
#         labels2=[]
#         values2=[]
#         labels3 = ['Servicios configurados']
#         values3= []
#         for j in real_week_dates:
#             kwargs = {'createdon': j}
#             values.append(Servicio.query.filter_by(**kwargs).count())
#             kwargs1 = {'createdon': j, 'active':1}
#             values1.append(Servicio.query.filter_by(**kwargs1).count())
#         colores=[coloresrandom(),coloresrandom(),coloresrandom(),coloresrandom(),coloresrandom(),coloresrandom(),
#                  coloresrandom(),coloresrandom(),coloresrandom(),coloresrandom()]
#         usuarios=[]
#         col='nombre_empresa'
#         total_usuarios= User.query.all()
#         for k in total_usuarios:
#             labels2.append(k.nombre_empresa)
#             usuarios.append([k.nombre_empresa, k.id_cliente])
#         for l in usuarios:
#             #print(usuarios.index(l))
#             #print(l[0])
#             kwargs = {'id_cliente': l[1]}
#             count= Servicio.query.filter_by(**kwargs).count()
#             values2.append(count)
#             #print(count)
#             #print(usuarios[usuarios.index(l)])
#             usuarios[usuarios.index(l)].append(count)
#         kwargs3 = {'active': 1}
#         values3.append(Servicio.query.filter_by(**kwargs3).count())
#         print(legend3,labels3,values3)
#         return render_template("statics.html", real_week_dates=real_week_dates,values=values,values1=values1, labels=labels,
#                                legend=legend,legend1=legend1,labels2=labels2,values2=values2,colores=colores,
#                                notification=notification, legend3=legend3, labels3=labels3,values3=values3,legend2=legend2)
#     else:
#         return redirect(url_for('homepage'))
#
#
# @app.route('/configview/<int:id>/<string:loc_a>/<string:loc_b>')
# def configview(id, loc_a,loc_b):
#     if current_user.is_authenticated and current_user.correo == "prueba@final.com":
#         nkwargs = {'checked': False}
#         notificaciones = Notificacion.query.filter_by(**nkwargs).all()
#         notification = False
#         if not notificaciones:
#             notification = False
#             print('ta vacia')
#         else:
#             notification = True
#             print('no ta vacia')
#         kwargs = {'id': id}
#         services = Servicio.query.filter_by(**kwargs).first()
#         if services.tipo_servicio == "L2vpn": ########## falta sacar las ip de l2vpn y analizar que hace eso jeje
#             with open("tasks/configce"+str(id)+str(loc_a).capitalize()+ ".txt", "r") as f:
#                 cefile_a = f.read()
#             with open("tasks/configce"+str(id)+str(loc_b).capitalize()+ ".txt", "r") as f:
#                 cefile_b = f.read()
#         internet_ips = mongo.db.Ippool.find({"location": loc_a, "service": "Internet"})
#         thispool = []
#         for ip in internet_ips:
#             thispool = ip["pool"]
#         ip1 = ''
#         for i, av in thispool.items():
#             print(i, av)
#             if av["id_service"] == str(id):
#                 ip1 = i
#         ip1 = ip1.replace(',', '.')
#         print(ip1)
#         cefile_a = ''
#         cefile_b = ''
#         rfile = ''
#         sfile = ''
#         with open("tasks/configr"+str(id)+str(loc_a).capitalize()+ ".txt", "r") as f:
#             rfile = f.read()
#         with open("tasks/configs"+str(id)+str(loc_a).capitalize()+ ".txt", "r") as f:
#             sfile = f.read()
#         return render_template("configview.html", rfile=rfile,sfile=sfile, cefile_a=cefile_a, cefil_b=cefile_b,ip1=ip1,notification=notification)
#     else:
#         return redirect(url_for('homepage'))




