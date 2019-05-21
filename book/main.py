from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import pymongo 

app = Flask(__name__)
app.secret_key = 'key'

#connect mongoDB
mongoURL = 'mongodb+srv://easy:easy0319@mongodb-owlwh.mongodb.net/test?retryWrites=true'
client = pymongo.MongoClient(mongoURL)
db = pymongo.database.Database(client, 'mongoDB')
books = pymongo.collection.Collection(db, 'Books')
users = pymongo.collection.Collection(db, 'Users')


@app.route('/')
def root():
	if not 'user_email' in session:
		return render_template('root.html')
	else:
		return render_template('welcome.html', info = session['user_email'])

@app.route('/function')
def function():
	if 'user_email' in session:
		return render_template('welcome.html', info = session['user_email'])
	return redirect(url_for('root'))

#regist book
@app.route('/register')
def register():
	if 'user_email' in session:
		return render_template('register.html')
	return redirect(url_for('root'))

@app.route('/book', methods=['GET', 'POST'])
def book():
	if 'user_email' in session:
		if request.method == 'POST':
			data = request.form.to_dict(flat='true')
			books.insert_one(data)
			#find data from mongoDB
			results = books.find()
			#client.close()
	
			return render_template('welcome.html', results = results, info = session['user_email'])
		else:
			#find data from mongoDB
			results = books.find()
       		        #client.close()

			return render_template('book.html', results = results)
	return redirect(url_for('root'))
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		if not 'user_email' in session:
			return render_template('signup.html')
		return render_template('welcome.html', info = session['user_email'])

	elif request.method == 'POST':
		if not 'user_email' in session:
			users.insert_one(request.form.to_dict(flat='true'))
			session['user_email'] = request.form['user_email']
			return render_template('welcome.html', info=session['user_email'])
		return render_template('welcome.html', info=session['user_email'])

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'GET':
		if 'user_email' in session:
			return render_template('welcome.html', info = session['user_email'])
		return render_template('signin.html')
	
	elif request.method == 'POST':
		if 'user_email' in session:
			return render_template('welcome.html', info = session['user_email'])
		elif users.find_one(request.form.to_dict(flat='true')) is not None:
			session['user_email'] = request.form['user_email']
			return render_template('welcome.html', info=session['user_email'])
		return redirect(url_for('root'))

@app.route('/logout')
def logout():
	if 'user_email' in session:
		session.pop('user_email')
		return redirect(url_for('root'))
	return redirect(url_for('root'))

@app.before_request
def make_session_permanent():
	session.permanent = True
	app.premanent_session_lifetime = timedelta(minutes=60)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
