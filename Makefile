
test:
	pytest -vv \
		--pep8 --flakes navec \
		--cov-report term-missing --cov-report xml \
		--cov-config setup.cfg --cov navec 

version:
	bumpversion minor

wheel:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

clean:
	find . \
		-name '*.pyc' \
		-o -name __pycache__ \
		-o -name .DS_Store \
		| xargs rm -rf
	rm -rf dist/ build/ .ipynb_checkpoints/ .pytest_cache/ .cache/ \
		*.egg-info .coverage coverage.xml
