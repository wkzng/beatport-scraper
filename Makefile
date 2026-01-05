sls_remote:
	sls invoke --stage dev --function beatport --path tests/events/beatport.json

sls_local:
	sls invoke local --stage dev --function beatport --path tests/events/beatport.json

debug:
	python -m src.handler

test_lambda:
	python -m tests.test_invoke_lambda

test_api:
	python -m tests.test_invoke_api

test_mcp:
	python -m tests.test_mcp