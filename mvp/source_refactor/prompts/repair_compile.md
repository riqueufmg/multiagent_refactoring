## CONTEXT

A refactoring block was applied to a Java project, but the configured Maven build failed.

The goal of this step is to repair the current workspace so that the applied refactoring block compiles and passes the configured build command.

This is a repair step, not a new refactoring step.

## TASK

Fix only the errors reported in the build log.

Use the current code state, the staged block, the files already changed by the executor, and the files mentioned by the build log to produce a minimal repair.

Do not redo the refactoring from scratch.

Do not change the refactoring strategy.

Do not undo the refactoring unless that is the smallest safe repair.

## CONSTRAINTS

- Modify only files listed in allowed_files.
- Return the full new content for every modified file.
- Do not return partial patches.
- Do not edit unrelated files.
- Do not edit unrelated tests.
- Do not remove tests.
- Do not weaken assertions.
- Do not change expected behavior to match a broken implementation.
- Do not introduce compatibility wrappers unless they are necessary to make the current refactoring compile.
- Do not undo previous successful blocks.
- If the error cannot be safely repaired using only allowed_files, return an empty files_to_write list and explain why in notes.
- Return only files that actually changed.
- Do not include unchanged files in files_to_write.

## INPUT

{input}

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