from flask import Flask , abort , jsonify , request
from db_config import HOST , USER , PASSWD , DB_NAME , AUTH_PLUGIN
from mysql import connector


app = Flask(__name__)

#building-------------------------------------
@app.route('/building/add' , methods=['POST'])
def add_building():
    cmd = 'INSERT INTO `building` (`name` , `cash` , `address` , `unit_count` , `manager_id`) VALUES ( \'%s\' , %i , \'%s\' , %i , %i)'%(request.form['name'] , float(request.form['cash']) , request.form['address'], int(request.form['unit_count']) , int(request.form['manager_id']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/building/remove' , methods=['POST'])
def remove_building():
    cmd = 'DELETE FROM `building` WHERE id=%i'%int(request.form['building_id'])
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/building/edit' , methods=['POST'])
def edit_building():
    cmd = 'UPDATE `building` SET `name`=\'%s\' , `cash`=%f , `address`=\'%s\' , `unit_count`=%i WHERE  `manager_id`=%i AND `id`=%i'%(request.form['building_name'] , float(request.form['cash']) , request.form['address'] , int(request.form['unit_count']) , int(request.form['manager_id']) , int(request.form['building_id']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})

#insert|delete|edit|db---------------------------
def manipulate_database(query):
    db = connector.connect(host=HOST , user=USER , passwd=PASSWD , database=DB_NAME , auth_plugin=AUTH_PLUGIN)

    if not db.is_connected():
        abort(500)

    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

    response = None
    if cursor.rowcount > 0:
        response = True
    else:
        response = False

    cursor.close()    
    return response

#run app----------------------------------------
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000 , debug=True)