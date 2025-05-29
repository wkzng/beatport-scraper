remote:
	sls invoke --stage dev --function beatport

local:
	sls invoke local --stage dev --function beatport

test:
	python -m src.invoke