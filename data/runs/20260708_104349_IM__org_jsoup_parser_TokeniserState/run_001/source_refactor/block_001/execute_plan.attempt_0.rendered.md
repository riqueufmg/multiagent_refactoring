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
  "repo_path": "/data/henrique/multiagent_refactoring/data/repositories/jsoup",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.jsoup.parser.TokeniserState"
  },
  "block": {
    "id": 1,
    "goal": "Introduce a new helper class to hold TokeniserState's static helper methods and related constants/arrays so the enum can be reduced in size and complexity.",
    "files": [
      "src/main/java/org/jsoup/parser/TokeniserStateHelpers.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/jsoup/parser/TokeniserState.java"
        ],
        "outputs": [
          "src/main/java/org/jsoup/parser/TokeniserStateHelpers.java"
        ],
        "details": "Create a new class org.jsoup.parser.TokeniserStateHelpers with the following static members copied from TokeniserState: nullChar, attributeNameCharsSorted, attributeValueUnquoted, replacementChar, replacementStr, eof, and the private static methods handleDataEndTag, readRawData, readCharRef, readEndTag, handleDataDoubleEscapeTag, readDoctypeInternalSubset. Place the new class in the same package (org.jsoup.parser). The implementations are identical copies so the project compiles after adding the helper class.",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/jsoup/parser/TokeniserStateHelpers.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/jsoup/parser/TokeniserStateHelpers.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/jsoup/parser/TokeniserStateHelpers.java",
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
