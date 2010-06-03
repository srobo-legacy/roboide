.PHONY: run dev clean

dev:
	mkdir repos
	bzr init-repo --no-trees --pack-0.92 repos/1
	bzr init-repo --no-trees --pack-0.92 repos/2
	paster setup-app development.ini

run:
	paster serve --reload development.ini

clean:
	rm -rf repos
	rm devdata.sqlite
