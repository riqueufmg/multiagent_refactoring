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
    "target_name": "org.apache.commons.io.channels"
  },
  "block": {
    "id": 1,
    "goal": "Move the cohesive FilterChannel family into a dedicated subpackage to reduce package-level complexity.",
    "files": [
      "src/main/java/org/apache/commons/io/channels/FilterByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/FilterChannel.java",
      "src/main/java/org/apache/commons/io/channels/FilterReadableByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/FilterSeekableByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/FilterWritableByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/filter/FilterByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/filter/FilterChannel.java",
      "src/main/java/org/apache/commons/io/channels/filter/FilterReadableByteChannel.java",
      "src/main/java/org/apache/commons/io/channels/filter/FilterWritableByteChannel.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.apache.commons.io.channels.filter"
        ],
        "details": "Create the destination subpackage for filter-related channel classes.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.FilterChannel"
        ],
        "outputs": [
          "org.apache.commons.io.channels.filter.FilterChannel"
        ],
        "details": "Move the FilterChannel base class to the filter subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.FilterByteChannel"
        ],
        "outputs": [
          "org.apache.commons.io.channels.filter.FilterByteChannel"
        ],
        "details": "Move the FilterByteChannel implementation to the filter subpackage alongside its base.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.FilterReadableByteChannel"
        ],
        "outputs": [
          "org.apache.commons.io.channels.filter.FilterReadableByteChannel"
        ],
        "details": "Move the FilterReadableByteChannel to co-locate with other filter variants.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.FilterWritableByteChannel"
        ],
        "outputs": [
          "org.apache.commons.io.channels.filter.FilterWritableByteChannel"
        ],
        "details": "Move the FilterWritableByteChannel to the filter subpackage to keep the filter family together.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.apache.commons.io.channels.FilterSeekableByteChannel",
          "org.apache.commons.io.channels.filter.FilterByteChannel",
          "org.apache.commons.io.channels.filter.FilterChannel",
          "org.apache.commons.io.channels.filter.FilterReadableByteChannel",
          "org.apache.commons.io.channels.filter.FilterWritableByteChannel"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/io/channels/FilterByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterReadableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterSeekableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterWritableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterReadableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterWritableByteChannel.java"
  ],
  "executor_existing_files": [
    "src/main/java/org/apache/commons/io/channels/FilterByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterReadableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterSeekableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/FilterWritableByteChannel.java"
  ],
  "executor_new_files": [
    "src/main/java/org/apache/commons/io/channels/filter/FilterByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterReadableByteChannel.java",
    "src/main/java/org/apache/commons/io/channels/filter/FilterWritableByteChannel.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/io/channels/FilterByteChannel.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/FilterChannel.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/FilterReadableByteChannel.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/FilterSeekableByteChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels;\n\nimport java.io.FilterInputStream;\nimport java.io.FilterOutputStream;\nimport java.io.FilterReader;\nimport java.io.IOException;\nimport java.nio.channels.SeekableByteChannel;\n\nimport org.apache.commons.io.channels.filter.FilterByteChannel;\nimport org.apache.commons.io.channels.filter.FilterWritableByteChannel;\nimport org.apache.commons.io.input.ProxyInputStream;\nimport org.apache.commons.io.input.ProxyReader;\nimport org.apache.commons.io.output.ProxyOutputStream;\nimport org.apache.commons.io.output.ProxyWriter;\n\n/**\n * A {@link SeekableByteChannel} filter which delegates to the wrapped {@link SeekableByteChannel}.\n * <p>\n * A {@code FilterSeekableByteChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or\n * providing additional functionality. The class {@code FilterSeekableByteChannel} itself simply overrides methods of {@code SeekableByteChannel} with versions\n * that pass all requests to the wrapped channel. Subclasses of {@code FilterSeekableByteChannel} may of course override any methods declared or inherited by\n * {@code FilterSeekableByteChannel}, and may also provide additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterSeekableByteChannel#FilterSeekableByteChannel(SeekableByteChannel) Channel constructor} and more\n * advanced instances through the {@link Builder}.\n * </p>\n *\n * @param <C> The {@link SeekableByteChannel} type.\n * @see FilterInputStream\n * @see FilterOutputStream\n * @see FilterReader\n * @see FilterWritableByteChannel\n * @see ProxyInputStream\n * @see ProxyOutputStream\n * @see ProxyReader\n * @see ProxyWriter\n * @since 2.22.0\n */\npublic class FilterSeekableByteChannel<C extends SeekableByteChannel> extends FilterByteChannel<C> implements SeekableByteChannel {\n\n    /**\n     * Builds instances of {@link FilterSeekableByteChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterSeekableByteChannel} type.\n     * @param <C> The {@link SeekableByteChannel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterSeekableByteChannel<C>, C extends SeekableByteChannel, B extends AbstractBuilder<F, C, B>>\n            extends FilterByteChannel.AbstractBuilder<F, C, B> {\n\n        /**\n         * Constructs a new builder for {@link FilterSeekableByteChannel}.\n         */\n        public AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterSeekableByteChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterSeekableByteChannel<SeekableByteChannel>, SeekableByteChannel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterSeekableByteChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterSeekableByteChannel<SeekableByteChannel> get() throws IOException {\n            return new FilterSeekableByteChannel<>(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forSeekableByteChannel() {\n        return new Builder();\n    }\n\n    FilterSeekableByteChannel(final Builder builder) throws IOException {\n        super(builder);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param channel The channel to wrap.\n     */\n    public FilterSeekableByteChannel(final C channel) {\n        super(channel);\n    }\n\n    @Override\n    public long position() throws IOException {\n        return channel.position();\n    }\n\n    @Override\n    public SeekableByteChannel position(final long newPosition) throws IOException {\n        return channel.position(newPosition);\n    }\n\n    @Override\n    public long size() throws IOException {\n        return channel.size();\n    }\n\n    @Override\n    public SeekableByteChannel truncate(final long size) throws IOException {\n        return channel.truncate(size);\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/FilterWritableByteChannel.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/filter/FilterByteChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.filter;\n\nimport java.io.FilterInputStream;\nimport java.io.FilterOutputStream;\nimport java.io.FilterReader;\nimport java.io.IOException;\nimport java.nio.ByteBuffer;\nimport java.nio.channels.ByteChannel;\n\nimport org.apache.commons.io.channels.filter.FilterChannel;\nimport org.apache.commons.io.input.ProxyInputStream;\nimport org.apache.commons.io.input.ProxyReader;\nimport org.apache.commons.io.output.ProxyOutputStream;\nimport org.apache.commons.io.output.ProxyWriter;\n\n/**\n * A {@link ByteChannel} filter which delegates to the wrapped {@link ByteChannel}.\n * <p>\n * A {@code FilterByteChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or providing\n * additional functionality. The class {@code FilterByteChannel} itself simply overrides methods of {@code ByteChannel} with versions that pass all requests to\n * the wrapped channel. Subclasses of {@code FilterByteChannel} may of course override any methods declared or inherited by {@code FilterByteChannel}, and may\n * also provide additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterByteChannel#FilterByteChannel(ByteChannel) channel constructor} and more advanced instances through the\n * {@link Builder}.\n * </p>\n *\n * @param <C> The {@link ByteChannel} type.\n * @see FilterInputStream\n * @see FilterOutputStream\n * @see FilterReader\n * @see FilterWritableByteChannel\n * @see ProxyInputStream\n * @see ProxyOutputStream\n * @see ProxyReader\n * @see ProxyWriter\n * @since 2.22.0\n */\npublic class FilterByteChannel<C extends ByteChannel> extends FilterChannel<C> implements ByteChannel {\n\n    /**\n     * Builds instances of {@link FilterByteChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterByteChannel} type.\n     * @param <C> The {@link ByteChannel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterByteChannel<C>, C extends ByteChannel, B extends AbstractBuilder<F, C, B>>\n            extends FilterChannel.AbstractBuilder<F, C, B> {\n\n        /**\n         * Constructs a new builder for {@link FilterByteChannel}.\n         */\n        protected AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterByteChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterByteChannel<ByteChannel>, ByteChannel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterByteChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterByteChannel<ByteChannel> get() throws IOException {\n            return new FilterByteChannel<>(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forByteChannel() {\n        return new Builder();\n    }\n\n    FilterByteChannel(final AbstractBuilder<?, ?, ?> builder) throws IOException {\n        super(builder);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param byteChannel The channel to wrap.\n     */\n    public FilterByteChannel(final C byteChannel) {\n        super(byteChannel);\n    }\n\n    @Override\n    public int read(final ByteBuffer dst) throws IOException {\n        return channel.read(dst);\n    }\n\n    @Override\n    public int write(final ByteBuffer src) throws IOException {\n        return channel.write(src);\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/filter/FilterChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.filter;\n\nimport java.io.FilterInputStream;\nimport java.io.FilterOutputStream;\nimport java.io.FilterReader;\nimport java.io.IOException;\nimport java.nio.channels.Channel;\n\nimport org.apache.commons.io.build.AbstractStreamBuilder;\nimport org.apache.commons.io.input.ProxyInputStream;\nimport org.apache.commons.io.input.ProxyReader;\nimport org.apache.commons.io.output.ProxyOutputStream;\nimport org.apache.commons.io.output.ProxyWriter;\n\n/**\n * A {@link Channel} filter which delegates to the wrapped {@link Channel}.\n * <p>\n * A {@code FilterChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or providing\n * additional functionality. The class {@code FilterChannel} itself simply overrides methods of {@code Channel} with versions that pass all requests to the\n * wrapped channel. Subclasses of {@code FilterChannel} may of course override any methods declared or inherited by {@code FilterChannel}, and may also provide\n * additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterChannel#FilterChannel(Channel) channel constructor} and more advanced instances through the\n * {@link Builder}.\n * </p>\n *\n * @param <C> The {@link Channel} type.\n * @see FilterInputStream\n * @see FilterOutputStream\n * @see FilterReader\n * @see FilterWritableByteChannel\n * @see ProxyInputStream\n * @see ProxyOutputStream\n * @see ProxyReader\n * @see ProxyWriter\n * @since 2.22.0\n */\npublic class FilterChannel<C extends Channel> implements Channel {\n\n    /**\n     * Builds instances of {@link FilterChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterChannel} type.\n     * @param <C> The {@link Channel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterChannel<C>, C extends Channel, B extends AbstractBuilder<F, C, B>>\n            extends AbstractStreamBuilder<F, AbstractBuilder<F, C, B>> {\n\n        /**\n         * Constructs instance for subclasses.\n         */\n        protected AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterChannel<Channel>, Channel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterChannel<Channel> get() throws IOException {\n            return new FilterChannel<>(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forChannel() {\n        return new Builder();\n    }\n\n    final C channel;\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param builder The source builder.\n     * @throws IOException if an I/O error occurs.\n     */\n    @SuppressWarnings(\"unchecked\")\n    FilterChannel(final AbstractBuilder<?, ?, ?> builder) throws IOException {\n        channel = (C) builder.getChannel(Channel.class);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param channel The channel to wrap.\n     */\n    public FilterChannel(final C channel) {\n        this.channel = channel;\n    }\n\n    @Override\n    public void close() throws IOException {\n        channel.close();\n    }\n\n    @Override\n    public boolean isOpen() {\n        return channel.isOpen();\n    }\n\n    /**\n     * Unwraps this instance by returning the underlying {@link Channel} of type {@code C}.\n     * <p>\n     * Use with caution.\n     * </p>\n     *\n     * @return the underlying channel of type {@code C}.\n     */\n    public C unwrap() {\n        return channel;\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/filter/FilterReadableByteChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.filter;\n\nimport java.io.FilterInputStream;\nimport java.io.FilterOutputStream;\nimport java.io.FilterReader;\nimport java.io.IOException;\nimport java.nio.ByteBuffer;\nimport java.nio.channels.ReadableByteChannel;\n\nimport org.apache.commons.io.channels.filter.FilterByteChannel;\nimport org.apache.commons.io.channels.filter.FilterChannel;\nimport org.apache.commons.io.input.ProxyInputStream;\nimport org.apache.commons.io.input.ProxyReader;\nimport org.apache.commons.io.output.ProxyOutputStream;\nimport org.apache.commons.io.output.ProxyWriter;\n\n/**\n * A {@link ReadableByteChannel} filter which delegates to the wrapped {@link ReadableByteChannel}.\n * <p>\n * A {@code FilterReadableByteChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or\n * providing additional functionality. The class {@code FilterReadableByteChannel} itself simply overrides methods of {@code ReadableByteChannel} with versions\n * that pass all requests to the wrapped channel. Subclasses of {@code FilterReadableByteChannel} may of course override any methods declared or inherited by\n * {@code FilterReadableByteChannel}, and may also provide additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterReadableByteChannel#FilterReadableByteChannel(ReadableByteChannel) channel constructor} and more\n * advanced instances through the {@link Builder}.\n * </p>\n *\n * @param <C> The {@link ReadableByteChannel} type.\n * @see FilterInputStream\n * @see FilterOutputStream\n * @see FilterReader\n * @see FilterWritableByteChannel\n * @see ProxyInputStream\n * @see ProxyOutputStream\n * @see ProxyReader\n * @see ProxyWriter\n * @since 2.22.0\n */\npublic class FilterReadableByteChannel<C extends ReadableByteChannel> extends FilterChannel<C> implements ReadableByteChannel {\n\n    /**\n     * Builds instances of {@link FilterReadableByteChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterReadableByteChannel} type.\n     * @param <C> The {@link ReadableByteChannel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterReadableByteChannel<C>, C extends ReadableByteChannel, B extends AbstractBuilder<F, C, B>>\n            extends FilterChannel.AbstractBuilder<F, C, B> {\n\n        /**\n         * Constructs a new builder for {@link FilterReadableByteChannel}.\n         */\n        public AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterByteChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterReadableByteChannel<ReadableByteChannel>, ReadableByteChannel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterByteChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterReadableByteChannel<ReadableByteChannel> get() throws IOException {\n            return new FilterReadableByteChannel<>(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forReadableByteChannel() {\n        return new Builder();\n    }\n\n    FilterReadableByteChannel(final Builder builder) throws IOException {\n        super(builder);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param channel The channel to wrap.\n     */\n    public FilterReadableByteChannel(final C channel) {\n        super(channel);\n    }\n\n    @Override\n    public int read(final ByteBuffer dst) throws IOException {\n        return channel.read(dst);\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/filter/FilterWritableByteChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.filter;\n\nimport java.io.FilterInputStream;\nimport java.io.FilterOutputStream;\nimport java.io.FilterReader;\nimport java.io.IOException;\nimport java.nio.ByteBuffer;\nimport java.nio.channels.WritableByteChannel;\n\nimport org.apache.commons.io.channels.filter.FilterByteChannel;\nimport org.apache.commons.io.channels.filter.FilterChannel;\nimport org.apache.commons.io.input.ProxyInputStream;\nimport org.apache.commons.io.input.ProxyReader;\nimport org.apache.commons.io.output.ProxyOutputStream;\nimport org.apache.commons.io.output.ProxyWriter;\n\n/**\n * A {@link WritableByteChannel} filter which delegates to the wrapped {@link WritableByteChannel}.\n * <p>\n * A {@code FilterWritableByteChannel} wraps some other channel, which it uses as its basic source of data, possibly transforming the data along the way or\n * providing additional functionality. The class {@code FilterWritableByteChannel} itself simply overrides methods of {@code WritableByteChannel} with versions\n * that pass all requests to the wrapped channel. Subclasses of {@code FilterWritableByteChannel} may of course override any methods declared or inherited by\n * {@code WritableByteChannel}, and may also provide additional fields and methods.\n * </p>\n * <p>\n * You construct s simple instance with the {@link FilterWritableByteChannel#FilterWritableByteChannel(WritableByteChannel) Channel constructor} and more\n * advanced instances through the {@link Builder}.\n * </p>\n *\n * @param <C> The {@link WritableByteChannel} type.\n * @see FilterInputStream\n * @see FilterOutputStream\n * @see FilterReader\n * @see FilterWritableByteChannel\n * @see ProxyInputStream\n * @see ProxyOutputStream\n * @see ProxyReader\n * @see ProxyWriter\n * @since 2.22.0\n */\npublic class FilterWritableByteChannel<C extends WritableByteChannel> extends FilterChannel<C> implements WritableByteChannel {\n\n    /**\n     * Builds instances of {@link FilterWritableByteChannel} for subclasses.\n     *\n     * @param <F> The {@link FilterWritableByteChannel} type.\n     * @param <C> The {@link WritableByteChannel} type wrapped by the FilterChannel.\n     * @param <B> The builder type.\n     */\n    public abstract static class AbstractBuilder<F extends FilterWritableByteChannel<C>, C extends WritableByteChannel, B extends AbstractBuilder<F, C, B>>\n            extends FilterChannel.AbstractBuilder<F, C, B> {\n\n        /**\n         * Constructs a new builder for {@link FilterWritableByteChannel}.\n         */\n        public AbstractBuilder() {\n            // empty\n        }\n    }\n\n    /**\n     * Builds instances of {@link FilterByteChannel}.\n     */\n    public static class Builder extends AbstractBuilder<FilterWritableByteChannel<WritableByteChannel>, WritableByteChannel, Builder> {\n\n        /**\n         * Builds instances of {@link FilterByteChannel}.\n         */\n        protected Builder() {\n            // empty\n        }\n\n        @Override\n        public FilterWritableByteChannel<WritableByteChannel> get() throws IOException {\n            return new FilterWritableByteChannel<>(this);\n        }\n    }\n\n    /**\n     * Creates a new {@link Builder}.\n     *\n     * @return a new {@link Builder}.\n     */\n    public static Builder forWritableByteChannel() {\n        return new Builder();\n    }\n\n    FilterWritableByteChannel(final Builder builder) throws IOException {\n        super(builder);\n    }\n\n    /**\n     * Constructs a new instance.\n     *\n     * @param channel The channel to wrap.\n     */\n    public FilterWritableByteChannel(final C channel) {\n        super(channel);\n    }\n\n    @Override\n    public int write(final ByteBuffer src) throws IOException {\n        return channel.write(src);\n    }\n}\n"
    }
  ],
  "feedback": "",
  "attempt": 0,
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
