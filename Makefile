#create venv: crv
#activate venv: acv
#pip upgrade: pipup
#install requirements: req
#update-ui: upui

crv:
	
	py -3.8 -m venv venv
	echo "venv creation: Done"

acv:
	
	.\venv\Scripts\activate.bat
	echo "venv activation: Done"

pipup:
	python -m pip install --upgrade pip 
	echo "venv activation: Done"
	
req:
	pip install -r requirements.txt
	echo "Packages installed: Done"

upui:
	pyuic5 gui.ui -o gui.py
