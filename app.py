from flask import Flask,jsonify,request,g,render_template
import sqlite3

app=Flask(__name__)

def connect_db():
	sql=sqlite3.connect('/Users/gauravjain/Documents/Flask_App/data.db')
	sql.row_factory = sqlite3.Row
	return sql
def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db=connect_db()
	return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


@app.route('/')
def index():
	return '''<h1>Hello!<h1>'''
@app.route('/json',methods=['POST','GET'])
def json():
	return jsonify({"key3": "value", "key2":[1,2,3]})
@app.route('/theform',methods=['POST','GET'])
def theform():
	return '''  <h1> Enter details to enter into database.</h1>
				<form method = "GET" action="/wel">
				<input type ="text" name="uname">
				<input type="password" name="password">
				<input type="submit" value="Submit">
				</form>
				<form method="GET" action="/viewresults">
				<input type="submit" value="See database">
				</form>'''
@app.route('/wel',methods=['GET'])
def wel():
	name =request.args.get('uname')
	#name='or 1=1;--'
	password=request.args.get('password')

	db=get_db()
	db.execute('insert into users(name,password) values(?,?)',(name,password))
	db.commit()
	return '''<h1>Hello, insert into database successfull</h1>
				<form method="GET" action="/viewresults">
				<input type="submit" value="See database">
				</form>
				<form method="GET" action="/theform">
				<input type="submit" value="Insert Another ID">
				</form>'''

@app.route('/viewresults',methods=['GET'])
def view():
			return '''<h1> Enter ID to view results.</h1>
				<form method = "GET" action="/result">
				<input type ="text" name="ids">
				<input type="submit" value="View Results">
			    </form>'''

@app.route('/result', methods=['GET'])
def result():
	id=request.args.get('ids')
	db = get_db()
	abc='select id ,name, password from users where id='+id
	cur=db.execute(abc)
	entry = cur.fetchall()
	return render_template('display.html',results=entry)

if __name__ == '__main__':
	app.run(debug=True)
