#
# Makefile for scripts directory
#

SUBDIRS = amsvis
DIST_FILES = Makefile

all:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d;)

dist:
	@mkdir $(PPUP_DIST_DIR)/scripts
	@cp $(DIST_FILES) $(PPUP_DIST_DIR)/scripts
	@$(foreach d,$(SUBDIRS), $(MAKE) PPUP_DIST_DIR=$(PPUP_DIST_DIR)/scripts -C $d dist;)

install:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d install;)

uninstall:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d uninstall;)

clean:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d clean;)

