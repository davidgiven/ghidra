JAVAC = javac
JAVA = java
ANTLR3 = antlr3
OBJ = .obj

JFLAGS = \
	--add-exports=java.desktop/sun.awt=ALL-UNNAMED \
	-nowarn \
	-proc:full \
	-g \

.PHONY: all
all: +all

include build/ab.mk

