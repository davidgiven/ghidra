JAVAC = chronic javac
JAVA = java
ANTLR3 = chronic antlr3
JAVACC = chronic javacc
OBJ = .obj

JFLAGS = \
	--add-exports=java.desktop/sun.awt=ALL-UNNAMED \
	-nowarn \
	-proc:full \
	-g \

.PHONY: all
all: +all

include build/ab.mk

