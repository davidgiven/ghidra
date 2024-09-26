JAVAC = chronic javac
JAVA = java
ANTLR3 = chronic antlr3
JAVACC = chronic javacc
OBJ = .obj

JFLAGS = \
	--source=23 \
	--target=23 \
	--add-exports=java.desktop/sun.awt=ALL-UNNAMED \
	-nowarn \
	-proc:full \
	-g \

CXXFLAGS = \
	-std=c++11 \
	-Wall \
	-O2 \
	-Wno-sign-compare \
	-DLINUX \
	-D_LINUX

.PHONY: all
all: +all

include build/ab.mk

