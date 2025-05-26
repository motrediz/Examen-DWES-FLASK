-- Consultas útiles que puedes hacer
-- 🔍 1. Consultar el contenido completo de una comanda (platos + cantidades)

SELECT c.id_comanda, p.nom, pc.quantitat
FROM comanda c
JOIN plats_comanda pc ON c.id_comanda = pc.id_comanda
JOIN plats p ON pc.id_plat = p.id_plat
WHERE c.id_comanda = 1;

-- 🧾 2. Añadir una nueva comanda

INSERT INTO comanda (taula, estat, preu)
VALUES (5, 'comanat', 0);
-- Y luego obtienes el último ID generado si estás en Python o similar con:

SELECT LAST_INSERT_ID();

-- 🍽 3. Añadir platos a una comanda

INSERT INTO plats_comanda (id_plat, id_comanda, quantitat)
VALUES (2, 3, 1), (3, 3, 2);
--(En este ejemplo, se añaden 1 ensalada y 2 sardinas a la comanda 3).

-- ➕ 4. Añadir un nuevo plato a la carta

INSERT INTO plats (tipus, nom)
VALUES ('segon', 'Entrecot amb patates');

--📋 5. Ver todas las comandas con sus estados y mesa

SELECT id_comanda, taula, estat, preu
FROM comanda
ORDER BY id_comanda DESC;

--💰 6. Calcular el precio total de una comanda (si los platos tienen precio)
--⚠️ Actualmente tu tabla plats no tiene precio, pero si se lo añades:

ALTER TABLE plats ADD COLUMN preu FLOAT DEFAULT 0;

--Entonces podrías hacer:

SELECT c.id_comanda, SUM(p.preu * pc.quantitat) AS total
FROM comanda c
JOIN plats_comanda pc ON c.id_comanda = pc.id_comanda
JOIN plats p ON pc.id_plat = p.id_plat
WHERE c.id_comanda = 1
GROUP BY c.id_comanda;


-- 7. Calcular el total de una comanda

-- SQL (cálculo):

SELECT SUM(p.preu * pc.quantitat) AS total
FROM plats_comanda pc
JOIN plats p ON pc.id_plat = p.id_plat
WHERE pc.id_comanda = 1;

-- SQL (actualización del campo en comanda):

UPDATE comanda
SET preu = (
  SELECT SUM(p.preu * pc.quantitat)
  FROM plats_comanda pc
  JOIN plats p ON pc.id_plat = p.id_plat
  WHERE pc.id_comanda = comanda.id_comanda
)
WHERE id_comanda = 1;

-- 8. Actualizar el estado de una comanda

UPDATE comanda
SET estat = 'preparat'
WHERE id_comanda = 1;

O

def actualitzaEstat(self, id_comanda, nou_estat):
    self.conecta()
    sql = (
        "UPDATE comanda "
        "SET estat = '" + nou_estat + "' "
        "WHERE id_comanda = " + str(id_comanda)
    )
    self.cursor.execute(sql)


-- 9. Mostrar los platos de una comanda específica

SELECT p.nom, pc.quantitat
FROM plats_comanda pc
JOIN plats p ON pc.id_plat = p.id_plat
WHERE pc.id_comanda = 1;
