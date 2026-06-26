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
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.apache.commons.io.function.IOStream"
  },
  "block": {
    "id": 1,
    "goal": "Create a dedicated interface holding terminal and terminal-like operations currently implemented as many default methods in IOStream, so these methods can be moved out of the large IOStream interface without breaking compilation.",
    "files": [
      "src/main/java/org/apache/commons/io/function/IOStreamTerminal.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_INTERFACE",
        "inputs": [
          "src/main/java/org/apache/commons/io/function/IOStream.java"
        ],
        "outputs": [
          "src/main/java/org/apache/commons/io/function/IOStreamTerminal.java"
        ],
        "details": "Create a new interface org.apache.commons.io.function.IOStreamTerminal<T> in the same package. The new interface will extend IOBaseStream<T, IOStream<T>, Stream<T>> and provide default implementations for terminal and terminal-like methods copied from IOStream: allMatch, anyMatch, collect(Collector), collect(IOSupplier, IOBiConsumer, IOBiConsumer), count, findAny, findFirst, forAll, forEach, forEachOrdered, toArray(), toArray(IntFunction), reduce variants (reduce(IOBinaryOperator), reduce(identity, IOBinaryOperator), reduce(identity, IOBiFunction, IOBinaryOperator)), max, min, noneMatch. The default implementations will be exact copies from IOStream so they rely on unwrap() from IOBaseStream and Erase helper methods already present in the project.",
        "risk": "low"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/io/function/IOStreamTerminal.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/apache/commons/io/function/IOStreamTerminal.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/io/function/IOStreamTerminal.java",
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
