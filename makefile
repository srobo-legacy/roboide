BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all dev bzr-repos run clean clean-pyc

all: dev

dev: bzr-repos devdata.sqlite

bzr-repos: repos $(BZR_REPOS)

repos:
	mkdir repos

devdata.sqlite:
	paster setup-app development.ini

$(BZR_REPOS):
	$(BZR_INIT) $@

run: dev
	paster serve --reload development.ini

clean: test-clean
	rm -rf repos
	rm -f devdata.sqlite

clean-pyc:
	find -name *.pyc | xargs rm -f


## Test related targets

TEST_REPOS = test-repos/1 test-repos/2
REPO_SWAP = s/\\/repos\\/TEAM/\\/test-repos\\/TEAM/
PORT_SWAP = s/^port.*=.*8080.*/port=12345/
DB_SWAP = s/devdata\.sqlite/testdata\.sqlite/

.PHONY: test test-run test-bzr-repos test-clean

test: test-clean test-bzr-repos testdata.sqlite test.ini
	tests/suite.py test.ini

test.ini:
	sed $(DB_SWAP) development.ini | sed $(REPO_SWAP) | sed $(PORT_SWAP) > test.ini

testdata.sqlite: test.ini
	paster setup-app test.ini

test-bzr-repos: test-repos $(TEST_REPOS)

test-repos:
	mkdir test-repos

$(TEST_REPOS):
	$(BZR_INIT) $@

test-run: test-bzr-repos testdata.sqlite test.ini
	paster serve test.ini

test-clean: clean-pyc
	rm -f test-log test.ini testdata.sqlite
	rm -rf test-repos
