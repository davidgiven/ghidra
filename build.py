from build.ab import (
    export,
    simplerule,
    Rule,
    Target,
    Targets,
    filenameof,
    filenamesof,
)
from build.java import javalibrary, externaljar, javaprogram
from build.utils import itemsof
from build.protobuf import protojava, proto
from os.path import *
from glob import glob
import re

EXTERNAL_JARS = [
    "TimingFramework",
    "asm",
    "antlr3",
    "antlr3-runtime",
    "bcpkix",
    "bcutil",
    "bnd",
    "bsaf",
    "commons-collections4",
    "commons-compress",
    "commons-dbcp2",
    "commons-io",
    "commons-lang3",
    "commons-text",
    "gson",
    "h2",
    "isorelax",
    "jdom1",
    "jgrapht-core",
    "jgrapht-io",
    "jh",
    "jna",
    "jna-platform",
    "jsch",
    "json-simple",
    "jung-algorithms",
    "jung-visualization",
    "junit4",
    "jython",
    "log4j-api",
    "log4j-core",
    "msv-core",
    "org.apache.felix.framework",
    "org.apache.felix.utils",
    "osgi.core",
    "protobuf",
    "smali",
    "xpp3",
    "baksmali",
]

EXTRA_JARS = [
    "jungrapht-layout-1.4",
    "jungrapht-visualization-1.4",
    "phidias-0.3.7",
    "dex-reader-2.4.18",
    "dex-reader-api-2.4.18",
    "dex-translator-2.4.18",
    "axmlprinter2-2016-07-27",
    "sevenzipjbinding-16.02-2.01",
    "java-sarif-2.0",
]

for j in EXTERNAL_JARS:
    externaljar(name=j, paths=[f"/usr/share/java/{j}.jar"])
for j in EXTRA_JARS:
    externaljar(name=j, paths=[f"{j}.jar"])

allmodules = {}


def ghidramodule(root, deps=[]):
    with open(join("Ghidra", root, "build.gradle")) as file:
        gradle = file.read()

    moduledeps = [
        "+module-" + d[1].lower()
        for d in re.finditer(r"api project\(['\"]:(.*)['\"]\)", gradle)
    ]

    depname = "module-" + root.lower().split("/")[-1]
    m = javalibrary(
        name=depname,
        srcitems=itemsof(
            pattern=join("Ghidra", root, "src/main/**/*.java"),
            root=join("Ghidra", root, "src"),
        ),
        deps=deps + moduledeps,
    )

    global allmodules
    allmodules["jars/" + depname + ".jar"] = m


ghidramodule("Framework/DB")
ghidramodule("Framework/Docking", deps=[".+TimingFramework", ".+commons-text"])
ghidramodule("Framework/Emulation")
ghidramodule("Framework/FileSystem")
ghidramodule(
    "Framework/Generic",
    deps=[
        ".+junit4",
        ".+jdom1",
        ".+log4j-api",
        ".+log4j-core",
        ".+commons-lang3",
        ".+commons-collections4",
        ".+commons-io",
        ".+commons-compress",
        ".+gson",
        ".+bcpkix",
        ".+bcutil",
    ],
)
ghidramodule("Framework/Graph", deps=[".+jung-visualization", ".+jgrapht-core"])
ghidramodule("Framework/Gui")
ghidramodule("Framework/Help", deps=[".+jh"])
ghidramodule("Framework/Project")
ghidramodule(
    "Framework/SoftwareModeling",
    deps=[
        ".+booleanexpression_antlr",
        ".+semanticlexer_antlr",
        ".+displaylexer_antlr",
        ".+baselexer_antlr",
        ".+sleighparser_antlr",
        ".+sleighecho_antlr",
        ".+sleighcompiler_antlr",
        ".+msv-core",
        ".+antlr3-runtime",
        ".+isorelax",
    ],
)
ghidramodule("Framework/Utility")
ghidramodule(
    "Features/Base",
    deps=[
        ".+c_jj",
        ".+cpp_jj",
        ".+osgi.core",
        ".+bnd",
        ".+org.apache.felix.framework",
        ".+phidias-0.3.7",
    ],
)
ghidramodule("Features/BSim", deps=[".+commons-dbcp2", ".+json-simple", ".+h2"])
ghidramodule("Features/BSimFeatureVisualizer")
ghidramodule("Features/BytePatterns")
ghidramodule("Features/ByteViewer")
ghidramodule("Features/CodeCompare")
ghidramodule("Features/DebugUtils")
ghidramodule("Features/Decompiler")
ghidramodule("Features/DecompilerDependent")
ghidramodule(
    "Features/FileFormats",
    deps=[
        ".+xpp3",
        ".+dex-reader-2.4.18",
        ".+dex-reader-api-2.4.18",
        ".+dex-translator-2.4.18",
        ".+baksmali",
        ".+asm",
        ".+axmlprinter2-2016-07-27",
        ".+sevenzipjbinding-16.02-2.01",
    ],
)
ghidramodule("Features/FunctionGraph")
ghidramodule("Features/FunctionGraphDecompilerExtension")
ghidramodule("Features/FunctionID")
ghidramodule("Features/GhidraGo")
ghidramodule("Features/GhidraServer")
ghidramodule("Features/GnuDemangler")
ghidramodule("Features/GraphFunctionCalls")
ghidramodule(
    "Features/GraphServices",
    deps=[
        ".+jgrapht-core",
        ".+jgrapht-io",
        ".+jungrapht-visualization-1.4",
        ".+jungrapht-layout-1.4",
    ],
)
ghidramodule("Features/MicrosoftCodeAnalyzer")
ghidramodule("Features/MicrosoftDemangler")
ghidramodule("Features/MicrosoftDmang")
ghidramodule("Features/PDB")
ghidramodule("Features/ProgramDiff")
ghidramodule("Features/ProgramGraph")
# ghidramodule("Features/Python", deps=[".+jython"])
ghidramodule("Features/Recognizers")
ghidramodule("Features/Sarif", deps=[".+java-sarif-2.0"])
ghidramodule("Features/SourceCodeLookup")
ghidramodule("Features/SystemEmulation")
ghidramodule("Features/VersionTracking")
ghidramodule("Features/VersionTrackingBSim")
ghidramodule("Debug/Debugger-isf", deps=[".+isfprotojava"])
ghidramodule("Debug/Framework-AsyncComm")
ghidramodule("Debug/Framework-Debugging")
ghidramodule("Debug/Framework-TraceModeling")
ghidramodule("Debug/ProposedUtils")
ghidramodule("Debug/Debugger")
ghidramodule("Debug/Debugger-api")

