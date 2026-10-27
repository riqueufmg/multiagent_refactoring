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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/byte-buddy/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "net.bytebuddy.build.gradle.android.ByteBuddyAndroidTaskExtension"
  },
  "block": {
    "id": 3,
    "goal": "Group task-adjustment related configuration (adjustment, adjustmentErrorHandler, adjustmentPostProcessor, threads, lazy) into a single Adjustment configuration class to reduce the count of getters/setters in the primary class.",
    "files": [
      "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidAdjustment.java",
      "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidTaskExtension.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidTaskExtension.java"
        ],
        "outputs": [
          "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidAdjustment.java"
        ],
        "details": "Create net.bytebuddy.build.gradle.android.ByteBuddyAndroidAdjustment that owns the fields: Adjustment adjustment; Adjustment.ErrorHandler adjustmentErrorHandler; Action<Task> adjustmentPostProcessor; int threads; boolean lazy. Provide getters and setters for each, and a constructor that establishes the same default values currently assigned in the ByteBuddyAndroidTaskExtension constructor (Adjustment.FULL, Adjustment.ErrorHandler.WARN, Adjustment.NoOpPostProcessor.INSTANCE, threads default 0, lazy default false).",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidAdjustment.java",
    "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidTaskExtension.java"
  ],
  "executor_existing_files": [
    "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidTaskExtension.java"
  ],
  "executor_new_files": [
    "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidAdjustment.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidAdjustment.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "byte-buddy-gradle-plugin/android-plugin/src/main/java/net/bytebuddy/build/gradle/android/ByteBuddyAndroidTaskExtension.java",
      "exists": "true",
      "content": "/*\n * Copyright 2014 - Present Rafael Winterhalter\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage net.bytebuddy.build.gradle.android;\n\nimport groovy.lang.Closure;\nimport net.bytebuddy.ClassFileVersion;\nimport net.bytebuddy.build.EntryPoint;\nimport net.bytebuddy.build.gradle.*;\nimport net.bytebuddy.utility.nullability.MaybeNull;\nimport net.bytebuddy.utility.nullability.UnknownNull;\nimport org.gradle.api.Action;\nimport org.gradle.api.JavaVersion;\nimport org.gradle.api.Project;\nimport org.gradle.api.Task;\nimport org.gradle.api.file.FileCollection;\n\nimport java.util.ArrayList;\nimport java.util.List;\n\n/**\n * A Byte Buddy task extension for Android.\n */\npublic abstract class ByteBuddyAndroidTaskExtension {\n\n    /**\n     * The current Gradle project.\n     */\n    private final Project project;\n\n    /**\n     * Encapsulated transformations manager.\n     */\n    private final ByteBuddyAndroidTransformations transformations;\n\n    /**\n     * The entry point to use.\n     */\n    private EntryPoint entryPoint;\n\n    /**\n     * The suffix to use for rebased methods or the empty string if a random suffix should be used.\n     */\n    private String suffix;\n\n    /**\n     * {@code true} if the transformation should fail if a live initializer is used.\n     */\n    private boolean failOnLiveInitializer;\n\n    /**\n     * {@code true} if a warning should be issued for an empty type set.\n     */\n    private boolean warnOnEmptyTypeSet;\n\n    /**\n     * {@code true} if the transformation should fail fast.\n     */\n    private boolean failFast;\n\n    /**\n     * {@code true} if extended parsing should be used.\n     */\n    private boolean extendedParsing;\n\n    /**\n     * Determines if the build should discover Byte Buddy build plugins on this Maven plugin's class loader.\n     * Discovered plugins are stored by their name in the <i>/META-INF/net.bytebuddy/build.plugins</i> file\n     * where each line contains the fully qualified class name. Discovered plugins are not provided with any\n     * explicit constructor arguments.\n     */\n    private Discovery discovery;\n\n    /**\n     * Determines what tasks are considered when adjusting the task dependency graph to include the Byte Buddy task.\n     * By default, only the altered task's project's task is considered but the adjustment can include subprojects or\n     * the entire project graph. Note that it might not always be legal to resolve such recursive dependencies.\n     */\n    private Adjustment adjustment;\n\n    /**\n     * Determines the reaction upon a failed task dependency resolution.\n     */\n    private Adjustment.ErrorHandler adjustmentErrorHandler;\n\n    /**\n     * The adjustment post processor that is applied after the graph dependencies are is resolved.\n     */\n    private Action<Task> adjustmentPostProcessor;\n\n    /**\n     * The number of threads to use for transforming or {@code 0} if the transformation should be applied in the main thread.\n     */\n    private int threads;\n\n    /**\n     * If {@code true}, task dependencies are only adjusted when the task graph is fully resolved.\n     */\n    private boolean lazy;\n\n    /**\n     * The class file version to use for creating auxiliary types or {@code null} if the\n     * version is determined implicitly.\n     */\n    @MaybeNull\n    private ClassFileVersion classFileVersion;\n\n    /**\n     * Creates a new abstract Byte Buddy task extension.\n     *\n     * @param project The current Gradle project.\n     */\n    public ByteBuddyAndroidTaskExtension(Project project) {\n        this.project = project;\n        this.transformations = new ByteBuddyAndroidTransformations(project);\n        entryPoint = EntryPoint.Default.REBASE;\n        suffix = \"\";\n        failOnLiveInitializer = true;\n        warnOnEmptyTypeSet = true;\n        failFast = true;\n        discovery = Discovery.EMPTY;\n        adjustment = Adjustment.FULL;\n        adjustmentErrorHandler = Adjustment.ErrorHandler.WARN;\n        adjustmentPostProcessor = Adjustment.NoOpPostProcessor.INSTANCE;\n    }\n\n    /**\n     * Returns the entry point to use.\n     *\n     * @return The entry point to use.\n     */\n    public EntryPoint getEntryPoint() {\n        return entryPoint;\n    }\n\n    /**\n     * Sets the entry point to use.\n     *\n     * @param entryPoint The entry point to use.\n     */\n    public void setEntryPoint(EntryPoint entryPoint) {\n        this.entryPoint = entryPoint;\n    }\n\n    /**\n     * Returns the suffix to use for rebased methods or the empty string if a random suffix should be used.\n     *\n     * @return The suffix to use for rebased methods or the empty string if a random suffix should be used.\n     */\n    public String getSuffix() {\n        return suffix;\n    }\n\n    /**\n     * Sets the suffix to use for rebased methods or the empty string if a random suffix should be used.\n     *\n     * @param suffix The suffix to use for rebased methods or the empty string if a random suffix should be used.\n     */\n    public void setSuffix(String suffix) {\n        this.suffix = suffix;\n    }\n\n    /**\n     * Returns {@code true} if the transformation should fail if a live initializer is used.\n     *\n     * @return {@code true} if the transformation should fail if a live initializer is used.\n     */\n    public boolean isFailOnLiveInitializer() {\n        return failOnLiveInitializer;\n    }\n\n    /**\n     * Determines if the transformation should fail if a live initializer is used.\n     *\n     * @param failOnLiveInitializer {@code true} if the transformation should fail if a live initializer is used.\n     */\n    public void setFailOnLiveInitializer(boolean failOnLiveInitializer) {\n        this.failOnLiveInitializer = failOnLiveInitializer;\n    }\n\n    /**\n     * Returns {@code true} if a warning should be issued for an empty type set.\n     *\n     * @return {@code true} if a warning should be issued for an empty type set.\n     */\n    public boolean isWarnOnEmptyTypeSet() {\n        return warnOnEmptyTypeSet;\n    }\n\n    /**\n     * Returns {@code true} if a warning should be issued for an empty type set.\n     *\n     * @param warnOnEmptyTypeSet {@code true} if a warning should be issued for an empty type set.\n     */\n    public void setWarnOnEmptyTypeSet(boolean warnOnEmptyTypeSet) {\n        this.warnOnEmptyTypeSet = warnOnEmptyTypeSet;\n    }\n\n    /**\n     * Returns {@code true} if a warning should be issued for an empty type set.\n     *\n     * @return {@code true} if a warning should be issued for an empty type set.\n     */\n    public boolean isFailFast() {\n        return failFast;\n    }\n\n    /**\n     * Determines if a warning should be issued for an empty type set.\n     *\n     * @param failFast {@code true} if a warning should be issued for an empty type set.\n     */\n    public void setFailFast(boolean failFast) {\n        this.failFast = failFast;\n    }\n\n    /**\n     * Returns {@code true} if extended parsing should be used.\n     *\n     * @return {@code true} if extended parsing should be used.\n     */\n    public boolean isExtendedParsing() {\n        return extendedParsing;\n    }\n\n    /**\n     * Determines if extended parsing should be used.\n     *\n     * @param extendedParsing {@code true} if extended parsing should be used.\n     */\n    public void setExtendedParsing(boolean extendedParsing) {\n        this.extendedParsing = extendedParsing;\n    }\n\n    /**\n     * Determines the discovery for finding plugins on the class path.\n     *\n     * @return The discovery for finding plugins on the class path.\n     */\n    public Discovery getDiscovery() {\n        return discovery;\n    }\n\n    /**\n     * Determines the discovery for finding plugins on the class path.\n     *\n     * @param discovery The discovery for finding plugins on the class path.\n     */\n    public void setDiscovery(Discovery discovery) {\n        this.discovery = discovery;\n    }\n\n    /**\n     * Determines the adjustment for tasks that might depend on post-processed compile tasks.\n     *\n     * @return The adjustment for tasks that might depend on post-processed compile tasks.\n     */\n    public Adjustment getAdjustment() {\n        return adjustment;\n    }\n\n    /**\n     * Determines the adjustment for tasks that might depend on post-processed compile tasks.\n     *\n     * @param adjustment The adjustment for tasks that might depend on post-processed compile tasks.\n     */\n    public void setAdjustment(Adjustment adjustment) {\n        this.adjustment = adjustment;\n    }\n\n    /**\n     * Returns the error handler to be used when a task dependency cannot be resolved.\n     *\n     * @return The error handler to be used when a task dependency cannot be resolved.\n     */\n    public Adjustment.ErrorHandler getAdjustmentErrorHandler() {\n        return adjustmentErrorHandler;\n    }\n\n    /**\n     * Sets the error handler to be used when a task dependency cannot be resolved.\n     *\n     * @param adjustmentErrorHandler The error handler to be used when a task dependency cannot be resolved.\n     */\n    public void setAdjustmentErrorHandler(Adjustment.ErrorHandler adjustmentErrorHandler) {\n        this.adjustmentErrorHandler = adjustmentErrorHandler;\n    }\n\n    /**\n     * Returns the adjustment post processor that is applied after the graph dependencies are is resolved.\n     *\n     * @return The adjustment post processor to apply.\n     */\n    public Action<Task> getAdjustmentPostProcessor() {\n        return adjustmentPostProcessor;\n    }\n\n    /**\n     * Sets the adjustment post processor that is applied after the graph dependencies are resolved.\n     *\n     * @param adjustmentPostProcessor The adjustment post processor to apply.\n     */\n    public void setAdjustmentPostProcessor(Action<Task> adjustmentPostProcessor) {\n        this.adjustmentPostProcessor = adjustmentPostProcessor;\n    }\n\n    /**\n     * Returns the number of threads to use for transforming or {@code 0} if the transformation should be applied in the main thread.\n     *\n     * @return The number of threads to use for transforming or {@code 0} if the transformation should be applied in the main thread.\n     */\n    public int getThreads() {\n        return threads;\n    }\n\n    /**\n     * Sets the number of threads to use for transforming or {@code 0} if the transformation should be applied in the main thread.\n     *\n     * @param threads The number of threads to use for transforming or {@code 0} if the transformation should be applied in the main thread.\n     */\n    public void setThreads(int threads) {\n        this.threads = threads;\n    }\n\n    /**\n     * Returns {@code true}, task dependencies are only adjusted when the task graph is fully resolved.\n     *\n     * @return {@code true}, task dependencies are only adjusted when the task graph is fully resolved.\n     */\n    public boolean isLazy() {\n        return lazy;\n    }\n\n    /**\n     * If set to {@code true}, task dependencies are only adjusted when the task graph is fully resolved.\n     *\n     * @param lazy {@code true}, task dependencies are only adjusted when the task graph is fully resolved.\n     */\n    public void setLazy(boolean lazy) {\n        this.lazy = lazy;\n    }\n\n    /**\n     * Returns the class file version to use for creating auxiliary types or {@code null} if the\n     * version is determined implicitly.\n     *\n     * @return The class file version to use for creating auxiliary types.\n     */\n    @MaybeNull\n    public ClassFileVersion getClassFileVersion() {\n        return classFileVersion;\n    }\n\n    /**\n     * Sets the class file version to use for creating auxiliary types or {@code null} if the\n     * version is determined implicitly.\n     *\n     * @param classFileVersion The class file version to use for creating auxiliary types.\n     */\n    public void setClassFileVersion(@MaybeNull ClassFileVersion classFileVersion) {\n        this.classFileVersion = classFileVersion;\n    }\n\n    /**\n     * Returns the list of transformations configured for this extension.\n     * Delegates to the encapsulated ByteBuddyAndroidTransformations instance.\n     *\n     * @return The list of transformations.\n     */\n    public List<Transformation> getTransformations() {\n        return transformations.getTransformations();\n    }\n\n    /**\n     * Adds a transformation configured by a Groovy closure.\n     * Delegates to the encapsulated ByteBuddyAndroidTransformations instance.\n     *\n     * @param closure The closure configuring the transformation.\n     */\n    public void transformation(Closure closure) {\n        transformations.transformation(closure);\n    }\n\n    /**\n     * Adds a transformation configured by an Action.\n     * Delegates to the encapsulated ByteBuddyAndroidTransformations instance.\n     *\n     * @param action The action configuring the transformation.\n     */\n    public void transformation(Action<? super Transformation> action) {\n        transformations.transformation(action);\n    }\n\n    /**\n     * Resolves default properties and considers the contextual Java version.\n     *\n     * @param version The Java version to resolve as a fallback if no explicit version is set.\n     */\n    protected void resolve(JavaVersion version) {\n        if (classFileVersion == null) {\n            classFileVersion = ClassFileVersion.ofJavaVersion(Integer.parseInt(version.getMajorVersion()));\n        }\n    }\n\n    /**\n     * Returns {@code true} if this extension defines an empty discovery.\n     *\n     * @return {@code true} if this extension defines an empty discovery.\n     */\n    protected abstract boolean isEmptyDiscovery();\n\n    /**\n     * Applies this extension's properties.\n     *\n     * @param task The task to configure.\n     */\n    protected void configure(T task) {\n//        task.getTransformations().addAll(getTransformations());\n        task.getEntryPoint().convention(getEntryPoint());\n//        task.setSuffix(getSuffix());\n//        task.setFailOnLiveInitializer(isFailOnLiveInitializer());\n//        task.setWarnOnEmptyTypeSet(isWarnOnEmptyTypeSet());\n//        task.setFailFast(isFailFast());\n//        task.setExtendedParsing(isExtendedParsing());\n//        task.setDiscovery(getDiscovery());\n//        task.setThreads(getThreads());\n//        task.setClassFileVersion(getClassFileVersion());\n    }\n}\n"
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
