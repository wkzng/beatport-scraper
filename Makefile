remote:
	sls invoke --stage dev --function beatport --path tests/events/beatport.json

local:
	sls invoke local --stage dev --function beatport --path tests/events/beatport.json

test:
	python -m src.handler