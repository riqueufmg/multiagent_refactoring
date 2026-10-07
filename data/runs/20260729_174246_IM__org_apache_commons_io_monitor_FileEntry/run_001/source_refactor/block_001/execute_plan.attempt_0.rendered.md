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
    "target_name": "org.apache.commons.io.monitor.FileEntry"
  },
  "block": {
    "id": 1,
    "goal": "Extract a cohesive File state holder to reduce the number of fields and related accessors in FileEntry. Move the file attribute fields and their getters/setters/refresh logic into a new FileEntryAttributes class in the same package.",
    "files": [
      "src/main/java/org/apache/commons/io/monitor/FileEntryAttributes.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/apache/commons/io/monitor/FileEntry.java:fields:name,exists,directory,lastModified,length",
          "src/main/java/org/apache/commons/io/monitor/FileEntry.java:methods:getLastModified(),getLastModifiedFileTime(),getLength(),getName(),isDirectory(),isExists(),setLastModified(FileTime),setLastModified(long),setLastModified(SerializableFileTime) [package-private],setLength(long),setName(String),setDirectory(boolean),setExists(boolean),refresh(File)"
        ],
        "outputs": [
          "src/main/java/org/apache/commons/io/monitor/FileEntryAttributes.java"
        ],
        "details": "Create a new class FileEntryAttributes in package org.apache.commons.io.monitor. The class will encapsulate the following fields: String name; boolean exists; boolean directory; SerializableFileTime lastModified; long length. It will provide the moved accessors and mutators: getName(), setName(String), isExists(), setExists(boolean), isDirectory(), setDirectory(boolean), getLastModified(), getLastModifiedFileTime(), setLastModified(FileTime), setLastModified(long), setLastModified(SerializableFileTime) (package-private or public as needed), getLength(), setLength(long). Move the refresh(File) implementation that reads the File to update these fields and returns a boolean indicating change (use Files.exists(file.toPath()), file.isDirectory(), FileUtils.lastModifiedFileTime(file) and file.length()). The class will import java.io.File, java.io.IOException, java.nio.file.Files, java.nio.file.attribute.FileTime and org.apache.commons.io.FileUtils and org.apache.commons.io.file.attribute.FileTimes and will use SerializableFileTime the same way as FileEntry. Put the new file in the same package (org.apache.commons.io.monitor). Ensure exception handling mirrors the original refresh implementation.",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/org/apache/commons/io/monitor/FileEntryAttributes.java"
  ],
  "executor_existing_files": [],
  "executor_new_files": [
    "src/main/java/org/apache/commons/io/monitor/FileEntryAttributes.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/apache/commons/io/monitor/FileEntryAttributes.java",
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
