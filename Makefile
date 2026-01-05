sls_remote:
	sls invoke --stage dev --function beatport --path tests/events/beatport.json

sls_local:
	sls invoke local --stage dev --function beatport --path tests/events/beatport.json

debug:
	python -m src.handler

test_lambda:
	python -m tests.invoke_lambda

test_api:
	python -m tests.invoke_api