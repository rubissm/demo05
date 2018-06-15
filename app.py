from flask import Flask, g, request, render_template, url_for, redirect, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

conexion = sqlite3.connect('info.db', check_same_thread=False)
cursor = conexion.cursor()

#cursor.execute("SELECT * FROM personas WHERE nro_tarjeta=12345678 ")
#usuario=cursor.fetchone()
#print(usuario)
#conexion.commit()
#conexion.close()

#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        session.pop('user', None)
#        if request.form['password'] == 'password':
#            session['user'] = request.form['username']
#            return redirect(url_for('consulta'))
#    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)
        username = request.form['username']
        password = request.form['password']
        print("LEE LOS VALORES")
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        validacion = cursor.fetchone() 
        conexion.commit()
        print("HACE LA VALIDACIÓN", validacion)
        if validacion != None:
            print("EXISTE EL REGISTRO",validacion)
            session['user'] = request.form['username']
            cursor.execute("SELECT password FROM personas WHERE nro_tarjeta="+username)
            passcorrect = str(cursor.fetchone()[0])
            conexion.commit()
            print(passcorrect)
            print(password)
            if password == passcorrect:
                print("VALIDA SESIÓN",passcorrect)
                return redirect(url_for('consulta'))

            else:
                print("Contraseña incorrecta")
        else:    
            print("uwu, no existe",username)
    return render_template('index.html')


@app.route('/consulta/')
def consulta():
    username = session["user"]
    print("HOLI PEXXXX",session["user"])
    if g.user:
        print("Hasta aquiiiiiiiiiiiiiiiii")
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        nombre = cursor.fetchone()[2]
        print(nombre)
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        apellido = cursor.fetchone()[3]
        print(apellido)
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        telefono = cursor.fetchone()[4]
        print(telefono)
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        correo = cursor. fetchone()[5]
        print(correo)
        cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
        banco = cursor.fetchone()[1]
        cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
        saldo = cursor.fetchone()[2]
        cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
        nrocuenta = cursor.fetchone()[3]
        cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
        nrocuentainter = cursor.fetchone()[4]
        print(nombre)
        return render_template('consulta.html', name = nombre, lastname = apellido, banco= banco, correo=correo, telef=telefono, saldo=saldo, nrocuenta=nrocuenta, nrocuentainter=nrocuentainter)
    return render_template('index.html')

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == '__main__':
    app.run(debug=True)