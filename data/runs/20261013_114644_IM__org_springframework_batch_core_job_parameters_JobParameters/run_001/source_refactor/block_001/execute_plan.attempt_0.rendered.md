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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/spring-batch/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.springframework.batch.core.job.parameters.JobParameters"
  },
  "block": {
    "id": 1,
    "goal": "Reduce the number of public methods and implementation complexity in JobParameters by extracting the cohesive type-specific parameter getter operations into a separate class while preserving the existing JobParameters API through delegation.",
    "files": [
      "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameterTypedAccessors.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.springframework.batch.core.job.parameters.JobParameters",
          "getLong(String)",
          "getLong(String, Long)",
          "getString(String)",
          "getString(String, String)",
          "getDouble(String)",
          "getDouble(String, Double)",
          "getDate(String)",
          "getDate(String, Date)",
          "getLocalDate(String)",
          "getLocalDate(String, LocalDate)",
          "getLocalTime(String)",
          "getLocalTime(String, LocalTime)",
          "getLocalDateTime(String)",
          "getLocalDateTime(String, LocalDateTime)",
          "parameters"
        ],
        "outputs": [
          "org.springframework.batch.core.job.parameters.JobParameterTypedAccessors"
        ],
        "details": "Create JobParameterTypedAccessors in the same package and move the cohesive typed getter implementations and their shared parameters field dependency into it. Preserve the existing null handling and IllegalArgumentException behavior for mismatched parameter types. Add a constructor accepting the parameter map so JobParameters can delegate to the extracted class.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.springframework.batch.core.job.parameters.JobParameters.getLong(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLong(String, Long)",
          "org.springframework.batch.core.job.parameters.JobParameters.getString(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getString(String, String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getDouble(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getDouble(String, Double)",
          "org.springframework.batch.core.job.parameters.JobParameters.getDate(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getDate(String, Date)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalDate(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalDate(String, LocalDate)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalTime(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalTime(String, LocalTime)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalDateTime(String)",
          "org.springframework.batch.core.job.parameters.JobParameters.getLocalDateTime(String, LocalDateTime)"
        ],
        "outputs": [
          "org.springframework.batch.core.job.parameters.JobParameterTypedAccessors"
        ],
        "details": "Move the listed methods from JobParameters to JobParameterTypedAccessors. Keep public delegating methods with the same signatures in JobParameters so existing callers remain source-compatible; each delegate forwards to the extracted accessor instance.",
        "risk": "medium"
      },
      {
        "op": "MOVE_FIELD",
        "inputs": [
          "org.springframework.batch.core.job.parameters.JobParameters.parameters"
        ],
        "outputs": [
          "org.springframework.batch.core.job.parameters.JobParameterTypedAccessors.parameters"
        ],
        "details": "Move the typed-getter-specific access to the existing parameters map into JobParameterTypedAccessors. JobParameters must continue to retain its map for getParameter(String), getParameters(), getIdentifyingParameters(), isEmpty(), equals(Object), hashCode(), and toString(). Initialize the accessor with the same map after each JobParameters construction.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameterTypedAccessors.java"
        ],
        "outputs": [
          "java.time.LocalDate",
          "java.time.LocalDateTime",
          "java.time.LocalTime",
          "java.util.Date",
          "java.util.Map",
          "org.springframework.batch.core.job.parameters.JobParameter",
          "org.jspecify.annotations.Nullable"
        ],
        "details": "Add only the imports required by the moved typed getter methods and remove imports from JobParameters that are no longer needed after extraction.",
        "risk": "low"
      }
    ]
  },
  "allowed_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameterTypedAccessors.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java"
  ],
  "executor_existing_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java"
  ],
  "executor_new_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameterTypedAccessors.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameterTypedAccessors.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java",
      "exists": "true",
      "content": "/*\n * Copyright 2006-2024 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.springframework.batch.core.job.parameters;\n\nimport java.io.Serializable;\nimport java.time.LocalDate;\nimport java.time.LocalDateTime;\nimport java.time.LocalTime;\nimport java.util.ArrayList;\nimport java.util.Collections;\nimport java.util.Date;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\nimport org.springframework.util.Assert;\n\nimport org.jspecify.annotations.Nullable;\n\n/**\n * Value object representing runtime parameters to a batch job. Because the parameters\n * have no individual meaning outside of the {@code JobParameters} object they are\n * contained within, it is a value object rather than an entity. It is also extremely\n * important that a parameters object can be reliably compared to another for equality, in\n * order to determine if one {@code JobParameters} object equals another. Furthermore,\n * because these parameters need to be persisted, it is vital that the types added are\n * restricted.\n * <p>\n * This class is immutable and, therefore, thread-safe.\n *\n * @author Lucas Ward\n * @author Michael Minella\n * @author Mahmoud Ben Hassine\n * @author Taeik Lim\n * @since 1.0\n */\npublic class JobParameters implements Serializable {\n\n\tprivate final Map<String, JobParameter<?>> parameters;\n\n\t/**\n\t * Default constructor.\n\t */\n\tpublic JobParameters() {\n\t\tthis.parameters = new HashMap<>();\n\t}\n\n\t/**\n\t * Constructor that is initialized with the content of a {@link Map} that contains a\n\t * {@code String} key and a {@link JobParameter} value.\n\t * @param parameters The {@link Map} that contains a {@code String} key and a\n\t * {@link JobParameter} value.\n\t */\n\tpublic JobParameters(Map<String, JobParameter<?>> parameters) {\n\t\tthis.parameters = new HashMap<>(parameters);\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Long} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return The {@link Long} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable Long getLong(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(Long.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type Long\");\n\t\t}\n\t\treturn (Long) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Long} represented by the provided key. If the key\n\t * does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable Long getLong(String key, @Nullable Long defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getLong(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link String} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return The {@link String} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable String getString(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(String.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type String\");\n\t\t}\n\t\treturn (String) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link String} represented by the provided key. If the key\n\t * does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The defult value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable String getString(String key, @Nullable String defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getString(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Double} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return The {@link Double} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable Double getDouble(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(Double.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type Double\");\n\t\t}\n\t\treturn (Double) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Double} represented by the provided key. If the key\n\t * does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable Double getDouble(String key, @Nullable Double defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getDouble(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Date} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return the {@link java.util.Date} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable Date getDate(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(Date.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type java.util.Date\");\n\t\t}\n\t\treturn (Date) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link Date} represented by the provided key. If the key\n\t * does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable Date getDate(String key, @Nullable Date defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getDate(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalDate} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return the {@link LocalDate} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable LocalDate getLocalDate(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(LocalDate.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type java.time.LocalDate\");\n\t\t}\n\t\treturn (LocalDate) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalDate} represented by the provided key. If the\n\t * key does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable LocalDate getLocalDate(String key, @Nullable LocalDate defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getLocalDate(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalTime} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return the {@link LocalTime} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable LocalTime getLocalTime(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(LocalTime.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type java.time.LocalTime\");\n\t\t}\n\t\treturn (LocalTime) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalTime} represented by the provided key. If the\n\t * key does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable LocalTime getLocalTime(String key, @Nullable LocalTime defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getLocalTime(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalDateTime} represented by the provided key.\n\t * @param key The key for which to get a value.\n\t * @return the {@link LocalDateTime} value or {@code null} if the key is absent.\n\t */\n\tpublic @Nullable LocalDateTime getLocalDateTime(String key) {\n\t\tif (!parameters.containsKey(key)) {\n\t\t\treturn null;\n\t\t}\n\t\tJobParameter<?> jobParameter = parameters.get(key);\n\t\tif (!jobParameter.getType().equals(LocalDateTime.class)) {\n\t\t\tthrow new IllegalArgumentException(\"Key \" + key + \" is not of type java.time.LocalDateTime\");\n\t\t}\n\t\treturn (LocalDateTime) jobParameter.getValue();\n\t}\n\n\t/**\n\t * Typesafe getter for the {@link LocalDateTime} represented by the provided key. If\n\t * the key does not exist, the default value is returned.\n\t * @param key The key for which to return the value.\n\t * @param defaultValue The default value to return if the value does not exist.\n\t * @return the parameter represented by the provided key or, if that is missing, the\n\t * default value.\n\t */\n\tpublic @Nullable LocalDateTime getLocalDateTime(String key, @Nullable LocalDateTime defaultValue) {\n\t\tif (parameters.containsKey(key)) {\n\t\t\treturn getLocalDateTime(key);\n\t\t}\n\t\telse {\n\t\t\treturn defaultValue;\n\t\t}\n\t}\n\n\tpublic @Nullable JobParameter<?> getParameter(String key) {\n\t\tAssert.notNull(key, \"key must not be null\");\n\t\treturn parameters.get(key);\n\t}\n\n\t/**\n\t * Get a map of all parameters.\n\t * @return an unmodifiable map containing all parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getParameters() {\n\t\treturn Collections.unmodifiableMap(parameters);\n\t}\n\n\t/**\n\t * Get a map of identifying parameters.\n\t * @since 5.1\n\t * @return an unmodifiable map containing identifying parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getIdentifyingParameters() {\n\t\tMap<String, JobParameter<?>> identifyingParameters = new HashMap<>();\n\t\tfor (Map.Entry<String, JobParameter<?>> entry : this.parameters.entrySet()) {\n\t\t\tif (entry.getValue().isIdentifying()) {\n\t\t\t\tidentifyingParameters.put(entry.getKey(), entry.getValue());\n\t\t\t}\n\t\t}\n\t\treturn Collections.unmodifiableMap(identifyingParameters);\n\t}\n\n\t/**\n\t * @return {@code true} if the parameters object is empty or {@code false} otherwise.\n\t */\n\tpublic boolean isEmpty() {\n\t\treturn parameters.isEmpty();\n\t}\n\n\t@Override\n\tpublic boolean equals(Object obj) {\n\t\tif (!(obj instanceof JobParameters rhs)) {\n\t\t\treturn false;\n\t\t}\n\n\t\tif (obj == this) {\n\t\t\treturn true;\n\t\t}\n\n\t\treturn this.parameters.equals(rhs.parameters);\n\t}\n\n\t@Override\n\tpublic int hashCode() {\n\t\treturn 17 + 23 * parameters.hashCode();\n\t}\n\n\t@Override\n\tpublic String toString() {\n\t\tList<String> parameters = new ArrayList<>();\n\t\tfor (Map.Entry<String, JobParameter<?>> entry : this.parameters.entrySet()) {\n\t\t\tparameters.add(String.format(\"'%s':'%s'\", entry.getKey(), entry.getValue()));\n\t\t}\n\t\treturn \"{\" + String.join(\",\", parameters) + \"}\";\n\t}\n\n}\n"
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
