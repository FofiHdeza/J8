import json
import time
import datetime
import os
from os import scandir
from flask import render_template, flash, url_for, redirect, request, send_file
from werkzeug.utils import secure_filename

from Web import app, UPLOAD_FOLDER, DOC_FOLDER, PROC_FOLDER
from Web.Data import posts
from Web.core import ssp_getallaccounts
from Web.forms import AdddeviceForm, UpdateDeviceForm, DeviceForm, AddproductForm, AccountMLForm, AddSSPAccForm, \
    AddMLAccForm, AddMLdeviceForm, VODForm, CreateFWInfo
#from Web.Database import User, Servicio, Notificacion
from flask_login import login_user, current_user, logout_user, login_required
from Web import core
import random
#from Web import Vcol, nr
import copy


def products(id):
    device = core.show_one_device(id)
    products = core.filter_entitlements(device[0][1])
    return products



@app.route('/SSP/Adddevice',methods=['GET', 'POST'])
def Adddevice():
    form= AdddeviceForm()
    if form.validate_on_submit():
        all_acc=core.ssp_getallaccounts()
        print(all_acc)
        accs= []
        for i in all_acc:
            if form.account.data in i:
                core.add_device(form.ide.data, form.casn.data, form.account.data)
                flash('Device Added', 'success')
                return redirect(url_for('SSP'))
        # if form.account.data == "Account_ADO":
        #     print(form.ide.data,form.casn.data,form.account.data)
        #     core.add_device(form.ide.data,form.casn.data,form.account.data)
        #     flash('Device Added', 'success')
        #     return redirect(url_for('SSP'))
        # elif form.account.data == "Account_Sagem":
        #     print(form.ide.data,form.casn.data,form.account.data)
        #     core.add_device(form.ide.data,form.casn.data,form.account.data)
        #     flash('Device Added', 'success')
        #     return redirect(url_for('SSP'))
        else:
            flash('Account does not exist, please verify or create it', 'danger')
            return redirect(url_for('SSP'))
    return render_template("AddDevice.html", posts=posts, form=form)


@app.route('/AccountML/AddMLAcc',methods=['GET', 'POST'])
def AddMLAcc():
    form= AddMLAccForm()
    if form.validate_on_submit():
        core.sdp_account_createnewacc(form.accnum.data,form.lastname.data,form.firstname.data,form.pwd.data,
                                      "ACTIVE","true","tlv",form.npvrprofile.data,form.credlimit.data)
        flash('Account Added', 'success')
        return redirect(url_for('AccountML'))
    return render_template("AddMLAcc.html", posts=posts, form=form)


@app.route('/SSP/AddSSPAcc',methods=['GET', 'POST'])
def AddSSPAcc():
    form= AddSSPAccForm()
    if form.validate_on_submit():
        core.ssp_addaccount(form.accid.data)
        flash('Device Added', 'success')
        return redirect(url_for('SSP'))
    return render_template("AddSSPAcc.html", posts=posts, form=form)


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
    acc_devices= core.show_devices_fromacc(device[0][1])
    print(acc_devices)
    # for i in devices:
    #     if device[0][1] in i:
    #         acc_devices.append(i)
    if form.validate_on_submit():
        core.add_entitlement(form.product.data, device[0][1], form.producttype.data)
        products = core.filter_entitlements(device[0][1])
        flash('Entitlement Added', 'success')
        return render_template("addproduct.html", posts=posts,products=products, form=form,id=id,
                           productscreated=productscreated,acc_devices=acc_devices, len_devices=len(acc_devices))
    return render_template("addproduct.html", posts=posts,products=products, form=form,id=id,
                           productscreated=productscreated,acc_devices=acc_devices,len_devices=len(acc_devices))


@app.route("/AccountML",methods=['GET', 'POST'])
def AccountML():
    form = AccountMLForm()
    accounts = []
    if request.method == 'POST':
        if form.filtertype.data == 'CASN':
            casn = str(form.filter.data)
            allaccounts = core.sdp_account_getbycasn(casn)
            devices = core.sdp_devices_getbyaccount((core.sdp_account_getbycasn(casn))[9])
            return render_template("AccountML.html", posts=posts, devices=allaccounts,acc_devices=devices,len_devices=len(devices), form=form)
        elif form.filtertype.data == 'Acc Num' and form.filter.data != '':
            acnum = str(form.filter.data)
            allaccounts = core.sdp_account_getbyaccnumber(acnum)
            devices = core.sdp_devices_getbyaccount((core.sdp_account_getbyaccnumber(acnum))[9])
            return render_template("AccountML.html", posts=posts, devices=allaccounts,acc_devices=devices,len_devices=len(devices), form=form)
    return render_template("AccountML.html", posts=posts, devices=accounts, form=form)


@app.route('/AccountML/AddMLdevice',methods=['GET', 'POST'])
def AddMLdevice():
    form= AddMLdeviceForm()
    if form.validate_on_submit():
        if form.account.data == "100015723":
            account=core.sdp_account_getbyaccnumber(form.account.data)
            core.sdp_device_createstb(form.casn.data,'false','true',account[9],'CARDLESS','ACTIVE','A')
            flash('Device Added', 'success')
            return redirect(url_for('AccountML'))
        else:
            flash('Account does not exist in {hardcored}, please verify or create it', 'danger')
            return redirect(url_for('SSP'))
    return render_template("AddMLDevice.html", posts=posts, form=form)


@app.route("/BTV")
def BTV():

    return render_template("BTV.html", posts=posts)


@app.route('/Homepage/Doc/FWInfo/Create',methods=['GET', 'POST'])
def CreateFWIfnfo():
    form= CreateFWInfo()
    if form.validate_on_submit():
        if form.ht.data == '' and form.rn.data=='':
            entry = {
                "Version": form.version.data,
                "Tpe": form.typ.data,
                "Env": form.env.data,
                "Improvements": form.improv.data
            }
            with open("Web/Doc/FWInfo.json", 'r+') as file:
                file_data = json.load(file)
                file_data['Software'].insert(0, entry)
                file_data.update("")
                file.seek(0)
                json.dump(file_data, file, indent=4)
            flash('Device Added', 'success')
            return redirect(url_for('FWInfo'))
        if form.rn.data == '':
            entry = {
                "Version": form.version.data,
                "Tpe": form.typ.data,
                "Env": form.env.data,
                "Improvements": form.improv.data,
                "HT": str(form.ht.data)
            }
            with open("Web/Doc/FWInfo.json", 'r+') as file:
                file_data = json.load(file)
                file_data['Software'].insert(0, entry)
                file_data.update("")
                file.seek(0)
                json.dump(file_data, file, indent=4)
            flash('Device Added', 'success')
            return redirect(url_for('FWInfo'))
        if form.ht.data == '':
            entry = {
                "Version": form.version.data,
                "Tpe": form.typ.data,
                "Env": form.env.data,
                "Improvements": form.improv.data,
                "RN": str(form.rn.data)
            }
            with open("Web/Doc/FWInfo.json", 'r+') as file:
                file_data = json.load(file)
                file_data['Software'].insert(0, entry)
                file_data.update("")
                file.seek(0)
                json.dump(file_data, file, indent=4)
            flash('Device Added', 'success')
            return redirect(url_for('FWInfo'))
        entry = {
            "Version": form.version.data,
            "Tpe": form.typ.data,
            "Env": form.env.data,
            "Improvements": form.improv.data,
            "RN": str(form.rn.data),
            "HT": str(form.ht.data)
        }
        with open("Web/Doc/FWInfo.json", 'r+') as file:
            file_data = json.load(file)
            file_data['Software'].insert(0, entry)
            file_data.update("")
            file.seek(0)
            json.dump(file_data, file, indent=4)
        flash('Device Added', 'success')
        return redirect(url_for('FWInfo'))
    return render_template("Createfwinfo.html", posts=posts, form=form)


