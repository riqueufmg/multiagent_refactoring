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
    "target_name": "org.apache.commons.io.EndianUtils"
  },
  "block": {
    "id": 3,
    "goal": "Update call sites in the codebase that prefer to use the new focused helper classes directly (optional / lower-priority). This reduces coupling to EndianUtils for stream or swap specific operations.",
    "files": [
      "all project source files that reference org.apache.commons.io.EndianUtils"
    ],
    "ops": [
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "calls to EndianUtils.readSwappedDouble(InputStream)",
          "calls to EndianUtils.readSwappedFloat(InputStream)",
          "calls to EndianUtils.readSwappedInteger(InputStream)",
          "calls to EndianUtils.readSwappedLong(InputStream)",
          "calls to EndianUtils.readSwappedShort(InputStream)",
          "calls to EndianUtils.readSwappedUnsignedInteger(InputStream)",
          "calls to EndianUtils.readSwappedUnsignedShort(InputStream)",
          "calls to EndianUtils.writeSwappedDouble(OutputStream, double)",
          "calls to EndianUtils.writeSwappedFloat(OutputStream, float)",
          "calls to EndianUtils.writeSwappedInteger(OutputStream, int)",
          "calls to EndianUtils.writeSwappedLong(OutputStream, long)",
          "calls to EndianUtils.writeSwappedShort(OutputStream, short)",
          "calls to EndianUtils.swapDouble(double)",
          "calls to EndianUtils.swapFloat(float)",
          "calls to EndianUtils.swapInteger(int)",
          "calls to EndianUtils.swapLong(long)",
          "calls to EndianUtils.swapShort(short)"
        ],
        "outputs": [
          "updated call sites (optional) to use EndianUtilsStream.* or EndianUtilsSwap.* where callers prefer the specialized helper"
        ],
        "details": "Optionally update external callers to reference the new classes directly (EndianUtilsStream and EndianUtilsSwap) when they only need stream-based or swap operations. This reduces the surface area of EndianUtils usage in the codebase. Because EndianUtils retains delegating methods, external update is optional and backward compatible; perform updates where it improves modularization and readability.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [],
  "executor_existing_files": [],
  "executor_new_files": [],
  "executor_rejected_files": [
    "all project source files that reference org.apache.commons.io.EndianUtils"
  ],
  "files_context": [],
  "feedback": "EXECUTOR_NO_CHANGES: The executor returned valid JSON, but produced no files_to_write or files_to_delete. Revise the same block and generate concrete file changes.",
  "attempt": 1,
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
