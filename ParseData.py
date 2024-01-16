from bs4 import BeautifulSoup as bs
import pickle
import os
import re
import sys

# sys.setrecursionlimit(100000)

def _pathExist(path:str) -> bool:
	if(not os.path.exists("/".join(path.split("/")[:-1]))):
		os.makedirs("/".join(path.split("/")[:-1]))
	elif(os.path.exists(path)):
		return True
	return False


def _formatText(str:str) -> str:
	return str.replace("\u00e9", "e").replace("\u2014", "-").replace("\u2019", "'").replace("\u00a3", "$").replace("\u200b", "").replace("\u00d7", "x")


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


def parsePokemon(pokemon:str, verbose:bool = False, force:bool = False) -> None:
	htmlFile = f"html/pokemon/{pokemon}/{pokemon}.html"
	path =  f"pkl/pokemon/{pokemon}/{pokemon}.pkl"
	
	if(_pathExist(path) and not force):
		return
	
	if(verbose):
		print(f"Pokemon: {pokemon}")
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	basic = html.select("#dex-basics")[0].find_next()
	
	# Get name
	name = html.select("main")[0].select("h1")[0].text
	data["name"] = _formatText(name)
	
	# Get basic data table
	subset = basic.select("table")[0].select("td")
	
	# Get national number
	number = subset[0].text
	data["national-number"] = _formatText(number)
	
	# Get type(s)
	types = subset[1].text.strip()
	data["types"] = _formatText(types).split(" ")
	
	# Get species
	species = subset[2].text
	data["species"] = _formatText(species)
	
	# Get height
	heights = subset[3].text
	heights = _formatText(heights).split(" ")
	meter = heights[0][:-1]
	imp = heights[1].strip("()")[:-1].split(chr(8242))
	inch = int(imp[0]) * 12 + int(imp[1])
	data["height"] = {"meter": meter, "inch": inch}
	
	# Get weight
	weights = subset[4].text
	weights = _formatText(weights).split(" ")
	kg = weights[0][:-2]
	lbs = weights[1].strip("()")[:-3]
	data["weight"] = {"kilogram": kg, "pound": lbs}
	
	# Get ability
	abilities = subset[5].select("span>a")
	hidden = subset[5].select("small>a")
	temp = []
	for ability in abilities:
		ability = ability.text
		temp.append(_formatText(ability))
	abilities = temp
	temp = []
	for ability in hidden:
		ability = ability.text
		temp.append(_formatText(ability))
	hidden = temp
	data["abilities"] = {"seen": abilities, "hidden": hidden}
	
	# Get local numbers
	localNums = subset[6].text
	localNums = _formatText(localNums).replace("(", "").split(")")
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
		name = _formatText(row.th.text)
		value = _formatText(row.td.text)
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
			base = _formatText(evo.select(".infocard")[0].small.text)[1:]
			for subtag in evo.select(".infocard-evo-split")[0].children:
				buff = []
				buff.append(base)
				for subsubtag in subtag.children:
					if(not subsubtag.has_attr("class")):
						continue
					if("infocard-arrow" in subsubtag["class"]):
						buff.append(_formatText(subsubtag.small.text).strip("()"))
					else:
						buff.append(_formatText(subsubtag.small.text)[1:])
				tempEvoData.append(buff)
		else:
			# Code for linear evos
			buff = []
			for subtag in evo.children:
				if("infocard-arrow" in subtag["class"]):
					buff.append(_formatText(subtag.small.text).strip("()"))
				else:
					buff.append(_formatText(subtag.small.text)[1:])
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
	try:
		subset = html.select("#dex-flavor")[0].find_next("div").select("tr")
		tempFlavor = []
		for tag in subset:
			games = []
			for subtag in tag.th.select("span"):
				games.append(_formatText(subtag.text))
			desc = _formatText(tag.td.text)
			tempFlavor.append({"game": games, "description": desc})
		data["description"] = tempFlavor
	except:
		with open("errors.txt", "a") as f:
			f.write(f"Pokemon.Pokedex: {pokemon}\n")
	
	
	# Get locations
	try:
		subset = html.select("#dex-locations")[0].find_next("div").select("tr")
		tempFlavor = []
		for tag in subset:
			games = []
			for subtag in tag.th.select("span"):
				games.append(_formatText(subtag.text))
			desc = _formatText(tag.td.text)
			tempFlavor.append({"game": games, "description": desc})
		data["location"] = tempFlavor
	except:
		with open("errors.txt", "a") as f:
			f.write(f"Pokemon.Locations: {pokemon}\n")
	
	
	# Get moves
	data["moves"] = {}
	for gen in [f for f in os.listdir(f"html/pokemon/{pokemon}") if re.match("gen\dMoves.html", f) != None]:
		htmlFile = f"html/pokemon/{pokemon}/{gen}"
		with open(htmlFile, "r", encoding="utf-8") as f:
			html = bs(f, "html.parser")
			f.close()
		
		tempMoves = {}
		
		try:
			if html.findAll(text="Moves learnt by level up") != []:
				tempMoves["level-up-moves"] = []
				for subtag in html.findAll(text="Moves learnt by level up")[0].find_next("tbody").children:
					lvl = _formatText(subtag.select(".cell-num")[0].text)
					name = _formatText(subtag.select(".cell-name")[0].text)
					tempMoves["level-up-moves"].append({"move-name": name, "level": lvl})
		except:
			with open("errors.txt", "a") as f:
				f.write(f"Pokemon.LVL-Moves: {pokemon} | {gen[:-10]}\n")
		
		try:
			if html.findAll(text="Egg moves") != []:
				tempMoves["egg-moves"] = []
				for subtag in html.findAll(text="Egg moves")[0].find_next("tbody").children:
					name = _formatText(subtag.select(".cell-name")[0].text)
					tempMoves["egg-moves"].append(name)
		except:
			with open("errors.txt", "a") as f:
				f.write(f"Pokemon.Egg-Moves: {pokemon} | {gen[:-10]}\n")
		
		try:
			if html.findAll(text="Moves learnt by HM") != []:
				tempMoves["HM-moves"] = []
				for subtag in html.findAll(text="Moves learnt by HM")[0].find_next("tbody").children:
					name = _formatText(subtag.select(".cell-name")[0].text)
					tempMoves["HM-moves"].append(name)
		except:
			with open("errors.txt", "a") as f:
				f.write(f"Pokemon.HM-Moves: {pokemon} | {gen[:-10]}\n")
		
		try:
			if html.findAll(text="Moves learnt by TM") != []:
				tempMoves["TM-moves"] = []
				for subtag in html.findAll(text="Moves learnt by TM")[0].find_next("tbody").children:
					name = _formatText(subtag.select(".cell-name")[0].text)
					tempMoves["TM-moves"].append(name)
		except:
			with open("errors.txt", "a") as f:
				f.write(f"Pokemon.TM-Moves: {pokemon} | {gen[:-10]}\n")
		
		try:
			if html.findAll(text="Moves learnt by TR") != []:
				tempMoves["TR-moves"] = []
				for subtag in html.findAll(text="Moves learnt by TR")[0].find_next("tbody").children:
					name = _formatText(subtag.select(".cell-name")[0].text)
					tempMoves["TR-moves"].append(name)
		except:
			with open("errors.txt", "a") as f:
				f.write(f"Pokemon.TR-Moves: {pokemon} | {gen[:-10]}\n")
		
		data["moves"][gen[:-10]] = tempMoves
		
	pickle.dump(data, open(path, "wb"))
	

