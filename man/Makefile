#
# Makefile for man directory
#

MAN_FILES = amsvis.1
GZMAN_FILES = amsvis.1.gz
MAN_DIR = /usr/share/man/man1
DIST_FILES = $(MAN_FILES) Makefile

INSTALL := `which install`
RM = `which rm`

all: $(GZMAN_FILES)

dist:
	@mkdir $(PPUP_DIST_DIR)/man
	@cp $(DIST_FILES) $(PPUP_DIST_DIR)/man

%.1.gz: %.1
	gzip -c $< > $@

install: $(GZMAN_FILES)
	@$(INSTALL) -d -m 755 $(DESTDIR)$(MAN_DIR)
	@$(foreach f,$(GZMAN_FILES), echo Installing $(f); $(INSTALL) -m 644 $(f) $(DESTDIR)$(MAN_DIR);)

uninstall:
	@$(foreach f,$(GZMAN_FILES), echo "Un-installing $(f); $(RM) $(DESTDIR)$(MAN_DIR)/$(f);)

clean:

