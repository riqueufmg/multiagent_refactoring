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
- ADD_OR_UPDATE_IMPORTS
- CREATE_PACKAGE
- DEPENDENCY_INVERSION
- EXTRACT_CLASS
- EXTRACT_INTERFACE
- INTRODUCE_FACADE
- MOVE_CLASS
- MOVE_FIELD
- MOVE_METHOD
- REPLACE_DEPENDENCY
- UPDATE_CALL_SITES

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "org.apache.commons.io.monitor.FileEntry",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260625_120517_IM__org_apache_commons_io_monitor_FileEntry/run_001/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "src/main/java/org/apache/commons/io/monitor/FileEntry.java",
  "target_source_root": "src/main/java",
  "target_code": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.apache.commons.io.monitor;\n\nimport java.io.File;\nimport java.io.IOException;\nimport java.io.Serializable;\nimport java.nio.file.Files;\nimport java.nio.file.attribute.FileTime;\nimport java.util.Objects;\n\nimport org.apache.commons.io.FileUtils;\nimport org.apache.commons.io.file.attribute.FileTimes;\n\n/**\n * The state of a file or directory, capturing the following {@link File} attributes at a point in time.\n * <ul>\n *   <li>File Name (see {@link File#getName()})</li>\n *   <li>Exists - whether the file exists or not (see {@link File#exists()})</li>\n *   <li>Directory - whether the file is a directory or not (see {@link File#isDirectory()})</li>\n *   <li>Last Modified Date/Time (see {@link FileUtils#lastModifiedUnchecked(File)})</li>\n *   <li>Length (see {@link File#length()}) - directories treated as zero</li>\n *   <li>Children - contents of a directory (see {@link File#listFiles(java.io.FileFilter)})</li>\n * </ul>\n *\n * <h2>Custom Implementations</h2>\n * <p>\n * If the state of additional {@link File} attributes is required then create a custom\n * {@link FileEntry} with properties for those attributes. Override the\n * {@link #newChildInstance(File)} to return a new instance of the appropriate type.\n * You may also want to override the {@link #refresh(File)} method.\n * </p>\n * <h2>Deprecating Serialization</h2>\n * <p>\n * <em>Serialization is deprecated and will be removed in 3.0.</em>\n * </p>\n *\n * @see FileAlterationObserver\n * @since 2.0\n */\npublic class FileEntry implements Serializable {\n\n    private static final long serialVersionUID = -2505664948818681153L;\n\n    static final FileEntry[] EMPTY_FILE_ENTRY_ARRAY = {};\n\n    /** The parent. */\n    private final FileEntry parent;\n\n    /** My children. */\n    private FileEntry[] children;\n\n    /** Monitored file. */\n    private final File file;\n\n    /** Monitored file name. */\n    private String name;\n\n    /** Whether the file exists. */\n    private boolean exists;\n\n    /** Whether the file is a directory or not. */\n    private boolean directory;\n\n    /** The file's last modified timestamp. */\n    private SerializableFileTime lastModified = SerializableFileTime.EPOCH;\n\n    /** The file's length. */\n    private long length;\n\n    /**\n     * Constructs a new monitor for a specified {@link File}.\n     *\n     * @param file The file being monitored.\n     */\n    public FileEntry(final File file) {\n        this(null, file);\n    }\n\n    /**\n     * Constructs a new monitor for a specified {@link File}.\n     *\n     * @param parent The parent.\n     * @param file The file being monitored.\n     */\n    public FileEntry(final FileEntry parent, final File file) {\n        this.file = Objects.requireNonNull(file, \"file\");\n        this.parent = parent;\n        this.name = file.getName();\n    }\n\n    /**\n     * Gets the directory's files.\n     *\n     * @return This directory's files or an empty\n     * array if the file is not a directory or the\n     * directory is empty.\n     */\n    public FileEntry[] getChildren() {\n        return children != null ? children : EMPTY_FILE_ENTRY_ARRAY;\n    }\n\n    /**\n     * Gets the file being monitored.\n     *\n     * @return the file being monitored.\n     */\n    public File getFile() {\n        return file;\n    }\n\n    /**\n     * Gets the last modified time from the last time it\n     * was checked.\n     *\n     * @return the last modified time in milliseconds.\n     */\n    public long getLastModified() {\n        return lastModified.toMillis();\n    }\n\n    /**\n     * Gets the last modified time from the last time it was checked.\n     *\n     * @return the last modified time.\n     * @since 2.12.0\n     */\n    public FileTime getLastModifiedFileTime() {\n        return lastModified.unwrap();\n    }\n\n    /**\n     * Gets the length.\n     *\n     * @return the length.\n     */\n    public long getLength() {\n        return length;\n    }\n\n    /**\n     * Gets the level\n     *\n     * @return the level.\n     */\n    public int getLevel() {\n        return parent == null ? 0 : parent.getLevel() + 1;\n    }\n\n    /**\n     * Gets the file name.\n     *\n     * @return the file name.\n     */\n    public String getName() {\n        return name;\n    }\n\n    /**\n     * Gets the parent entry.\n     *\n     * @return the parent entry.\n     */\n    public FileEntry getParent() {\n        return parent;\n    }\n\n    /**\n     * Tests whether the file is a directory or not.\n     *\n     * @return whether the file is a directory or not.\n     */\n    public boolean isDirectory() {\n        return directory;\n    }\n\n    /**\n     * Tests whether the file existed the last time it\n     * was checked.\n     *\n     * @return whether the file existed.\n     */\n    public boolean isExists() {\n        return exists;\n    }\n\n    /**\n     * Constructs a new child instance.\n     * <p>\n     * Custom implementations should override this method to return\n     * a new instance of the appropriate type.\n     * </p>\n     *\n     * @param file The child file.\n     * @return a new child instance.\n     */\n    public FileEntry newChildInstance(final File file) {\n        return new FileEntry(this, file);\n    }\n\n    /**\n     * Refreshes the attributes from the {@link File}, indicating\n     * whether the file has changed.\n     * <p>\n     * This implementation refreshes the {@code name}, {@code exists},\n     * {@code directory}, {@code lastModified} and {@code length}\n     * properties.\n     * </p>\n     * <p>\n     * The {@code exists}, {@code directory}, {@code lastModified}\n     * and {@code length} properties are compared for changes\n     * </p>\n     *\n     * @param file the file instance to compare to.\n     * @return {@code true} if the file has changed, otherwise {@code false}.\n     */\n    public boolean refresh(final File file) {\n        // cache original values\n        final boolean origExists = exists;\n        final SerializableFileTime origLastModified = lastModified;\n        final boolean origDirectory = directory;\n        final long origLength = length;\n\n        // refresh the values\n        name = file.getName();\n        exists = Files.exists(file.toPath());\n        directory = exists && file.isDirectory();\n        try {\n            setLastModified(exists ? FileUtils.lastModifiedFileTime(file) : FileTimes.EPOCH);\n        } catch (final IOException e) {\n            setLastModified(SerializableFileTime.EPOCH);\n        }\n        length = exists && !directory ? file.length() : 0;\n\n        // Return if there are changes\n        return exists != origExists || !lastModified.equals(origLastModified) || directory != origDirectory\n            || length != origLength;\n    }\n\n    /**\n     * Sets the directory's files.\n     *\n     * @param children This directory's files, may be null.\n     */\n    public void setChildren(final FileEntry... children) {\n        this.children = children;\n    }\n\n    /**\n     * Sets whether the file is a directory or not.\n     *\n     * @param directory whether the file is a directory or not.\n     */\n    public void setDirectory(final boolean directory) {\n        this.directory = directory;\n    }\n\n    /**\n     * Sets whether the file existed the last time it\n     * was checked.\n     *\n     * @param exists whether the file exists or not.\n     */\n    public void setExists(final boolean exists) {\n        this.exists = exists;\n    }\n\n    /**\n     * Sets the last modified time from the last time it was checked.\n     *\n     * @param lastModified The last modified time.\n     * @since 2.12.0\n     */\n    public void setLastModified(final FileTime lastModified) {\n        setLastModified(new SerializableFileTime(lastModified));\n    }\n\n    /**\n     * Sets the last modified time from the last time it\n     * was checked.\n     *\n     * @param lastModified The last modified time in milliseconds.\n     */\n    public void setLastModified(final long lastModified) {\n        setLastModified(FileTime.fromMillis(lastModified));\n    }\n\n    void setLastModified(final SerializableFileTime lastModified) {\n        this.lastModified = lastModified;\n    }\n\n    /**\n     * Sets the length.\n     *\n     * @param length the length.\n     */\n    public void setLength(final long length) {\n        this.length = length;\n    }\n\n    /**\n     * Sets the file name.\n     *\n     * @param name the file name.\n     */\n    public void setName(final String name) {\n        this.name = name;\n    }\n}\n"
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