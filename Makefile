VENV = .venv
ACT = $(VENV)/bin/activate
INSTALL = pip install
TEST_DIR = _trial_temp

build-venv:
	virtualenv $(VENV)

deps:
	. $(ACT) && $(INSTALL) genshi
	. $(ACT) && $(INSTALL) progressbar
	. $(ACT) && $(INSTALL) lxml

testing-deps:
	@# we use Twisted's trial as our test-runner
	. $(ACT) && $(INSTALL) twisted

check: build-venv deps testing-deps
	clear
	. $(ACT) && trial ./test

clean:
	rm -rf $(VENV) $(TEST_DIR)