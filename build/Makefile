# Pulse Linux Build Makefile

SHELL := /bin/bash
REPO_ROOT := $(shell pwd)
PYTHON := python3

.PHONY: all toolchain rootfs initramfs iso test clean help

all: iso

help:
	@echo "Pulse Linux Build System"
	@echo "  make toolchain - Verify and stage build toolchains"
	@echo "  make rootfs    - Download base packages and generate root filesystem"
	@echo "  make initramfs - Assemble bootable live initramfs"
	@echo "  make iso       - Build bootable hybrid UEFI/BIOS ISO"
	@echo "  make test      - Execute QEMU boot verification test"
	@echo "  make clean     - Clean intermediate build work directories"

toolchain:
	$(PYTHON) build/scripts/00_setup_toolchain.py

rootfs: toolchain
	$(PYTHON) build/scripts/01_build_rootfs.py

initramfs: rootfs
	$(PYTHON) build/scripts/02_build_initramfs.py

iso: initramfs
	$(PYTHON) build/scripts/03_build_iso.py

test:
	./build/scripts/04_test_qemu.sh

clean:
	rm -rf build/work/rootfs build/work/iso_tree build/work/initrd_tree
	@echo "Cleaned build work directories."
