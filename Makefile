all: test deploy

deploy:
	sls deploy -v
dfunc:
	sls deploy function --function $(name)
test:
	tableName=test keyName=Key ttlName=Expires py.test --cov=handler handler_test.py
acceptance:
	API_KEY=$(apikey) SERVICE_ENDPOINT=$(endpoint) pytest -s acceptance.py

remove:
	sls remove -v
