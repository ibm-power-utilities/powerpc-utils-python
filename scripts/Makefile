#
# Makefile for scripts directory
#

SUBDIRS = amsvis

all:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d;)

install:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d install;)

uninstall:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d uninstall;)

clean:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d clean;)

