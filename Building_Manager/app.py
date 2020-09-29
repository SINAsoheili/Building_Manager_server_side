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
        return jsonify(response) 
    else :
        response = {"status":True}
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



#run app----------------------------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000 , debug=True)