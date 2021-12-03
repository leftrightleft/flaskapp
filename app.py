from flask import Flask,jsonify,request,g,render_template
import sqlite3

app=Flask(__name__)

def connect_db():
	sql=sqlite3.connect('./data.db')
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
	return '''	<h1> Enter your name paduwan</h1>
				<form method = "GET" action="/hel">
				<input type ="text" name="fname">
				<input type="submit" value="Submit">
				</form>'''
@app.route('/hel')
def hel():
	na=request.args.get('fname')
	db=get_db()
	db.execute('insert into profile(pname) values(?)',(na,))
	db.commit()
	return '''  <h1> Hello {}.</h1>
				<h2>Search other ID's<h2>
				<form method = "GET" action="/serc">
				<input type ="text" name="idd">
				<input type="submit" value="See database">
				</form>
				<form method = "GET" action="/">
				<input type="submit" value="Enter name again">
				</form>'''.format(na)
@app.route('/serc')
def serc():
		idd =request.args.get('idd')
		db=get_db()
 		abc='select * from profile where id='+idd
		cur=db.execute(abc)
		entr=cur.fetchone()
		return '<h1>Hello {}</h1>'.format(entr[1])
		

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
# 	abc = "SELECT * FROM books WHERE name LIKE '%" + id + "%'"
	# abc='select id ,name, password from users where id='+id
# 	print(abc)
	cur=db.execute("SELECT * FROM profile WHERE id LIKE '%" + ids + "%'")
	entry = cur.fetchall()
	return render_template('display.html',results=entry)

if __name__ == '__main__':
	app.run(debug=True)
