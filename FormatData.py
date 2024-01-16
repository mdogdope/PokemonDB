import pickle

def combinePokemon(dataFileList:list) -> None:
	data = []
	for dataFile in dataFileList:
		fileName = f"pkl/pokemon/{dataFile}/{dataFile}.pkl"
		data.append(pickle.load(open(fileName, "rb")))
	
	pickle.dump(data, open("pkl/pokemon.pkl", "wb"))


def combineMoves(dataFileList:list) -> None:
	data = []
	for dataFile in dataFileList:
		fileName = f"pkl/moves/{dataFile}/{dataFile}.pkl"
		data.append(pickle.load(open(fileName, "rb")))
	
	pickle.dump(data, open("pkl/moves.pkl", "wb"))


def combineAbilities(dataFileList:list) -> None:
	data = []
	for dataFile in dataFileList:
		fileName = f"pkl/abilities/{dataFile}/{dataFile}.pkl"
		data.append(pickle.load(open(fileName, "rb")))
	
	pickle.dump(data, open("pkl/abilities.pkl", "wb"))


def combineItems(dataFileList:list) -> None:
	data = []
	for dataFile in dataFileList:
		fileName = f"pkl/items/{dataFile}/{dataFile}.pkl"
		data.append(pickle.load(open(fileName, "rb")))
	
	pickle.dump(data, open("pkl/items.pkl", "wb"))


def combineKeyItems(dataFileList:list) -> None:
	data = []
	for dataFile in dataFileList:
		fileName = f"pkl/keyitems/{dataFile}/{dataFile}.pkl"
		data.append(pickle.load(open(fileName, "rb")))
	
	pickle.dump(data, open("pkl/keyitems.pkl", "wb"))


def combineAllData(dataFileList:list) -> None:
	data = {}
	for dataFile in dataFileList:
		print(f"Loading: {dataFile}")
		fileName = f"pkl/{dataFile}.pkl"
		data[dataFile] = pickle.load(open(fileName, "rb"))
	
	pickle.dump(data, open("pkl/AllData.pkl", "wb"))