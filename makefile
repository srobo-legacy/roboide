BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all dev bzr-repos run clean clean-pyc

all: dev

dev: bzr-repos devdata.sqlite

bzr-repos: repos $(BZR_REPOS)

repos:
	mkdir repos

devdata.sqlite:
	tg-admin -c dev.cfg sql create

$(BZR_REPOS):
	$(BZR_INIT) $@

run: dev
	./start-roboide.py dev.cfg

clean: clean-pyc test-clean
	rm -rf repos
	rm -f devdata.sqlite

clean-pyc:
	find -name *.pyc | xargs rm -f


## Test related targets

TEST_REPOS = test-repos/1 test-repos/2
REPO_SWAP = s/s\\/repos\\/TEAM/s\\/test-repos\\/TEAM/
DB_SWAP = s/devdata.sqlite/testdata.sqlite/

.PHONY: test test-run test-bzr-repos test-clean

test: test-clean test-bzr-repos testdata.sqlite test.cfg
	tests/suite.py

test.cfg:
	sed $(DB_SWAP) dev.cfg | sed $(REPO_SWAP) > test.cfg

testdata.sqlite: test.cfg
	tg-admin -c test.cfg sql create

test-bzr-repos: test-repos $(TEST_REPOS)

test-repos:
	mkdir test-repos

$(TEST_REPOS):
	$(BZR_INIT) $@

test-run: test-bzr-repos testdata.sqlite test.cfg
	./start-roboide.py test.cfg

test-clean: clean-pyc
	rm -f test-log test.cfg testdata.sqlite
	rm -rf test-repos
