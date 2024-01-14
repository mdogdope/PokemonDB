import pickle
import os

import GetHTML
import ParseData

baseURL = "https://pokemondb.net"



# import requests
# img = requests.get("https://img.pokemondb.net/artwork/bulbasaur.jpg")

# with open("test.jpg", "wb") as f:
# 	f.write(img.content)


# test = [f for f in os.listdir("html") if os.path.isdir(f"html/{f}")]
# print(test)

# print(chr(8242), chr(0x2032))

# exit()








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




pokemonDirs = [f for f in os.listdir("html/pokemon") if os.path.isdir(f"html/pokemon/{f}")]
pokemonDirs = ["abomasnow", "eevee", "ivysaur", "persian", "zygarde"] # For testing
indexToRun = 0 # For testing
for id, dir in enumerate(pokemonDirs):
	if(indexToRun == id) or (indexToRun == -1):
		ParseData.parsePokemon(f"html/pokemon/{dir}/{dir}.html", f"pkl/pokemon/{dir}.pkl")
