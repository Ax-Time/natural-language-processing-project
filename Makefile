up:
	# Create virtual environment and install dependencies
	python -m venv .env
	python -m pip install -r requirements.txt

load:
	mkdir wizard_of_wikipedia
	wget -c https://parl.ai/downloads/wizard_of_wikipedia/wizard_of_wikipedia.tgz -O - | tar -xz -C ./wizard_of_wikipedia