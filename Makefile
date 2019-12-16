install:
	pip install -r bot/requirements.txt
	cd leaderboard-ui && npm i

rating:
	python bot/get_ratings.py

deploy: rating
	cd leaderboard-ui && npm run deploy

start:
	python bot/main.py
