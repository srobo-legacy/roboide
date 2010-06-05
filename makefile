BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all run dev bzr-repos clean

all: dev

dev: bzr-repos devdata.sqlite

bzr-repos: repos $(BZR_REPOS)

repos:
	mkdir repos

devdata.sqlite:
	paster setup-app development.ini

$(BZR_REPOS):
	$(BZR_INIT) $@

run:
	paster serve --reload development.ini

clean:
	rm -rf repos
	rm -f devdata.sqlite
