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
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "org.springframework.batch.core.job.parameters.JobParameters",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261015_092513_IM__org_springframework_batch_core_job_parameters_JobParameters/run_005/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "spring-batch-core/src/main/java/org/springframework/batch/core/job/parameters/JobParameters.java",
  "target_source_root": "spring-batch-core/src/main/java",
  "target_code": "/*\n * Copyright 2006-2024 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.springframework.batch.core.job.parameters;\n\nimport java.io.Serializable;\nimport java.util.ArrayList;\nimport java.util.List;\nimport java.util.Map;\n\nimport com.fasterxml.jackson.annotation.JsonCreator;\nimport com.fasterxml.jackson.annotation.JsonProperty;\n\n/**\n * Value object representing runtime parameters to a batch job. Because the parameters\n * have no individual meaning outside of the {@code JobParameters} object they are\n * contained within, it is a value object rather than an entity. It is also extremely\n * important that a parameters object can be reliably compared to another for equality, in\n * order to determine if one {@code JobParameters} object equals another. Furthermore,\n * because these parameters need to be persisted, it is vital that the types added are\n * restricted.\n * <p>\n * This class is immutable and, therefore, thread-safe.\n *\n * @author Lucas Ward\n * @author Michael Minella\n * @author Mahmoud Ben Hassine\n * @author Taeik Lim\n * @since 1.0\n */\npublic class JobParameters implements Serializable {\n\n\tprivate final JobParametersStore parameterStore;\n\n\tprivate final JobParametersTypedAccessors typedAccessors;\n\n\t/**\n\t * Default constructor.\n\t */\n\tpublic JobParameters() {\n\t\tthis.parameterStore = new JobParametersStore();\n\t\tthis.typedAccessors = new JobParametersTypedAccessors(this.parameterStore.getParameters());\n\t}\n\n\t/**\n\t * Constructor that is initialized with the content of a {@link Map} that contains a\n\t * {@code String} key and a {@link JobParameter} value.\n\t * @param parameters The {@link Map} that contains a {@code String} key and a\n\t * {@link JobParameter} value.\n\t */\n\t@JsonCreator\n\tpublic JobParameters(@JsonProperty(\"parameters\") Map<String, JobParameter<?>> parameters) {\n\t\tthis.parameterStore = new JobParametersStore(parameters);\n\t\tthis.typedAccessors = new JobParametersTypedAccessors(this.parameterStore.getParameters());\n\t}\n\n\tpublic Long getLong(String key) {\n\t\treturn this.typedAccessors.getLong(key);\n\t}\n\n\tpublic Long getLong(String key, Long defaultValue) {\n\t\treturn this.typedAccessors.getLong(key, defaultValue);\n\t}\n\n\tpublic String getString(String key) {\n\t\treturn this.typedAccessors.getString(key);\n\t}\n\n\tpublic String getString(String key, String defaultValue) {\n\t\treturn this.typedAccessors.getString(key, defaultValue);\n\t}\n\n\tpublic Double getDouble(String key) {\n\t\treturn this.typedAccessors.getDouble(key);\n\t}\n\n\tpublic Double getDouble(String key, Double defaultValue) {\n\t\treturn this.typedAccessors.getDouble(key, defaultValue);\n\t}\n\n\tpublic java.util.Date getDate(String key) {\n\t\treturn this.typedAccessors.getDate(key);\n\t}\n\n\tpublic java.util.Date getDate(String key, java.util.Date defaultValue) {\n\t\treturn this.typedAccessors.getDate(key, defaultValue);\n\t}\n\n\tpublic java.time.LocalDate getLocalDate(String key) {\n\t\treturn this.typedAccessors.getLocalDate(key);\n\t}\n\n\tpublic java.time.LocalDate getLocalDate(String key, java.time.LocalDate defaultValue) {\n\t\treturn this.typedAccessors.getLocalDate(key, defaultValue);\n\t}\n\n\tpublic java.time.LocalTime getLocalTime(String key) {\n\t\treturn this.typedAccessors.getLocalTime(key);\n\t}\n\n\tpublic java.time.LocalTime getLocalTime(String key, java.time.LocalTime defaultValue) {\n\t\treturn this.typedAccessors.getLocalTime(key, defaultValue);\n\t}\n\n\tpublic java.time.LocalDateTime getLocalDateTime(String key) {\n\t\treturn this.typedAccessors.getLocalDateTime(key);\n\t}\n\n\tpublic java.time.LocalDateTime getLocalDateTime(String key, java.time.LocalDateTime defaultValue) {\n\t\treturn this.typedAccessors.getLocalDateTime(key, defaultValue);\n\t}\n\n\tpublic JobParameter<?> getParameter(String key) {\n\t\treturn this.parameterStore.getParameter(key);\n\t}\n\n\t/**\n\t * Get a map of all parameters.\n\t * @return an unmodifiable map containing all parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getParameters() {\n\t\treturn this.parameterStore.getParameters();\n\t}\n\n\t/**\n\t * Get a map of identifying parameters.\n\t * @since 5.1\n\t * @return an unmodifiable map containing identifying parameters.\n\t */\n\tpublic Map<String, JobParameter<?>> getIdentifyingParameters() {\n\t\treturn this.parameterStore.getIdentifyingParameters();\n\t}\n\n\t/**\n\t * @return {@code true} if the parameters object is empty or {@code false} otherwise.\n\t */\n\tpublic boolean isEmpty() {\n\t\treturn this.parameterStore.isEmpty();\n\t}\n\n\t@Override\n\tpublic boolean equals(Object obj) {\n\t\tif (!(obj instanceof JobParameters rhs)) {\n\t\t\treturn false;\n\t\t}\n\n\t\tif (obj == this) {\n\t\t\treturn true;\n\t\t}\n\n\t\treturn this.getParameters().equals(rhs.getParameters());\n\t}\n\n\t@Override\n\tpublic int hashCode() {\n\t\treturn 17 + 23 * this.getParameters().hashCode();\n\t}\n\n\t@Override\n\tpublic String toString() {\n\t\tList<String> parameters = new ArrayList<>();\n\t\tfor (Map.Entry<String, JobParameter<?>> entry : this.getParameters().entrySet()) {\n\t\t\tparameters.add(String.format(\"'%s':'%s'\", entry.getKey(), entry.getValue()));\n\t\t}\n\t\treturn \"{\" + String.join(\",\", parameters) + \"}\";\n\t}\n\n}\n"
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