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
        if len(result) == 0 :
            result = {"status":True , "manager_id":-1} 
            return result   
        else:
            row = result[0]
            id = row[0]
            result = {"status":True , "manager_id":id} 
            return result
    else :
        result = {"status":False , "manager_id":-1}
        return result


#run app----------------------------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000 , debug=True)