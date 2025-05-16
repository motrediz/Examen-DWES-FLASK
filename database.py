import pymysql.cursors
import datetime


class vols(object):
    def conecta(self):
        #Conexion a la BBDD del servidor mySQL
        self.db = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     db='vols',
                                     charset='utf8mb4',
                                     autocommit=True,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.cursor=self.db.cursor()

    def desconecta(self):
        self.db.close()

    def cargaAeroports(self):
        self.conecta()
        sql="SELECT * from airports"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery

    def cargaArribades(self,aeroport,fecha_hora):
        self.conecta()
        fechasql=fecha_hora.strftime("%Y-%m-%d")
        sql="SELECT * from flights where arrival_airport='"+aeroport
        sql=sql+"' AND arrival_time>='"+fechasql+"' order by arrival_time limit 10"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery             

    def cargaSortides(self,aeroport,fecha_hora):
        self.conecta()
        fechasql=fecha_hora.strftime("%Y-%m-%d")
        sql="SELECT * from flights where departure_airport='"+aeroport
        sql=sql+"' AND departure_time>='"+fechasql+"' order by departure_time limit 10"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery
    
    def cargaArribadesNacionals(self,aeroport,fecha_hora):
        self.conecta()
        fechasql=fecha_hora.strftime("%Y-%m-%d")
        self.cursor.execute("SELECT country from airports where id_airport='"+aeroport+"'")
        pais=self.cursor.fetchone()['country']
        sql="SELECT * from flights where arrival_airport='"+aeroport
        sql=sql+"' AND departure_airport IN (SELECT id_airport FROM airports WHERE country='"+pais+"') AND arrival_time>='"+fechasql+"' order by arrival_time limit 10"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery  
    
    def cargaSortidesNacionals(self,aeroport,fecha_hora):
        self.conecta()
        fechasql=fecha_hora.strftime("%Y-%m-%d")
        self.cursor.execute("SELECT country from airports where id_airport='"+aeroport+"'")
        pais=self.cursor.fetchone()['country']
        sql="SELECT * from flights where departure_airport='"+aeroport
        sql=sql+"' AND arrival_airport IN (SELECT id_airport FROM airports WHERE country='"+pais+"') AND arrival_time>='"+fechasql+"' order by arrival_time limit 10"
        self.cursor.execute(sql)
        ResQuery=self.cursor.fetchall()
        return ResQuery  
    
    def retardaVol(self, id_vol):
        self.conecta()
        sql = (
            "UPDATE flights "
            "SET departure_time = DATE_ADD(departure_time, INTERVAL 2 HOUR), "
            "arrival_time = DATE_ADD(arrival_time, INTERVAL 2 HOUR) "
            "WHERE id_flight = " + str(id_vol)
        )
        print("▶ SQL RETARD:", sql)
        self.cursor.execute(sql)

 