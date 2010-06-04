dev:
	mkdir repos
	bzr init-repo --no-trees --pack-0.92 repos/1
	bzr init-repo --no-trees --pack-0.92 repos/2
	tg-admin -c dev.cfg sql create

clean:
	rm -rf repos
	rm -f devdata.sqlite
