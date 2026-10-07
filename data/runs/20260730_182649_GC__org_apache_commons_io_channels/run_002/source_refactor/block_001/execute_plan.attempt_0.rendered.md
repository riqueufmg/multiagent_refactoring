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
    "goal": "Move the selected cluster classes to a new subpackage.",
    "files": [
      "src/main/java/org/apache/commons/io/channels/CloseShieldChannel.java",
      "src/main/java/org/apache/commons/io/channels/CloseShieldChannelHandler.java",
      "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannel.java",
      "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannelHandler.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.apache.commons.io.channels.internal"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.CloseShieldChannel"
        ],
        "outputs": [
          "org.apache.commons.io.channels.internal.CloseShieldChannel"
        ],
        "details": "Move this class to the destination package.",
        "risk": "low",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.io.channels.CloseShieldChannelHandler"
        ],
        "outputs": [
          "org.apache.commons.io.channels.internal.CloseShieldChannelHandler"
        ],
        "details": "Move this class to the destination package.",
        "risk": "low",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.apache.commons.io.channels.internal.CloseShieldChannel",
          "org.apache.commons.io.channels.internal.CloseShieldChannelHandler"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/io/channels/CloseShieldChannel.java",
    "src/main/java/org/apache/commons/io/channels/CloseShieldChannelHandler.java",
    "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannel.java",
    "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannelHandler.java"
  ],
  "executor_existing_files": [
    "src/main/java/org/apache/commons/io/channels/CloseShieldChannel.java",
    "src/main/java/org/apache/commons/io/channels/CloseShieldChannelHandler.java"
  ],
  "executor_new_files": [
    "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannel.java",
    "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannelHandler.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/io/channels/CloseShieldChannel.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/CloseShieldChannelHandler.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannel.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.internal;\n\nimport java.io.Closeable;\nimport java.lang.reflect.Proxy;\nimport java.nio.channels.AsynchronousChannel;\nimport java.nio.channels.ByteChannel;\nimport java.nio.channels.Channel;\nimport java.nio.channels.GatheringByteChannel;\nimport java.nio.channels.InterruptibleChannel;\nimport java.nio.channels.NetworkChannel;\nimport java.nio.channels.ReadableByteChannel;\nimport java.nio.channels.ScatteringByteChannel;\nimport java.nio.channels.SeekableByteChannel;\nimport java.nio.channels.WritableByteChannel;\nimport java.util.LinkedHashSet;\nimport java.util.Objects;\nimport java.util.Set;\n\n/**\n * Creates a close-shielding proxy for a {@link Channel}.\n *\n * <p>\n * The returned proxy implements all {@link Channel} sub-interfaces that are both supported by this implementation and actually implemented by the given\n * delegate.\n * </p>\n * <p>\n * The following interfaces are supported:\n * </p>\n * <ul>\n * <li>{@link AsynchronousChannel}</li>\n * <li>{@link ByteChannel}</li>\n * <li>{@link Channel}</li>\n * <li>{@link GatheringByteChannel}</li>\n * <li>{@link InterruptibleChannel}</li>\n * <li>{@link NetworkChannel}</li>\n * <li>{@link ReadableByteChannel}</li>\n * <li>{@link ScatteringByteChannel}</li>\n * <li>{@link SeekableByteChannel}</li>\n * <li>{@link WritableByteChannel}</li>\n * </ul>\n *\n * @see Channel\n * @see Closeable\n * @since 2.21.0\n */\npublic final class CloseShieldChannel {\n\n    private static final Class<?>[] EMPTY = {};\n\n    private static Set<Class<?>> collectChannelInterfaces(final Class<?> type, final Set<Class<?>> out) {\n        Class<?> currentType = type;\n        // Visit interfaces\n        while (currentType != null) {\n            for (final Class<?> iface : currentType.getInterfaces()) {\n                if (CloseShieldChannelHandler.isSupported(iface) && out.add(iface)) {\n                    collectChannelInterfaces(iface, out);\n                }\n            }\n            currentType = currentType.getSuperclass();\n        }\n        return out;\n    }\n\n    /**\n     * Wraps a channel to shield it from being closed.\n     *\n     * @param channel The underlying channel to shield, not {@code null}.\n     * @param <T>     A supported channel type.\n     * @return A proxy that shields {@code close()} and enforces closed semantics on other calls.\n     * @throws ClassCastException if {@code T} is not a supported channel type.\n     * @throws NullPointerException if {@code channel} is {@code null}.\n     */\n    @SuppressWarnings({ \"unchecked\", \"resource\" }) // caller closes\n    public static <T extends Channel> T wrap(final T channel) {\n        Objects.requireNonNull(channel, \"channel\");\n        // Fast path: already our shield\n        if (Proxy.isProxyClass(channel.getClass()) && Proxy.getInvocationHandler(channel) instanceof CloseShieldChannelHandler) {\n            return channel;\n        }\n        // Collect only Channel sub-interfaces.\n        final Set<Class<?>> set = collectChannelInterfaces(channel.getClass(), new LinkedHashSet<>());\n        // fallback to root surface\n        return (T) Proxy.newProxyInstance(channel.getClass().getClassLoader(), // use delegate's loader\n                set.isEmpty() ? new Class<?>[] { Channel.class } : set.toArray(EMPTY), new CloseShieldChannelHandler(channel));\n    }\n\n    private CloseShieldChannel() {\n        // no instance\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/io/channels/internal/CloseShieldChannelHandler.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.io.channels.internal;\n\nimport java.lang.reflect.InvocationHandler;\nimport java.lang.reflect.InvocationTargetException;\nimport java.lang.reflect.Method;\nimport java.lang.reflect.Proxy;\nimport java.nio.channels.AsynchronousChannel;\nimport java.nio.channels.ByteChannel;\nimport java.nio.channels.Channel;\nimport java.nio.channels.ClosedChannelException;\nimport java.nio.channels.GatheringByteChannel;\nimport java.nio.channels.InterruptibleChannel;\nimport java.nio.channels.NetworkChannel;\nimport java.nio.channels.ReadableByteChannel;\nimport java.nio.channels.ScatteringByteChannel;\nimport java.nio.channels.SeekableByteChannel;\nimport java.nio.channels.WritableByteChannel;\nimport java.util.Collections;\nimport java.util.HashSet;\nimport java.util.Objects;\nimport java.util.Set;\n\nimport org.apache.commons.io.channels.internal.CloseShieldChannel;\n\n/**\n * An {@link InvocationHandler} supporting the implementation of {@link CloseShieldChannel}.\n */\nfinal class CloseShieldChannelHandler implements InvocationHandler {\n\n    private static final Set<Class<? extends Channel>> SUPPORTED_INTERFACES;\n\n    static {\n        final Set<Class<? extends Channel>> interfaces = new HashSet<>();\n        interfaces.add(AsynchronousChannel.class);\n        interfaces.add(ByteChannel.class);\n        interfaces.add(Channel.class);\n        interfaces.add(GatheringByteChannel.class);\n        interfaces.add(InterruptibleChannel.class);\n        interfaces.add(NetworkChannel.class);\n        interfaces.add(ReadableByteChannel.class);\n        interfaces.add(ScatteringByteChannel.class);\n        interfaces.add(SeekableByteChannel.class);\n        interfaces.add(WritableByteChannel.class);\n        SUPPORTED_INTERFACES = Collections.unmodifiableSet(interfaces);\n    }\n\n    /**\n     * Tests whether the given method is allowed to be called after the shield is closed.\n     *\n     * @param declaringClass The class declaring the method.\n     * @param name           The method name.\n     * @param parameterCount The number of parameters.\n     * @return {@code true} if the method is allowed after {@code close()}, {@code false} otherwise.\n     */\n    private static boolean isAllowedAfterClose(final Class<?> declaringClass, final String name, final int parameterCount) {\n        // JDK explicitly allows NetworkChannel.supportedOptions() post-close\n        return parameterCount == 0 && name.equals(\"supportedOptions\") && NetworkChannel.class.equals(declaringClass);\n    }\n\n    static boolean isSupported(final Class<?> interfaceClass) {\n        return SUPPORTED_INTERFACES.contains(interfaceClass);\n    }\n\n    /**\n     * Tests whether the given method returns 'this' (the channel) as per JDK spec.\n     *\n     * @param declaringClass The class declaring the method.\n     * @param name           The method name.\n     * @param parameterCount The number of parameters.\n     * @return {@code true} if the method returns 'this', {@code false} otherwise.\n     */\n    private static boolean returnsThis(final Class<?> declaringClass, final String name, final int parameterCount) {\n        if (SeekableByteChannel.class.equals(declaringClass)) {\n            // SeekableByteChannel.position(long) and truncate(long) return 'this'\n            return parameterCount == 1 && (name.equals(\"position\") || name.equals(\"truncate\"));\n        }\n        if (NetworkChannel.class.equals(declaringClass)) {\n            // NetworkChannel.bind and NetworkChannel.setOption returns 'this'\n            return parameterCount == 1 && name.equals(\"bind\") || parameterCount == 2 && name.equals(\"setOption\");\n        }\n        return false;\n    }\n\n    private final Channel delegate;\n    private volatile boolean closed;\n\n    CloseShieldChannelHandler(final Channel delegate) {\n        this.delegate = Objects.requireNonNull(delegate, \"delegate\");\n    }\n\n    @Override\n    public Object invoke(final Object proxy, final Method method, final Object[] args) throws Throwable {\n        final Class<?> declaringClass = method.getDeclaringClass();\n        final String name = method.getName();\n        final int parameterCount = method.getParameterCount();\n        // 1) java.lang.Object methods\n        if (declaringClass == Object.class) {\n            return invokeObjectMethod(proxy, method, args);\n        }\n        // 2) Channel.close(): mark shield closed, do NOT close the delegate\n        if (parameterCount == 0 && name.equals(\"close\")) {\n            closed = true;\n            return null;\n        }\n        // 3) Channel.isOpen(): reflect shield state only\n        if (parameterCount == 0 && name.equals(\"isOpen\")) {\n            return !closed && delegate.isOpen();\n        }\n        // 4) After the shield is closed, only allow a tiny allowlist of safe queries\n        if (closed && !isAllowedAfterClose(declaringClass, name, parameterCount)) {\n            throw new ClosedChannelException();\n        }\n        // 5) Delegate to the underlying channel and unwrap target exceptions\n        try {\n            final Object result = method.invoke(delegate, args);\n            return returnsThis(declaringClass, name, parameterCount) ? proxy : result;\n        } catch (final InvocationTargetException e) {\n            throw e.getCause();\n        }\n    }\n\n    private Object invokeObjectMethod(final Object proxy, final Method method, final Object[] args) {\n        switch (method.getName()) {\n        case \"toString\":\n            return \"CloseShieldChannel(\" + delegate + \")\";\n        case \"hashCode\":\n            return Objects.hashCode(delegate);\n        case \"equals\": {\n            final Object other = args[0];\n            if (other == null) {\n                return false;\n            }\n            if (proxy == other) {\n                return true;\n            }\n            if (Proxy.isProxyClass(other.getClass())) {\n                final InvocationHandler h = Proxy.getInvocationHandler(other);\n                if (h instanceof CloseShieldChannelHandler) {\n                    return Objects.equals(((CloseShieldChannelHandler) h).delegate, this.delegate);\n                }\n            }\n            return false;\n        }\n        default:\n            // Not possible, all non-final Object methods are handled above.\n            return null;\n        }\n    }\n}\n"
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
