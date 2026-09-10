.PHONY: all test test-reference
all:
	python3 build.py

test: all
	python3 verify.py
	python3 reference_tests.py --legacy-only

test-reference: all
	python3 reference_tests.py
