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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/accumulo/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.apache.accumulo.tserver.tablet.CompactableUtils"
  },
  "block": {
    "id": 3,
    "goal": "Reduce the remaining orchestration responsibility of CompactableUtils by delegating compaction override resolution to the extracted compaction utility.",
    "files": [
      "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
    ],
    "ops": [
      {
        "op": "REPLACE_DEPENDENCY",
        "inputs": [
          "org.apache.accumulo.tserver.tablet.CompactableUtils",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils"
        ],
        "outputs": [],
        "details": "Replace the direct dependency on the extracted getOverrides implementation in CompactableUtils.compact with CompactableCompactionUtils.getOverrides, leaving CompactableUtils responsible only for FileCompactor construction, compaction execution, and bringing files online.",
        "risk": "low"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
        ],
        "outputs": [],
        "details": "Remove imports used exclusively by the extracted compaction plugin logic and retain only imports required by compact, bringOnline, and the remaining class members.",
        "risk": "low"
      }
    ]
  },
  "allowed_files": [
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
  ],
  "executor_existing_files": [
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
  ],
  "executor_new_files": [],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.tserver.tablet;\n\nimport java.io.IOException;\nimport java.util.Collection;\nimport java.util.Map;\nimport java.util.Optional;\nimport java.util.Set;\n\nimport org.apache.accumulo.core.client.admin.CompactionConfig;\nimport org.apache.accumulo.core.client.admin.PluginConfig;\nimport org.apache.accumulo.core.client.admin.compaction.CompactableFile;\nimport org.apache.accumulo.core.conf.AccumuloConfiguration;\nimport org.apache.accumulo.core.conf.ConfigurationCopy;\nimport org.apache.accumulo.core.data.Key;\nimport org.apache.accumulo.core.dataImpl.KeyExtent;\nimport org.apache.accumulo.core.metadata.ReferencedTabletFile;\nimport org.apache.accumulo.core.metadata.StoredTabletFile;\nimport org.apache.accumulo.core.metadata.schema.DataFileValue;\nimport org.apache.accumulo.core.spi.compaction.CompactionJob;\nimport org.apache.accumulo.core.spi.compaction.CompactionKind;\nimport org.apache.accumulo.core.util.Pair;\nimport org.apache.accumulo.server.compaction.CompactionStats;\nimport org.apache.accumulo.server.compaction.FileCompactor;\nimport org.apache.accumulo.server.compaction.FileCompactor.CompactionCanceledException;\nimport org.apache.accumulo.server.compaction.FileCompactor.CompactionEnv;\nimport org.apache.accumulo.server.conf.TableConfiguration;\n\npublic class CompactableUtils {\n\n  public static Map<StoredTabletFile,Pair<Key,Key>> getFirstAndLastKeys(Tablet tablet,\n      Set<StoredTabletFile> allFiles) throws IOException {\n    return CompactableFileUtils.getFirstAndLastKeys(tablet, allFiles);\n  }\n\n  public static Set<StoredTabletFile> findChopFiles(KeyExtent extent,\n      Map<StoredTabletFile,Pair<Key,Key>> firstAndLastKeys, Collection<StoredTabletFile> allFiles) {\n    return CompactableFileUtils.findChopFiles(extent, firstAndLastKeys, allFiles);\n  }\n\n  static Map<String,String> computeOverrides(Tablet tablet, Set<CompactableFile> files) {\n    return CompactableCompactionUtils.computeOverrides(tablet, files);\n  }\n\n  static Map<String,String> computeOverrides(Tablet tablet, Set<CompactableFile> files,\n      PluginConfig cfg) {\n    return CompactableCompactionUtils.computeOverrides(tablet, files, cfg);\n  }\n\n  static <T> T newInstance(AccumuloConfiguration tableConfig, String className,\n      Class<T> baseClass) {\n    return CompactableCompactionUtils.newInstance(tableConfig, className, baseClass);\n  }\n\n  static Set<StoredTabletFile> selectFiles(Tablet tablet,\n      java.util.SortedMap<StoredTabletFile,DataFileValue> datafiles, PluginConfig selectorConfig) {\n    return CompactableCompactionUtils.selectFiles(tablet, datafiles, selectorConfig);\n  }\n\n  public static CompactableImpl.CompactionHelper getHelper(CompactionKind kind, Tablet tablet,\n      Long compactionId, CompactionConfig compactionConfig) {\n    return CompactableCompactionUtils.getHelper(kind, tablet, compactionId, compactionConfig);\n  }\n\n  public static Map<String,String> getOverrides(CompactionKind kind, Tablet tablet,\n      CompactableImpl.CompactionHelper driver, Set<CompactableFile> files) {\n    return CompactableCompactionUtils.getOverrides(kind, tablet, driver, files);\n  }\n\n  private static AccumuloConfiguration getCompactionConfig(TableConfiguration tableConfiguration,\n      Map<String,String> overrides) {\n    if (overrides.isEmpty()) {\n      return tableConfiguration;\n    }\n    ConfigurationCopy copy = new ConfigurationCopy(tableConfiguration);\n    overrides.forEach((k, v) -> copy.set(k, v));\n    return copy;\n  }\n\n  static CompactionStats compact(Tablet tablet, CompactionJob job,\n      CompactableImpl.CompactionInfo cInfo, CompactionEnv cenv,\n      Map<StoredTabletFile,DataFileValue> compactFiles, ReferencedTabletFile tmpFileName)\n      throws IOException, CompactionCanceledException {\n    TableConfiguration tableConf = tablet.getTableConfiguration();\n    AccumuloConfiguration compactionConfig =\n        getCompactionConfig(tableConf, CompactableCompactionUtils.getOverrides(job.getKind(),\n            tablet, cInfo.localHelper, job.getFiles()));\n    FileCompactor compactor = new FileCompactor(tablet.getContext(), tablet.getExtent(),\n        compactFiles, tmpFileName, cInfo.propagateDeletes, cenv, cInfo.iters, compactionConfig,\n        tableConf.getCryptoService(), tablet.getPausedCompactionMetrics());\n    return compactor.call();\n  }\n\n  static Optional<StoredTabletFile> bringOnline(DatafileManager datafileManager,\n      CompactableImpl.CompactionInfo cInfo, CompactionStats stats,\n      Map<StoredTabletFile,DataFileValue> compactFiles, ReferencedTabletFile compactTmpName)\n      throws IOException {\n    var dfv = new DataFileValue(stats.getFileSize(), stats.getEntriesWritten());\n    return datafileManager.bringMajorCompactionOnline(compactFiles.keySet(), compactTmpName,\n        cInfo.checkCompactionId, cInfo.selectedFiles, dfv, Optional.empty());\n  }\n}\n"
    }
  ],
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
