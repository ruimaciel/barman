.PHONY: test


test:
	python3 -m unittest tests/test_dofs.py
	python3 -m unittest tests/test_elements.py
	python3 -m unittest tests/test_models_linear_elastic.py
