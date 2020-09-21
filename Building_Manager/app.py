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



#unit-------------------------------------
@app.route('/unit/add' , methods=['POST'])
def add_unit():
    cmd = 'INSERT INTO `unit` (`owner_name` , `phone` ,`unit_number` , `tag` , `building_id`) VALUES (\'%s\' , \'%s\' , %i , %i , %i)'%(request.form['owner_name']  , request.form['phone'] , int(request.form['unit_number']) , int(request.form['tag']) , int(request.form['building_id']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/unit/remove' , methods=['POST'])
def remove_unit():
    cmd = 'DELETE FROM `unit` WHERE `building_id`=%i AND `unit_number`=%i'%(int(request.form['building_id']) , int(request.form['unit_number']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/unit/edit' , methods=['POST'])
def edit_unit():
    cmd = 'UPDATE `unit` SET `owner_name`=\'%s\' , `phone`=\'%s\' ,`unit_number`=%i , `tag`=%i WHERE `building_id`=%i AND unit_number=%i'%(request.form['owner_name'] , request.form['phone'] , int(request.form['unit_number']) ,  int(request.form['tag']) , int(request.form['building_id']) , int(request.form['prev_unit_number']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#manager-------------------------------------
@app.route('/manager/add' , methods=['POST'])
def add_manager():
    cmd = 'INSERT INTO `manager` (`passwd` , `phone`) VALUES (\'%s\' , \'%s\')'%(request.form['passwd'] , request.form['phone'])
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/manager/remove' , methods=['POST'])
def remove_manager():
    cmd = 'DELETE FROM `manager` WHERE id=%i'%int(request.form['manager_id'])
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/manager/edit' , methods=['POST'])
def edit_manager():
    cmd = 'UPDATE `manager` SET `passwd`=\'%s\' , `phone`=\'%s\' WHERE `id`=%i'%(request.form['passwd'] , request.form['phone'] , int(request.form['manager_id']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})



#notification-------------------------------------
@app.route('/notification/add' , methods=['POST'])
def add_notification():
    cmd = 'INSERT INTO `notification` (`text` , `title` , `date` , `building_id`) VALUES (\'%s\' , \'%s\' , \'%s\' , %i)'%(request.form['text'] , request.form['title'] , request.form['date'] , int(request.form['building_id']))
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/notification/remove' , methods=['POST'])
def remove_notification():
    cmd = 'DELETE FROM `notification` WHERE `id`=%i'%int(request.form['notification_id'])
    result = manipulate_database(cmd)
    return jsonify({'response':result})


@app.route('/notification/edit' , methods=['POST'])
def edit_notification():
    cmd = 'UPDATE `notification` SET `text`=\'%s\' , `title`=\'%s\' , `date`=\'%s\' WHERE id=%i'%(request.form['text'] , request.form['title'] , request.form['date'] , int(request.form['notification_id']))
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
    manager_id  = int(request.form['manager_id'])
    building_id = int(request.form['building_id'])
    unit_number = int(request.form['unit_number'])

    cmd = 'UPDATE `charge` SET `amount`=%f ,`status`=%i , `issue_date`=\'%s\' , `pay_date`=\'%s\' WHERE `manager_id`=%i AND `building_id`=%i AND `unit_number`=%i'%(amount ,status , issue_date  , pay_date , manager_id , building_id , unit_number)
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