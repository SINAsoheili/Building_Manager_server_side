from flask import Flask , abort , jsonify , request
from db_config import HOST , USER , PASSWD , DB_NAME , AUTH_PLUGIN
from mysql import connector


app = Flask(__name__)

#building-------------------------------------
@app.route('/building/add' , methods=['POST'])
def add_building():
    name        = request.form['name'] 
    cash        = float(request.form['cash']) 
    address     = request.form['address']
    unit_count  = int(request.form['unit_count']) 
    manager_id  = int(request.form['manager_id'])

    cmd = 'INSERT INTO `building` (`name` , `cash` , `address` , `unit_count` , `manager_id`) VALUES ( \'%s\' , %i , \'%s\' , %i , %i)'%(name , cash , address , unit_count , manager_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/building/remove' , methods=['POST'])
def remove_building():
    building_id = int(request.form['building_id'])

    cmd = 'DELETE FROM `building` WHERE id=%i'%building_id
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/building/edit' , methods=['POST'])
def edit_building():
    building_name = request.form['building_name'] 
    cash        = float(request.form['cash']) 
    address     = request.form['address'] 
    unit_count  = int(request.form['unit_count']) 
    manager_id  = int(request.form['manager_id']) 
    buildign_id = int(request.form['building_id'])

    cmd = 'UPDATE `building` SET `name`=\'%s\' , `cash`=%f , `address`=\'%s\' , `unit_count`=%i WHERE  `manager_id`=%i AND `id`=%i'%(building_name  , cash , address , unit_count , manager_id , buildign_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#unit-------------------------------------
@app.route('/unit/add' , methods=['POST'])
def add_unit():
    owner_name  = request.form['owner_name'] 
    phone       = request.form['phone'] 
    unit_number = int(request.form['unit_number']) 
    tag         = int(request.form['tag']) 
    building_id = int(request.form['building_id'])

    cmd = 'INSERT INTO `unit` (`owner_name` , `phone` ,`unit_number` , `tag` , `building_id`) VALUES (\'%s\' , \'%s\' , %i , %i , %i)'%(owner_name , phone , unit_number , tag , building_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/unit/remove' , methods=['POST'])
def remove_unit():
    building_id = int(request.form['building_id'])
    unit_number = int(request.form['unit_number'])

    cmd = 'DELETE FROM `unit` WHERE `building_id`=%i AND `unit_number`=%i'%(building_id , unit_number)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/unit/edit' , methods=['POST'])
def edit_unit():
    owner_name = request.form['owner_name']
    phone = request.form['phone']
    unit_number = int(request.form['unit_number'])
    tag = int(request.form['tag'])
    building_id = int(request.form['building_id'])
    prev_unit_number = int(request.form['prev_unit_number'])

    cmd = 'UPDATE `unit` SET `owner_name`=\'%s\' , `phone`=\'%s\' ,`unit_number`=%i , `tag`=%i WHERE `building_id`=%i AND unit_number=%i'%(owner_name , phone , unit_number , tag , building_id , prev_unit_number)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#manager-------------------------------------
@app.route('/manager/add' , methods=['POST'])
def add_manager():
    passwd = request.form['passwd']
    phone = request.form['phone']

    cmd = 'INSERT INTO `manager` (`passwd` , `phone`) VALUES (\'%s\' , \'%s\')'%(passwd , phone)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/manager/remove' , methods=['POST'])
def remove_manager():
    manager_id = int(request.form['manager_id'])

    cmd = 'DELETE FROM `manager` WHERE id=%i'%manager_id
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/manager/edit' , methods=['POST'])
def edit_manager():
    passwd = request.form['passwd']
    phone = request.form['phone']
    manager_id = int(request.form['manager_id'])

    cmd = 'UPDATE `manager` SET `passwd`=\'%s\' , `phone`=\'%s\' WHERE `id`=%i'%(passwd , phone , manager_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#notification-------------------------------------
@app.route('/notification/add' , methods=['POST'])
def add_notification():
    text = request.form['text']
    title = request.form['title']
    date = request.form['date']
    building_id = int(request.form['building_id'])

    cmd = 'INSERT INTO `notification` (`text` , `title` , `date` , `building_id`) VALUES (\'%s\' , \'%s\' , \'%s\' , %i)'%(text , title , date , building_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/notification/remove' , methods=['POST'])
def remove_notification():
    notification_id = int(request.form['notification_id'])

    cmd = 'DELETE FROM `notification` WHERE `id`=%i'%notification_id
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/notification/edit' , methods=['POST'])
def edit_notification():
    text = request.form['text']
    title = request.form['title']
    date = request.form['date']
    notification_id = int(request.form['notification_id'])

    cmd = 'UPDATE `notification` SET `text`=\'%s\' , `title`=\'%s\' , `date`=\'%s\' WHERE id=%i'%(text , title , date , notification_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#charge-------------------------------------
@app.route('/charge/add' , methods=['POST'])
def add_charge():
    amount      = float(request.form['amount'])
    status      = int(request.form['status'])
    issue_date  = request.form['issue_date']
    pay_date    = request.form['pay_date']
    manager_id  = int(request.form['manager_id'])
    building_id = int(request.form['building_id'])
    unit_number = int(request.form['unit_number'])

    cmd = 'INSERT INTO `charge` (`amount` ,`status` , `issue_date` , `pay_date` , `manager_id` , `building_id` , `unit_number`) VALUES (%f , %i , \'%s\' , \'%s\' , %i ,%i , %i)'%(amount ,status , issue_date  , pay_date , manager_id , building_id , unit_number)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/charge/edit' , methods=['POST'])
def edit_charge():
    amount      = float(request.form['amount'])
    status      = int(request.form['status'])
    issue_date  = request.form['issue_date']
    pay_date    = request.form['pay_date']
    id  = int(request.form['charge_id'])

    cmd = 'UPDATE `charge` SET `amount`=%f ,`status`=%i , `issue_date`=\'%s\' , `pay_date`=\'%s\' WHERE `id`=%i'%(amount ,status , issue_date  , pay_date , id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#repair-------------------------------------
@app.route('/repair/add' , methods=['POST'])
def add_repair():
    date        = request.form['date']
    comment     = request.form['comment']
    title       = request.form['title']
    amount      = float(request.form['amount'])
    building_id = int(request.form['building_id'])

    cmd = 'INSERT INTO `repair` (`date` , `comment` , `title` , `amount` , `building_id`)VALUES (\'%s\' , \'%s\' , \'%s\' , %f , %i)'%(date , comment , title , amount , building_id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/repair/edit' , methods=['POST'])
def edit_repair():
    date        = request.form['date']
    comment     = request.form['comment']
    title       = request.form['title']
    amount      = float(request.form['amount'])
    id = int(request.form['repair_id'])

    cmd = 'UPDATE `repair` SET `date`=\'%s\' , `comment`=\'%s\' , `title`=\'%s\' , `amount`=%f WHERE `id`=%i'%(date , comment, title , amount , id)
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#receipt-------------------------------------
@app.route('/receipt/add' , methods=['POST'])
def add_receipt():
    receipt_type= int(request.form['type'])  # water=1   power=2   gas=0
    pay_date    = request.form['pay_date']
    issue_date  = request.form['issue_date']
    amount      = float(request.form['amount'])
    id_receipt  = request.form['id_receipt']
    id_payment  = request.form['id_payment']
    building_id = int(request.form['building_id'])

    cmd = 'INSERT INTO `receipt` (`type` , `pay_date` , `issue_date` , `amount` , `id_receipt` , `id_payment` , `building_id`) VALUES (%i , \'%s\' , \'%s\' , %f , \'%s\' , \'%s\' , %i)'%(receipt_type , pay_date, issue_date , amount , id_receipt , id_payment , building_id)
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