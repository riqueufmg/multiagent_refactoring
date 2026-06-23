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
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.apache.commons.lang3.mutable.MutableByte"
  },
  "block": {
    "id": 1,
    "goal": "Introduce a dedicated helper class to host the byte arithmetic and state-manipulation implementations so that MutableByte's public API is smaller and more cohesive.",
    "files": [
      "src/main/java/org/apache/commons/lang3/mutable/MutableByteArithmetic.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::add(byte)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::add(java.lang.Number)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::subtract(byte)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::subtract(java.lang.Number)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::increment()",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::decrement()",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::addAndGet(byte)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::addAndGet(java.lang.Number)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::getAndAdd(byte)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::getAndAdd(java.lang.Number)",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::incrementAndGet()",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::decrementAndGet()",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::getAndIncrement()",
          "src/main/java/org/apache/commons/lang3/mutable/MutableByte.java::getAndDecrement()"
        ],
        "outputs": [
          "src/main/java/org/apache/commons/lang3/mutable/MutableByteArithmetic.java"
        ],
        "details": "Create a new class org.apache.commons.lang3.mutable.MutableByteArithmetic with public static methods implementing the byte arithmetic and get/and variants. Method signatures use primitives and java.lang.Number where appropriate so the helper is independent of MutableByte's private fields. Example methods to create: add(byte current, byte operand), add(byte current, java.lang.Number operand), subtract(...), increment(...), decrement(...), addAndGet(...), getAndAdd(...), incrementAndGet(...), getAndIncrement(...), decrementAndGet(...), getAndDecrement(...). The helper will be placed in the same package org.apache.commons.lang3.mutable.",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/lang3/mutable/MutableByteArithmetic.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/apache/commons/lang3/mutable/MutableByteArithmetic.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/lang3/mutable/MutableByteArithmetic.java",
      "exists": "false",
      "content": ""
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
