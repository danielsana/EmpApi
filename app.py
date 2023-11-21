# using flask_restful
from flask import Flask,jsonify,request
from flask_restful import Resource, Api

import pymysql

# create the flask app
app = Flask(__name__)

# create an Api object
api =Api(app)

#make a class for a particular resource
#the get, post,put and delete methods correspond to get,post,put and delete requests
#they are automatically mapped by flask_restful,

class Employee(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='myemployees')

        cursor = connection.cursor()
        sql = "select*from employees"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({'message':'No Records'})
        else:
            employees = cursor.fetchall()
            return jsonify(employees)
    
    def post(self):
        data = request.json
        id_number = data['id_number']
        username = data['username']
        others = data['others']
        salary = data['salary']
        department = data['department']

        connection = pymysql.connect(host='localhost', user='root', password='', database='myemployees')

        cursor = connection.cursor()
        sql = "insert into employees (id_number, username,others, salary, department)values(%s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (id_number, username, others, salary, department))
            connection.commit()
            return jsonify({'message': 'POST SUCCESS. RECORD SAVED'})
        except:
            connection.rollback()
            return jsonify({'message': 'POST FAILED. RECORD NOT SAVED'})
        
    def put(self):
        data =request.json
        id_number = data['id_number']
        salary = data['salary']

        connection = pymysql.connect(host='localhost', user='root', password='', database='myemployees')

        cursor = connection.cursor()

        sql = "update employees SET salary = %s where id_number = %s"
        try:
            cursor.execute(sql,(salary,id_number))
            connection.commit()

            return jsonify({'message' : 'UPDATE SUCCESS'})
        except:
            connection.rollback()
            return jsonify({'message':'update failed'})
    
    def delete(self):
        data =request.json
        id_number= data['id_number']

        connection = pymysql.connect(host='localhost', user='root', password='', database='myemployees')

        cursor = connection.cursor()

        sql ="delete from employees where id_number = %s"
        try:
            cursor.execute(sql,(id_number))
            connection.commit()
            return jsonify({'message':'DELETE SUCCESS'})
        except:
            connection.rollback()
            return jsonify({'message':'DELETE FAILED'})

api.add_resource(Employee,'/employees')

if __name__=='__main__':
    app.run(debug=True)

