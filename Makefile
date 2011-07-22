#
# Makefile for powerpc-utils-python
#

PPU_PYTHON_VERSION = 1.2.1
SUBDIRS = scripts man
FILES = README COPYRIGHT
DIST_FILES = $(FILES) Makefile powerpc-utils-python.spec.in
DIST_DIR = powerpc-utils-python-$(PPU_PYTHON_VERSION)
DOCS_DIR = /usr/share/doc/packages/powerpc-utils-python

INSTALL := `which install`
RM := `which rm`
RPMBUILD = `which rpmbuild`
SED = `which sed`

IN_FILES = powerpc-utils-python.spec

PYTHON_VERSION = `python -c "from platform import python_version_tuple; (x,y,z) = python_version_tuple(); print '%s.%s' % (x,y)" 2>/dev/null`
PYTHON_INSTDIR = `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`

all: specfile
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d;)

specfile:
	@echo "Configuring powerpc-utils-python.spec"
	@$(SED) "s|\@PPU_PYTHON_VERSION\@|$(PPU_PYTHON_VERSION)|g;	\
		 s|\@PY_VERSION\@|$(PYTHON_VERSION)|g;			\
		 s|\@PYTHON_SITE_PKGS\@|$(PYTHON_INSTDIR)|g"		\
		 powerpc-utils-python.spec.in > powerpc-utils-python.spec

install: all
	@$(INSTALL) -d -m 755 $(DESTDIR)$(DOCS_DIR)
	@$(foreach f,$(FILES), echo Installing $(f); $(INSTALL) -m 644 $(f) $(DESTDIR)$(DOCS_DIR);)
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d install;)

uninstall:
	@$(foreach f,$(FILES), echo Un-installing $(f); $(RM) $(DESTDIR)$(DOCS_DIR)/$(f);)
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d uninstall;)

dist:
	@echo "Creating dist..."
	@$(RM) $(DIST_DIR).tar.gz
	@mkdir $(DIST_DIR)
	@cp $(DIST_FILES) $(DIST_DIR)
	@$(MAKE) PPUP_DIST_DIR=$(PWD)/$(DIST_DIR) -C man dist
	@$(MAKE) PPUP_DIST_DIR=$(PWD)/$(DIST_DIR) -C scripts dist
	@tar cf $(DIST_DIR).tar $(DIST_DIR)
	@gzip $(DIST_DIR).tar
	@$(RM) -r $(DIST_DIR)

clean:
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d clean;)

distclean: clean
	@$(RM) $(IN_FILES) $(DIST_DIR).tar.gz
	@$(foreach d,$(SUBDIRS), $(MAKE) -C $d distclean;)
