#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

from app import app
from flask import render_template, request, url_for, redirect, session, make_response
import json
import os
import sys
import random
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    #print (url_for('static', filename=os.path.abspath('static')+'/''estilo.css'), file=sys.stderr)
    #print(os.path.abspath('users/julian'))
    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title="Home", movies=catalogue['peliculas'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if 'existuser' in session:
        session.pop('existuser', None)
        return render_template("login.html", title="Acceder", existUser=True)
    if 'username' in request.form:
        if 'usuario' in session:
            return redirect(url_for('index'))
        username = request.form["username"]
        encpaswrd = hashlib.md5(request.form["pass"].encode()).hexdigest()
        # aqui se deberia validar con fichero .dat del usuario
        if os.path.isdir(dir_path+"/users/"+username):
            f = open(dir_path+"/users/"+username+'/data.dat', 'r')
            datos = f.readlines()
            #(datos)
            if datos[1].split('\n')[0] == encpaswrd:
                session['usuario'] = username
                session.modified = True
                return redirect(url_for('index'))
            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            else:
                return render_template('login.html', title="Sign In", invalidlogin=True)
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido
            return render_template('login.html', title="Sign In", invalidlogin=True)
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen'] = request.referrer
        session.modified=True
        lastuser = request.cookies.get('lastuser')        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        if lastuser == None:
            return render_template("login.html", title = "Sign In")
        #print(lastuser)
        return render_template("login.html", title = "Sign In", lastuser = lastuser)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in request.form:
        dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        username = request.form['username']
        email = request.form['email']
        tarjeta = request.form['tarjeta']
        if os.path.isdir(dir_path+"/users/"+username):
            session['existuser'] = True
            session.modified = True
            return redirect(url_for('login'))
        else:
            os.mkdir(dir_path+"/users/"+username)
            os.chmod(dir_path+"/users/"+username, 0o777)
            paswrd = request.form['passr']
            encpass = hashlib.md5(paswrd.encode()).hexdigest()
            f = open(dir_path+"/users/"+username+'/data.dat', 'w')
            os.chmod(dir_path+"/users/"+username+'/data.dat', 0o777)
            f.write(username+'\n')
            f.write(encpass+'\n')
            f.write(email+'\n')
            f.write(tarjeta+'\n')
            f.write(str(random.randrange(100)))
            f.close()
            f = open(dir_path+"/users/"+username+'/historial.json', 'w')
            os.chmod(dir_path+"/users/"+username+'/historial.json', 0o777)
            init = {}
            init['peliculas'] = []
            json.dump(init, f, indent=4)
            f.close()
            session['usuario'] = username
            session.modified = True
            return redirect(url_for('index'))
    else:
        return render_template(url_for('login'), title="Acceder")


@app.route('/detalle', methods=['GET', 'POST']) 
def detalle():
    if 'detalle' in session:
        movie = session['detalle']
        session.pop('detalle',None)
        return render_template('detalle.html', movie=movie)

    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']
    if 'id' in request.form:
        #print(request.form['id'])
        for movie in movies :
            if movie['id'] == int(request.form['id']) :
                return render_template('detalle.html', movie=movie)
    else:
        return render_template('detalle.html')


@app.route('/busqueda', methods=['GET', 'POST'])   
def busqueda():
    catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas'] 
    error = 'No se han encontrado resultados para tu búsqueda.'
    listap = []

    if 'buscar' in request.form and request.form.get('filtro') == '0' and len(request.form['buscar']) != 0:
        for movie in movies:
            if movie['titulo'].lower().startswith(request.form['buscar'].lower()):
                listap.append(movie)
        return render_template('busqueda.html', title='Búsqueda de ' + '"' + request.form['buscar'] + '"', listap=listap)

    if 'buscar' in request.form and request.form.get('filtro') != '0' and len(request.form['buscar']) != 0:
        for movie in movies:
            if movie['titulo'].lower().startswith(request.form['buscar'].lower() and movie['categoria'].find(request.form.get('filtro')) != -1:
                return render_template('busqueda.html', title = "busqueda", movie = movie)
        return render_template('busqueda.html', title = "busqueda", error = error)
    elif 'buscar' in request.form and request.form.get('filtro') != '0':
        for movie in movies :
            if movie['categoria'].find(request.form.get('filtro')) != -1:
                listap.append(movie)
        return render_template('busqueda.html', title = "busqueda", listap=listap)
    else:
        return redirect(url_for('index'))



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = session['usuario']
    session.pop('usuario', None)
    resp = make_response(redirect('index'))
    resp.set_cookie('lastuser', user)
    return resp

@app.route('/add2cart', methods=['GET' , 'POST'])
def add2cart():
    if 'id' in request.form:
        id = request.form['id']
        catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
        catalogue = json.loads(catalogue_data)
        movies = catalogue['peliculas']
        if  'carrito' not in session:
            session['carrito']=[]
        session['carrito'].append(id)
        session.modified = True
        for movie in movies :
            if movie['id'] == int(request.form['id']) :
                session['detalle']=movie
                return redirect('detalle')
        

@app.route('/carrito', methods=['GET' , 'POST'])
def carrito():
    if 'carrito' in session:
        total = 0
        listap = []
        catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
        catalogue = json.loads(catalogue_data)
        movies = catalogue['peliculas']
        for id in session['carrito']:
            for movie in movies :
                if movie['id'] == int(id):
                    listap.append(movie)
                    total += movie['precio']

        return render_template('carrito.html', items=listap, title="Carrito", total = total)
    else:
        return   render_template('carrito.html',title="Carrito")


@app.route('/delitem', methods=['GET' , 'POST'])
def delitem():
    if 'index' in request.form:
        session['carrito'].pop(int(request.form['index'])-1)
        if len(session['carrito']) <= 0:
            session.pop('carrito', None)
        session.modified = True  
    return redirect(url_for('carrito'))


@app.route('/fincompra', methods=['GET' , 'POST'])
def fincompra():
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if 'total' not in request.form:
        return render_template('carrito.html',title="Carrito")

    if 'usuario' in session :
        username = session['usuario']
        f = open(dir_path+"/users/"+username+'/data.dat', 'r')
        datos = f.readlines()
        f.close()
        dinerocuenta = float(datos[4].split('\n')[0])
        totalcarrito = float(request.form['total'])

        if dinerocuenta >= totalcarrito:
            catalogue_data = open(os.path.join(app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
            catalogue = json.loads(catalogue_data)
            movies = catalogue['peliculas']
            f = open( dir_path+"/users/"+session['usuario'] + '/data.dat', 'w')
            f.write(datos[0])
            f.write(datos[1])
            f.write(datos[2])
            f.write(datos[3])
            f.write("{0:.2f}".format(dinerocuenta - totalcarrito))
            f.close()
            #LO AÑADIMOS AL HISTORIAL
            historial_data = open(dir_path+"/users/"+session['usuario'] +'/historial.json', encoding="utf-8").read()
            comprados = json.loads(historial_data)
            for id in session['carrito']:
                for movie in movies :
                    if movie['id'] == int(id):
                        comprados['peliculas'].append({
                            'id': movie['id'],
                            'precio' : movie['precio'],
                            'fecha' : datetime.now().strftime("%d/%m/%Y"),
                            'hora'  : datetime.now().strftime("%H:%M:%S"),
                            'titulo': movie['titulo'],
                            'poster' : movie['poster']
                        })
            session.pop('carrito', None)
            session.modified = True
            f = open(dir_path+"/users/"+session['usuario'] +'/historial.json', 'w')
            json.dump(comprados,f,indent=4)
            f.close()
            return render_template('carrito.html',title="Carrito", succeed = True)
        else:
            return render_template('carrito.html',title="Carrito", failed = True)
    else:
        return redirect(url_for('login'))


@app.route('/historial', methods=['GET' , 'POST'])
def historial():
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if 'usuario' in session:
        dir_path+"/users/"+session['usuario']
        historial_data = open(dir_path+"/users/"+session['usuario'] +'/historial.json', encoding="utf-8").read()
        historial = json.loads(historial_data)
        balance = open(dir_path+"/users/"+session['usuario'] +'/data.dat','r').readlines()[4]
        if len(historial['peliculas']) < 1:
            return render_template('historial.html',title = "Historial",balance = balance)
        return render_template('historial.html',title = "Historial", items = historial['peliculas'], balance = balance)
    return redirect(url_for('login'))


@app.route('/addmoney', methods=['GET' , 'POST'])
def addmoney():
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lineas = open(dir_path+"/users/"+session['usuario'] +'/data.dat','r').readlines()
    f = open(dir_path+"/users/"+session['usuario'] +'/data.dat','w')
    f.write(lineas[0])
    f.write(lineas[1])
    f.write(lineas[2])
    f.write(lineas[3])
    f.write(str(float(lineas[4])+float(request.form["cantidad"])))
    f.close()
    return redirect(url_for('historial'))


@app.route('/rand', methods=['GET'])
def rand():
    num = str(random.randrange(100))
    return str(num)
