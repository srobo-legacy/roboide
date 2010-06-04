BZR_REPOS = repos/1 repos/2
BZR_INIT = bzr init-repo --no-trees --pack-0.92

.PHONY: all
.PHONY: dev
all: dev

dev: repos bzr def.cfg

repos:
	mkdir repos
def.cfg:
	tg-admin -c dev.cgf sql create

.PHONY: clean
.PHONY: bzr
bzr: $(BZR_REPOS)

$(BZR_REPOS):
	$(BZR_INIT) $@


clean:
	rm -rf repos
	rm -f devdata.sqlite