def parseMoves(move:str, verbose:bool = False, force:bool = False) -> None:
	htmlFile = f"html/moves/{move}/{move}.html"
	path =  f"pkl/moves/{move}/{move}.pkl"
	
	if(_pathExist(path) and not force):
		return
	
	if(verbose):
		print(f"Move: {move}")
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	
	
	# Get name
	data["name"] = html.select("main>h1")[0].find(text=True).strip()
	
	
	# Get move data
	subset = html.select("table.vitals-table")[0].select("tr")
	
	# Get type
	temp = _formatText(subset[0].td.text).lower().strip()
	data["type"] = "-" if (temp == "—") else temp
	# Get catigory
	temp = _formatText(subset[1].td.text).lower().strip()
	data["catigory"] = "-" if (temp == "—") else temp
	# Get power
	temp = _formatText(subset[2].td.text).lower().strip()
	data["power"] = "-" if (temp == "—") else temp
	# Get accuracy
	temp = _formatText(subset[3].td.text).lower().strip()
	data["accuracy"] = "-" if (temp == "—") else temp
	# Get PP
	temp = _formatText(subset[4].td.text).lower().strip()
	data["pp"] = "-" if (temp == "—") else temp
	# Get max PP
	try:
		data["max-pp"] = _formatText(subset[4].td.text).lower().split(" ")[2].strip()
	except:
		data["max-pp"] = "-"
	# Get makes contact
	temp = _formatText(subset[5].td.text).lower().strip()
	data["makes-contact"] = "-" if (temp == "—") else temp
	# Get introduced
	temp = _formatText(subset[6].td.text).lower().strip()
	data["introduced"] = "-" if (temp == "—") else temp[:3]+temp[-2:].strip()
	
	
	# Get machine/record
	data["machine/record"] = []
	subset = html.select("table.vitals-table")[1].select("tr")
	for tag in subset:
		game = _formatText(tag.th.text)
		value = _formatText(tag.td.text).strip()
		data["machine/record"].append({"game": game, "number": value})
	
	
	# Get effects
	subset = html.select("#move-effects")[0].next_siblings
	tempEffect = ""
	for tag in subset:
		if(tag.name == "p"):
			tempEffect += _formatText(tag.text)
		elif(tag.name == "h3"):
			break
	
	data["effects"] = tempEffect.strip()
	
	
	# Get z-move effects
	subset = html.select("#move-effects")[0].next_siblings
	tempEffect = ""
	for tag in subset:
		if(tag.name == "p"):
			tempEffect += _formatText(tag.text)
		elif(tag.name == "h3"):
			tempEffect = ""
	
	data["z-effects"] = tempEffect.strip()
	
	
	# Get move descriptions
	data["description"] = []
	try:
		subset = html.select("#move-descr")[0].next_sibling.select("tr")
		for tag in subset:
			games = tag.th.select("span")
			tempGame = []
			for game in games:
				tempGame.append(_formatText(game.text))
			data["description"].append({"game": tempGame, "description": _formatText(tag.td.text)})
	except:
		with open("errors.txt", "a") as f:
			f.write(f"Moves.Description: {move}\n")
	
	pickle.dump(data, open(path, "wb"))


