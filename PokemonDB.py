import pickle
import os
import json
import time
import datetime

import GetHTML
import ParseData
import FormatData


if(os.path.exists("errors.txt")):
	os.remove("errors.txt")


baseURL = "https://pokemondb.net"







# data = json.load(open("pokemondb.json", "r"))

# ab = data["abilities"]

# print(json.dumps(ab[0], indent=4))

# exit()







timeStart = time.time()



# ## Get urls and pages.
# categories = [("pokemon", "https://pokemondb.net/pokedex/all"),
# 		  ("moves", "https://pokemondb.net/move/all"),
# 		  ("abilities", "https://pokemondb.net/ability"),
# 		  ("items", "https://pokemondb.net/item/all"),
# 		  ("keyItems", "https://pokemondb.net/item/type/key")]

# for category, url in categories:
# 	# Get master list
# 	masterListName = f"masterList{category[0].upper() + category[1:]}"
# 	GetHTML.reqGet(url, f"html/{masterListName}")
	
# 	# Parse urls
# 	ParseData.parseMaster(f"html/{masterListName}", f"pkl/{masterListName}")
	
# 	# Get html for each url
# 	masterURLs = pickle.load(open(f"pkl/{masterListName}.pkl", "rb"))
# 	for id, url in enumerate(masterURLs):
# 		name = url.split("/")[-1]
		
# 		path = f"html/{category.lower()}/{name}"
		
# 		GetHTML.reqGet(baseURL + url, f"{path}/{name}.html")
# 		if(category == "pokemon"):
# 			url += "/moves/0"
# 			GetHTML.reqGet(baseURL+url, f"{path}/moves.html")
# 			ParseData.parseMoveGensList(f"{path}/moves.html", f"pkl/pokemon/{name}/moves.pkl")
# 			moveURLs = pickle.load(open(f"pkl/pokemon/{name}/moves.pkl", "rb"))
# 			for moveUrl in moveURLs:
# 				moveGen = moveUrl.split("/")[-1]
# 				GetHTML.reqGet(baseURL+moveUrl, f"{path}/gen{moveGen}Moves.html")
		
# 			GetHTML.reqGetImg(ParseData.parseImgUrl(f"{path}/{name}.html"), f"img/pokemon/{name}/{name}")
			
# 		print(f"{category} | ({id+1}/{len(masterURLs)}) {name}: done")






## Parse Pokemon data.
pokemonDirs = [f for f in os.listdir("html/pokemon") if os.path.isdir(f"html/pokemon/{f}")]
# pokemonDirs = ["abomasnow", "eevee", "ivysaur", "persian", "zygarde", "jolteon", "bulbasaur", "nincada"] # For testing
indexToRun = []
for id, dir in enumerate(pokemonDirs):
	if(id in indexToRun) or (len(indexToRun) == 0):
		ParseData.parsePokemon(dir, verbose=True)

## Combine Pokemon data.
if(os.path.exists("pkl/pokemon.pkl")):
	os.remove("pkl/pokemon.pkl")
FormatData.combinePokemon(pokemonDirs)






## Parse Move data.
moveDirs = [f for f in os.listdir("html/moves") if os.path.isdir(f"html/moves/{f}")]
# moveDirs = ["air-slash", "crunch", "fly", "blazing-torque", "max-airstream"] # For testing
indexToRun = []
for id, dir in enumerate(moveDirs):
	if(id in indexToRun) or (len(indexToRun) == 0):
		ParseData.parseMoves(dir, verbose=True)

## Combine Move data.
if(os.path.exists("pkl/moves.pkl")):
	os.remove("pkl/moves.pkl")
FormatData.combineMoves(moveDirs)








## Parse Ability data.
abilityDirs = [f for f in os.listdir("html/abilities") if os.path.isdir(f"html/abilities/{f}")]
# abilityDirs = ["as-one", "adaptability", "fluffy", "hustle"] # For testing
indexToRun = []
for id, dir in enumerate(abilityDirs):
	if(id in indexToRun) or (len(indexToRun) == 0):
		ParseData.parseAbilities(dir, verbose=True)

## Combine Ability data.
if(os.path.exists("pkl/abilities.pkl")):
	os.remove("pkl/abilities.pkl")
FormatData.combineAbilities(abilityDirs)


exit()





## Parse Item data.
itemDirs = [f for f in os.listdir("html/items") if os.path.isdir(f"html/items/{f}")]
# itemDirs = ["ability-capsule", "big-root", "bottle-cap"] # For testing
indexToRun = []
for id, dir in enumerate(itemDirs):
	if(id in indexToRun) or (len(indexToRun) == 0):
		ParseData.parseItems(dir, verbose=True)

## Combine Item data.
if(os.path.exists("pkl/items.pkl")):
	os.remove("pkl/items.pkl")
FormatData.combineItems(itemDirs)








## Parse Key Item data.
itemDirs = [f for f in os.listdir("html/keyitems") if os.path.isdir(f"html/keyitems/{f}")]
# itemDirs = ["acro-bike", "camping-gear", "data-card-12"] # For testing
indexToRun = []
for id, dir in enumerate(itemDirs):
	if(id in indexToRun) or (len(indexToRun) == 0):
		ParseData.parseKeyItems(dir, verbose=True)

## Combine Key Item data.
if(os.path.exists("pkl/keyitems.pkl")):
	os.remove("pkl/keyitems.pkl")
FormatData.combineKeyItems(itemDirs)






## Combine all data.
dataDirs = ["abilities", "items", "keyitems", "moves", "pokemon"]
if(os.path.exists("pkl/AllData.pkl")):
	os.remove("pkl/AllData.pkl")
FormatData.combineAllData(dataDirs)






## Write to json file
data = pickle.load(open("pkl/AllData.pkl", "rb"))
with open("pokemondb.json", "w") as f:
	json.dump(data, f, indent=4)





timeEnd = time.time()
dt = datetime.timedelta(seconds=abs(timeEnd - timeStart))
print(f"This took: {dt}")