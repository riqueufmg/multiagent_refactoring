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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/dropwizard/repository",
  "target": {
    "smell": "GC",
    "smell_name": "God Component",
    "target_type": "package",
    "target_name": "io.dropwizard.jersey.optional"
  },
  "block": {
    "id": 1,
    "goal": "Move the cohesive optional parameter binding cluster into a dedicated subpackage.",
    "files": [
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamBinder.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalDoubleParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalIntParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalLongParamConverterProvider.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalParamBinder.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "io.dropwizard.jersey.optional.param"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalParamBinder"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.param.OptionalParamBinder"
        ],
        "details": "Move the optional parameter binder to the dedicated parameter subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalDoubleParamConverterProvider"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.param.OptionalDoubleParamConverterProvider"
        ],
        "details": "Move the optional double parameter converter provider to the dedicated parameter subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalIntParamConverterProvider"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.param.OptionalIntParamConverterProvider"
        ],
        "details": "Move the optional int parameter converter provider to the dedicated parameter subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalLongParamConverterProvider"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.param.OptionalLongParamConverterProvider"
        ],
        "details": "Move the optional long parameter converter provider to the dedicated parameter subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalParamConverterProvider",
          "io.dropwizard.jersey.optional.param.OptionalDoubleParamConverterProvider",
          "io.dropwizard.jersey.optional.param.OptionalIntParamConverterProvider",
          "io.dropwizard.jersey.optional.param.OptionalLongParamConverterProvider",
          "io.dropwizard.jersey.optional.param.OptionalParamBinder"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamBinder.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalDoubleParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalIntParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalLongParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalParamBinder.java"
  ],
  "executor_existing_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamBinder.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamConverterProvider.java"
  ],
  "executor_new_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalDoubleParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalIntParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalLongParamConverterProvider.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalParamBinder.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleParamConverterProvider.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntParamConverterProvider.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongParamConverterProvider.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamBinder.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalParamConverterProvider.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional;\n\nimport org.glassfish.jersey.internal.inject.InjectionManager;\nimport org.glassfish.jersey.internal.inject.Providers;\nimport org.glassfish.jersey.internal.util.ReflectionHelper;\nimport org.glassfish.jersey.internal.util.collection.ClassTypePair;\n\nimport javax.annotation.Nullable;\nimport javax.inject.Inject;\nimport javax.inject.Singleton;\nimport javax.ws.rs.ext.ParamConverter;\nimport javax.ws.rs.ext.ParamConverterProvider;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.util.List;\nimport java.util.Optional;\n\n@Singleton\npublic class OptionalParamConverterProvider implements ParamConverterProvider {\n    private final InjectionManager manager;\n\n    @Inject\n    public OptionalParamConverterProvider(final InjectionManager manager) {\n        this.manager = manager;\n    }\n\n    /**\n     * {@inheritDoc}\n     */\n    @Override\n    @Nullable\n    public <T> ParamConverter<T> getConverter(final Class<T> rawType, final Type genericType,\n                                              final Annotation[] annotations) {\n        if (Optional.class.equals(rawType)) {\n            final List<ClassTypePair> ctps = ReflectionHelper.getTypeArgumentAndClass(genericType);\n            final ClassTypePair ctp = (ctps.size() == 1) ? ctps.get(0) : null;\n\n            if (ctp == null || ctp.rawClass() == String.class) {\n                return new ParamConverter<T>() {\n                    @Override\n                    public T fromString(final String value) {\n                        return rawType.cast(Optional.ofNullable(value));\n                    }\n\n                    @Override\n                    public String toString(final T value) {\n                        return value.toString();\n                    }\n                };\n            }\n\n            for (ParamConverterProvider provider : Providers.getProviders(manager, ParamConverterProvider.class)) {\n                final ParamConverter<?> converter = provider.getConverter(ctp.rawClass(), ctp.type(), annotations);\n                if (converter != null) {\n                    return new ParamConverter<T>() {\n                        @Override\n                        public T fromString(final String value) {\n                            return rawType.cast(Optional.ofNullable(value).map(s -> converter.fromString(value)));\n                        }\n\n                        @Override\n                        public String toString(final T value) {\n                            return value.toString();\n                        }\n                    };\n                }\n            }\n        }\n\n        return null;\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalDoubleParamConverterProvider.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.param;\n\nimport io.dropwizard.jersey.DefaultValueUtils;\n\nimport javax.annotation.Nullable;\nimport javax.inject.Singleton;\nimport javax.ws.rs.ext.ParamConverter;\nimport javax.ws.rs.ext.ParamConverterProvider;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.util.OptionalDouble;\n\n@Singleton\npublic class OptionalDoubleParamConverterProvider implements ParamConverterProvider {\n    private final OptionalDoubleParamConverter paramConverter = new OptionalDoubleParamConverter();\n\n    /**\n     * {@inheritDoc}\n     */\n    @Override\n    @SuppressWarnings(\"unchecked\")\n    @Nullable\n    public <T> ParamConverter<T> getConverter(final Class<T> rawType, final Type genericType,\n                                              final Annotation[] annotations) {\n        if (!OptionalDouble.class.equals(rawType)) {\n            return null;\n        }\n        final String defaultValue = DefaultValueUtils.getDefaultValue(annotations);\n        return (ParamConverter<T>) (defaultValue == null ? paramConverter : new OptionalDoubleParamConverter(defaultValue));\n    }\n\n    public static class OptionalDoubleParamConverter implements ParamConverter<OptionalDouble> {\n\n        @Nullable\n        private final String defaultValue;\n\n        public OptionalDoubleParamConverter() {\n            this(null);\n        }\n\n        public OptionalDoubleParamConverter(@Nullable String defaultValue) {\n            this.defaultValue = defaultValue;\n        }\n\n        @SuppressWarnings(\"OptionalAssignedToNull\")\n        @Override\n        @Nullable\n        public OptionalDouble fromString(final String value) {\n            try {\n                final double d = Double.parseDouble(value);\n                return OptionalDouble.of(d);\n            } catch (NullPointerException | NumberFormatException e) {\n                if (defaultValue != null) {\n                    // If an invalid default value is specified, we want to fail fast.\n                    // This is the same behavior as DropWizard 1.3.x and matches Jersey's handling of @DefaultValue for Double.\n                    if (defaultValue.equals(value)) {\n                        throw e;\n                    }\n                    // In order to fall back to use a default value for an empty query param, we must return null here.\n                    // This preserves backwards compatibility with DropWizard 1.3.x handling of empty query params.\n                    if (value == null || value.isEmpty()) {\n                        return null;\n                    }\n                }\n                return OptionalDouble.empty();\n            }\n        }\n\n        @Override\n        public String toString(final OptionalDouble value) {\n            if (value == null) {\n                throw new IllegalArgumentException(\"value must not be null\");\n            }\n            return value.isPresent() ? Double.toString(value.getAsDouble()) : \"\";\n        }\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalIntParamConverterProvider.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.param;\n\nimport io.dropwizard.jersey.DefaultValueUtils;\n\nimport javax.annotation.Nullable;\nimport javax.inject.Singleton;\nimport javax.ws.rs.ext.ParamConverter;\nimport javax.ws.rs.ext.ParamConverterProvider;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.util.OptionalInt;\n\n@Singleton\npublic class OptionalIntParamConverterProvider implements ParamConverterProvider {\n    private final OptionalIntParamConverter paramConverter = new OptionalIntParamConverter();\n\n    /**\n     * {@inheritDoc}\n     */\n    @Override\n    @SuppressWarnings(\"unchecked\")\n    @Nullable\n    public <T> ParamConverter<T> getConverter(final Class<T> rawType, final Type genericType,\n                                              final Annotation[] annotations) {\n        if (!OptionalInt.class.equals(rawType)) {\n            return null;\n        }\n        final String defaultValue = DefaultValueUtils.getDefaultValue(annotations);\n        return (ParamConverter<T>) (defaultValue == null ? paramConverter : new OptionalIntParamConverter(defaultValue));\n    }\n\n    public static class OptionalIntParamConverter implements ParamConverter<OptionalInt> {\n\n        @Nullable\n        private final String defaultValue;\n\n        public OptionalIntParamConverter() {\n            this(null);\n        }\n\n        public OptionalIntParamConverter(@Nullable String defaultValue) {\n            this.defaultValue = defaultValue;\n        }\n\n        @SuppressWarnings(\"OptionalAssignedToNull\")\n        @Override\n        @Nullable\n        public OptionalInt fromString(final String value) {\n            try {\n                final int i = Integer.parseInt(value);\n                return OptionalInt.of(i);\n            } catch (NullPointerException | NumberFormatException e) {\n                if (defaultValue != null) {\n                    // If an invalid default value is specified, we want to fail fast.\n                    // This is the same behavior as DropWizard 1.3.x and matches Jersey's handling of @DefaultValue for Integer.\n                    if (defaultValue.equals(value)) {\n                        throw e;\n                    }\n                    // In order to fall back to use a default value for an empty query param, we must return null here.\n                    // This preserves backwards compatibility with DropWizard 1.3.x handling of empty query params.\n                    if (value == null || value.isEmpty()) {\n                        return null;\n                    }\n                }\n                return OptionalInt.empty();\n            }\n        }\n\n        @Override\n        public String toString(final OptionalInt value) {\n            if (value == null) {\n                throw new IllegalArgumentException(\"value must not be null\");\n            }\n            return value.isPresent() ? Integer.toString(value.getAsInt()) : \"\";\n        }\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalLongParamConverterProvider.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.param;\n\nimport io.dropwizard.jersey.DefaultValueUtils;\n\nimport javax.annotation.Nullable;\nimport javax.inject.Singleton;\nimport javax.ws.rs.ext.ParamConverter;\nimport javax.ws.rs.ext.ParamConverterProvider;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.util.OptionalLong;\n\n@Singleton\npublic class OptionalLongParamConverterProvider implements ParamConverterProvider {\n    private final OptionalLongParamConverter paramConverter = new OptionalLongParamConverter();\n\n    /**\n     * {@inheritDoc}\n     */\n    @Override\n    @SuppressWarnings(\"unchecked\")\n    @Nullable\n    public <T> ParamConverter<T> getConverter(final Class<T> rawType, final Type genericType,\n                                              final Annotation[] annotations) {\n        if (!OptionalLong.class.equals(rawType)) {\n            return null;\n        }\n        final String defaultValue = DefaultValueUtils.getDefaultValue(annotations);\n        return (ParamConverter<T>) ((defaultValue == null) ? paramConverter : new OptionalLongParamConverter(defaultValue));\n    }\n\n    public static class OptionalLongParamConverter implements ParamConverter<OptionalLong> {\n\n        @Nullable\n        private final String defaultValue;\n\n        public OptionalLongParamConverter() {\n            this(null);\n        }\n\n        public OptionalLongParamConverter(@Nullable String defaultValue) {\n            this.defaultValue = defaultValue;\n        }\n\n        @SuppressWarnings(\"OptionalAssignedToNull\")\n        @Override\n        @Nullable\n        public OptionalLong fromString(final String value) {\n            try {\n                final long l = Long.parseLong(value);\n                return OptionalLong.of(l);\n            } catch (NullPointerException | NumberFormatException e) {\n                if (defaultValue != null) {\n                    // If an invalid default value is specified, we want to fail fast.\n                    // This is the same behavior as DropWizard 1.3.x and matches Jersey's handling of @DefaultValue for Long.\n                    if (defaultValue.equals(value)) {\n                        throw e;\n                    }\n                    // In order to fall back to use a default value for an empty query param, we must return null here.\n                    // This preserves backwards compatibility with DropWizard 1.3.x handling of empty query params.\n                    if (value == null || value.isEmpty()) {\n                        return null;\n                    }\n                }\n                return OptionalLong.empty();\n            }\n        }\n\n        @Override\n        public String toString(final OptionalLong value) {\n            if (value == null) {\n                throw new IllegalArgumentException(\"value must not be null\");\n            }\n            return value.isPresent() ? Long.toString(value.getAsLong()) : \"\";\n        }\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/param/OptionalParamBinder.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.param;\n\nimport org.glassfish.jersey.internal.inject.AbstractBinder;\n\nimport javax.inject.Singleton;\nimport javax.ws.rs.ext.ParamConverterProvider;\n\npublic class OptionalParamBinder extends AbstractBinder {\n    @Override\n    protected void configure() {\n        // Param converter providers\n        bind(OptionalParamConverterProvider.class).to(ParamConverterProvider.class).in(Singleton.class);\n        bind(OptionalDoubleParamConverterProvider.class).to(ParamConverterProvider.class).in(Singleton.class);\n        bind(OptionalIntParamConverterProvider.class).to(ParamConverterProvider.class).in(Singleton.class);\n        bind(OptionalLongParamConverterProvider.class).to(ParamConverterProvider.class).in(Singleton.class);\n    }\n}\n"
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
