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
    "target_name": "org.apache.commons.lang3.BitField"
  },
  "block": {
    "id": 1,
    "goal": "Extract long- and small-primitive-specific implementations out of BitField into a new helper class to reduce the size and complexity of BitField.",
    "files": [
      "src/main/java/org/apache/commons/lang3/BitFieldSupport.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/apache/commons/lang3/BitField.java: public BitField(final long mask)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long clear(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long getRawValue(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long getValue(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public boolean isAllSet(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public boolean isSet(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long set(final long holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long setBoolean(final long holder, final boolean flag)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public long setValue(final long holder, final long value)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public byte clearByte(final byte holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short clearShort(final short holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short getShortRawValue(final short holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short getShortValue(final short holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public byte setByte(final byte holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public byte setByteBoolean(final byte holder, final boolean flag)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short setShort(final short holder)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short setShortBoolean(final short holder, final boolean flag)",
          "src/main/java/org/apache/commons/lang3/BitField.java: public short setShortValue(final short holder, final short value)"
        ],
        "outputs": [
          "src/main/java/org/apache/commons/lang3/BitFieldSupport.java"
        ],
        "details": "Create a new helper class BitFieldSupport in package org.apache.commons.lang3. Move the implementations of the long-specific instance constructor and all long overloads, together with the byte/short wrapper implementations, into BitFieldSupport as static methods that accept mask and shiftCount (or the mask only where appropriate). The new class exposes static methods with signatures corresponding to the moved behavior, e.g. clearLong(long mask, int shiftCount, long holder) (or clearLong(long mask, long holder)), getRawValueLong(long mask, long holder), getValueLong(long mask, int shiftCount, long holder), setValueLong(long mask, int shiftCount, long holder, long value), and analogous methods for byte/short wrappers. This concentrates multi-type logic in one place and reduces BitField's implementation size.",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/lang3/BitFieldSupport.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/apache/commons/lang3/BitFieldSupport.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/lang3/BitFieldSupport.java",
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
