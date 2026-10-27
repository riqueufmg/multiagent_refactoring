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
  "target_name": "org.springframework.batch.core.job.parameters.JobParameters",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261013_114644_IM__org_springframework_batch_core_job_parameters_JobParameters/run_002/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java",
  "target_source_root": "spring-batch-core/src/main/java",
  "target_code": "/*\n * Copyright 2006-2024 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.springframework.batch.core.job.parameters;\n\nimport java.io.Serializable;\nimport java.time.LocalDate;\nimport java.time.LocalDateTime;\nimport java.time.LocalTime;\nimport java.util.ArrayList;\nimport java.util.Collections;\nimport java.util.Date;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\nimport org.springframework.util.Assert;\n\nimport org.jspecify.annotations.Nullable;\n\n/**\n * Value object representing runtime parameters to a batch job. Because the parameters\n * have no individual meaning outside of the {@code JobParameters} object they are\n * contained within, it is a value object rather than an entity. It is also extremely\n * important that a parameters object can be reliably compared to another for equality, in\n * order to determine if one {@code JobParameters} object equals another. Furthermore,\n * because these parameters need to be persisted, it is vital that the types added are\n * restricted.\n * <p>\n * This class is immutable and, therefore, thread-safe.\n *\n * @author Lucas Ward\n * @author Michael Minella\n * @author Mahmoud Ben Hassine\n * @author Taeik Lim\n * @since 1.0\n */\npublic class JobParameters implements Serializable {\n\n\tprivate final Map<String, JobParameter<?>> parameters;\n\n\tprivate final JobParameterTypedAccessors typedAccessors;\n\n\t/**\n\t * Default constructor.\n\t */\n\tpublic JobParameters() {\n\t\tthis.parameters = new HashMap<>();\n\t\tthis.typedAccessors = new JobParameterTypedAccessors(this.parameters);\n\t}\n\n\t/**\n\t * Constructor that is initialized with the content of a {@link Map} that contains a\n\t * {@code String} key and a {@link JobParameter} value.\n\t * @param parameters The {@link Map} that contains a {@code String} key and a\n\t * {@link JobParameter} value.\n\t */\n\tpublic JobParameters(Map<String, JobParameter<?>> parameters) {\n\t\tthis.parameters = new HashMap<>(parameters);\n\t\tthis.typedAccessors = new JobParameterTypedAccessors(this.parameters);\n\t}\n\n\tpublic @Nullable Long getLong(String key) {\n\t\treturn typedAccessors.getLong(key);\n\t}\n\n\tpublic @Nullable Long getLong(String key, @Nullable Long defaultValue) {\n\t\treturn typedAccessors.getLong(key, defaultValue);\n\t}\n\n\tpublic @Nullable String getString(String key) {\n\t\treturn typedAccessors.getString(key);\n\t}\n\n\tpublic @Nullable String getString(String key, @Nullable String defaultValue) {\n\t\treturn typedAccessors.getString(key, defaultValue);\n\t}\n\n\tpublic @Nullable Double getDouble(String key) {\n\t\treturn typedAccessors.getDouble(key);\n\t}\n\n\tpublic @Nullable Double getDouble(String key, @Nullable Double defaultValue) {\n\t\treturn typedAccessors.getDouble(key, defaultValue);\n\t}\n\n\tpublic @Nullable Date getDate(String key) {\n\t\treturn typedAccessors.getDate(key);\n\t}\n\n\tpublic @Nullable Date getDate(String key, @Nullable Date defaultValue) {\n\t\treturn typedAccessors.getDate(key, defaultValue);\n\t}\n\n\tpublic @Nullable LocalDate getLocalDate(String key) {\n\t\treturn typedAccessors.getLocalDate(key);\n\t}\n\n\tpublic @Nullable LocalDate getLocalDate(String key, @Nullable LocalDate defaultValue) {\n\t\treturn typedAccessors.getLocalDate(key, defaultValue);\n\t}\n\n\tpublic @Nullable LocalTime getLocalTime(String key) {\n\t\treturn typedAccessors.getLocalTime(key);\n\t}\n\n\tpublic @Nullable LocalTime getLocalTime(String key, @Nullable LocalTime defaultValue) {\n\t\treturn typedAccessors.getLocalTime(key, defaultValue);\n\t}\n\n\tpublic @Nullable LocalDateTime getLocalDateTime(String key) {\n\t\treturn typedAccessors.getLocalDateTime(key);\n\t}\n\n\tpublic @Nullable LocalDateTime getLocalDateTime(String key, @Nullable LocalDateTime defaultValue) {\n\t\treturn typedAccessors.getLocalDateTime(key, defaultValue);\n\t}\n\n\tpublic @Nullable JobParameter<?> getParameter(String key) {\n\t\tAssert.notNull(key, \"key must not be null\");\n\t\treturn parameters.get(key);\n\t}\n\n\t/**\n\t * Get a map of all parameters.\n\t * @return an unmodifiable map containing all parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getParameters() {\n\t\treturn Collections.unmodifiableMap(parameters);\n\t}\n\n\t/**\n\t * Get a map of identifying parameters.\n\t * @since 5.1\n\t * @return an unmodifiable map containing identifying parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getIdentifyingParameters() {\n\t\tMap<String, JobParameter<?>> identifyingParameters = new HashMap<>();\n\t\tfor (Map.Entry<String, JobParameter<?>> entry : this.parameters.entrySet()) {\n\t\t\tif (entry.getValue().isIdentifying()) {\n\t\t\t\tidentifyingParameters.put(entry.getKey(), entry.getValue());\n\t\t\t}\n\t\t}\n\t\treturn Collections.unmodifiableMap(identifyingParameters);\n\t}\n\n\t/**\n\t * @return {@code true} if the parameters object is empty or {@code false} otherwise.\n\t */\n\tpublic boolean isEmpty() {\n\t\treturn parameters.isEmpty();\n\t}\n\n\t@Override\n\tpublic boolean equals(Object obj) {\n\t\tif (!(obj instanceof JobParameters rhs)) {\n\t\t\treturn false;\n\t\t}\n\n\t\tif (obj == this) {\n\t\t\treturn true;\n\t\t}\n\n\t\treturn this.parameters.equals(rhs.parameters);\n\t}\n\n\t@Override\n\tpublic int hashCode() {\n\t\treturn 17 + 23 * parameters.hashCode();\n\t}\n\n\t@Override\n\tpublic String toString() {\n\t\tList<String> parameters = new ArrayList<>();\n\t\tfor (Map.Entry<String, JobParameter<?>> entry : this.parameters.entrySet()) {\n\t\t\tparameters.add(String.format(\"'%s':'%s'\", entry.getKey(), entry.getValue()));\n\t\t}\n\t\treturn \"{\" + String.join(\",\", parameters) + \"}\";\n\t}\n\n}\n"
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