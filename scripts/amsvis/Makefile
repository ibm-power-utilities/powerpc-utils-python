#
# Makefile for powerpc-utils/scripts/amsvis
#

AMSVIS_VERSION = `grep "define version" ../../powerpc-utils-python.spec.in | cut -d " " -f 3`

# Files built from .in files
IN_FILES = setup.py

MODULES_DIR = powerpcAMS
MODULE_FILES := $(notdir $(wildcard $(MODULES_DIR)/*.py))

# The location where python site libraries are installed is needed for
# the uninstall method.  It is found by calling distutils in python.
PYTHONLIBS := `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
PYTHONLIBS_AMS := $(DESTDIR)/$(PYTHONLIBS)/$(MODULES_DIR)

DIST_FILES = amsvis Makefile setup.py.in
DIST_DIRS = powerpcAMS

INSTALL := `which install`
RM := `which rm`

all:
	@echo "Configuring setup.py"
	@sed "s|\@VERSION\@|$(AMSVIS_VERSION)|g" setup.py.in > setup.py
	@echo "Running setup.py"
	@python setup.py build

dist:
	@mkdir $(PPUP_DIST_DIR)/amsvis
	@cp $(DIST_FILES) $(PPUP_DIST_DIR)/amsvis
	@mkdir $(PPUP_DIST_DIR)/amsvis/powerpcAMS
	@cp powerpcAMS/* $(PPUP_DIST_DIR)/amsvis/powerpcAMS

install: all
	@echo "Installing amsvis"
	@$(INSTALL) -d -m 755 $(DESTDIR)/usr/bin
	@$(INSTALL) -m 755 amsvis $(DESTDIR)/usr/bin/
	@python setup.py install --prefix=$(DESTDIR)/usr

uninstall:
	@echo "Un-installing amsvis"
	@$(RM) -f $(DESTDIR)/usr/bin/amsvis
	@$(RM) -rf $(PYTHONLIBS_AMS)
	@$(RM) -f $(DESTDIR)/$(PYTHONLIBS)/$(MODULES_DIR)*.egg.info

clean:
	@echo "Cleaning up scripts/amsvis files..."
	@rm -Rf build

distclean:
	@echo "Cleaning up scripts/amsvis files..."
	@rm -Rf build $(IN_FILES)

maintainer-clean: distclean