@app.route('/Homepage/Doc',methods=['GET', 'POST'])
def Doc():
    ruta = 'Web/Doc/'
    #ruta = '/Users/ivanhdeza/Desktop/Headend/STBsoftwares/FW_2.8.0/Debug/'
    archivos=[]
    with os.scandir(ruta) as directorio:
        for archivo in directorio:
            nombretmp= str(archivo)
            nombrearchivo=nombretmp[11:-2]
            if nombrearchivo[0] !=".":
                archivos.append(nombrearchivo)
        print(archivos)
    return render_template("Doc.html", posts=posts, archivos=archivos,ruta=ruta)


@app.route('/downloadProc/<filename>')
def downloadProc(filename):
    file_path = PROC_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/downloadRNHT/<filename>')
def downloadRNHT(filename):
    file_path = DOC_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/download/<filename>')
def download(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/DeleteSSPAcc/<string:id>',methods=['GET', 'POST'])
def DeleteSSPAcc(id):
    core.ssp_deleteaccount(id)
    flash('Account emilinated', 'success')
    return redirect(url_for('SSP'))


@app.route('/Deletedevice/<string:id>',methods=['GET', 'POST'])
def Deletedevice(id):
    core.delete_device(id)
    flash('Device emilinated', 'success')
    return redirect(url_for('SSP'))


@app.route('/Deleteproduct/<string:id>',methods=['GET', 'POST'])
def Deleteproduct(id):
    core.delete_entitlement(id)
    return redirect(url_for('Devices'))


@app.route('/DeleteMLAcc/<string:id>',methods=['GET', 'POST'])
def DeleteMLAcc(id):
    core.sdp_account_deleteacc(id,"?")
    flash('Account emilinated', 'success')
    return redirect(url_for('AccountML'))


@app.route('/DeleteMLdevice/<string:casn>/<string:id>',methods=['GET', 'POST'])
def DeleteMLdevice(casn,id):
    casn = " " +casn
    id = " " + id
    print(casn,id)

    core.sdp_device_deletestb(casn,id)
    flash('Device emilinated', 'success')
    return redirect(url_for('AccountML'))


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


@app.route('/Homepage/Doc/FWInfo',methods=['GET', 'POST'])
def FWInfo():
    with open("Web/Doc/FWInfo.json", "r") as f:
        file = f.read()
    finalfile = json.loads(file)
    print(finalfile['Software'])
    versions = finalfile['Software']
    #ruta = 'Web/Doc/'
    #ruta = '/Users/ivanhdeza/Desktop/Headend/STBsoftwares/FW_2.8.0/Debug/'
    #archivos=[]
    #with os.scandir(ruta) as directorio:
    #    for archivo in directorio:
    #        nombretmp= str(archivo)
    #        nombrearchivo=nombretmp[11:-2]
    #        if nombrearchivo[0] !=".":
    #            archivos.append(nombrearchivo)
    return render_template("FWInfo.html", posts=posts,versions=versions)


@app.route('/Homepage/FW',methods=['GET', 'POST'])
def FW():
    ruta = 'Web/uploads/'
    #ruta = '/Users/ivanhdeza/Desktop/Headend/STBsoftwares/FW_2.8.0/Debug/'
    archivos=[]
    with os.scandir(ruta) as directorio:
        for archivo in directorio:
            nombretmp= str(archivo)
            nombrearchivo=nombretmp[11:-2]
            if nombrearchivo[0] !=".":
                archivos.append(nombrearchivo)
        print(archivos)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('no file', 'danger')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('no filename', 'danger')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join("Web/uploads/", filename))
            flash('saved file successfully', 'success')
      #send file name as parameter to downlad
    return render_template("FW.html", posts=posts, archivos=archivos,ruta=ruta)


@app.route('/')
@app.route('/HomePage')
def HomePage():
    return render_template("HomePage.html", posts=posts)


@app.route('/Homepage/Jarvis',methods=['GET', 'POST'])
def Jarvis():
    ruta = 'Web/Doc/'
    #ruta = '/Users/ivanhdeza/Desktop/Headend/STBsoftwares/FW_2.8.0/Debug/'
    archivos=[]
    with os.scandir(ruta) as directorio:
        for archivo in directorio:
            nombretmp= str(archivo)
            nombrearchivo=nombretmp[11:-2]
            if nombrearchivo[0] !=".":
                archivos.append(nombrearchivo)
        print(archivos)
    return render_template("Jarvis.html", posts=posts, archivos=archivos,ruta=ruta)


@app.route('/Homepage/Doc/Midivi')
def Midivi():
    return render_template("Midivi.html")


@app.route('/Homepage/Doc/Proc',methods=['GET', 'POST'])
def Proc():
    with open("Web/Procedures/Procedures.json", "r") as f:
        file = f.read()
    finalfile = json.loads(file)
    print(finalfile['Procedure'])
    procedures = finalfile['Procedure']
    return render_template("Proc.html", posts=posts, procedures=procedures)


