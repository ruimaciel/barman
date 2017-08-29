.PHONY: test


test:
	python3 -m unittest tests/test_dofs.py
	python3 -m unittest tests/test_elements.py
	python3 -m unittest tests/test_models_Static.py
	python3 -m unittest tests/test_analysis_LinearStatic.py