simplerule(
    name="sleightokens",
    ins=glob(
        "Ghidra/Framework/SoftwareModeling/src/main/antlr/ghidra/sleigh/grammar/*.g"
    ),
    outs=["=SleighLexer.tokens"],
    commands=[
        "$(ANTLR3) Ghidra/Framework/SoftwareModeling/src/main/antlr/ghidra/sleigh/grammar/SleighLexer.g -o $(dir {outs[0]})"
    ],
    label="ANTLR3",
)

proto(
    name="isfproto", srcs=["Ghidra/Debug/Debugger-isf/src/main/proto/isf.proto"]
)
protojava(name="isfprotojava", srcs=[".+isfproto"], deps=[".+protobuf"])


@Rule
def antlr(self, name, src: Target, tokens: Target, deps: Targets = []):
    r = simplerule(
        replaces=self,
        ins=[src, tokens] + deps,
        outs=[f"={self.localname}.srcjar"],
        commands=[
            "rm -rf {dir}/srcs",
            "mkdir -p {dir}/srcs",
            (
                "$(ANTLR3) {ins[0]} -lib "
                + dirname(filenameof(tokens))
                + " -o {dir}/srcs"
            ),
            "find {dir}/srcs -name '*.java' | xargs sed -i '1ipackage ghidra.sleigh.grammar;'",
            "(cd {dir}/srcs && $(JAR) cf $(abspath {outs[0]}) .)",
        ],
        label="ANTLR3",
    )
    r.traits.add("srcjar")


ANTLRFILES = glob(
    "Ghidra/Framework/SoftwareModeling/src/main/antlr/ghidra/sleigh/grammar/*.g"
)

for f in ANTLRFILES:
    (fd, _) = splitext(basename(f))
    antlr(name=f"{fd.lower()}_antlr", tokens=".+sleightokens", src=f)


@Rule
def jj(self, name, src: Target):
    r = simplerule(
        replaces=self,
        ins=[src],
        outs=[f"={self.localname}.srcjar"],
        commands=[
            "mkdir -p {dir}/srcs",
            "$(JAVACC) -g -OUTPUT_DIRECTORY={dir}/srcs {ins}",
            "(cd {dir}/srcs && $(JAR) cf $(abspath {outs[0]}) .)",
        ],
        label="JAVACC",
    )
    r.traits.add("srcjar")


jj(
    name="c_jj",
    src="Ghidra/Features/Base/src/main/javacc/ghidra/app/util/cparser/C/C.jj",
)
jj(
    name="cpp_jj",
    src="Ghidra/Features/Base/src/main/javacc/ghidra/app/util/cparser/CPP/CPP.jj",
)

javaprogram(
    name="sleigh",
    mainclass="ghidra.pcodeCPort.slgh_compile.SleighCompile",
    deps=[".+module-softwaremodeling"],
)


def ghidraprocessor(root, deps=[]):
    path = f"Ghidra/Processors/{root}/data/languages"
    s = simplerule(
        name=f"{root}_sla",
        ins=[".+sleigh"] + glob(path + "/*.{sla,slaspec}"),
        outs=[f"={root}.srcjar"],
        commands=[
            "mkdir -p {dir}/srcs",
            "chronic $(JAVA) -jar {ins[0]} -a " + path + " {dir}/srcs",
            "(cd {dir}/srcs && $(JAR) cf $(abspath {outs[0]}) .)",
        ],
        label="SLEIGH",
        traits={"srcjar"},
    )

    ghidramodule("Processors/" + root, deps + [s])


for m in glob("Ghidra/Processors/*"):
    if exists(m + "/build.gradle"):
        ghidraprocessor(basename(m))

javaprogram(
    name="ghidra", mainclass="ghidra.GhidraRun", deps=allmodules.values()
)

export(
    name="all",
    items={
        "sleigh.jar": ".+sleigh",
        "ghidra.jar": ".+ghidra",
        "decompile": "Ghidra/Features/Decompiler/src/decompile+decompile",
        # "sleigh": "Ghidra/Features/Decompiler/src/decompile+sleigh",
    },
)
