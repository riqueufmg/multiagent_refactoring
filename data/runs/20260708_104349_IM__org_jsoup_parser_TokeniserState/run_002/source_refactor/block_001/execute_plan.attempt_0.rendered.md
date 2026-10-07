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
    "goal": "Extract static helper fields and methods from the large enum into a dedicated helper class to group cohesive parsing utilities and reduce the size/complexity of TokeniserState.",
    "files": [
      "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/jsoup/parser/TokeniserState.java"
        ],
        "outputs": [
          "src/main/java/org/jsoup/parser/TokeniserStateHelper.java"
        ],
        "details": "Create a new class org.jsoup.parser.TokeniserStateHelper and copy the following static members from TokeniserState into it (preserve signatures and visibility as package-private or private static as appropriate):\n- static final char nullChar\n- static final char[] attributeNameCharsSorted\n- static final char[] attributeValueUnquoted\n- private static final char replacementChar\n- private static final String replacementStr\n- private static final char eof\n- private static void handleDataEndTag(Tokeniser t, CharacterReader r, TokeniserState elseTransition)\n- private static void readRawData(Tokeniser t, CharacterReader r, TokeniserState current, TokeniserState advance)\n- private static void readCharRef(Tokeniser t, TokeniserState advance)\n- private static void readEndTag(Tokeniser t, CharacterReader r, TokeniserState a, TokeniserState b)\n- private static void handleDataDoubleEscapeTag(Tokeniser t, CharacterReader r, TokeniserState primary, TokeniserState fallback)\n- private static void readDoctypeInternalSubset(Tokeniser t, CharacterReader r, TokeniserState current)\nPlace the class in package org.jsoup.parser. Keep references to Tokeniser, CharacterReader, TokeniserState, TokenData, Token, Tokeniser.replacementChar, StringUtil and DocumentType as in the original file.",
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
