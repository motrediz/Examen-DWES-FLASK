from flask import Flask, render_template, request, session, redirect, url_for
import datetime
from database import vols


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/')
def home():
    return redirect(url_for('volsAeroport', codiAeroport="PMI"))

@app.route('/vols/<codiAeroport>')
def volsAeroport(codiAeroport):
	aeroports=vols().cargaAeroports()
	
	arribades=vols().cargaArribades(codiAeroport,datetime.datetime(2025, 1, 14))
	
	sortides=vols().cargaSortides(codiAeroport,datetime.datetime(2025, 1, 14))
	
	arribadesNacionals=vols().cargaArribadesNacionals(codiAeroport,datetime.datetime(2025, 1, 14))
 
	sortidesNacionals=vols().cargaSortidesNacionals(codiAeroport,datetime.datetime(2025, 1, 14))
	
	return render_template('aeroport.html',codi=codiAeroport,
						aeroports=aeroports,arribades=arribades,sortides=sortides,
      					arribadesNacionals=arribadesNacionals,
           				sortidesNacionals=sortidesNacionals)

@app.route('/retardar_vol/<int:id_vol>/<codiAeroport>')
def retardarVol(id_vol, codiAeroport):
    v = vols()
    v.retardaVol(id_vol)
    return redirect(url_for('volsAeroport', codiAeroport=codiAeroport))


if __name__ == '__main__':
	app.run(debug=True)
