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
    "goal": "Introduce a helper class to host the large, cohesive private static helper routines from TokeniserState to reduce the size and complexity of the enum.",
    "files": [
      "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/jsoup/parser/TokeniserState.java::handleDataEndTag",
          "src/main/java/org/jsoup/parser/TokeniserState.java::readRawData",
          "src/main/java/org/jsoup/parser/TokeniserState.java::readCharRef",
          "src/main/java/org/jsoup/parser/TokeniserState.java::readEndTag",
          "src/main/java/org/jsoup/parser/TokeniserState.java::handleDataDoubleEscapeTag",
          "src/main/java/org/jsoup/parser/TokeniserState.java::readDoctypeInternalSubset"
        ],
        "outputs": [
          "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
        ],
        "details": "Create a new class org.jsoup.parser.TokeniserStateHelper in the same package and copy the six private static methods from TokeniserState into it as public static methods with identical signatures: handleDataEndTag(Tokeniser, CharacterReader, TokeniserState), readRawData(Tokeniser, CharacterReader, TokeniserState, TokeniserState), readCharRef(Tokeniser, TokeniserState), readEndTag(Tokeniser, CharacterReader, TokeniserState, TokeniserState), handleDataDoubleEscapeTag(Tokeniser, CharacterReader, TokeniserState, TokeniserState), readDoctypeInternalSubset(Tokeniser, CharacterReader, TokeniserState). Add the necessary imports used by these methods (org.jsoup.internal.StringUtil and org.jsoup.nodes.DocumentType as in the original file). The implementations should reference Tokeniser.replacementChar and CharacterReader.EOF directly where needed (instead of relying on TokeniserState's private constants).",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/jsoup/parser/TokeniserStateHelper.java",
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
