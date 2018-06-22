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
                print("CONTRASEÑA INCORRECTA")
        else:    
            print("NO EXISTE EL USUARIO",username)
    return render_template('index.html')

@app.route('/consulta')
def consulta():
    username = session["user"]
    if g.user:
        cursor.execute("SELECT * FROM personas WHERE nro_tarjeta="+username)
        usuario = cursor.fetchone()
        cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
        infobanco = cursor.fetchone()
        cursor.execute("SELECT * FROM old_transaccion WHERE nro_tar_desde="+username)
        transacciones = cursor.fetchall()
        print(transacciones)
        #print(transaccion)
        return render_template('consulta.html', name = usuario[2], lastname = usuario[3], banco= infobanco[1],
        correo=usuario[5], telef=usuario[4], saldo=infobanco[2], nrocuenta=infobanco[3], nrocuentainter=infobanco[4],
        transacciones=transacciones)
    return render_template('index.html')

 # Agregar función "transacción"
@app.route('/transaccion', methods=['GET','POST'])
def transaccion():
    username = session["user"]
    print("SIGUE EN SESION EL USUARIO", username)
    if request.method == 'POST':
        monto = int(request.form['monto'])
        nrocuentadestino = request.form['nrocuentadestino']
        fecha_ven = request.form['fechaven']
        cod_seg = int(request.form['codseg'])
        cursor.execute("SELECT * FROM infobancaria WHERE nrocuenta="+nrocuentadestino)
        info_destino = cursor.fetchone() 
        conexion.commit()
        print("HACE LA VALIDACIÓN", info_destino)
        if info_destino != None:
            print("EXISTE EL REGISTRO",info_destino)
            cursor.execute("SELECT * FROM infobancaria WHERE nro_tar="+username)
            info_origen = cursor.fetchone()
            conexion.commit()
            if monto <= info_origen[2]:
                print("TIENE SUFICIENTE SALDO")
                if cod_seg == info_origen[6]:
                    print("CODIGO DE SEGURIDAD CORRECTO")
                    nsaldo_destino = info_destino[2]+monto
                    nsaldo_origen = info_origen[2]-monto
                    cursor.execute("UPDATE infobancaria SET saldo="+str(nsaldo_destino)+" WHERE nro_tar="+str(nrocuentadestino))
                    conexion.commit()
                    cursor.execute("UPDATE infobancaria SET saldo="+str(nsaldo_origen)+" WHERE nro_tar="+username)
                    conexion.commit()
                    cursor.execute("INSERT INTO old_transaccion VALUES("+username+","+str(nrocuentadestino)+", "+str(monto)+");")
                    conexion.commit()
                    return render_template('exito_consulta.html')
                else:
                    print("CODIGO DE SEGURIDAD INCORRECTO")    
            else:
                print ("NO TIENE SALDO SUFICIENTE")
    #            print("VALIDA SESIÓN",passcorrect)
    #            return redirect(url_for('consulta'))
        else:    
            print("NO EXISTE EL USUARIO ")

    return render_template('transaccion.html')

@app.route('/exito_transaccion', methods=['GET', 'POST'])
def exito_transaccion():
    username = session["user"]
    print("SIGUE EN SESION EL USUARIO", username)
    if request.method == 'POST':
        return render_template('consulta.html')



@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

if __name__ == '__main__':
    app.run(debug=True)
    