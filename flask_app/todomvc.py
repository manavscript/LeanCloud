from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'due_date': fields.Date(required=True, description='The task due date'),
    'status': fields.String(required=True, description='Write: Finished, Not Started or In Progress')
})

nd = api.namespace("due", description='Due Date')
nf = api.namespace('finished', Description='Finished')
nod = api.namespace('overdue', Description='Overdue')

conn=sqlite3.connect('test9.db')
print ("Opened DB success")

conn.execute('''CREATE TABLE IF NOT EXISTS TODO 
         (ID     INT         PRIMARY KEY     NOT NULL,
         TASK    TEXT        NOT NULL,
         DUEDATE DATETIME    NOT NULL,
         STATUS  CHAR(65)    NOT NULL);''')
conn.commit()
conn.close()

class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []
        self.otodos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def getF(self):
        self.delo()
        for todo in self.todos:
            if todo['status']=="Finished":
                self.otodos.append(todo)
        return self.otodos

    def delo(self):
        try:
            for todo in self.otodos[:]:
                self.otodos.remove(todo)
        except:
            return

    def getO(self):
        self.delo()
        n = datetime.now()
        for todo in self.todos:
                if datetime.strptime(todo['due_date'], "%Y-%m-%d") < n: 
                    self.otodos.append(todo)
        return self.otodos

    def getD(self, due_date):
        self.delo()
        for todo in self.todos: 
               if todo['status']!="Finished" and datetime.strptime(todo['due_date'], "%Y-%m-%d") == datetime.strptime(due_date, "%Y-%m-%d"):
                    self.otodos.append(todo)
        return self.otodos

    def create(self, data):
        if data['status'] != 'Finished' and data['status'] != 'Not Started' and data['status'] != 'In Progress':
            api.abort(405, "Check your spelling or fill whether task finished or not properly".format(id))
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        try:
            conn=sqlite3.connect('test9.db')
            cursor = conn.cursor()
            sqlite_insert = """INSERT INTO TODO 
            (ID,TASK,DUEDATE,STATUS) 
            VALUES (?, ?, ?, ?);""";
            data_tuple = (todo['id'], todo['task'], todo['due_date'], todo['status'])
            cursor.execute(sqlite_insert, data_tuple)
            conn.commit()
            cursor.close()
            conn.close()
        except:
            print("Already exists")
        return todo

    def update(self, id, data):
        todo = self.get(id)
        if data['status'] != 'Finished' and data['status'] != 'Not Started' and data['status'] != 'In Progress':
            api.abort(405, "Check your spelling or fill whether task finished or not properly".format(id))
        todo.update(data)
        try:
            conn=sqlite3.connect('test9.db')
            cursor = conn.cursor()
            sqlite_insert = """UPDATE TODO SET TASK = ?, DUEDATE = ?, WHERE ID = ?) 
            VALUES (?, ?, ?, ?);""";
            data_tuple = (todo['task'], todo['due_date'], todo['status'], todo['id'])
            cursor.execute(sqlite_insert, data_tuple)
            conn.commit()
            cursor.close()
            conn.close()
        except:
            print("Already exists")
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)
        conn=sqlite3.connect('test9.db')
        cursor = conn.cursor()
        sql = """DELETE FROM TODO where ID=? """
        cursor.execute(sql, (todo['id'], ))
        conn.commit()
        cursor.close()
        conn.close()


    def deleteAllTasks(self):
        try:
            for todo in self.todos[:]:
                self.todos.remove(todo)
        except:
            return

    def deleteHistory(self):
        try:
            for todo in self.todos:
                conn=sqlite3.connect('test9.db')
                cursor = conn.cursor()
                sql = """DELETE FROM TODO where ID=? """
                cursor.execute(sql, (todo['id'], ))
                cursor.execute('DELETE FROM TODO;',);
                conn.commit()
                cursor.close()
                conn.close()
        finally:
            self.deleteAllTasks()
            return


DAO = TodoDAO()
DAO.create({'task': 'Build an API', 'due_date':'2020-01-09', 'status':'Finished'})
DAO.create({'task': '?????', 'due_date': '2020-01-09', 'status': 'In Progress'})
DAO.create({'task': 'profit!', 'due_date': '2020-01-09', 'status': 'Not Started'})

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201

    @ns.doc('deleteAllHistory')
    @ns.marshal_list_with(todo)
    def delete(self):
        '''Deletes Database history and list history'''
        return DAO.deleteHistory()

@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)

@nf.route('/')
class TodoL(Resource):
    @nf.doc('get_finished')
    @nf.marshal_with(todo)
    def get(self):
        return DAO.getF()

@nod.route('/')
class Tdl(Resource):
    @nod.doc('overdue')
    @nod.marshal_with(todo)

    def get(self):
        return DAO.getO()

@nd.route("due_date=<string:due_date>")
@nd.param('due_date', 'due_date')
class Tdlo(Resource):
    @nd.doc('due_date')
    @nd.marshal_with(todo)

    def get(self, due_date):
        return DAO.getD(due_date)

if __name__ == '__main__':
    app.run(debug=True)