## CONTEXT

A plan was developed to refactor a target that suffers from a specific type of code smell. The plan consists of blocks, each of which is formed by a list of refactoring operations. The blocks were designed to perform the refactoring in steps, such that after the execution of each block, it will have a compilable sub-solution with functional tests. For this, both the source code mentioned in the plan and the related tests may need to be rewritten.

## TASK

Apply the staged refactoring block to the provided Java source files.

Preserving behavior does not require preserving the original target-class API when the plan explicitly moves methods or responsibilities to another class.

## CONSTRAINTS

- Modify only files listed in allowed_files field.
- Return the full new content for every modified file.
- Do not return partial patches.
- Do not edit unrelated tests.
- Do not change unrelated code.
- Do not undo previous refactorings.
- If the block cannot be safely applied, return an empty files_to_write list and explain the reason in "notes".
- Return only files that actually changed.
- Do not include unchanged files in files_to_write.
- Implement the refactoring operations requested in the current block. Do not replace the requested refactoring with a more conservative alternative.

## INPUT PLAN

{
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/classgraph/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "io.github.classgraph.base.internal.utils.AcceptReject"
  },
  "block": {
    "id": 1,
    "goal": "Extract accept/reject criteria state management and related concrete behavior from the abstract API class, reducing its field count and implementation complexity while preserving the existing abstract matching contract and compatibility methods.",
    "files": [
      "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptReject.java",
      "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptRejectCriteria.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "io.github.classgraph.base.internal.utils.AcceptReject",
          "io.github.classgraph.base.internal.utils.AcceptRejectCriteria"
        ],
        "outputs": [
          "io.github.classgraph.base.internal.utils.AcceptRejectCriteria"
        ],
        "details": "Extract the cohesive accept/reject state and concrete behavior represented by accept, reject, acceptPrefixesSet, acceptPrefixes, rejectPrefixes, acceptGlobs, rejectGlobs, acceptPatterns, acceptPrefixPatterns, rejectPatterns, acceptIsEmpty(), rejectIsEmpty(), acceptAndRejectAreEmpty(), isSpecificallyAcceptedAndNotRejected(String), isSpecificallyAccepted(String), sortPrefixes(), and toString(). Keep the abstract methods addToAccept(String), addToReject(String), isAcceptedAndNotRejected(String), isAccepted(String), acceptHasPrefix(String), and isRejected(String) in AcceptReject. Preserve the existing protected state access required by the existing AcceptRejectPrefix, AcceptRejectWholeString, and AcceptRejectLeafname implementations through the extraction-generated delegation or protected access bridge, so those classes continue to compile.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptReject.java",
    "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptRejectCriteria.java"
  ],
  "executor_existing_files": [
    "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptReject.java"
  ],
  "executor_new_files": [
    "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptRejectCriteria.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptReject.java",
      "exists": "true",
      "content": "/*\n * This file is part of ClassGraph.\n *\n * The MIT License (MIT)\n */\npackage io.github.classgraph.base.internal.utils;\n\nimport java.util.ArrayList;\nimport java.util.Collection;\nimport java.util.List;\nimport java.util.Set;\nimport java.util.regex.Pattern;\n\nimport org.jspecify.annotations.Nullable;\n\n/** A class storing accept or reject criteria. */\npublic abstract class AcceptReject {\n    protected @Nullable Set<String> accept;\n    protected @Nullable Set<String> reject;\n    protected @Nullable Set<String> acceptPrefixesSet;\n    protected @Nullable List<String> acceptPrefixes;\n    protected @Nullable List<String> rejectPrefixes;\n    protected @Nullable Set<String> acceptGlobs;\n    protected @Nullable Set<String> rejectGlobs;\n    protected @Nullable List<Pattern> acceptPatterns;\n    protected @Nullable List<Pattern> acceptPrefixPatterns;\n    protected @Nullable List<Pattern> rejectPatterns;\n    protected char separatorChar;\n\n    protected AcceptReject(final char separatorChar) {\n        this.separatorChar = separatorChar;\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static Pattern globToPattern(final String glob, final char separatorChar, final boolean prefixMatch) {\n        return AcceptRejectUtils.globToPattern(glob, separatorChar, prefixMatch);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String stripTrailingDoubleGlob(final String packageOrPath, final char separatorChar) {\n        return AcceptRejectUtils.stripTrailingDoubleGlob(packageOrPath, separatorChar);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static boolean containsWildcard(final String str) {\n        return AcceptRejectUtils.containsWildcard(str);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String normalizePath(final String path) {\n        return AcceptRejectUtils.normalizePath(path);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String normalizePackageOrClassName(final String packageOrClassName) {\n        return AcceptRejectUtils.normalizePackageOrClassName(packageOrClassName);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String pathToPackageName(final String path) {\n        return AcceptRejectUtils.pathToPackageName(path);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String packageNameToPath(final String packageName) {\n        return AcceptRejectUtils.packageNameToPath(packageName);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static String classNameToClassfilePath(final String className) {\n        return AcceptRejectUtils.classNameToClassfilePath(className);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static boolean matchesPatternList(final String str, final @Nullable List<Pattern> patterns) {\n        return AcceptRejectUtils.matchesPatternList(str, patterns);\n    }\n\n    /** Compatibility delegation for callers that still reference the pre-extraction API. */\n    public static void quoteList(final Collection<String> coll, final StringBuilder buf) {\n        AcceptRejectUtils.quoteList(coll, buf);\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectPrefix extends io.github.classgraph.base.internal.utils.AcceptRejectPrefix {\n        public AcceptRejectPrefix(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectWholeString\n            extends io.github.classgraph.base.internal.utils.AcceptRejectWholeString {\n        public AcceptRejectWholeString(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    /** Compatibility adapter for the extracted top-level implementation. */\n    public static class AcceptRejectLeafname extends io.github.classgraph.base.internal.utils.AcceptRejectLeafname {\n        public AcceptRejectLeafname(final char separatorChar) {\n            super(separatorChar);\n        }\n    }\n\n    public abstract void addToAccept(String str);\n\n    public abstract void addToReject(String str);\n\n    public abstract boolean isAcceptedAndNotRejected(String str);\n\n    public abstract boolean isAccepted(String str);\n\n    public abstract boolean acceptHasPrefix(String str);\n\n    public abstract boolean isRejected(String str);\n\n    public boolean acceptIsEmpty() {\n        return accept == null && acceptPrefixes == null && acceptPrefixesSet == null && acceptGlobs == null;\n    }\n\n    public boolean rejectIsEmpty() {\n        return reject == null && rejectPrefixes == null && rejectGlobs == null;\n    }\n\n    public boolean acceptAndRejectAreEmpty() {\n        return acceptIsEmpty() && rejectIsEmpty();\n    }\n\n    public boolean isSpecificallyAcceptedAndNotRejected(final String str) {\n        return !acceptIsEmpty() && isAcceptedAndNotRejected(str);\n    }\n\n    public boolean isSpecificallyAccepted(final String str) {\n        return !acceptIsEmpty() && isAccepted(str);\n    }\n\n    public void sortPrefixes() {\n        if (acceptPrefixesSet != null) {\n            acceptPrefixes = new ArrayList<>(acceptPrefixesSet);\n        }\n        if (acceptPrefixes != null) {\n            CollectionUtils.sortIfNotEmpty(acceptPrefixes);\n        }\n        if (rejectPrefixes != null) {\n            CollectionUtils.sortIfNotEmpty(rejectPrefixes);\n        }\n    }\n\n    @Override\n    public String toString() {\n        final StringBuilder buf = new StringBuilder();\n        if (accept != null) {\n            buf.append(\"accept: \");\n            AcceptRejectUtils.quoteList(accept, buf);\n        }\n        if (acceptPrefixes != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"acceptPrefixes: \");\n            AcceptRejectUtils.quoteList(acceptPrefixes, buf);\n        }\n        if (acceptGlobs != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"acceptGlobs: \");\n            AcceptRejectUtils.quoteList(acceptGlobs, buf);\n        }\n        if (reject != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"reject: \");\n            AcceptRejectUtils.quoteList(reject, buf);\n        }\n        if (rejectPrefixes != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"rejectPrefixes: \");\n            AcceptRejectUtils.quoteList(rejectPrefixes, buf);\n        }\n        if (rejectGlobs != null) {\n            if (!buf.isEmpty())\n                buf.append(\"; \");\n            buf.append(\"rejectGlobs: \");\n            AcceptRejectUtils.quoteList(rejectGlobs, buf);\n        }\n        return buf.toString();\n    }\n}\n"
    },
    {
      "path": "classgraph-base/src/main/java/io/github/classgraph/base/internal/utils/AcceptRejectCriteria.java",
      "exists": "false",
      "content": ""
    }
  ],
  "feedback": "EXECUTOR_INVALID_JSON: Illegal trailing comma before end of object: line 5 column 4365 (char 4500)",
  "attempt": 1,
  "move_class_constraints": {
    "moved_old_files": [],
    "moved_new_files": [],
    "rule": "When MOVE_CLASS is present, OpenRewrite has already moved the classes before this executor runs. Do not recreate or write files listed in moved_old_files. Edit destination files and related remaining files only."
  }
}

## OUTPUT

Return ONLY valid JSON in this format:

{
  "files_to_write": [
    {
      "path": "src/main/java/..." or "src/test/java/...",
      "content": "full file content here"
    }
  ],
  "files_to_delete": [],
  "notes": "short explanation"
}
