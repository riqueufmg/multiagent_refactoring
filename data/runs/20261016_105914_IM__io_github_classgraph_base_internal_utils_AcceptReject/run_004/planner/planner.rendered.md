## CONTEXT

Insufficient Modularization is a design smell that occurs when a class exists that has not been completely decomposed, and a further decomposition could reduce its size, implementation complexity, or both.

The factors that characterize Insufficient Modularization are considered in the following priority order:
- Too many public methods (poorly cohesive API).
- Too many general methods.
- Overly complex methods.

## TASK

Evaluate the input elements and create a plan in JSON format with the goal of removing (or reducing) Insufficient Modularization.

Strategy:
- Reduce the size and complexity of the class by grouping cohesive attributes and methods.
- MOVE and CREATE refactorings are only allowed at the same level as the entry or at a sub-level.
- When the smell is caused by too many public methods, prefer plans that move a cohesive group of public and private methods out of the target class.
- Test refactoring does not need to be included, as this will be done later.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "io.github.classgraph.base.internal.utils.AcceptReject",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261016_105914_IM__io_github_classgraph_base_internal_utils_AcceptReject/run_004/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptReject.java",
  "target_source_root": "classgraph-base/src/main/java",
  "target_code": "/*\n * This file is part of ClassGraph.\n *\n * The MIT License (MIT)\n */\npackage io.github.classgraph.base.internal.utils;\n\nimport java.util.ArrayList;\nimport java.util.Collection;\nimport java.util.List;\nimport java.util.Set;\nimport java.util.regex.Pattern;\n\nimport org.jspecify.annotations.Nullable;\n\n/** A class storing accept or reject criteria. */\npublic abstract class AcceptReject {\n    protected @Nullable Set<String> accept;\n    protected @Nullable Set<String> reject;\n    protected @Nullable Set<String> acceptPrefixesSet;\n    protected @Nullable List<String> acceptPrefixes;\n    protected @Nullable List<String> rejectPrefixes;\n    protected @Nullable Set<String> acceptGlobs;\n    protected @Nullable Set<String> rejectGlobs;\n    protected @Nullable List<Pattern> acceptPatterns;\n    protected @Nullable List<Pattern> acceptPrefixPatterns;\n    protected @Nullable List<Pattern> rejectPatterns;\n    protected char separatorChar;\n\n    protected AcceptReject(final char separatorChar) {\n        this.separatorChar = separatorChar;\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static Pattern globToPattern(final String glob, final char separatorChar, final boolean prefixMatch) {\n        return AcceptRejectUtils.globToPattern(glob, separatorChar, prefixMatch);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String stripTrailingDoubleGlob(final String packageOrPath, final char separatorChar) {\n        return AcceptRejectUtils.stripTrailingDoubleGlob(packageOrPath, separatorChar);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static boolean containsWildcard(final String str) {\n        return AcceptRejectUtils.containsWildcard(str);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String normalizePath(final String path) {\n        return AcceptRejectUtils.normalizePath(path);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String normalizePackageOrClassName(final String packageOrClassName) {\n        return AcceptRejectUtils.normalizePackageOrClassName(packageOrClassName);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String pathToPackageName(final String path) {\n        return AcceptRejectUtils.pathToPackageName(path);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String packageNameToPath(final String packageName) {\n        return AcceptRejectUtils.packageNameToPath(packageName);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String classNameToClassfilePath(final String className) {\n        return AcceptRejectUtils.classNameToClassfilePath(className);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static boolean matchesPatternList(final String str, final @Nullable List<Pattern> patterns) {\n        return AcceptRejectUtils.matchesPatternList(str, patterns);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static void quoteList(final Collection<String> coll, final StringBuilder buf) {\n        AcceptRejectUtils.quoteList(coll, buf);\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectPrefix extends io.github.classgraph.base.internal.utils.AcceptRejectPrefix {\n        public AcceptRejectPrefix(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectWholeString\n            extends io.github.classgraph.base.internal.utils.AcceptRejectWholeString {\n        public AcceptRejectWholeString(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectLeafname extends io.github.classgraph.base.internal.utils.AcceptRejectLeafname {\n        public AcceptRejectLeafname(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    public abstract void addToAccept(String str);\n\n    public abstract void addToReject(String str);\n\n    public abstract boolean isAcceptedAndNotRejected(String str);\n\n    public abstract boolean isAccepted(String str);\n\n    public abstract boolean acceptHasPrefix(String str);\n\n    public abstract boolean isRejected(String str);\n\n    public boolean acceptIsEmpty() {\n        return accept == null && acceptPrefixes == null && acceptPrefixesSet == null && acceptGlobs == null;\n    }\n\n    public boolean rejectIsEmpty() {\n        return reject == null && rejectPrefixes == null && rejectGlobs == null;\n    }\n\n    public boolean acceptAndRejectAreEmpty() {\n        return acceptIsEmpty() && rejectIsEmpty();\n    }\n\n    public boolean isSpecificallyAcceptedAndNotRejected(final String str) {\n        return !acceptIsEmpty() && isAcceptedAndNotRejected(str);\n    }\n\n    public boolean isSpecificallyAccepted(final String str) {\n        return !acceptIsEmpty() && isAccepted(str);\n    }\n\n    public void sortPrefixes() {\n        if (acceptPrefixesSet != null) {\n            acceptPrefixes = new ArrayList<>(acceptPrefixesSet);\n        }\n        if (acceptPrefixes != null) {\n            CollectionUtils.sortIfNotEmpty(acceptPrefixes);\n        }\n        if (rejectPrefixes != null) {\n            CollectionUtils.sortIfNotEmpty(rejectPrefixes);\n        }\n    }\n\n    @Override\n    public String toString() {\n        final StringBuilder buf = new StringBuilder();\n        if (accept != null) {\n            buf.append(\"accept: \");\n            AcceptRejectUtils.quoteList(accept, buf);\n        }\n        if (acceptPrefixes != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"acceptPrefixes: \");\n            AcceptRejectUtils.quoteList(acceptPrefixes, buf);\n        }\n        if (acceptGlobs != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"acceptGlobs: \");\n            AcceptRejectUtils.quoteList(acceptGlobs, buf);\n        }\n        if (reject != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"reject: \");\n            AcceptRejectUtils.quoteList(reject, buf);\n        }\n        if (rejectPrefixes != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"rejectPrefixes: \");\n            AcceptRejectUtils.quoteList(rejectPrefixes, buf);\n        }\n        if (rejectGlobs != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"rejectGlobs: \");\n            AcceptRejectUtils.quoteList(rejectGlobs, buf);\n        }\n        return buf.toString();\n    }\n}\n"
}

## OUTPUT

The expected output format and contraints for that output are presented below.

{
  "smell_type": "Insufficient Modularization",
  "target_level": "class",
  "target": "<class FQN from input>",
  "blocks": [
    {
      "id": 1,
      "goal": "...",
      "files": ["..."],
      "ops": [
        {
          "op": "<allowed op>",
          "inputs": ["..."],
          "outputs": ["..."],
          "details": "...",
          "risk": "low|medium|high"
        }
      ]
    }
  ]
}

Contraints:
- Reference only packages, classes, methods, and fields present in the input.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.