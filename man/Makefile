#
# Makefile for man directory
#

MAN_FILES = amsvis.1
MAN_DIR = /usr/share/man/man1

INSTALL := `which install`
RM = `which rm`

all:

install:
	@$(INSTALL) -d -m 755 $(DESTDIR)$(MAN_DIR)
	@$(foreach f,$(MAN_FILES), echo Installing $(f); $(INSTALL) -m 644 $(f) $(DESTDIR)$(MAN_DIR);)

uninstall:
	@$(foreach f,$(MAN_FILES), echo "Un-installing $(f); $(RM) $(DESTDIR)$(MAN_DIR)/$(f);)

clean:

