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
  "target_name": "org.apache.commons.io.channels.FilterFileChannel",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260625_130415_IM__org_apache_commons_io_channels_FilterFileChannel/run_001/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "src/main/java/org/apache/commons/io/channels/FilterFileChannel.java",
  "target_source_root": "src/main/java",
  "target_code": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels;\n\nimport java.io.IOException;\nimport java.nio.ByteBuffer;\nimport java.nio.MappedByteBuffer;\nimport java.nio.channels.Channel;\nimport java.nio.channels.FileChannel;\nimport java.nio.channels.FileLock;\nimport java.nio.channels.ReadableByteChannel;\nimport java.nio.channels.WritableByteChannel;\nimport java.util.Objects;\n\nimport org.apache.commons.io.build.AbstractStreamBuilder;\n\n/**\n * Filters a {@link FileChannel}.\n * <p>\n * A {@code FilterFileChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or providing\n * additional functionality. The class {@code FilterFileChannel} itself simply overrides methods of {@code FileChannel} with versions that pass all requests to\n * the wrapped channel. Subclasses of {@code FilterFileChannel} may of course override any methods declared or inherited by {@code FilterFileChannel}, and may\n * also provide additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterFileChannel#FilterFileChannel(FileChannel) channel constructor} and more advanced instances through the\n * {@link Builder}.\n * </p>\n *\n * @since 2.22.0\n */\npublic class FilterFileChannel extends FileChannel {\n\n    /**\n     * Builds instances of {@link FilterFileChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterFileChannel} type.\n     * @param <C> The {@link Channel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterFileChannel, C extends FileChannel, B extends AbstractBuilder<F, C, B>>\n            extends AbstractStreamBuilder<F, AbstractBuilder<F, C, B>> {\n\n        /**\n         * Constructs instance for subclasses.\n         */\n        protected AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterFileChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterFileChannel, FileChannel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterFileChannel get() throws IOException {\n            return new FilterFileChannel(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forFilterFileChannel() {\n        return new Builder();\n    }\n\n    final FileChannel fileChannel;\n\n    private FilterFileChannel(final Builder builder) throws IOException {\n        this.fileChannel = builder.getChannel(FileChannel.class);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param fileChannel the file channel to wrap.\n     */\n    public FilterFileChannel(final FileChannel fileChannel) {\n        this.fileChannel = Objects.requireNonNull(fileChannel, \"fileChannel\");\n    }\n\n    @Override\n    public boolean equals(final Object o) {\n        return fileChannel.equals(o);\n    }\n\n    @Override\n    public void force(final boolean metaData) throws IOException {\n        fileChannel.force(metaData);\n    }\n\n    @Override\n    public int hashCode() {\n        return fileChannel.hashCode();\n    }\n\n    @Override\n    protected void implCloseChannel() throws IOException {\n        fileChannel.close();\n    }\n\n    @Override\n    public FileLock lock(final long position, final long size, final boolean shared) throws IOException {\n        return fileChannel.lock(position, size, shared);\n    }\n\n    @Override\n    public MappedByteBuffer map(final MapMode mode, final long position, final long size) throws IOException {\n        return fileChannel.map(mode, position, size);\n    }\n\n    @Override\n    public long position() throws IOException {\n        return fileChannel.position();\n    }\n\n    @Override\n    public FileChannel position(final long newPosition) throws IOException {\n        return fileChannel.position(newPosition);\n    }\n\n    @Override\n    public int read(final ByteBuffer dst) throws IOException {\n        return fileChannel.read(dst);\n    }\n\n    @Override\n    public int read(final ByteBuffer dst, final long position) throws IOException {\n        return fileChannel.read(dst, position);\n    }\n\n    @Override\n    public long read(final ByteBuffer[] dsts, final int offset, final int length) throws IOException {\n        return fileChannel.read(dsts, offset, length);\n    }\n\n    @Override\n    public long size() throws IOException {\n        return fileChannel.size();\n    }\n\n    @Override\n    public String toString() {\n        return fileChannel.toString();\n    }\n\n    @Override\n    public long transferFrom(final ReadableByteChannel src, final long position, final long count) throws IOException {\n        return fileChannel.transferFrom(src, position, count);\n    }\n\n    @Override\n    public long transferTo(final long position, final long count, final WritableByteChannel target) throws IOException {\n        return fileChannel.transferTo(position, count, target);\n    }\n\n    @Override\n    public FileChannel truncate(final long size) throws IOException {\n        return fileChannel.truncate(size);\n    }\n\n    @Override\n    public FileLock tryLock(final long position, final long size, final boolean shared) throws IOException {\n        return fileChannel.tryLock(position, size, shared);\n    }\n\n    /**\n     * Unwraps this instance by returning the underlying {@link FileChannel}.\n     * <p>\n     * Use with caution.\n     * </p>\n     *\n     * @return the underlying {@link FileChannel}.\n     */\n    public FileChannel unwrap() {\n        return fileChannel;\n    }\n\n    @Override\n    public int write(final ByteBuffer src) throws IOException {\n        return fileChannel.write(src);\n    }\n\n    @Override\n    public int write(final ByteBuffer src, final long position) throws IOException {\n        return fileChannel.write(src, position);\n    }\n\n    @Override\n    public long write(final ByteBuffer[] srcs, final int offset, final int length) throws IOException {\n        return fileChannel.write(srcs, offset, length);\n    }\n}\n"
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