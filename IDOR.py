from flask import Flask,jsonify,request,g
import sqlite3

def connect_db():
	sql=sqlite3.connect('/Users/gauravjain/Documents/Flask_App/data.db')
	sql.row_factory = sqlite3.Row
	return sql
def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db=connect_db()
	return g.sqlite_db

app=Flask(__name__)

@app.route('/',methods=['GET'])
def hg():
	return '<h1>Hello</h1>'

@app.route('/view/<id>', methods=['GET'])
def index(id):
	db = get_db()
	abc='select id ,name, password from users where id='+id
	cur=db.execute(abc)
	entry = cur.fetchall()
	#return jsonify(entry)
	return '''  <h1> ID|Name|Passowrd </h1>  
				<h1>{} | {} | {}</h1>'''.format(entry[0],entry[1],entry[2])



if __name__ == '__main__':
	app.run(debug=True)