@app.route('/SSP',methods=['GET', 'POST'])
def SSP():
    form=DeviceForm()
    devices = []
    if request.method == 'POST':
        if form.filter.data == '' and form.filtertype.data == 'CaSN':
            flag= 'casn'
            #devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE'], ['vm-gos-133', 'Account_01', 'vm-gos-133', '5f55f9394a6d86754ee1a4cf', 'ENABLED', '2020-09-07T09:11:21.404Z', '2020-09-07T09:11:21.407Z', 'ACTIVE'], ['0000123456', 'Account_01', '0000123456', '5f55fa8e4a6d86754ee1a4d0', 'ENABLED', '2020-09-07T09:17:02.625Z', '2020-09-14T10:13:57.026Z', 'ACTIVE'], ['0000138147', 'Account_Wiztivi', '0000138147', '5f8eaa1b45f48c4ef284f292', 'ENABLED', '2020-10-20T09:12:59.797Z', '2020-10-20T09:12:59.798Z', 'ACTIVE'], ['0000138286', 'Account_Wiztivi', '0000138286', '5f8eaa3c45f48c4ef284f294', 'ENABLED', '2020-10-20T09:13:32.295Z', '2020-10-20T09:13:32.299Z', 'ACTIVE'], ['0000138301', 'Account_Wiztivi', '0000138301', '5f8ebb7645f48c4ef284f295', 'ENABLED', '2020-10-20T10:27:02.756Z', '2020-10-20T10:27:02.760Z', 'ACTIVE'], ['0000138300', 'Account_Wiztivi', '0000138300', '5f8ebb8845f48c4ef284f296', 'ENABLED', '2020-10-20T10:27:20.988Z', '2020-10-20T10:27:20.989Z', 'ACTIVE'], ['0000138283', 'Account_Wiztivi', '0000138283', '5f8ebba245f48c4ef284f297', 'ENABLED', '2020-10-20T10:27:46.667Z', '2020-10-20T10:27:46.669Z', 'ACTIVE'], ['0000138293', 'Account_Sagem', '0000138293', '5f9022bb45f48c4ef284f298', 'ENABLED', '2020-10-21T11:59:55.678Z', '2020-10-21T11:59:55.680Z', 'ACTIVE'], ['0000138297', 'Account_Sagem', '0000138297', '5f9022c745f48c4ef284f299', 'ENABLED', '2020-10-21T12:00:07.109Z', '2020-10-21T12:00:07.112Z', 'ACTIVE'], ['0000138298', 'Account_Sagem', '0000138298', '5f9022de45f48c4ef284f29a', 'ENABLED', '2020-10-21T12:00:30.500Z', '2020-10-21T12:00:30.502Z', 'ACTIVE'], ['2153121438', 'Account_ADO', '2153121438', '5fda61ab45f48c4ef284f2b4', 'ENABLED', '2020-12-16T19:36:11.217Z', '2020-12-16T19:36:11.219Z', 'ACTIVE'], ['2153121415', 'Account_ADO', '2153121415', '5fda61b645f48c4ef284f2b5', 'ENABLED', '2020-12-16T19:36:22.678Z', '2020-12-16T19:36:22.679Z', 'ACTIVE'], ['2153121422', 'Account_ADO', '2153121422', '5fda61c145f48c4ef284f2b6', 'ENABLED', '2020-12-16T19:36:33.897Z', '2020-12-16T19:36:33.898Z', 'ACTIVE'], ['2153121428', 'Account_ADO', '2153121428', '5fda61cf45f48c4ef284f2b7', 'ENABLED', '2020-12-16T19:36:47.424Z', '2020-12-16T19:36:47.425Z', 'ACTIVE'], ['2153121435', 'Account_ADO', '2153121435', '5fda61da45f48c4ef284f2b8', 'ENABLED', '2020-12-16T19:36:58.700Z', '2020-12-16T19:36:58.701Z', 'ACTIVE'], ['2153121423', 'Account_ADO', '2153121423', '5fda61e645f48c4ef284f2b9', 'ENABLED', '2020-12-16T19:37:10.638Z', '2020-12-16T19:37:10.640Z', 'ACTIVE'], ['2153121392', 'Account_ADO', '2153121392', '5fda61f245f48c4ef284f2ba', 'ENABLED', '2020-12-16T19:37:22.239Z', '2020-12-16T19:37:22.240Z', 'ACTIVE'], ['2153121421', 'Account_ADO', '2153121421', '5fda61fe45f48c4ef284f2bb', 'ENABLED', '2020-12-16T19:37:34.376Z', '2020-12-16T19:37:34.377Z', 'ACTIVE'], ['2153121393', 'Account_ADO', '2153121393', '5fda621045f48c4ef284f2bc', 'ENABLED', '2020-12-16T19:37:52.241Z', '2020-12-18T11:13:17.389Z', 'ACTIVE'], ['2153121441', 'Account_ADO', '2153121441', '5fdb2f4645f48c4ef284f2bd', 'ENABLED', '2020-12-17T10:13:26.727Z', '2020-12-17T10:13:26.729Z', 'ACTIVE'], ['2153121446', 'Account_ADO', '2153121446', '5fdb2f5345f48c4ef284f2be', 'ENABLED', '2020-12-17T10:13:39.569Z', '2020-12-17T10:13:39.571Z', 'ACTIVE'], ['2153121457', 'Account_ADO', '2153121457', '5fdb2f5b45f48c4ef284f2bf', 'ENABLED', '2020-12-17T10:13:47.248Z', '2020-12-17T10:13:47.249Z', 'ACTIVE'], ['2153121467', 'Account_ADO', '2153121467', '5fdb2f6345f48c4ef284f2c0', 'ENABLED', '2020-12-17T10:13:55.009Z', '2020-12-17T10:13:55.011Z', 'ACTIVE'], ['2153121416', 'Account_ADO', '2153121416', '5fdb2f6b45f48c4ef284f2c1', 'ENABLED', '2020-12-17T10:14:03.126Z', '2020-12-17T10:14:03.129Z', 'ACTIVE'], ['2153121411', 'Account_ADO', '2153121411', '5fdb2f7245f48c4ef284f2c2', 'ENABLED', '2020-12-17T10:14:10.772Z', '2020-12-17T10:14:10.775Z', 'ACTIVE'], ['2153121407', 'Account_ADO', '2153121407', '5fdb2f7c45f48c4ef284f2c3', 'ENABLED', '2020-12-17T10:14:20.585Z', '2020-12-17T10:14:20.586Z', 'ACTIVE'], ['2153121447', 'Account_ADO', '2153121447', '5fdb2f8445f48c4ef284f2c4', 'ENABLED', '2020-12-17T10:14:28.537Z', '2020-12-17T10:14:28.538Z', 'ACTIVE'], ['2153121475', 'Account_ADO', '2153121475', '5fe1b32345f48c4ef284f2c5', 'ENABLED', '2020-12-22T08:49:39.269Z', '2020-12-22T08:49:39.270Z', 'ACTIVE'], ['2153121455', 'Account_ADO', '2153121455', '5fe1b36945f48c4ef284f2c6', 'ENABLED', '2020-12-22T08:50:49.996Z', '2020-12-22T08:50:49.998Z', 'ACTIVE'], ['2153121427', 'Account_ADO', '2153121427', '5fe2064045f48c4ef284f2c7', 'ENABLED', '2020-12-22T14:44:16.700Z', '2020-12-22T14:44:16.701Z', 'ACTIVE'], ['2153121417', 'Account_ADO', '2153121417', '5fe2064b45f48c4ef284f2c8', 'ENABLED', '2020-12-22T14:44:27.125Z', '2020-12-22T14:44:27.126Z', 'ACTIVE'], ['2153121436', 'Account_ADO', '2153121436', '5fe2065a45f48c4ef284f2c9', 'ENABLED', '2020-12-22T14:44:42.028Z', '2020-12-22T14:44:42.029Z', 'ACTIVE'], ['2153121429', 'Account_ADO', '2153121429', '5fe2066845f48c4ef284f2ca', 'ENABLED', '2020-12-22T14:44:56.132Z', '2020-12-22T14:44:56.136Z', 'ACTIVE'], ['2153121425', 'Account_ADO', '2153121425', '5fe2067245f48c4ef284f2cb', 'ENABLED', '2020-12-22T14:45:06.767Z', '2020-12-22T14:45:06.768Z', 'ACTIVE'], ['2313212156', 'Account_ADO_TEST', '2313212156', '5fe22ace45f48c4ef284f2cc', 'ENABLED', '2020-12-22T17:20:14.383Z', '2020-12-22T17:20:14.384Z', 'ACTIVE'], ['098765432112', 'Account_Wiztivi', '098765432112', '5fe38f6045f48c4ef284f2ce', 'ENABLED', '2020-12-23T18:41:36.819Z', '2020-12-23T18:41:36.821Z', 'ACTIVE']]
            devices = core.show_devices()
            return render_template("SSP.html", posts=posts, devices=devices, flag=flag, form=form)
        elif form.filtertype.data == 'CaSN' and form.filter.data != '':
            flag = 'casn'
            devices = core.show_one_device(form.filter.data)
            #devices=[['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED', '2020-08-25T08:06:06.291Z','2020-08-25T08:06:06.294Z', 'ACTIVE']]
            return render_template("SSP.html", posts=posts, devices=devices,flag=flag, form=form)
        elif form.filtertype.data == 'AccountId' and form.filter.data == '':
            flag = 'acc'
            device = form.filter.data
            alldevices = core.ssp_getallaccounts()
            devices = []
            for i in alldevices:
                if device in i:
                    devices.append(i)
            # devices = core.show_one_device(form.filter.data)
            # devices = [['123456789', 'Account_Wiztivi', '123456789', '5f44c66e4eeb213f12a8a7f1', 'ENABLED',
            #             '2020-08-25T08:06:06.291Z', '2020-08-25T08:06:06.294Z', 'ACTIVE']]
            return render_template("SSP.html", posts=posts, devices=alldevices,flag=flag, form=form)
        elif form.filtertype.data == 'AccountId' and form.filter.data != '':
            flag = 'acc'
            accs= core.ssp_getallaccounts()
            accnum=''
            for j in accs:
                if form.filter.data in j:
                    accnum= j[0]
            acc = core.ssp_getoneaccount(accnum)
            if not acc:
                flash('Use the correct filter for the request', 'danger')
                return render_template("SSP.html", posts=posts, devices=devices, form=form)
            accdevices = core.show_devices_fromacc(acc[0][1])
            # devices = []
            # for i in alldevices:
            #     print(i)
            #     if acc[0][1] == i[1]:
            #         devices.append(i)
            # print(devices)
            return render_template("SSP.html", posts=posts, devices=acc,flag=flag,acc_devices= accdevices,len_devices=len(accdevices),form=form)
    return render_template("SSP.html", posts=posts, devices=devices, form=form)


