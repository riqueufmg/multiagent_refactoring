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
  "repo_path": "/data/henrique/multiagent_refactoring/data/repositories/commons-lang",
  "target": {
    "smell": "GC",
    "smell_name": "God Component",
    "target_type": "package",
    "target_name": "org.apache.commons.lang3.function"
  },
  "block": {
    "id": 1,
    "goal": "Move the selected cluster of related failable functional interfaces into the failable subpackage to reduce surface area of the top-level function package.",
    "files": [
      "src/main/java/org/apache/commons/lang3/function/FailableBiConsumer.java",
      "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
      "src/main/java/org/apache/commons/lang3/function/FailableRunnable.java",
      "src/main/java/org/apache/commons/lang3/function/MethodInvokers.java",
      "src/main/java/org/apache/commons/lang3/function/failable/FailableBiConsumer.java",
      "src/main/java/org/apache/commons/lang3/function/failable/FailableConsumer.java",
      "src/main/java/org/apache/commons/lang3/function/failable/FailableRunnable.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.apache.commons.lang3.function.failable"
        ],
        "details": "Create the destination subpackage org.apache.commons.lang3.function.failable if it does not already exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.lang3.function.FailableConsumer"
        ],
        "outputs": [
          "org.apache.commons.lang3.function.failable.FailableConsumer"
        ],
        "details": "Move FailableConsumer to the failable subpackage to colocate failable functional interfaces.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.lang3.function.FailableBiConsumer"
        ],
        "outputs": [
          "org.apache.commons.lang3.function.failable.FailableBiConsumer"
        ],
        "details": "Move FailableBiConsumer to the failable subpackage to keep binary and consumer variants together.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.apache.commons.lang3.function.FailableRunnable"
        ],
        "outputs": [
          "org.apache.commons.lang3.function.failable.FailableRunnable"
        ],
        "details": "Move FailableRunnable to the failable subpackage to group runnable-style failable interfaces with other failable types.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.apache.commons.lang3.function.MethodInvokers",
          "org.apache.commons.lang3.function.failable.FailableBiConsumer",
          "org.apache.commons.lang3.function.failable.FailableConsumer",
          "org.apache.commons.lang3.function.failable.FailableRunnable"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/lang3/function/FailableBiConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableRunnable.java",
    "src/main/java/org/apache/commons/lang3/function/MethodInvokers.java",
    "src/main/java/org/apache/commons/lang3/function/failable/FailableBiConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/failable/FailableConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/failable/FailableRunnable.java"
  ],
  "executor_existing_files": [
    "src/main/java/org/apache/commons/lang3/function/FailableBiConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableRunnable.java",
    "src/main/java/org/apache/commons/lang3/function/MethodInvokers.java"
  ],
  "executor_new_files": [
    "src/main/java/org/apache/commons/lang3/function/failable/FailableBiConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/failable/FailableConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/failable/FailableRunnable.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/lang3/function/FailableBiConsumer.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/FailableRunnable.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/MethodInvokers.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.lang3.function;\n\nimport java.lang.invoke.MethodHandle;\nimport java.lang.invoke.MethodHandleProxies;\nimport java.lang.invoke.MethodHandles;\nimport java.lang.reflect.Method;\nimport java.util.Objects;\nimport java.util.function.BiConsumer;\nimport java.util.function.BiFunction;\nimport java.util.function.Function;\nimport java.util.function.Supplier;\n\nimport org.apache.commons.lang3.exception.UncheckedIllegalAccessException;\nimport org.apache.commons.lang3.function.failable.FailableBiConsumer;\nimport org.apache.commons.lang3.function.failable.FailableBiFunction;\nimport org.apache.commons.lang3.function.failable.FailableFunction;\nimport org.apache.commons.lang3.function.failable.FailableSupplier;\n\n/**\n * Converts {@link Method} objects to lambdas.\n * <p>\n * More specifically, produces instances of single-method interfaces which redirect calls to methods; see\n * {@link #asInterfaceInstance(Class, Method)}.\n * </p>\n * <h2>Calling supplier methods with no arguments</h2>\n * <p>\n * If the interface's single-method defines no arguments, use {@link #asFunction(Method)} and then apply the function\n * passing in the object to receive the method call.\n * </p>\n * <p>\n * For example to invoke {@link String#length()}:\n * </p>\n *\n * <pre>{@code\n * final Method method = String.class.getMethod(\"length\");\n * final Function<String, Integer> function = MethodInvokers.asFunction(method);\n * assertEquals(3, function.apply(\"ABC\"));\n * }</pre>\n *\n * <h2>Calling function methods with one argument</h2>\n * <p>\n * If the interface's single-method defines one argument, use {@link #asBiFunction(Method)} and then apply the function\n * passing in the object to receive the method call. The second argument to the function is the only argument to the\n * method.\n * </p>\n * <p>\n * For example to invoke {@link String#charAt(int)}:\n * </p>\n *\n * <pre>{@code\n * final Method method = String.class.getMethod(\"charAt\", int.class);\n * final BiFunction<String, Integer, Character> function = MethodInvokers.asBiFunction(method);\n * assertEquals('C', function.apply(\"ABC\", 2));\n * }</pre>\n *\n * @since 3.13.0\n */\npublic final class MethodInvokers {\n\n    /**\n     * Produces a {@link BiConsumer} for a given <em>consumer</em> Method. For example, a classic setter method (as opposed\n     * to a fluent setter). You call the BiConsumer with two arguments: (1) the object receiving the method call, and (2)\n     * the method argument.\n     *\n     * @param <T> the type of the first argument to the operation: The type containing the Method.\n     * @param <U> the type of the second argument to the operation: The type of the method argument.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, U> BiConsumer<T, U> asBiConsumer(final Method method) {\n        return asInterfaceInstance(BiConsumer.class, method);\n    }\n\n    /**\n     * Produces a {@link BiFunction} for a given a <em>function</em> Method. You call the BiFunction with two arguments: (1)\n     * the object receiving the method call, and (2) the method argument. The BiFunction return type must match the method's\n     * return type.\n     * <p>\n     * For example to invoke {@link String#charAt(int)}:\n     * </p>\n     *\n     * <pre>{@code\n     * final Method method = String.class.getMethod(\"charAt\", int.class);\n     * final BiFunction<String, Integer, Character> function = MethodInvokers.asBiFunction(method);\n     * assertEquals('C', function.apply(\"ABC\", 2));\n     * }</pre>\n     *\n     * @param <T> the type of the first argument to the function: The type containing the method.\n     * @param <U> the type of the second argument to the function: the method argument type.\n     * @param <R> the type of the result of the function: The method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, U, R> BiFunction<T, U, R> asBiFunction(final Method method) {\n        return asInterfaceInstance(BiFunction.class, method);\n    }\n\n    /**\n     * Produces a {@link FailableBiConsumer} for a given <em>consumer</em> Method. For example, a classic setter method (as\n     * opposed to a fluent setter). You call the FailableBiConsumer with two arguments: (1) the object receiving the method\n     * call, and (2) the method argument.\n     *\n     * @param <T> the type of the first argument to the operation: The type containing the Method.\n     * @param <U> the type of the second argument to the operation: The type of the method argument.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, U> FailableBiConsumer<T, U, Throwable> asFailableBiConsumer(final Method method) {\n        return asInterfaceInstance(FailableBiConsumer.class, method);\n    }\n\n    /**\n     * Produces a {@link FailableBiFunction} for a given a <em>function</em> Method. You call the FailableBiFunction with\n     * two arguments: (1) the object receiving the method call, and (2) the method argument. The BiFunction return type must\n     * match the method's return type.\n     *\n     * @param <T> the type of the first argument to the function: The type containing the method.\n     * @param <U> the type of the second argument to the function: the method argument type.\n     * @param <R> the type of the result of the function: The method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, U, R> FailableBiFunction<T, U, R, Throwable> asFailableBiFunction(final Method method) {\n        return asInterfaceInstance(FailableBiFunction.class, method);\n    }\n\n    /**\n     * Produces a {@link FailableFunction} for a given a <em>supplier</em> Method. You call the Function with one argument:\n     * the object receiving the method call. The FailableFunction return type must match the method's return type.\n     *\n     * @param <T> the type of the first argument to the function: The type containing the method.\n     * @param <R> the type of the result of the function: The method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, R> FailableFunction<T, R, Throwable> asFailableFunction(final Method method) {\n        return asInterfaceInstance(FailableFunction.class, method);\n    }\n\n    /**\n     * Produces a {@link FailableSupplier} for a given a <em>supplier</em> Method. The FailableSupplier return type must\n     * match the method's return type.\n     * <p>\n     * Only works with static methods.\n     * </p>\n     *\n     * @param <R> The Method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <R> FailableSupplier<R, Throwable> asFailableSupplier(final Method method) {\n        return asInterfaceInstance(FailableSupplier.class, method);\n    }\n\n    /**\n     * Produces a {@link Function} for a given a <em>supplier</em> Method. You call the Function with one argument: the\n     * object receiving the method call. The Function return type must match the method's return type.\n     * <p>\n     * For example to invoke {@link String#length()}:\n     * </p>\n     *\n     * <pre>{@code\n     * final Method method = String.class.getMethod(\"length\");\n     * final Function<String, Integer> function = MethodInvokers.asFunction(method);\n     * assertEquals(3, function.apply(\"ABC\"));\n     * }</pre>\n     *\n     * @param <T> the type of the first argument to the function: The type containing the method.\n     * @param <R> the type of the result of the function: The method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <T, R> Function<T, R> asFunction(final Method method) {\n        return asInterfaceInstance(Function.class, method);\n    }\n\n    /**\n     * Produces an instance of the given single-method interface which redirects its calls to the given method.\n     * <p>\n     * For the definition of \"single-method\", see {@link MethodHandleProxies#asInterfaceInstance(Class, MethodHandle)}.\n     * </p>\n     *\n     * @param <T> The interface type.\n     * @param interfaceClass a class object representing {@code T}.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     * @see MethodHandleProxies#asInterfaceInstance(Class, MethodHandle)\n     */\n    public static <T> T asInterfaceInstance(final Class<T> interfaceClass, final Method method) {\n        return MethodHandleProxies.asInterfaceInstance(Objects.requireNonNull(interfaceClass, \"interfaceClass\"), unreflectUnchecked(method));\n    }\n\n    /**\n     * Produces a {@link Supplier} for a given a <em>supplier</em> Method. The Supplier return type must match the method's\n     * return type.\n     * <p>\n     * Only works with static methods.\n     * </p>\n     *\n     * @param <R> The Method return type.\n     * @param method the method to invoke.\n     * @return a correctly-typed wrapper for the given target.\n     */\n    @SuppressWarnings(\"unchecked\")\n    public static <R> Supplier<R> asSupplier(final Method method) {\n        return asInterfaceInstance(Supplier.class, method);\n    }\n\n    /**\n     * Throws NullPointerException if {@code method} is {@code null}.\n     *\n     * @param method The method to test.\n     * @return The given method.\n     * @throws NullPointerException if {@code method} is {@code null}.\n     */\n    private static Method requireMethod(final Method method) {\n        return Objects.requireNonNull(method, \"method\");\n    }\n\n    private static MethodHandle unreflect(final Method method) throws IllegalAccessException {\n        return MethodHandles.lookup().unreflect(requireMethod(method));\n    }\n\n    private static MethodHandle unreflectUnchecked(final Method method) {\n        try {\n            return unreflect(method);\n        } catch (final IllegalAccessException e) {\n            throw new UncheckedIllegalAccessException(e);\n        }\n    }\n\n    /**\n     * No need to create instances.\n     */\n    private MethodInvokers() {\n        // noop\n    }\n\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/failable/FailableBiConsumer.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.lang3.function.failable;\n\nimport java.util.Objects;\nimport java.util.function.BiConsumer;\n\n/**\n * A functional interface like {@link BiConsumer} that declares a {@link Throwable}.\n *\n * @param <T> Consumed type 1.\n * @param <U> Consumed type 2.\n * @param <E> The kind of thrown exception or error.\n * @since 3.11\n */\n@FunctionalInterface\npublic interface FailableBiConsumer<T, U, E extends Throwable> {\n\n    /** NOP singleton */\n    @SuppressWarnings(\"rawtypes\")\n    FailableBiConsumer NOP = (t, u) -> { /* NOP */ };\n\n    /**\n     * Gets the NOP singleton.\n     *\n     * @param <T> Consumed type 1.\n     * @param <U> Consumed type 2.\n     * @param <E> The kind of thrown exception or error.\n     * @return The NOP singleton.\n     */\n    @SuppressWarnings(\"unchecked\")\n    static <T, U, E extends Throwable> FailableBiConsumer<T, U, E> nop() {\n        return NOP;\n    }\n\n    /**\n     * Accepts the given arguments.\n     *\n     * @param t the first parameter for the consumable to accept\n     * @param u the second parameter for the consumable to accept\n     * @throws E Thrown when the consumer fails.\n     */\n    void accept(T t, U u) throws E;\n\n    /**\n     * Returns a composed {@link FailableBiConsumer} like {@link BiConsumer#andThen(BiConsumer)}.\n     *\n     * @param after the operation to perform after this one.\n     * @return a composed {@link FailableBiConsumer} like {@link BiConsumer#andThen(BiConsumer)}.\n     * @throws NullPointerException when {@code after} is null.\n     */\n    default FailableBiConsumer<T, U, E> andThen(final FailableBiConsumer<? super T, ? super U, E> after) {\n        Objects.requireNonNull(after);\n        return (t, u) -> {\n            accept(t, u);\n            after.accept(t, u);\n        };\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/failable/FailableConsumer.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.lang3.function.failable;\n\nimport java.util.Objects;\nimport java.util.function.Consumer;\nimport java.util.function.Function;\n\n/**\n * A functional interface like {@link Consumer} that declares a {@link Throwable}.\n *\n * <p>\n * This is a functional interface whose functional method is {@link #accept(Object)}.\n * </p>\n *\n * @param <T> the type of the argument the consumer accepts.\n * @param <E> The thrown exception type.\n * @since 3.11\n */\n@FunctionalInterface\npublic interface FailableConsumer<T, E extends Throwable> {\n\n    /** NOP singleton */\n    @SuppressWarnings(\"rawtypes\")\n    FailableConsumer NOP = Function.identity()::apply;\n\n    /**\n     * Applies the given {@link FailableConsumer} action to the object if the consumer is not {@code null}. Otherwise, does nothing.\n     *\n     * @param consumer the consumer to consume.\n     * @param object   the object to be consumed.\n     * @param <T>      the type of the argument the consumer accepts.\n     * @param <E>      The thrown exception type.\n     * @throws E Thrown when the consumer fails.\n     * @since 3.21.0\n     */\n    static <T, E extends Throwable> void accept(final FailableConsumer<T, E> consumer, final T object) throws E {\n        if (consumer != null) {\n            consumer.accept(object);\n        }\n    }\n\n    /**\n     * Gets the NOP singleton.\n     *\n     * @param <T> the type of the argument the consumer accepts.\n     * @param <E> The thrown exception type.\n     * @return The NOP singleton.\n     */\n    @SuppressWarnings(\"unchecked\")\n    static <T, E extends Throwable> FailableConsumer<T, E> nop() {\n        return NOP;\n    }\n\n    /**\n     * Accepts the given arguments.\n     *\n     * @param object the parameter for the consumable to accept\n     * @throws E Thrown when the consumer fails.\n     */\n    void accept(T object) throws E;\n\n    /**\n     * Returns a composed {@link Consumer} like {@link Consumer#andThen(Consumer)}.\n     *\n     * @param after the operation to perform after this operation\n     * @return a composed {@link Consumer} like {@link Consumer#andThen(Consumer)}.\n     * @throws NullPointerException when {@code after} is null\n     */\n    default FailableConsumer<T, E> andThen(final FailableConsumer<? super T, E> after) {\n        Objects.requireNonNull(after);\n        return (final T t) -> {\n            accept(t);\n            after.accept(t);\n        };\n    }\n}\n"
    },
    {
      "path": "src/main/java/org/apache/commons/lang3/function/failable/FailableRunnable.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements.  See the NOTICE file distributed with\n * this work for additional information regarding copyright ownership.\n * The ASF licenses this file to You under the Apache License, Version 2.0\n * (the \"License\"); you may not use this file except in compliance with\n * the License.  You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.apache.commons.lang3.function.failable;\n\n/**\n * A functional interface like {@link Runnable} that declares a kind of {@link Throwable}.\n *\n * @param <E> The kind of {@link Throwable}.\n * @since 3.11\n */\n@FunctionalInterface\npublic interface FailableRunnable<E extends Throwable> {\n\n    /**\n     * Runs the function.\n     *\n     * @throws E Thrown when the function fails.\n     */\n    void run() throws E;\n}\n"
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
