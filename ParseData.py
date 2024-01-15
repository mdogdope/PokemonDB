from bs4 import BeautifulSoup as bs
import pickle
import os


def _pathExist(path:str) -> bool:
	if(not os.path.exists("/".join(path.split("/")[:-1]))):
		os.makedirs("/".join(path.split("/")[:-1]))
	elif(os.path.exists(path)):
		return True
	return False

def parseMaster(htmlFile:str, path:str = "data.pkl") -> None:
	if(not path.endswith(".pkl")):
		path += ".pkl"
	
	if(not htmlFile.endswith(".html")):
		htmlFile += ".html"
	
	_pathExist(path)	
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = []
	tags = html.select("tbody")[0].select("a.ent-name")
	for tag in tags:
		data.append(tag.attrs["href"])
	
	with open(path, "wb") as f:
		pickle.dump(data, f)


def parseMoveGensList(htmlFile:str, path:str = "data.pkl") -> None:
	if(not path.endswith(".pkl")):
		path += ".pkl"
	
	if(not htmlFile.endswith(".html")):
		htmlFile += ".html"
	
	_pathExist(path)
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = []
	subset = html.select("li")
	for tag in subset:
		url = tag.a["href"]
		data.append(url)
	
	with open(path, "wb") as f:
		pickle.dump(data, f)
	

def parseImgUrl(htmlFile:str) -> str:
	if(not htmlFile.endswith(".html")):
		htmlFile += ".html"
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	imgTag = html.select("p>a>picture>img")
	if(len(imgTag) == 0):
		imgTag = html.select("p>img")[0]
	else:
		imgTag = imgTag[0]
	return imgTag["src"]


def parsePokemon(htmlFile:str, path:str = "data.pkl") -> None:
	if(not path.endswith(".pkl")):
		path += ".pkl"
	
	if(not htmlFile.endswith(".html")):
		htmlFile += ".html"
	
	_pathExist(path)
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	basic = html.select("#dex-basics")[0].find_next()
	
	# Get name
	name = html.select("main")[0].select("h1")[0].text
	data["name"] = name
	
	# Get basic data table
	subset = basic.select("table")[0].select("td")
	
	# Get national number
	number = subset[0].text
	data["national-number"] = number
	
	# Get type(s)
	types = subset[1].text.strip().split(" ")
	data["types"] = types
	
	# Get species
	species = subset[2].text
	data["species"] = species
	
	# Get height
	heights = subset[3].text.replace(chr(160), "").split(" ")
	meter = heights[0][:-1]
	imp = heights[1].strip("()")[:-1].split(chr(8242))
	inch = int(imp[0]) * 12 + int(imp[1])
	data["height"] = {"meter": meter, "inch": inch}
	
	# Get weight
	weights = subset[4].text.replace(chr(160), "").split(" ")
	kg = weights[0][:-2]
	lbs = weights[1].strip("()")[:-3]
	data["weight"] = {"kilogram": kg, "pound": lbs}
	
	# Get ability
	abilities = subset[5].select("span>a")
	hidden = subset[5].select("small>a")
	temp = []
	for ability in abilities:
		ability = ability.text
		temp.append(ability)
	abilities = temp
	temp = []
	for ability in hidden:
		ability = ability.text
		temp.append(ability)
	hidden = temp
	data["abilities"] = {"seen": abilities, "hidden": hidden}
	
	# Get local numbers
	localNums = subset[6].text.replace("(", "").split(")")
	temp = {}
	for localNum in localNums:
		if(localNum == ""):
			continue
		firstSpace = localNum.find(" ")
		num = localNum[:firstSpace]
		game = localNum[firstSpace+1:]
		temp[game] = num
	data["local-number"] = temp
	
	
	# Get base stats 
	temp = {}
	for row in basic.select("#dex-stats")[0].find_next("tbody").select("tr"):
		name = row.th.text
		value = row.td.text
		temp[name] = value
	data["base-stats"] = temp
	
	
	# Get evolution tree
	evosData = []
	for tag in html.select("#dex-evolution")[0].next_siblings:
		if(tag.has_attr("class")):
			if("infocard-list-evo" in tag["class"]):
				evosData.append(tag)
	
	# Parse out all data into an easier form
	tempEvoData = []
	for evo in evosData:
		isSplit = False
		for subtag in evo.children:
			if("infocard-evo-split" in subtag["class"]):
				isSplit = True
		
		if(isSplit):
			# Code for split evos
			base = evo.select(".infocard")[0].small.text[1:]
			for subtag in evo.select(".infocard-evo-split")[0].children:
				buff = []
				buff.append(base)
				for subsubtag in subtag.children:
					if(not subsubtag.has_attr("class")):
						# print(data["name"])
						continue
					if("infocard-arrow" in subsubtag["class"]):
						buff.append(subsubtag.small.text.strip("()"))
					else:
						buff.append(subsubtag.small.text[1:])
				tempEvoData.append(buff)
		else:
			# Code for linear evos
			buff = []
			for subtag in evo.children:
				if("infocard-arrow" in subtag["class"]):
					buff.append(subtag.small.text.strip("()"))
				else:
					buff.append(subtag.small.text[1:])
			tempEvoData.append(buff)
			pass
	
	# Parse out data that only has to do with the current pokemon.
	data["evo-from"] = []
	data["evo-to"] = []
	for tree in tempEvoData:
		if(data["national-number"] in tree):
			currLoc = tree.index(data["national-number"])
			
			if(currLoc >= 2):
				data["evo-from"].append({"national-number": tree[currLoc - 2], "condition": tree[currLoc - 1]})
			
			if(currLoc + 3 < len(tree) and (len(tree)%2) == 0):
				data["evo-to"].append({"national-number": tree[currLoc + 2] + " + " + tree[currLoc + 3], "condition": tree[currLoc + 1]})
			elif(currLoc + 2 < len(tree)):
				data["evo-to"].append({"national-number": tree[currLoc + 2], "condition": tree[currLoc + 1]})
	
	
	# Get Pokedex entries
	if(html.select("#dex-flavor")[0].find_next().text != ""):
		subset = html.select("#dex-flavor")[0].find_next("tbody").select("tr")
		tempFlavor = {}
		for tag in subset:
			for subtag in tag.th:
				gameName = subtag.text
				if(gameName != ""):
					tempFlavor[gameName] = tag.td.text
		data["pokedex"] = tempFlavor
	
	
	# Get locations
	subset = html.select("#dex-locations")[0].find_next("tbody").select("tr")
	tempLocation = {}
	for tag in subset:
		for subtag in tag.th:
			gameName = subtag.text
			if(gameName != ""):
				tempLocation[gameName] = tag.td.text
	data["location"] = tempLocation
	
	
	# Get moves
	