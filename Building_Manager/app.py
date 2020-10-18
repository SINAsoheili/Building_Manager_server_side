from flask import Flask , abort , jsonify , request
from db_config import HOST , USER , PASSWD , DB_NAME , AUTH_PLUGIN
from mysql import connector


app = Flask(__name__)

#Manager-------------------------------------
@app.route("/manager/register" , methods=["GET"])
def manager_register():
    passwd = request.args.get("password")
    phone  = request.args.get("phone")

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)

    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "INSERT INTO `manager` (passwd , phone) VALUES ('%s'  , '%s')"%(passwd , phone)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount > 0 :
        cmd = "SELECT * FROM `manager` WHERE phone='%s'"%phone
        cursor.execute(cmd)

        result = cursor.fetchall()
        cursor.close()
        db.close()
        if len(result) == 0 :
            result = {"status":True , "manager_id":-1} 
            cursor.close()
            return result   
        else:
            row = result[0]
            id = row[0]
            result = {"status":True , "manager_id":id} 
            return result
    else :
        cursor.close()
        db.close()
        result = {"status":False , "manager_id":-1}
        return result



#Building---------------------------------------
@app.route("/building/register" , methods=["get"])
def building_register():
    name = request.args.get("name")
    cash = float(request.args.get("cash"))
    address = request.args.get("address")
    unit_count = int(request.args.get("unit_count"))
    manager_id = int(request.args.get("manager_id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "INSERT INTO `building` (name , cash , address , unit_count , manager_id) VALUES ('%s' , %f , '%s' , %i , %i)"%(name , cash , address , unit_count , manager_id)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        respose = {"status":False , "id":-1}
        cursor.close()
        db.close()
        return respose
    else:
        cmd = "SELECT id FROM `building` WHERE manager_id=%i"%manager_id
        cursor.execute(cmd)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        if len(result) == 0:
            respose = {"status":True , "id":-1}
            return respose
        else :
            row = result[len(result)-1]
            id = row[0]
            respose = {"status":True , "id":id}
            return respose


@app.route("/building/list" , methods=["get"])
def building_list():
    manager_id = int(request.args.get("manager_id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `building` WHERE manager_id=%i"%manager_id
    cursor.execute(cmd)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    list_response = []
    for obj in result:
        id , name , cash , address , unit_count , manager_id = obj
        response = {
            "id": id , 
            "name": name ,
            "cash": cash , 
            "address": address , 
            "unit_count": unit_count , 
            "manager_id": manager_id
        }

        list_response.append(response)

    return jsonify(list_response)



#Unit-------------------------------------------
@app.route("/unit/add" , methods=['GET'])
def unit_register():
    owner_name  = request.args.get("owner_name")
    phone       = request.args.get("phone")
    unit_number = request.args.get("unit_number")
    tag         = request.args.get("tag")
    building_id = request.args.get("building_id")

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "INSERT INTO `unit` (owner_name , phone , unit_number , tag , building_id) VALUES ('%s' , '%s' , %i , %i , %i)"%(owner_name , phone , int(unit_number) , int(tag) , int(building_id))
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0:
        response = {"status":False}
    else :
        response = {"status":True}

    cursor.close()
    db.close()    
    return jsonify(response)


@app.route("/unit/list" , methods=["get"])
def unit_list():
    building_id = int(request.args.get("building_id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `unit` WHERE building_id=%i"%building_id
    cursor.execute(cmd)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    list_response = []
    for obj in result:
        owner_name , phone , unit_number , tag , building_id = obj
        response = {
            "owner_name":owner_name , 
            "phone":phone ,
            "unit_number":unit_number , 
            "tag":tag , 
            "building_id":building_id
        }

        list_response.append(response)

    return jsonify(list_response)

@app.route("/unit/del" , methods=['GET'])
def unit_delete():
    phone       = request.args.get("phone")
    unit_number = int(request.args.get("unit_number"))
    building_id = int(request.args.get("building_id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "DELETE FROM `unit` WHERE phone=%s AND unit_number=%i AND building_id=%i"%(phone , unit_number , building_id)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0:
        response = {"status":False}
    else :
        response = {"status":True}

    cursor.close()
    db.close()    
    return jsonify(response)

#notification ----------------------------------
@app.route("/notification/add" , methods=['GET'])
def notification_add():
    text = request.args.get("text")
    date = request.args.get("date")
    title = request.args.get("title")
    buildingId = int(request.args.get("buildingId"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "INSERT INTO `notification` (text , date , title , building_id) VALUES('%s' , '%s' , '%s' , %i)"%(text , date , title , buildingId)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0:
        result = {"result":False}
    else :
        result = {"result":True}

    cursor.close()
    db.close()
    return result     

@app.route("/notification/list" , methods=['GET'])
def notification_list():
    buildingId = int(request.args.get("buildingId"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `notification` where building_id=%i"%buildingId
    cursor.execute(cmd)
    itmes = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for obj in itmes:
        id , text , date , title , building_id = obj
        item = {
            "id":id , 
            "text":text , 
            "date":date , 
            "title":title ,
            "building_id":building_id
        }
        result.append(item)
    
    return jsonify(result)

@app.route("/notification/del" , methods=["GET"])
def notification_del():
    id = int(request.args.get("id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "DELETE FROM notification WHERE id=%i"%id
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result  

#repair-----------------------------------------
@app.route("/repair/add" , methods=["GET"])
def repair_add():
    date = request.args.get("date")
    comment = request.args.get("comment")
    title = request.args.get("title")
    amount = float(request.args.get("amount"))
    building_id = int(request.args.get("buildingId"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "INSERT INTO `repair` (date , comment , title , amount , building_id) VALUES ('%s' , '%s' , '%s' , %f , %i)"%(date , comment , title , amount , building_id)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result    

@app.route("/repair/list" , methods=["GET"])
def repair_list():
    buildingId = int(request.args.get("buildingId"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `repair` where building_id=%i"%buildingId
    cursor.execute(cmd)
    itmes = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for obj in itmes:
        id , date , comment , title , amount , building_id = obj
        item = {
            "id":id , 
            "date":date , 
            "comment":comment , 
            "title":title ,
            "amount":amount , 
            "building_id":building_id , 
        }
        result.append(item)
    
    return jsonify(result)

@app.route("/repair/del" , methods=["GET"])
def repair_del():
    id = int(request.args.get("id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "DELETE FROM repair WHERE id=%i"%id
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result    

#receipt----------------------------------------
@app.route("/receipt/add" , methods=["GET"])
def receipt_add():
    receipt_type = int(request.args.get("receipt_type"))
    pay_date = request.args.get("pay_date")
    issue_date = request.args.get("issue_date")
    amount = float(request.args.get("amount"))
    id_receipt = request.args.get("id_receipt")
    id_payment = request.args.get("id_payment")
    building_id = int(request.args.get("building_id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "INSERT INTO `receipt` (type , pay_date , issue_date , amount , id_receipt , id_payment , building_id) VALUES (%i , '%s' , '%s'  , %f , '%s' , '%s' , %i)"%(receipt_type , pay_date , issue_date , amount , id_receipt , id_payment , building_id)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result    

@app.route("/receipt/list" , methods=["GET"])
def receipt_list():
    buildingId = int(request.args.get("buildingId"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `receipt` where building_id=%i"%buildingId
    cursor.execute(cmd)
    itmes = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for obj in itmes:
        id , receiptType , payDate , issueDate , amount , idReceipt , idPayment , building_id = obj
        item = {
            "id":id , 
            "type":receiptType ,
            "pay_date":payDate ,
            "issue_date":issueDate , 
            "amount":amount ,
            "id_receipt":idReceipt , 
            "id_payment":idPayment , 
            "building_id":building_id
        }
        result.append(item)
    
    return jsonify(result)

@app.route("/receipt/del" , methods=["GET"])
def receipt_del():
    id = int(request.args.get("id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "DELETE FROM receipt WHERE id=%i"%id
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result 

#charge----------------------------------------
@app.route("/charge/add" , methods=["GET"])
def charge_add():
    amount = float(request.args.get("amount"))
    status = int(request.args.get("status"))
    issue_date = request.args.get("issue_date")
    pay_date = request.args.get("pay_date")
    manager_id = int(request.args.get("manager_id"))
    building_id = int(request.args.get("building_id"))
    unit_number = int(request.args.get("unit_number"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "INSERT INTO `charge` (amount , status , issue_date , pay_date , manager_id , building_id , unit_number) VALUES (%f , %i , '%s' , '%s' , %i , %i , %i)"%(amount , status , issue_date , pay_date , manager_id , building_id , unit_number)
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result  

@app.route("/charge/list" , methods=["GET"])
def charge_list():
    buildingId = int(request.args.get("buildingId"))
    unitNumber = int(request.args.get("unitNumber"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM `charge` where building_id=%i AND unit_number=%i"%(buildingId , unitNumber)
    cursor.execute(cmd)
    itmes = cursor.fetchall()
    cursor.close()
    db.close()

    result = []
    for obj in itmes:
        id , amount, status , issue_date , pay_date , manager_id , building_id , unit_number = obj

        item = {
            "id":id ,
            "amount":amount ,
            "status":status , 
            "issue_date":issue_date , 
            "pay_date":pay_date , 
            "manager_id":manager_id , 
            "building_id":building_id , 
            "unit_number":unit_number
        }
        result.append(item)
    
    return jsonify(result)

@app.route("/charge/delete" , methods=["GET"])
def charge_delete():
    id = int(request.args.get("id"))

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)
    
    cursor = db.cursor()
    cmd = "DELETE FROM charge WHERE id=%i"%id
    cursor.execute(cmd)
    db.commit()

    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result  

@app.route("/charge/update" , methods=["GET"])
def charge_update():
    id = int(request.args.get("id"))
    amount = float(request.args.get("amount"))
    status = int(request.args.get("status"))
    issue_date = request.args.get("issue_date")
    pay_date = request.args.get("pay_date")

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "UPDATE charge SET amount=%f , status=%i , issue_date='%s' , pay_date='%s' WHERE id=%i"%(amount , status , issue_date , pay_date , id)
    cursor.execute(cmd)
    db.commit()
    
    if cursor.rowcount == 0 :
        result = {"result":False}
    else:
        result = {"result":True}

    cursor.close()
    db.close()
    return result 

#user ------------------------------------------
@app.route("/user/authentication" , methods=["GET"])
def user_authentication():
    buildingId = int(request.args.get("buildingId"))
    phone = request.args.get("phone")

    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)
    if db.is_connected == False:
        abort(500)

    cursor = db.cursor()
    cmd = "SELECT * FROM unit WHERE phone='%s' AND building_id=%i"%(phone , buildingId)
    cursor.execute(cmd)

    all = cursor.fetchall()

    if len(all) == 1:
        owner_name , phone , unit_number , tag , building_id = all[0]
        result = {"result":True , "unitNumber":unit_number}
    else:
        result = {"result":False , "unitNumber":-1}

    cursor.close()
    db.close()
    
    return jsonify(result)
    
#run app----------------------------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000 , debug=True)