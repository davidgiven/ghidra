from build.ab import (
    export,
    simplerule,
    Rule,
    Target,
    Targets,
    filenameof,
    filenamesof,
)
from build.java import (
    javalibrary,
    externaljar,
    javaprogram,
    javalink,
    mavenjar,
    httpjar,
)
from build.utils import itemsof
from build.protobuf import protojava, proto
from build.zip import zip
from os.path import *
from glob import glob
import re

EXTERNAL_JARS = {
    "TimingFramework": "net.java.dev.timingframework:timingframework:1.0",
    "antlr3-runtime": "org.antlr:antlr-runtime:3.5.2",
    "asm": "org.ow2.asm:asm-debug-all:5.0.3",
    "baksmali": "org.smali:baksmali:2.5.2",
    "bcpkix": "org.bouncycastle:bcpkix-jdk15on:1.69",
    "bcprov": "org.bouncycastle:bcprov-jdk15on:1.69",
    "bcutil": "org.bouncycastle:bcutil-jdk15on:1.69",
    "bnd": "biz.aQute.bnd:biz.aQute.bnd.util:7.0.0",
    "bndlib": "biz.aQute.bnd:biz.aQute.bndlib:7.0.0",
    "commons-collections4": "org.apache.commons:commons-collections4:4.4",
    "commons-compress": "org.apache.commons:commons-compress:1.27.1",
    "commons-dbcp2": "org.apache.commons:commons-dbcp2:2.9.0",
    "commons-io": "commons-io:commons-io:2.11.0",
    "commons-lang3": "org.apache.commons:commons-lang3:3.17.0",
    "commons-text": "org.apache.commons:commons-text:1.10.0",
    "dex-reader": "de.femtopedia.dex2jar:dex-reader:2.4.24",
    "dex-reader-api": "de.femtopedia.dex2jar:dex-reader-api:2.4.24",
    "dex-translator": "de.femtopedia.dex2jar:dex-translator:2.4.24",
    "dexlib2": "org.smali:dexlib2:2.5.2",
    "flatlaf": "com.formdev:flatlaf:3.2.1",
    "gson": "com.google.code.gson:gson:2.9.0",
    "guava": "com.google.guava:guava:32.1.3-jre",
    "h2": "com.h2database:h2:2.2.220",
    "isorelax": "msv:isorelax:20050913",
    "jdom1": "org.jdom:jdom-legacy:1.1.3",
    "jgrapht-core": "org.jgrapht:jgrapht-core:1.5.1",
    "jgrapht-io": "org.jgrapht:jgrapht-io:1.5.1",
    "jh": "javax.help:javahelp:2.0.05",
    "jna": "net.java.dev.jna:jna:5.14.0",
    "jna-platform": "net.java.dev.jna:jna-platform:5.14.0",
    "jsch": "com.jcraft:jsch:0.1.55",
    "json-simple": "com.googlecode.json-simple:json-simple:1.1.1",
    "jung-algorithms": "net.sf.jung:jung-algorithms:2.1.1",
    "jung-api": "net.sf.jung:jung-api:2.1.1",
    "jung-graph-impl": "net.sf.jung:jung-graph-impl:2.1.1",
    "jung-visualization": "net.sf.jung:jung-visualization:2.1.1",
    "jungrapht-io": "org.jgrapht:jgrapht-io:1.5.1",
    "jungrapht-layout": "com.github.tomnelson:jungrapht-layout:1.4",
    "jungrapht-visualization": "com.github.tomnelson:jungrapht-visualization:1.4",
    "junit4": "junit:junit:4.12",
    "log4j-api": "org.apache.logging.log4j:log4j-api:2.17.1",
    "log4j-core": "org.apache.logging.log4j:log4j-core:2.17.1",
    "msv": "msv:msv:20050913",
    "olcut-protobuf": "com.oracle.labs.olcut:olcut-config-protobuf:5.2.0",
    "org.apache.felix.framework": "org.apache.felix:org.apache.felix.framework:7.0.5",
    "org.apache.felix.utils": "org.apache.felix:org.apache.felix.utils:7.0.5",
    "osgi.core": "org.osgi:osgi.core:8.0.0",
    "osgi.promise": "org.osgi:org.osgi.util.promise:1.3.0",
    "phidias": "com.github.rotty3000:phidias:0.3.7",
    "protobuf": "com.google.protobuf:protobuf-java:3.19.6",
    "sevenzipjbinding": "net.sf.sevenzipjbinding:sevenzipjbinding:16.02-2.01",
    "sevenzipjbinding": "net.sf.sevenzipjbinding:sevenzipjbinding:16.02-2.01",
    "slf4j-api": "org.slf4j:slf4j-api:1.7.25",
    "smali": "org.smali:util:2.5.2",
    "xpp3": "org.ogce:xpp3:1.1.6",
    "xz": "org.tukaani:xz:1.9",
#"antlr3",
#"bsaf",
#"jython",
}

