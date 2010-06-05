BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all dev bzr clean

all: dev

dev: repos bzr devdata.sqlite

repos:
	mkdir repos

devdata.sqlite:
	tg-admin -c dev.cgf sql create

bzr: $(BZR_REPOS)

$(BZR_REPOS):
	$(BZR_INIT) $@

clean:
	rm -rf repos
	rm -f devdata.sqlite

