import shapefile
import csv
import os

if __name__ == "__main__":
	donnees = {}
	with open("population-departements.csv") as file:
		csv = csv.DictReader(file)
		for ligne in csv:
			departement = ligne["Département"]
			population = int(ligne["Population"])
			donnees[departement] = population

	shapeR = shapefile.Reader("departements-20180101.shp")
	shapeW = shapefile.Writer("departements-20180101-edited.shp")

	shapeW.fields = list(shapeR.fields)

	if "population" not in shapeW.fields:
		shapeW.field("population", "N", 10,0)
	if "densite" not in shapeW.fields:
		shapeW.field("densite", "N", 10, 0)

	champs = [champ[0] for champ in shapeW.fields]
	index_champ_departement = champs.index("code_insee") - 1
	index_champ_km2 = champs.index("surf_km2") - 1

	for shapeatt in shapeR.shapeRecords():
		att = shapeatt.record
		departement = str(att[index_champ_departement])
		surface = att[index_champ_km2]

		if departement.startswith("0"):
			departement = departement.lstrip("0")

		population = donnees[departement]
		att.append(population)

		densite = population/surface
		att.append(densite)

		shapeW.record(*att)
		shapeW.shape(shapeatt.shape)

	print("Import réalisé avec succès sur le nouveau fichier")

	fichiers_a_remplacer = ['.shp', '.shx', '.dbf']
	nom_original = "departements-20180101"
	nom_edite = "departements-20180101-edited"

	for extension in fichiers_a_remplacer:
		fichier_source = nom_edite + extension
		fichier_destination = nom_original + extension

		if os.path.exists(fichier_source):
			os.replace(fichier_source, fichier_destination)

	print("Le fichier original a été écrasé avec succès")

	shapeR.close()
	shapeW.close()