def parseAbilities(ability:str, verbose:bool = False, force:bool = False) -> None:
	htmlFile = f"html/abilities/{ability}/{ability}.html"
	path =  f"pkl/abilities/{ability}/{ability}.pkl"
	
	if(_pathExist(path) and not force):
		return
	
	if(verbose):
		print(f"Ability: {ability}")
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	
	
	# Get name
	data["name"] = html.select("main>h1")[0].find(text=True).strip()
	
	
	# Get effect
	try:
		tempEffect = ""
		subset = html.findAll(text="Effect")[0].find_next()
		while subset.name == "p":
			tempEffect += _formatText(subset.text) + " "
			subset = subset.next_sibling
		tempEffect = tempEffect.strip()
		# if(len(tempEffect) > 800):
		# 	with open("temperrors.txt", "a") as f:
		# 		f.write(f"Ability.Effect: {ability} {len(tempEffect)}\n")
		data["effect"] = tempEffect
	except:
		with open("errors.txt", "a") as f:
			f.write(f"Abilities.Effect: {ability}\n")
		
		subset = html.findAll(text="Effect")[0].find_next("p")
		tempEffect = str(subset).replace("<p>", "")
		tempEffect = tempEffect[:tempEffect.find("<")]
		tempEffect = _formatText(tempEffect)
		data["effect"] = tempEffect
	
	
	# Get descriptions
	subset = html.select(".vitals-table")[0].select("tr")
	data["description"] = []
	for tag in subset:
		games = []
		for g in tag.th.select("span"):
			games.append(_formatText(g.text))
		desc = _formatText(tag.td.text)
		data["description"].append({"game": games, "description": desc})
	
	
	pickle.dump(data, open(path, "wb"))


def parseItems(item:str, verbose:bool = False, force:bool = False) -> None:
	htmlFile = f"html/items/{item}/{item}.html"
	path =  f"pkl/items/{item}/{item}.pkl"
	
	if(_pathExist(path) and not force):
		return
	
	if(verbose):
		print(f"Item: {item}")
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	
	
	# Get name
	data["name"] = html.select("main>h1")[0].find(text=True).strip()
	
	
	# Get effects
	data["effect"] = _formatText(html.findAll(text="Effects")[0].find_next("p").text).strip()
	
	
	# Get descriptions
	try:
		subset = html.select(".vitals-table")[0].select("tr")
		data["description"] = []
		for tag in subset:
			games = []
			for g in tag.th.select("span"):
				games.append(_formatText(g.text))
			desc = _formatText(tag.td.text)
			data["description"].append({"game": games, "description": desc})
	except:
		with open("errors.txt", "a") as f:
			f.write(f"Items.Description: {item}\n")
	
	
	pickle.dump(data, open(path, "wb"))


def parseKeyItems(keyitem:str, verbose:bool = False, force:bool = False) -> None:
	htmlFile = f"html/keyitems/{keyitem}/{keyitem}.html"
	path =  f"pkl/keyitems/{keyitem}/{keyitem}.pkl"
	
	if(_pathExist(path) and not force):
		return
	
	if(verbose):
		print(f"KeyItem: {keyitem}")
	
	with open(htmlFile, "r", encoding="utf-8") as f:
		html = bs(f, "html.parser")
		f.close()
	
	data = {}
	
	
	# Get name
	data["name"] = html.select("main>h1")[0].find(text=True).strip()
	
	
	# Get effects
	data["effect"] = _formatText(html.findAll(text="Effects")[0].find_next("p").text).strip()
	
	
	# Get descriptions
	try:
		subset = html.select(".vitals-table")[0].select("tr")
		data["description"] = []
		for tag in subset:
			games = []
			for g in tag.th.select("span"):
				games.append(_formatText(g.text))
			desc = _formatText(tag.td.text)
			data["description"].append({"game": games, "description": desc})
	except:
		with open("errors.txt", "a") as f:
			f.write(f"KeyItems.Description: {keyitem}\n")
	
	
	pickle.dump(data, open(path, "wb"))