for name, artifact in EXTERNAL_JARS.items():
    mavenjar(name=name, artifact=artifact)

httpjar(
    name="java-sarif",
    url="https://github.com/NationalSecurityAgency/ghidra-data/raw/refs/heads/main/lib/java-sarif-2.1-modified.jar"
)
httpjar(
    name="axmlprinter2",
    url="https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/android4me/AXMLPrinter2.jar")

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
        args={"modulename": root},
    )

    global allmodules
    allmodules[root] = m


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
        ".+bcprov",
    ],
)
ghidramodule(
    "Framework/Graph",
    deps=[
        ".+guava",
        ".+jung-api",
        ".+jung-visualization",
        ".+jung-algorithms",
        ".+jung-graph-impl",
        ".+jgrapht-core",
    ],
)
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
        ".+msv",
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
        ".+phidias",
        ".+bnd",
        ".+bndlib",
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
        ".+dex-reader",
        ".+dex-reader-api",
        ".+dex-translator",
        ".+dexlib2",
        ".+baksmali",
        ".+asm",
        ".+axmlprinter2",
        ".+sevenzipjbinding",
        ".+xz",
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
        ".+jungrapht-visualization",
        ".+jungrapht-layout",
    ],
)
ghidramodule("Features/MicrosoftCodeAnalyzer")
ghidramodule("Features/MicrosoftDemangler")
ghidramodule("Features/MicrosoftDmang")
ghidramodule("Features/PDB")
ghidramodule("Features/ProgramDiff")
ghidramodule("Features/ProgramGraph")
#ghidramodule("Features/Python", deps = [".+jython"])
ghidramodule("Features/Recognizers")
ghidramodule("Features/Sarif", deps=[".+java-sarif"])
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
            "chronic {ins[0]} -a " + path + " {dir}/srcs",
            "(cd {dir}/srcs && $(JAR) cf $(abspath {outs[0]}) .)",
        ],
        label="SLEIGH",
        traits={"srcjar"},
    )

    ghidramodule("Processors/" + root, deps + [s])


for m in glob("Ghidra/Processors/*"):
    if exists(m + "/build.gradle"):
        ghidraprocessor(basename(m))

javalibrary(
    name="launchsupport",
    srcitems=itemsof(
        pattern="GhidraBuild/LaunchSupport/src/main/**/*.java",
        root="GhidraBuild/LaunchSupport",
    ),
)

export(
    name="all",
    items={
        "dist/ghidraRun": "./Ghidra/RuntimeScripts/Linux/ghidraRun",
        "dist/support/launch.sh": "./Ghidra/RuntimeScripts/Linux/support/launch.sh",
        "dist/support/launch.properties": "./Ghidra/RuntimeScripts/Common/support/launch.properties",
        "dist/support/debug.log4j.xml": "./Ghidra/RuntimeScripts/Common/support/debug.log4j.xml",
        "dist/support/LaunchSupport.jar": "+launchsupport",
        "dist/decompile": "Ghidra/Features/Decompiler/src/decompile+decompile",
        "dist/Ghidra/application.properties": "Ghidra/application.properties",
#"sleigh" : "Ghidra/Features/Decompiler/src/decompile+sleigh",
    }
    | {
        f"dist/Ghidra/{root}/lib/{basename(root)}.jar": t
        for root, t in allmodules.items()
    }
    | {
        f"dist/Ghidra/{root}/Module.manifest": f"Ghidra/{root}/Module.manifest"
        for root in allmodules.keys()
    },
)
