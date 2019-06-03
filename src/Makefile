TODAY:=$(shell date +%Y-%m-%d)
DESTDIR:=/tmp
SRCBASE:=$(DESTDIR)/script_inception_public_$(TODAY)_source
DOCBASE:=$(DESTDIR)/script_inception_public_$(TODAY)_doc

all: package_source package_doc

package_source:
	# TODO: fix so it works without cd, or move the Makefile, etc
	cd .. && git archive --format=zip --output=$(SRCBASE).zip HEAD

package_doc:
	cd docs && $(MAKE) BUILDDIR=$(DOCBASE) html-without-todo
	cd $(DOCBASE) && zip --filesync --recurse-paths $(DOCBASE).zip .

test:
	echo $(SRCBASE)
	echo $(DOCBASE)
