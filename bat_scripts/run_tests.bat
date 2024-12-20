:: run_tests.bat
:: To run specific tests, use:
:: run_tests.bat [file_name]::[test_class]::[test_method]
@echo off

set test_file=%1

pytest --cov-report term-missing --cov-report html:tests\cov_html --cov=src tests/%test_file% --html=tests/report/test_report.html