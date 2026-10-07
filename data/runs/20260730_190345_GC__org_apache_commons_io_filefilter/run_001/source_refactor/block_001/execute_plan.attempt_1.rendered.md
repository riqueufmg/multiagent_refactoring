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
  "repo_path": "/data/henrique/multiagent_refactoring/data/repositories/commons-io",
  "target": {
    "smell": "GC",
    "smell_name": "God Component",
    "target_type": "package",
    "target_name": "org.apache.commons.io.filefilter"
  },
  "block": {
    "id": 1,
    "goal": "Move the name-based file filter cluster (NameFileFilter, PrefixFileFilter, SuffixFileFilter) into a dedicated subpackage to reduce the god component size.",
    "files": [
      "src/main/java/org/apache/commons/io/filefilter/NameFileFilter.java",
      "src/main/java/org/apache/commons/io/filefilter/PrefixFileFilter.java",
      "src/main/java/org/apache/commons/io/filefilter/SuffixFileFilter.java",
      "src/main/java/org/apache/commons/io/filefilter/name/NameFileFilter.java",
      "src/main/java/org/apache/commons/io/filefilter/name/PrefixFileFilter.java",
      "src/main/java/org/apache/commons/io/filefilter/name/SuffixFileFilter.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.apache.commons.io.filefilter.name"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.filefilter.NameFileFilter"
        ],
        "outputs": [
          "org.apache.commons.io.filefilter.name.NameFileFilter"
        ],
        "details": "Move NameFileFilter to the name subpackage.",
        "risk": "low",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.filefilter.PrefixFileFilter"
        ],
        "outputs": [
          "org.apache.commons.io.filefilter.name.PrefixFileFilter"
        ],
        "details": "Move PrefixFileFilter to the name subpackage.",
        "risk": "low",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.filefilter.SuffixFileFilter"
        ],
        "outputs": [
          "org.apache.commons.io.filefilter.name.SuffixFileFilter"
        ],
        "details": "Move SuffixFileFilter to the name subpackage.",
        "risk": "low",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.apache.commons.io.filefilter.name.NameFileFilter",
          "org.apache.commons.io.filefilter.name.PrefixFileFilter",
          "org.apache.commons.io.filefilter.name.SuffixFileFilter"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/io/filefilter/NameFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/PrefixFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/SuffixFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/name/NameFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/name/PrefixFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/name/SuffixFileFilter.java"
  ],
  "executor_existing_files": [
    "src/main/java/org/apache/commons/io/filefilter/NameFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/PrefixFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/SuffixFileFilter.java"
  ],
  "executor_new_files": [
    "src/main/java/org/apache/commons/io/filefilter/name/NameFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/name/PrefixFileFilter.java",
    "src/main/java/org/apache/commons/io/filefilter/name/SuffixFileFilter.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/NameFileFilter.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/PrefixFileFilter.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/SuffixFileFilter.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/name/NameFileFilter.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.apache.commons.io.filefilter.name;\n\nimport java.io.File;\nimport java.io.Serializable;\nimport java.nio.file.FileVisitResult;\nimport java.nio.file.Path;\nimport java.nio.file.attribute.BasicFileAttributes;\nimport java.util.List;\nimport java.util.Objects;\nimport java.util.stream.Stream;\n\nimport org.apache.commons.io.IOCase;\nimport org.apache.commons.io.file.PathUtils;\n\n/**\n * Filters file names for a certain name.\n * <p>\n * For example, to print all files and directories in the\n * current directory whose name is {@code Test}:\n * </p>\n * <h2>Using Classic IO</h2>\n * <pre>\n * File dir = FileUtils.current();\n * String[] files = dir.list(new NameFileFilter(\"Test\"));\n * for (String file : files) {\n *     System.out.println(file);\n * }\n * </pre>\n *\n * <h2>Using NIO</h2>\n * <pre>\n * final Path dir = PathUtils.current();\n * final AccumulatorPathVisitor visitor = AccumulatorPathVisitor.withLongCounters(new NameFileFilter(\"Test\"));\n * //\n * // Walk one directory\n * Files.<strong>walkFileTree</strong>(dir, Collections.emptySet(), 1, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getFileList());\n * //\n * visitor.getPathCounters().reset();\n * //\n * // Walk directory tree\n * Files.<strong>walkFileTree</strong>(dir, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getDirList());\n * System.out.println(visitor.getFileList());\n * </pre>\n * <h2>Deprecating Serialization</h2>\n * <p>\n * <em>Serialization is deprecated and will be removed in 3.0.</em>\n * </p>\n *\n * @since 1.0\n * @see FileFilterUtils#nameFileFilter(String)\n * @see FileFilterUtils#nameFileFilter(String, IOCase)\n */\npublic class NameFileFilter extends AbstractFileFilter implements Serializable {\n\n    private static final long serialVersionUID = 176844364689077340L;\n\n    /** The file names to search for */\n    private final String[] names;\n\n    /** Whether the comparison is case-sensitive. */\n    private final IOCase ioCase;\n\n    /**\n     * Constructs a new case-sensitive name file filter for a list of names.\n     *\n     * @param names  The names to allow, must not be null.\n     * @throws IllegalArgumentException if the name list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     */\n    public NameFileFilter(final List<String> names) {\n        this(names, null);\n    }\n\n    /**\n     * Constructs a new name file filter for a list of names specifying case-sensitivity.\n     *\n     * @param names  The names to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the name list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     */\n    public NameFileFilter(final List<String> names, final IOCase ioCase) {\n        Objects.requireNonNull(names, \"names\");\n        this.names = names.toArray(EMPTY_STRING_ARRAY);\n        this.ioCase = toIOCase(ioCase);\n    }\n\n    /**\n     * Constructs a new case-sensitive name file filter for a single name.\n     *\n     * @param name  The name to allow, must not be null.\n     * @throws IllegalArgumentException if the name is null.\n     */\n    public NameFileFilter(final String name) {\n        this(name, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new case-sensitive name file filter for an array of names.\n     * <p>\n     * The array is not cloned, so could be changed after constructing the\n     * instance. This would be inadvisable however.\n     * </p>\n     *\n     * @param names  The names to allow, must not be null.\n     * @throws IllegalArgumentException if the names array is null.\n     */\n    public NameFileFilter(final String... names) {\n        this(names, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new name file filter specifying case-sensitivity.\n     *\n     * @param name  The name to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the name is null.\n     */\n    public NameFileFilter(final String name, final IOCase ioCase) {\n        Objects.requireNonNull(name, \"name\");\n        this.names = new String[] {name};\n        this.ioCase = toIOCase(ioCase);\n    }\n\n    /**\n     * Constructs a new name file filter for an array of names specifying case-sensitivity.\n     *\n     * @param names  The names to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the names array is null.\n     */\n    public NameFileFilter(final String[] names, final IOCase ioCase) {\n        Objects.requireNonNull(names, \"names\");\n        this.names = names.clone();\n        this.ioCase = toIOCase(ioCase);\n    }\n\n    /**\n     * Tests to see if the file name matches.\n     *\n     * @param file  The File to check.\n     * @return true if the file name matches.\n     */\n    @Override\n    public boolean accept(final File file) {\n        return file != null && acceptBaseName(file.getName());\n    }\n\n    /**\n     * Tests to see if the file name matches.\n     *\n     * @param dir  The File directory (ignored).\n     * @param name  The file name.\n     * @return true if the file name matches.\n     */\n    @Override\n    public boolean accept(final File dir, final String name) {\n        return acceptBaseName(name);\n    }\n\n    /**\n     * Checks to see if the file name matches.\n     *\n     * @param path  The File to check.\n     * @param attributes The path's basic attributes (may be null).\n     * @return true if the file name matches.\n     * @since 2.9.0\n     */\n    @Override\n    public FileVisitResult accept(final Path path, final BasicFileAttributes attributes) {\n        return toFileVisitResult(acceptBaseName(PathUtils.getFileNameString(path)));\n    }\n\n    private boolean acceptBaseName(final String baseName) {\n        return Stream.of(names).anyMatch(testName -> ioCase.checkEquals(baseName, testName));\n    }\n\n    private IOCase toIOCase(final IOCase ioCase) {\n        return IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Provide a String representation of this file filter.\n     *\n     * @return A String representation.\n     */\n    @Override\n    public String toString() {\n        final StringBuilder buffer = new StringBuilder();\n        buffer.append(super.toString());\n        buffer.append(\"(\");\n        append(names, buffer);\n        buffer.append(\")\");\n        return buffer.toString();\n    }\n\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/name/PrefixFileFilter.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.apache.commons.io.filefilter.name;\n\nimport java.io.File;\nimport java.io.Serializable;\nimport java.nio.file.FileVisitResult;\nimport java.nio.file.Path;\nimport java.nio.file.attribute.BasicFileAttributes;\nimport java.util.List;\nimport java.util.Objects;\nimport java.util.stream.Stream;\n\nimport org.apache.commons.io.IOCase;\nimport org.apache.commons.io.file.PathUtils;\n\n/**\n * Filters file names for a certain prefix.\n * <p>\n * For example, to print all files and directories in the\n * current directory whose name starts with {@code Test}:\n * </p>\n * <h2>Using Classic IO</h2>\n * <pre>\n * File dir = FileUtils.current();\n * String[] files = dir.list(new PrefixFileFilter(\"Test\"));\n * for (String file : files) {\n *     System.out.println(file);\n * }\n * </pre>\n *\n * <h2>Using NIO</h2>\n * <pre>\n * final Path dir = PathUtils.current();\n * final AccumulatorPathVisitor visitor = AccumulatorPathVisitor.withLongCounters(new PrefixFileFilter(\"Test\"));\n * //\n * // Walk one directory\n * Files.<strong>walkFileTree</strong>(dir, Collections.emptySet(), 1, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getFileList());\n * //\n * visitor.getPathCounters().reset();\n * //\n * // Walk directory tree\n * Files.<strong>walkFileTree</strong>(dir, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getDirList());\n * System.out.println(visitor.getFileList());\n * </pre>\n * <h2>Deprecating Serialization</h2>\n * <p>\n * <em>Serialization is deprecated and will be removed in 3.0.</em>\n * </p>\n *\n * @since 1.0\n * @see FileFilterUtils#prefixFileFilter(String)\n * @see FileFilterUtils#prefixFileFilter(String, IOCase)\n */\npublic class PrefixFileFilter extends AbstractFileFilter implements Serializable {\n\n    private static final long serialVersionUID = 8533897440809599867L;\n\n    /** The file name prefixes to search for */\n    private final String[] prefixes;\n\n    /** Whether the comparison is case-sensitive. */\n    private final IOCase isCase;\n\n    /**\n     * Constructs a new Prefix file filter for a list of prefixes.\n     *\n     * @param prefixes  The prefixes to allow, must not be null.\n     * @throws NullPointerException if the prefix list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     */\n    public PrefixFileFilter(final List<String> prefixes) {\n        this(prefixes, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Prefix file filter for a list of prefixes\n     * specifying case-sensitivity.\n     *\n     * @param prefixes  The prefixes to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the prefix list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     * @since 1.4\n     */\n    public PrefixFileFilter(final List<String> prefixes, final IOCase ioCase) {\n        Objects.requireNonNull(prefixes, \"prefixes\");\n        this.prefixes = prefixes.toArray(EMPTY_STRING_ARRAY);\n        this.isCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Prefix file filter for a single prefix.\n     *\n     * @param prefix  The prefix to allow, must not be null.\n     * @throws IllegalArgumentException if the prefix is null.\n     */\n    public PrefixFileFilter(final String prefix) {\n        this(prefix, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Prefix file filter for any of an array of prefixes.\n     * <p>\n     * The array is not cloned, so could be changed after constructing the\n     * instance. This would be inadvisable however.\n     * </p>\n     *\n     * @param prefixes  The prefixes to allow, must not be null.\n     * @throws IllegalArgumentException if the prefix array is null.\n     */\n    public PrefixFileFilter(final String... prefixes) {\n        this(prefixes, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Prefix file filter for a single prefix\n     * specifying case-sensitivity.\n     *\n     * @param prefix  The prefix to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws IllegalArgumentException if the prefix is null.\n     * @since 1.4\n     */\n    public PrefixFileFilter(final String prefix, final IOCase ioCase) {\n        Objects.requireNonNull(prefix, \"prefix\");\n        this.prefixes = new String[] {prefix};\n        this.isCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Prefix file filter for any of an array of prefixes\n     * specifying case-sensitivity.\n     *\n     * @param prefixes  The prefixes to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws IllegalArgumentException if the prefix is null.\n     * @since 1.4\n     */\n    public PrefixFileFilter(final String[] prefixes, final IOCase ioCase) {\n        Objects.requireNonNull(prefixes, \"prefixes\");\n        this.prefixes = prefixes.clone();\n        this.isCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Tests to see if the file name starts with the prefix.\n     *\n     * @param file  The File to check.\n     * @return true if the file name starts with one of our prefixes.\n     */\n    @Override\n    public boolean accept(final File file) {\n        return accept(file == null ? null : file.getName());\n    }\n\n    /**\n     * Tests to see if the file name starts with the prefix.\n     *\n     * @param file  The File directory.\n     * @param name  The file name.\n     * @return true if the file name starts with one of our prefixes.\n     */\n    @Override\n    public boolean accept(final File file, final String name) {\n        return accept(name);\n    }\n\n    /**\n     * Tests to see if the file name starts with the prefix.\n     *\n     * @param file  The File to check.\n     * @param attributes The path's basic attributes (may be null).\n     * @return true if the file name starts with one of our prefixes.\n     * @since 2.9.0\n     */\n    @Override\n    public FileVisitResult accept(final Path file, final BasicFileAttributes attributes) {\n        return toFileVisitResult(accept(PathUtils.getFileName(file, Path::toFile)));\n    }\n\n    private boolean accept(final String name) {\n        return Stream.of(prefixes).anyMatch(prefix -> isCase.checkStartsWith(name, prefix));\n    }\n\n    /**\n     * Provides a String representation of this file filter.\n     *\n     * @return A String representation.\n     */\n    @Override\n    public String toString() {\n        final StringBuilder buffer = new StringBuilder();\n        buffer.append(super.toString());\n        buffer.append(\"(\");\n        append(prefixes, buffer);\n        buffer.append(\")\");\n        return buffer.toString();\n    }\n\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/filefilter/name/SuffixFileFilter.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.apache.commons.io.filefilter.name;\n\nimport java.io.File;\nimport java.io.Serializable;\nimport java.nio.file.FileVisitResult;\nimport java.nio.file.Path;\nimport java.nio.file.attribute.BasicFileAttributes;\nimport java.util.List;\nimport java.util.Objects;\nimport java.util.stream.Stream;\n\nimport org.apache.commons.io.IOCase;\nimport org.apache.commons.io.file.PathUtils;\n\n/**\n * Filters files based on the suffix (what the file name ends with).\n * This is used in retrieving all the files of a particular type.\n * <p>\n * For example, to retrieve and print all {@code *.java} files\n * in the current directory:\n * </p>\n * <h2>Using Classic IO</h2>\n * <pre>\n * File dir = FileUtils.current();\n * String[] files = dir.list(new SuffixFileFilter(\".java\"));\n * for (String file : files) {\n *     System.out.println(file);\n * }\n * </pre>\n *\n * <h2>Using NIO</h2>\n * <pre>\n * final Path dir = PathUtils.current();\n * final AccumulatorPathVisitor visitor = AccumulatorPathVisitor.withLongCounters(new SuffixFileFilter(\".java\"));\n * //\n * // Walk one directory\n * Files.<strong>walkFileTree</strong>(dir, Collections.emptySet(), 1, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getFileList());\n * //\n * visitor.getPathCounters().reset();\n * //\n * // Walk directory tree\n * Files.<strong>walkFileTree</strong>(dir, visitor);\n * System.out.println(visitor.getPathCounters());\n * System.out.println(visitor.getDirList());\n * System.out.println(visitor.getFileList());\n * </pre>\n * <h2>Deprecating Serialization</h2>\n * <p>\n * <em>Serialization is deprecated and will be removed in 3.0.</em>\n * </p>\n *\n * @since 1.0\n * @see FileFilterUtils#suffixFileFilter(String)\n * @see FileFilterUtils#suffixFileFilter(String, IOCase)\n */\npublic class SuffixFileFilter extends AbstractFileFilter implements Serializable {\n\n    private static final long serialVersionUID = -3389157631240246157L;\n\n    /** The file name suffixes to search for */\n    private final String[] suffixes;\n\n    /** Whether the comparison is case-sensitive. */\n    private final IOCase ioCase;\n\n    /**\n     * Constructs a new Suffix file filter for a list of suffixes.\n     *\n     * @param suffixes  The suffixes to allow, must not be null.\n     * @throws IllegalArgumentException if the suffix list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     */\n    public SuffixFileFilter(final List<String> suffixes) {\n        this(suffixes, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Suffix file filter for a list of suffixes\n     * specifying case-sensitivity.\n     *\n     * @param suffixes  The suffixes to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws IllegalArgumentException if the suffix list is null.\n     * @throws ClassCastException if the list does not contain Strings.\n     * @since 1.4\n     */\n    public SuffixFileFilter(final List<String> suffixes, final IOCase ioCase) {\n        Objects.requireNonNull(suffixes, \"suffixes\");\n        this.suffixes = suffixes.toArray(EMPTY_STRING_ARRAY);\n        this.ioCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Suffix file filter for a single extension.\n     *\n     * @param suffix  The suffix to allow, must not be null.\n     * @throws IllegalArgumentException if the suffix is null.\n     */\n    public SuffixFileFilter(final String suffix) {\n        this(suffix, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Suffix file filter for an array of suffixes.\n     * <p>\n     * The array is not cloned, so could be changed after constructing the\n     * instance. This would be inadvisable however.\n     * </p>\n     *\n     * @param suffixes  The suffixes to allow, must not be null.\n     * @throws NullPointerException if the suffix array is null.\n     */\n    public SuffixFileFilter(final String... suffixes) {\n        this(suffixes, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Suffix file filter for a single extension\n     * specifying case-sensitivity.\n     *\n     * @param suffix  The suffix to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the suffix is null.\n     * @since 1.4\n     */\n    public SuffixFileFilter(final String suffix, final IOCase ioCase) {\n        Objects.requireNonNull(suffix, \"suffix\");\n        this.suffixes = new String[] {suffix};\n        this.ioCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Constructs a new Suffix file filter for an array of suffixes\n     * specifying case-sensitivity.\n     *\n     * @param suffixes  The suffixes to allow, must not be null.\n     * @param ioCase  how to handle case sensitivity, null means case-sensitive.\n     * @throws NullPointerException if the suffix array is null.\n     * @since 1.4\n     */\n    public SuffixFileFilter(final String[] suffixes, final IOCase ioCase) {\n        Objects.requireNonNull(suffixes, \"suffixes\");\n        this.suffixes = suffixes.clone();\n        this.ioCase = IOCase.value(ioCase, IOCase.SENSITIVE);\n    }\n\n    /**\n     * Tests to see if the file name ends with the suffix.\n     *\n     * @param file  The File to check.\n     * @return true if the file name ends with one of our suffixes.\n     */\n    @Override\n    public boolean accept(final File file) {\n        return accept(file.getName());\n    }\n\n    /**\n     * Tests to see if the file name ends with the suffix.\n     *\n     * @param file  The File directory.\n     * @param name  The file name.\n     * @return true if the file name ends with one of our suffixes.\n     */\n    @Override\n    public boolean accept(final File file, final String name) {\n        return accept(name);\n    }\n\n    /**\n     * Tests to see if the file name ends with the suffix.\n     *\n     * @param path       The File to check.\n     * @param attributes The path's basic attributes (may be null).\n     * @return true if the file name ends with one of our suffixes.\n     * @since 2.9.0\n     */\n    @Override\n    public FileVisitResult accept(final Path path, final BasicFileAttributes attributes) {\n        return toFileVisitResult(accept(PathUtils.getFileNameString(path)));\n    }\n\n    private boolean accept(final String name) {\n        return Stream.of(suffixes).anyMatch(suffix -> ioCase.checkEndsWith(name, suffix));\n    }\n\n    /**\n     * Provides a String representation of this file filter.\n     *\n     * @return A String representation.\n     */\n    @Override\n    public String toString() {\n        final StringBuilder buffer = new StringBuilder();\n        buffer.append(super.toString());\n        buffer.append(\"(\");\n        append(suffixes, buffer);\n        buffer.append(\")\");\n        return buffer.toString();\n    }\n\n}\n"
    }
  ],
  "feedback": "EXECUTOR_NO_CHANGES: The executor returned valid JSON, but produced no files_to_write or files_to_delete. Revise the same block and generate concrete file changes.",
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
