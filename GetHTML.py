import requests
import os
from selenium import webdriver

def _pathExist(path:str) -> bool:
	if(not os.path.exists("/".join(path.split("/")[:-1]))):
		os.makedirs("/".join(path.split("/")[:-1]))
	elif(os.path.exists(path)):
		return True
	return False

def reqGetImg(url:str, path:str = "img.png") -> None:
	if(not path.endswith(".png")):
		path += ".png"
	
	if(_pathExist(path)):
		return
	
	d = requests.get(url)
	
	with open(path, "wb") as f:
		f.write(d.content)

def reqGet(url:str, path:str = "page.html") -> None:
	if(not path.endswith(".html")):
		path += ".html"
	
	if(_pathExist(path)):
		return
	
	d = requests.get(url)
	
	with open(path, "w", encoding="utf-8") as f:
		f.write(d.text.replace("\n",""))

def selGet(url:str, path:str = "page.html") -> None:
	if(not path.endswith(".html")):
		path += ".html"
	
	if(_pathExist(path)):
		return
	
	driver = webdriver.Chrome()
	driver.get(url)
	
	with open(path, "w", encoding="utf-8") as f:
		f.write(driver.page_source.replace("\n", ""))