BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all dev bzr-repos run clean

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

clean:
	rm -rf repos
	rm -f devdata.sqlite

