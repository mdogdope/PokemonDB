import pickle

def CombinePokemon(dataFileList:list) -> None:
	data = {}
	for dataFile in dataFileList:
		fileName = f"pkl/pokemon/{dataFile}/{dataFile}.pkl"
		data[dataFile] = pickle.load(open(fileName, "rb"))
	
	pickle.dump(data, open("pkl/pokemon.pkl", "wb"))
		