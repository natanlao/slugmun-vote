# -*- coding: utf-8 -*-
from flask import Flask, flash, redirect, render_template, request, session, url_for
import flask_socketio

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'lsdfkj390jf0e9sjfpj'
socketio = flask_socketio.SocketIO(app)

countries = list(enumerate(['Afghanistan', 'Albania', 'Angola', 'Argentina', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Botswana', 'Brazil', 'Cambodia', 'Cameroon', 'Canada', 'Chile', 'China', 'Congo (Democratic Republic of the)', 'Costa Rica', "Côte d’Ivoire", 'Cuba', 'Cyprus', 'Denmark', 'Djibouti', 'Dominican Republic', 'Egypt', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', "Korea (Democratic People's Republic of)", 'Korea (Republic of)', 'Libya', 'Luxembourg', 'Madagascar', 'Malawi', 'Maldives', 'Mauritania', 'Mexico', 'Mongolia', 'Morocco', 'Netherlands', 'New Zealand', 'Nicaragua', 'Norway', 'Panama', 'Peru', 'Philippines', 'Poland', 'Qatar', 'Rwanda', 'Sierra Leone', 'South Africa', 'Spain', 'Sudan', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 'Uruguay', 'Venezuela (Bolivarian Republic of)', 'Viet Nam (Socialist Republic of)']))


@app.route('/vote', methods=['POST'])
def vote():
    ballot = {
        'choice': request.form['choice'],
        'name': request.form['name']
    }
    socketio.emit('vote', ballot)
    flash('Voted ' + ballot['choice'])
    return redirect(url_for('serve_ballot'))


@app.route('/', methods=['GET', 'POST'])
def serve_index():
    if 'country' in session:
        return redirect(url_for('serve_ballot'))
    if request.method == 'GET':
        return render_template('index.html', countries=countries)
    elif request.method == 'POST':
        session['country'] = request.form['country']
        return redirect(url_for('serve_ballot'))


@app.route('/ballot', methods=['POST', 'GET'])
def serve_ballot():
    return render_template('ballot.html', country=countries[int(session['country'])][1], country_id=session['country'])


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@app.route('/tally')
def serve_tally():
    return render_template('tally.html', countries=countries, countries_split=chunks(countries, 21))


if __name__ == '__main__':
    socketio.run(app)