@app.route('/ViewProc/<filename>')
def ViewProc(filename):
    with open("Web/" +PROC_FOLDER +str(filename), "r") as f:
        procedure = f.read()
    return render_template("ProcView.html", posts=posts, procedure=procedure)


@app.route("/VOD",methods=['GET', 'POST'])
def VOD():
    form= VODForm()
    if form.validate_on_submit():
        if form.filtertype.data == "Nodes" and form.filter.data != '':
            response = json.dumps(core.vod_getnodes(form.filter.data), sort_keys=True, indent=4, separators=(',', ': '))
            return render_template("VOD.html", posts=posts, form=form, response=response)
        elif form.filtertype.data == "Editorials" and form.filter.data != '':
            content = core.vod_geteditorials()
    response = ''

    #####en el html de vod hay que printear la tabla de las peliculas, poner un if dependiendo del filtro que tiene
    #response =[['Title 1', 'LYS000000141', ['LYS000000143', 'LYS000000145'], [], True], ['Title 2', 'LYS000000142', [], [], True], ['RootTricomTree', 'LYS000002864', ['CAT100000012', 'CAT000000002', 'CAT000000003', 'CAT000000001', 'CAT000000004'], [], True], ['Promotions', 'LYS000006023', ['LYS000006025', 'LYS000015918', 'LYS000015920', 'LYS000017668', 'LYS1000000001', 'LYS1000000003', 'LYS1000000002', 'LYS1000000004'], [], True], ['SAT1', 'LYS000006255', [], [], True], ['SAT2', 'SAT2', [], [], True], ['SAT3', 'SAT3', [], [], True], ['SAT22', 'SAT22', [], [], True], ['SAT05', 'SAT5', [], [], True], ['Terror', 'CAT300000010', [], ['LYS000002864', 'CAT000000001'], False], ['Thriller', 'CAT300000011', [], ['LYS000002864', 'CAT000000001'], False], ['Estrenos', 'CAT300000012', [], ['LYS000002864', 'CAT000000001'], False], ['Acción', 'CAT300000001', [], ['LYS000002864', 'CAT000000001'], False], ['Animación', 'CAT300000002', [], ['LYS000002864', 'CAT000000001'], False], ['Aventura', 'CAT300000003', [], ['LYS000002864', 'CAT000000001'], False], ['Caribbean Cinemas', 'CAT300000013', [], ['LYS000002864', 'CAT000000001'], False], ['Comedia', 'CAT300000004', [], ['LYS000002864', 'CAT000000001'], False], ['Documental', 'CAT300000005', [], ['LYS000002864', 'CAT000000001'], False], ['Drama', 'CAT300000006', [], ['LYS000002864', 'CAT000000001'], False], ['Familia', 'CAT300000007', [], ['LYS000002864', 'CAT000000001'], False], ['Romance', 'CAT300000008', [], ['LYS000002864', 'CAT000000001'], False], ['Sci-Fi', 'CAT300000009', [], ['LYS000002864', 'CAT000000001'], False], ['Acción', 'CAT100000001', [], ['LYS000002864', 'CAT000000002'], False], ['Animación', 'CAT100000008', [], ['LYS000002864', 'CAT000000002'], False], ['Aventura', 'CAT100000002', [], ['LYS000002864', 'CAT000000002'], False], ['Comedia', 'CAT100000003', [], ['LYS000002864', 'CAT000000002'], False], ['Documental', 'CAT100000010', [], ['LYS000002864', 'CAT000000002'], False], ['Drama', 'CAT100000004', [], ['LYS000002864', 'CAT000000002'], False], ['Romance', 'CAT100000011', [], ['LYS000002864', 'CAT000000002'], False], ['Sci-Fi', 'CAT100000005', [], ['LYS000002864', 'CAT000000002'], False], ['Terror', 'CAT100000006', [], ['LYS000002864', 'CAT000000002'], False], ['Thriller', 'CAT100000007', [], ['LYS000002864', 'CAT000000002'], False], ['Familia', 'CAT100000009', [], ['LYS000002864', 'CAT000000002'], False], ['Películas', 'CAT200000001', [], ['LYS000002864', 'CAT000000003'], False], ['Series', 'CAT200000002', ['GJL019512', 'GJL016163', 'GJL016114', 'GJL016198', 'GJL016103', 'GJL020357', 'GJL019505', 'GJL020390', 'GJL017149', 'GJL016148', 'GJL019503', 'GJL020404', 'GJL016215', 'GJL020353', 'GJL016247', 'GJL016124', 'GJL020240', 'GJL016286', 'GJL020242', 'GJL020056', 'GJL021780', 'GJL016122', 'GJL019583', 'GJL020244', 'GJL016065', 'GJL019248', 'GJL016119', 'GJL020199', 'GJL016157', 'GJL019501', 'GJL016273', 'GJL019266', 'GJL017382', 'GJL017387', 'GJL017145', 'GJL017154', 'GJL017143', 'GJL017385', 'GJL023035', 'GJL016070', 'GJL016243', 'GJL016063', 'GJL020347', 'GJL016175', 'GJL016211', 'GJL016230', 'GJL016239', 'GJL016257', 'GJL023245'], ['LYS000002864', 'CAT000000003'], False], ['All', 'CAT400000011', ['GJL00001', 'GJL00003', 'GJL00004', 'GJL00012', 'GJL00015', 'GJL00014', 'GJL00018', 'GJL00019', 'GJL00024', 'GJL00020', 'GJL00021', 'GJL00028', 'GJL00031', 'GJL00030'], ['LYS000002864', 'CAT000000004'], False], ['Maigret', 'GJL021494', ['GJL021495', 'GJL026620'], ['LYS000002864', 'CAT100000012'], False], ['19-2', 'GJL021811', ['GJL021812', 'GJL021813', 'GJL021814', 'GJL028552'], ['LYS000002864', 'CAT100000012'], False], ['North & South', 'GJL020933', ['GJL020934'], ['LYS000002864', 'CAT100000012'], False], ['Broken', 'GJL028599', ['GJL028600'], ['LYS000002864', 'CAT100000012'], False], ['Jane Eyre', 'GJL020935', ['GJL020936'], ['LYS000002864', 'CAT100000012'], False], ['Class', 'GJL026746', ['GJL026747'], ['LYS000002864', 'CAT100000012'], False], ['Born To Kill', 'GJL028607', ['GJL028608'], ['LYS000002864', 'CAT100000012'], False], ['Women in Love', 'GJL020954', ['GJL020955'], ['LYS000002864', 'CAT100000012'], False], ['Pride And Prejudice', 'GJL020931', ['GJL020932'], ['LYS000002864', 'CAT100000012'], False], ['Silk', 'GJL028613', ['GJL028614', 'GJL028615', 'GJL028616'], ['LYS000002864', 'CAT100000012'], False], ['The Bletchley Circle', 'GJL019806', ['GJL019807', 'GJL021806'], ['LYS000002864', 'CAT100000012'], False], ['Run', 'GJL028546', ['GJL028547'], ['LYS000002864', 'CAT100000012'], False], ['Luther', 'GJL020923', ['GJL020924', 'GJL020925', 'GJL020926', 'GJL021299'], ['LYS000002864', 'CAT100000012'], False], ['The Driver', 'GJL028540', ['GJL028550'], ['LYS000002864', 'CAT100000012'], False], ['Cranford', 'GJL020941', ['GJL020942'], ['LYS000002864', 'CAT100000012'], False], ['Line of Duty', 'GJL019804', ['GJL019805', 'GJL021942', 'GJL021943', 'GJL021944'], ['LYS000002864', 'CAT100000012'], False], ['Emma', 'GJL020937', ['GJL020938'], ['LYS000002864', 'CAT100000012'], False], ['Bleak House', 'GJL020950', ['GJL020951'], ['LYS000002864', 'CAT100000012'], False], ['Heartland', 'GJL019808', ['GJL019809', 'GJL021845', 'GJL021846', 'GJL021847', 'GJL021848', 'GJL021849'], ['LYS000002864', 'CAT100000012'], False], ['Great Expectations', 'GJL020948', ['GJL020949'], ['LYS000002864', 'CAT100000012'], False], ['Return to Cranford', 'GJL020943', ['GJL020944'], ['LYS000002864', 'CAT100000012'], False], ['Upstairs Downstairs', 'GJL020945', ['GJL020946', 'GJL020947'], ['LYS000002864', 'CAT100000012'], False], ['Sense & Sensibility', 'GJL020939', ['GJL020940'], ['LYS000002864', 'CAT100000012'], False], ['Life On Mars', 'GJL013607', ['GJL013608', 'GJL013609'], ['LYS000002864', 'CAT100000012'], False], ['Doctor Who', 'GJL020912', ['GJL020913', 'GJL020914', 'GJL020915', 'GJL020916', 'GJL020917', 'GJL020918', 'GJL020919', 'GJL020920', 'GJL020921'], ['LYS000002864', 'CAT100000012'], False], ['Infiltrados', 'GJL022652', ['GJL022653'], ['LYS000002864', 'CAT100000012'], False], ['Sin Tetas No Hay Paraiso', 'GJL022533', ['GJL022534'], ['LYS000002864', 'CAT100000012'], False], ['Fugitivos', 'GJL022610', ['GJL022611'], ['LYS000002864', 'CAT100000012'], False], ['12 Monos', 'GJL028434', ['GJL028486', 'GJL028487', 'GJL028488', 'GJL028489'], ['LYS000002864', 'CAT100000012'], False], ['Mundo sin Fin', 'GJL022007', ['GJL022008'], ['LYS000002864', 'CAT100000012'], False], ['Continuum', 'GJL016091', ['GJL016092'], ['LYS000002864', 'CAT100000012'], False], ['Camelot', 'GJL016072', ['GJL016071'], ['LYS000002864', 'CAT100000012'], False], ['The Pillars of the Earth', 'GJL016259', ['GJL016260'], ['LYS000002864', 'CAT100000012'], False], ['Ripper Street', 'GJL020927', ['GJL020928', 'GJL020929', 'GJL020930', 'GJL021535', 'GJL028635'], ['LYS000002864', 'CAT100000012'], False], ['The Interceptor', 'GJL021543', ['GJL021544'], ['LYS000002864', 'CAT100000012'], False], ['Bo on the Go', 'GJL019512', ['GJL019686'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Littlest Pet Shop', 'GJL017143', ['GJL017144'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Heathcliff', 'GJL016163', ['GJL016164'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Kaijudo', 'GJL017385', ['GJL017386'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Dino Squad', 'GJL016114', ['GJL016115'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Martha Speaks', 'GJL016198', ['GJL016199'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Molang', 'GJL023035', ['GJL023036', 'GJL023037'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Dennis the Menace', 'GJL016103', ['GJL016104'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Ultimate Spider-Man', 'GJL016286', ['GJL022479'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Caillou', 'GJL016070', ['GJL016069'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Gravity Falls', 'GJL020242', ['GJL020243'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Charlie & Lola', 'GJL020357', ['GJL020356'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Strawberry Shortcake', 'GJL016243', ['GJL016244'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Mickey Mouse Clubhouse', 'GJL020056', ['GJL020057'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Sarah & Duck', 'GJL019505', ['GJL019506'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Animal Mechanicals', 'GJL016063', ['GJL020340'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Disney Motorcity', 'GJL021780', ['GJL021781'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Little Einsteins', 'GJL016122', ['GJL016123'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ["Archie's Weird Mysteries", 'GJL020347', ['GJL020346'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Los Numtums', 'GJL020390', ['GJL020389'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Kim Possible', 'GJL019583', ['GJL019584'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['El Inspector Gadget', 'GJL016175', ['GJL016176'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Dragon', 'GJL017149', ['GJL017150'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Star contra las fuerzas del mal', 'GJL020244', ['GJL020245'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Los Vengadores: ¡los héroes más poderosos del mundo!', 'GJL016065', ['GJL016064'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Mona The Vampire', 'GJL016211', ['GJL016212'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Flight Squad', 'GJL016148', ['GJL016149'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Sabrina, Animated Series', 'GJL016230', ['GJL016232'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Ave y Tres', 'GJL019503', ['GJL019504'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Disney Liv & Maddie', 'GJL019248', ['GJL019250', 'GJL019249'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Sonic the Hedgehog', 'GJL016239', ['GJL016240'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Lilo & Stitch', 'GJL016119', ['GJL016121'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Little Robots', 'GJL020404', ['GJL020405', 'GJL020406'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['The Little Lulu Show', 'GJL016257', ['GJL016258'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Phineas y Ferb', 'GJL020199', ['GJL020182'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Mummies Alive', 'GJL016215', ['GJL016216'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Pirata & Capitano', 'GJL023245', ['GJL023246'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Los Ositos Cariñosos', 'GJL020353', ['GJL020352'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Manny Manitas', 'GJL016157', ['GJL016158'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['The Adventures of Paddington Bear', 'GJL016247', ['GJL016248'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Los magos de Waverly Place', 'GJL016124', ['GJL021750'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Hulk y los agentes de S.M.A.S.H.', 'GJL019501', ['GJL019502'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Randy Cunningham: Ninja Total', 'GJL020240', ['GJL020241'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['The Super Hero Squad Show', 'GJL016273', ['GJL016274'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Disney Austin & Ally', 'GJL019266', ['GJL019267', 'GJL019268'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['My Little Pony: La Magia de la Amistad', 'GJL017382', ['GJL017383'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Rescue Bots', 'GJL017387', ['GJL017388'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Transformers Prime', 'GJL017145', ['GJL017146'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Transformers Animated', 'GJL017154', ['GJL017155', 'GJL017156'], ['LYS000002864', 'CAT000000003', 'CAT200000002'], False], ['Line of Duty', 'GJL00001', ['GJL00009', 'GJL00035'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Private Eyes', 'GJL00003', ['GJL00011'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Ransom', 'GJL00004', ['GJL00005'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Bates Motel', 'GJL00012', ['GJL00013'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Run', 'GJL00015', ['GJL00017'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Sin Tetas No Hay Paraiso', 'GJL00014', ['GJL00016'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Bellevue', 'GJL00018', ['GJL00026'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Maigret', 'GJL00019', ['GJL00027'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Rookie Blue', 'GJL00024', ['GJL00025'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['The Driver', 'GJL00020', ['GJL00023'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['The Great Train Robbery', 'GJL00021', ['GJL00022'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Mary Kills People', 'GJL00028', ['GJL00029'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Heartland', 'GJL00031', ['GJL00033', 'GJL00034', 'GJL00036', 'GJL00037', 'GJL00038'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Jack Taylor', 'GJL00030', ['GJL00032'], ['LYS000002864', 'CAT000000004', 'CAT400000011'], False], ['Line of Duty T01', 'GJL00009', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00001'], False], ['Line of Duty T02', 'GJL00035', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00001'], False], ['Private Eyes T01', 'GJL00011', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00003'], False], ['Ransom T03', 'GJL00005', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00004'], False], ['Motel Bates T01', 'GJL00013', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00012'], False], ['Sin Tetas No Hay Paraiso T01', 'GJL00016', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00014'], False], ['Run T01', 'GJL00017', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00015'], False], ['Bellevue T01', 'GJL00026', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00018'], False], ['Maigret T01', 'GJL00027', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00019'], False], ['The Driver T01', 'GJL00023', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00020'], False], ['The Great Train Robbery T01', 'GJL00022', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00021'], False], ['Rookie Blue T01', 'GJL00025', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00024'], False], ['Mary Kills People T01', 'GJL00029', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00028'], False], ['Jack Taylor T01', 'GJL00032', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00030'], False], ['Heartland T01', 'GJL00033', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00031'], False], ['Heartland T02', 'GJL00034', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00031'], False], ['Heartland T03', 'GJL00036', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00031'], False], ['Heartland T04', 'GJL00037', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00031'], False], ['Heartland T05', 'GJL00038', [], ['LYS000002864', 'CAT000000004', 'CAT400000011', 'GJL00031'], False], ['Life On Mars T01', 'GJL013608', [], ['LYS000002864', 'CAT100000012', 'GJL013607'], False], ['Life On Mars T02', 'GJL013609', [], ['LYS000002864', 'CAT100000012', 'GJL013607'], False], ['Animal Mechanicals T02', 'GJL020340', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016063'], False], ['Los Vengadores: ¡los héroes más poderosos del mundo! T01', 'GJL016064', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016065'], False], ['Caillou T04', 'GJL016069', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016070'], False], ['Camelot T01', 'GJL016071', [], ['LYS000002864', 'CAT100000012', 'GJL016072'], False], ['Continuum T01', 'GJL016092', [], ['LYS000002864', 'CAT100000012', 'GJL016091'], False], ['Dennis the Menace T01', 'GJL016104', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016103'], False], ['Dino Squad T01', 'GJL016115', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016114'], False], ['Lilo & Stitch T02', 'GJL016121', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016119'], False], ['Little Einsteins T01', 'GJL016123', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016122'], False], ['Los magos de Waverly Place T01', 'GJL021750', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016124'], False], ['Flight Squad T01', 'GJL016149', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016148'], False], ['Manny Manitas T01', 'GJL016158', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016157'], False], ['Heathcliff T01', 'GJL016164', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016163'], False], ['El Inspector Gadget T01', 'GJL016176', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016175'], False], ['Martha Speaks T01', 'GJL016199', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016198'], False], ['Mona The Vampire T01', 'GJL016212', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016211'], False], ['Mummies Alive T01', 'GJL016216', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016215'], False], ['Sabrina, Animated Series T02', 'GJL016232', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016230'], False], ['Sonic the Hedgehog T01', 'GJL016240', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016239'], False], ['Strawberry Shortcake T01', 'GJL016244', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016243'], False], ['The Adventures of Paddington Bear T02', 'GJL016248', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016247'], False], ['The Little Lulu Show T01', 'GJL016258', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016257'], False], ['The Pillars of the Earth T01', 'GJL016260', [], ['LYS000002864', 'CAT100000012', 'GJL016259'], False], ['The Super Hero Squad Show T01', 'GJL016274', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016273'], False], ['Ultimate Spider-Man T03', 'GJL022479', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL016286'], False], ['Littlest Pet Shop T01', 'GJL017144', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017143'], False], ['Transformers Prime T01', 'GJL017146', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017145'], False], ['Dragon  T01', 'GJL017150', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017149'], False], ['Transformers Animated T01', 'GJL017155', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017154'], False], ['Transformers Animated T02', 'GJL017156', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017154'], False], ['My Little Pony: La Magia de la Amistad T01', 'GJL017383', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017382'], False], ['Kaijudo T01', 'GJL017386', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017385'], False], ['Rescue Bots T01', 'GJL017388', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL017387'], False], ['Disney Liv & Maddie T01', 'GJL019250', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019248'], False], ['Disney Liv & Maddie T02', 'GJL019249', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019248'], False], ['Disney Austin & Ally  T03', 'GJL019267', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019266'], False], ['Disney Austin & Ally  T04', 'GJL019268', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019266'], False], ['Hulk y los agentes de S.M.A.S.H. T01', 'GJL019502', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019501'], False], ['Ave y Tres T01', 'GJL019504', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019503'], False], ['Sarah & Duck T01', 'GJL019506', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019505'], False], ['Bo on the Go T02', 'GJL019686', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019512'], False], ['Kim Possible T01', 'GJL019584', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL019583'], False], ['Line of Duty T01', 'GJL019805', [], ['LYS000002864', 'CAT100000012', 'GJL019804'], False], ['Line of Duty T02', 'GJL021942', [], ['LYS000002864', 'CAT100000012', 'GJL019804'], False], ['Line of Duty T03', 'GJL021943', [], ['LYS000002864', 'CAT100000012', 'GJL019804'], False], ['Line of Duty T04', 'GJL021944', [], ['LYS000002864', 'CAT100000012', 'GJL019804'], False], ['The Bletchley Circle T01', 'GJL019807', [], ['LYS000002864', 'CAT100000012', 'GJL019806'], False], ['The Bletchley Circle T02', 'GJL021806', [], ['LYS000002864', 'CAT100000012', 'GJL019806'], False], ['Heartland T01', 'GJL019809', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Heartland T02', 'GJL021845', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Heartland T03', 'GJL021846', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Heartland T04', 'GJL021847', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Heartland T05', 'GJL021848', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Heartland T06', 'GJL021849', [], ['LYS000002864', 'CAT100000012', 'GJL019808'], False], ['Mickey Mouse Clubhouse T01', 'GJL020057', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020056'], False], ['Phineas y Ferb T01', 'GJL020182', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020199'], False], ['Randy Cunningham: Ninja Total T02', 'GJL020241', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020240'], False], ['Gravity Falls T01', 'GJL020243', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020242'], False], ['Star contra las fuerzas del mal T01', 'GJL020245', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020244'], False], ["Archie's Weird Mysteries T01", 'GJL020346', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020347'], False], ['Los Ositos Cariñosos T01', 'GJL020352', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020353'], False], ['Charlie & Lola T01', 'GJL020356', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020357'], False], ['Los Numtums T01', 'GJL020389', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020390'], False], ['Little Robots T01', 'GJL020405', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020404'], False], ['Little Robots T02', 'GJL020406', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL020404'], False], ['Doctor Who T01', 'GJL020913', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T02', 'GJL020914', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T03', 'GJL020915', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T04', 'GJL020916', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T05', 'GJL020917', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T06', 'GJL020918', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T07', 'GJL020919', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T08', 'GJL020920', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Doctor Who T09', 'GJL020921', [], ['LYS000002864', 'CAT100000012', 'GJL020912'], False], ['Luther T01', 'GJL020924', [], ['LYS000002864', 'CAT100000012', 'GJL020923'], False], ['Luther T02', 'GJL020925', [], ['LYS000002864', 'CAT100000012', 'GJL020923'], False], ['Luther T03', 'GJL020926', [], ['LYS000002864', 'CAT100000012', 'GJL020923'], False], ['Luther T04', 'GJL021299', [], ['LYS000002864', 'CAT100000012', 'GJL020923'], False], ['Ripper Street T01', 'GJL020928', [], ['LYS000002864', 'CAT100000012', 'GJL020927'], False], ['Ripper Street T02', 'GJL020929', [], ['LYS000002864', 'CAT100000012', 'GJL020927'], False], ['Ripper Street T03', 'GJL020930', [], ['LYS000002864', 'CAT100000012', 'GJL020927'], False], ['Ripper Street T04', 'GJL021535', [], ['LYS000002864', 'CAT100000012', 'GJL020927'], False], ['Ripper Street T05', 'GJL028635', [], ['LYS000002864', 'CAT100000012', 'GJL020927'], False], ['Pride And Prejudice T01', 'GJL020932', [], ['LYS000002864', 'CAT100000012', 'GJL020931'], False], ['North & South T01', 'GJL020934', [], ['LYS000002864', 'CAT100000012', 'GJL020933'], False], ['Jane Eyre T01', 'GJL020936', [], ['LYS000002864', 'CAT100000012', 'GJL020935'], False], ['Emma T01', 'GJL020938', [], ['LYS000002864', 'CAT100000012', 'GJL020937'], False], ['Sense & Sensibility T01', 'GJL020940', [], ['LYS000002864', 'CAT100000012', 'GJL020939'], False], ['Cranford T01', 'GJL020942', [], ['LYS000002864', 'CAT100000012', 'GJL020941'], False], ['Return to Cranford T01', 'GJL020944', [], ['LYS000002864', 'CAT100000012', 'GJL020943'], False], ['Upstairs Downstairs T01', 'GJL020946', [], ['LYS000002864', 'CAT100000012', 'GJL020945'], False], ['Upstairs Downstairs T02', 'GJL020947', [], ['LYS000002864', 'CAT100000012', 'GJL020945'], False], ['Great Expectations T01', 'GJL020949', [], ['LYS000002864', 'CAT100000012', 'GJL020948'], False], ['Bleak House T01', 'GJL020951', [], ['LYS000002864', 'CAT100000012', 'GJL020950'], False], ['Women in Love T01', 'GJL020955', [], ['LYS000002864', 'CAT100000012', 'GJL020954'], False], ['Maigret T01', 'GJL021495', [], ['LYS000002864', 'CAT100000012', 'GJL021494'], False], ['Maigret T02', 'GJL026620', [], ['LYS000002864', 'CAT100000012', 'GJL021494'], False], ['The Interceptor T01', 'GJL021544', [], ['LYS000002864', 'CAT100000012', 'GJL021543'], False], ['Disney Motorcity T01', 'GJL021781', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL021780'], False], ['19-2 T01', 'GJL021812', [], ['LYS000002864', 'CAT100000012', 'GJL021811'], False], ['19-2 T02', 'GJL021813', [], ['LYS000002864', 'CAT100000012', 'GJL021811'], False], ['19-2 T03', 'GJL021814', [], ['LYS000002864', 'CAT100000012', 'GJL021811'], False], ['19-2 T04', 'GJL028552', [], ['LYS000002864', 'CAT100000012', 'GJL021811'], False], ['Mundo sin Fin T01', 'GJL022008', [], ['LYS000002864', 'CAT100000012', 'GJL022007'], False], ['Sin Tetas No Hay Paraiso T01', 'GJL022534', [], ['LYS000002864', 'CAT100000012', 'GJL022533'], False], ['Fugitivos T01', 'GJL022611', [], ['LYS000002864', 'CAT100000012', 'GJL022610'], False], ['Infiltrados T01', 'GJL022653', [], ['LYS000002864', 'CAT100000012', 'GJL022652'], False], ['Molang T01', 'GJL023036', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL023035'], False], ['Molang T02', 'GJL023037', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL023035'], False], ['Pirata & Capitano T01', 'GJL023246', [], ['LYS000002864', 'CAT000000003', 'CAT200000002', 'GJL023245'], False], ['Class T01', 'GJL026747', [], ['LYS000002864', 'CAT100000012', 'GJL026746'], False], ['12 Monos T01', 'GJL028486', [], ['LYS000002864', 'CAT100000012', 'GJL028434'], False], ['12 Monos T02', 'GJL028487', [], ['LYS000002864', 'CAT100000012', 'GJL028434'], False], ['12 Monos T03', 'GJL028488', [], ['LYS000002864', 'CAT100000012', 'GJL028434'], False], ['12 Monos T04', 'GJL028489', [], ['LYS000002864', 'CAT100000012', 'GJL028434'], False], ['The Driver T01', 'GJL028550', [], ['LYS000002864', 'CAT100000012', 'GJL028540'], False], ['Run T01', 'GJL028547', [], ['LYS000002864', 'CAT100000012', 'GJL028546'], False], ['Broken T01', 'GJL028600', [], ['LYS000002864', 'CAT100000012', 'GJL028599'], False], ['Born To Kill T01', 'GJL028608', [], ['LYS000002864', 'CAT100000012', 'GJL028607'], False], ['Silk T01', 'GJL028614', [], ['LYS000002864', 'CAT100000012', 'GJL028613'], False], ['Silk T02', 'GJL028615', [], ['LYS000002864', 'CAT100000012', 'GJL028613'], False], ['Silk T03', 'GJL028616', [], ['LYS000002864', 'CAT100000012', 'GJL028613'], False], ['Title 1 1', 'LYS000000143', [], ['LYS000000141'], False], ['Title 1 2', 'LYS000000145', ['LYS000005824'], ['LYS000000141'], False], ['Title 1 1 1', 'LYS000005824', [], ['LYS000000141', 'LYS000000145'], False], ['Witzy', 'CAT000000004', ['CAT400000011'], ['LYS000002864'], False], ['Películas', 'CAT000000002', ['CAT100000002', 'CAT100000003', 'CAT100000010', 'CAT100000004', 'CAT100000011', 'CAT100000005', 'CAT100000006', 'CAT100000007', 'CAT100000009', 'CAT100000001', 'CAT100000008'], ['LYS000002864'], False], ['Renta', 'CAT000000001', ['CAT300000012', 'CAT300000001', 'CAT300000002', 'CAT300000003', 'CAT300000013', 'CAT300000004', 'CAT300000005', 'CAT300000006', 'CAT300000007', 'CAT300000008', 'CAT300000009', 'CAT300000010', 'CAT300000011'], ['LYS000002864'], False], ['Series', 'CAT100000012', ['GJL020933', 'GJL020935', 'GJL020954', 'GJL020931', 'GJL020923', 'GJL020941', 'GJL020937', 'GJL020950', 'GJL020948', 'GJL020943', 'GJL020945', 'GJL020939', 'GJL013607', 'GJL019808', 'GJL020912', 'GJL022652', 'GJL022533', 'GJL022610', 'GJL028434', 'GJL022007', 'GJL016091', 'GJL016072', 'GJL020927', 'GJL021543', 'GJL021494', 'GJL021811', 'GJL028599', 'GJL026746', 'GJL028607', 'GJL028613', 'GJL019806', 'GJL028546', 'GJL028540', 'GJL019804', 'GJL016259'], ['LYS000002864'], False], ['Ninos', 'CAT000000003', ['CAT200000001', 'CAT200000002'], ['LYS000002864'], False], ['Series', 'LYS000006025', ['PM020200317083306', 'PM020200317083459', 'PM020200422033432', 'PM020200422033650'], ['LYS000006023'], False], ['Series', 'LYS000015918', [], ['LYS000006023'], False], ['Series', 'LYS000015920', ['PM020200422035132', 'PM020200422035207'], ['LYS000006023'], False], ['Renta', 'LYS000017668', [], ['LYS000006023'], False], ['STBSeries', 'LYS1000000001', ['PM020191120111907', 'PM020191120112032', 'PM020191120112159', 'PM020200317084505', 'PM020200317084628', 'PM020200422035503'], ['LYS000006023'], False], ['STBNinos', 'LYS1000000003', ['PM020191120112702', 'PM020200422035636'], ['LYS000006023'], False], ['STBPeliculas', 'LYS1000000002', [], ['LYS000006023'], False], ['STBRenta', 'LYS1000000004', [], ['LYS000006023'], False], ['The Interceptor', 'PM020200422033432', ['PM020200422033437'], ['LYS000006023', 'LYS000006025'], False], ['Class', 'PM020200317083306', [], ['LYS000006023', 'LYS000006025'], False], ['Broken', 'PM020200422033650', [], ['LYS000006023', 'LYS000006025'], False], ['Born to Kill', 'PM020200317083459', [], ['LYS000006023', 'LYS000006025'], False], ['Bo on the Go', 'PM020200422035132', ['PM020200422035137'], ['LYS000006023', 'LYS000015920'], False], ['Bo on the Go', 'PM020200422035207', ['PM020200422035212'], ['LYS000006023', 'LYS000015920'], False], ['Sin Tetas No Hay Paraiso', 'PM020191120111907', ['PM020191120111912'], ['LYS000006023', 'LYS1000000001'], False], ['Fugitivos', 'PM020191120112159', ['PM020191120112204'], ['LYS000006023', 'LYS1000000001'], False], ['Infiltrados', 'PM020191120112032', [], ['LYS000006023', 'LYS1000000001'], False], ['Class', 'PM020200317084505', [], ['LYS000006023', 'LYS1000000001'], False], ['12 Monkeys', 'PM020200422035503', ['PM020200422035508'], ['LYS000006023', 'LYS1000000001'], False], ['Born to Kill', 'PM020200317084628', [], ['LYS000006023', 'LYS1000000001'], False], ['Strawberry Shortcake', 'PM020191120112702', ['PM020191120112707'], ['LYS000006023', 'LYS1000000003'], False], ['Bo on the Go', 'PM020200422035636', ['PM020200422035641'], ['LYS000006023', 'LYS1000000003'], False], ['Sin Tetas No Hay Paraiso', 'PM020191120111912', [], ['LYS000006023', 'LYS1000000001', 'PM020191120111907'], False], ['Fugitivos', 'PM020191120112204', [], ['LYS000006023', 'LYS1000000001', 'PM020191120112159'], False], ['Strawberry Shortcake', 'PM020191120112707', [], ['LYS000006023', 'LYS1000000003', 'PM020191120112702'], False], ['The Interceptor', 'PM020200422033437', [], ['LYS000006023', 'LYS000006025', 'PM020200422033432'], False], ['Bo on the Go', 'PM020200422035137', [], ['LYS000006023', 'LYS000015920', 'PM020200422035132'], False], ['Bo on the Go', 'PM020200422035212', [], ['LYS000006023', 'LYS000015920', 'PM020200422035207'], False], ['12 Monkeys', 'PM020200422035508', [], ['LYS000006023', 'LYS1000000001', 'PM020200422035503'], False], ['Bo on the Go', 'PM020200422035641', [], ['LYS000006023', 'LYS1000000003', 'PM020200422035636'], False]]
    #print(core.vod_getnodes('2153121588'))
    return render_template("VOD.html", posts=posts, form=form, response=response, content=content)


@app.route('/Homepage/Doc/Wmspanel')
def Wmspanel():
    return render_template("Wmspanel.html")

