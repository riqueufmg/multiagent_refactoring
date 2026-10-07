# GOAL
Refactor ONE cohesive cluster from the TARGET PACKAGE to reduce the God Component smell.

A single run must move only ONE cluster. All classes in the selected cluster must be moved to the SAME new subpackage.

# INPUT DATA
- `target_files`: files currently in the target package.
- `internal_deps`: dependencies between classes inside the target package.
- `incoming_deps`: external classes that depend on classes in the target package.
- `outgoing_deps`: target package classes depending on external classes.

# TASK
Choose exactly ONE cohesive cluster of classes from the target package.

Then generate a refactoring plan where:
- all classes in the cluster move to the same new subpackage;
- the plan contains exactly ONE block;
- that block moves all classes in the selected cluster together;
- the block contains 2 to 10 MOVE_CLASS operations.

# CLUSTER MOVEMENT STRATEGY

For God Component refactoring, each block must move one cohesive cluster, not a single isolated class.

A cluster must contain 2 to 4 classes.

All classes in the selected cluster must be moved to the same destination package.

Prefer clusters whose classes have strong internal relationships and many package-private interactions with each other.

Avoid moving highly central parser/state-machine classes alone.

Avoid selecting clusters that would require exposing many package-private members from classes that remain in the original package.

Each block must contain:
- optionally one CREATE_PACKAGE operation;
- two to four MOVE_CLASS operations;
- no UPDATE_VISIBILITY operation. UPDATE_VISIBILITY will be added automatically later.

Do not create one block per class.

Do not move all package classes in one block.

Prefer small cohesive clusters that can compile after limited visibility updates.

# PACKAGE RULES
- Move classes only from the TARGET PACKAGE to a subpackage of the TARGET PACKAGE.
- All moved classes must use the same destination package.
- Do not move classes to unrelated packages.
- Do not introduce facades.
- API changes are allowed.

# BLOCK RULES
- The plan must contain exactly ONE block.
- This single block represents the whole selected cluster.
- The block must contain 2 to 4 MOVE_CLASS operations.
- All MOVE_CLASS operations must move classes to the same destination package.
- The block may include one CREATE_PACKAGE operation before the MOVE_CLASS operations.
- The block files list must include the original source file path of every moved class.
- Do not create one block per class.
- Do not split the selected cluster across multiple blocks.
- Do not update external files in the plan; OpenRewrite will handle references/imports later.
- The executor will handle minimal package-private visibility changes in related internal files.

# ALLOWED OPS
CREATE_PACKAGE, MOVE_CLASS, ADD_OR_UPDATE_IMPORTS, UPDATE_CALL_SITES, UPDATE_VISIBILITY, NO_OP.

# OUTPUT
Return ONLY valid JSON.

{
  "smell_type": "<copied from input>",
  "target_level": "package",
  "target": "<target_name from input>",
  "selected_cluster": [
    "<class FQN>"
  ],
  "destination_package": "<new subpackage FQN>",
  "cluster_reason": "<why this cluster is cohesive and relatively safe>",
  "risk": "low|medium|high",
  "blocks": [
    {
      "id": 1,
      "goal": "Move one class from the selected cluster.",
      "files": [
        "<source file path from target_files>"
      ],
      "ops": [
        {
          "op": "CREATE_PACKAGE",
          "inputs": [],
          "outputs": ["<destination package FQN>"],
          "details": "Create the destination subpackage if it does not exist.",
          "risk": "low",
          "api_change": false
        },
        {
          "op": "MOVE_CLASS",
          "inputs": ["<old class FQN>"],
          "outputs": ["<new class FQN>"],
          "details": "Move this class to the destination package.",
          "risk": "low|medium|high",
          "api_change": true
        }
      ]
    }
  ]
}

# INPUT
```json
{
  "smell": "God Component",
  "target_type": "package",
  "target_name": "org.apache.commons.io.file",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260730_184144_GC__org_apache_commons_io_file/run_002/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/org/apache/commons/io/file/AccumulatorPathVisitor.java",
    "src/main/java/org/apache/commons/io/file/CleaningPathVisitor.java",
    "src/main/java/org/apache/commons/io/file/CopyDirectoryVisitor.java",
    "src/main/java/org/apache/commons/io/file/Counters.java",
    "src/main/java/org/apache/commons/io/file/CountingPathVisitor.java",
    "src/main/java/org/apache/commons/io/file/DeleteOption.java",
    "src/main/java/org/apache/commons/io/file/DeletingPathVisitor.java",
    "src/main/java/org/apache/commons/io/file/DirectoryStreamFilter.java",
    "src/main/java/org/apache/commons/io/file/FilesUncheck.java",
    "src/main/java/org/apache/commons/io/file/NoopPathVisitor.java",
    "src/main/java/org/apache/commons/io/file/PathFilter.java",
    "src/main/java/org/apache/commons/io/file/PathUtils.java",
    "src/main/java/org/apache/commons/io/file/PathVisitor.java",
    "src/main/java/org/apache/commons/io/file/SimplePathVisitor.java",
    "src/main/java/org/apache/commons/io/file/StandardDeleteOption.java",
    "src/main/java/org/apache/commons/io/file/package-info.java"
  ],
  "internal_deps": [
    [
      "org.apache.commons.io.file.CounterAssertions",
      "org.apache.commons.io.file.CountingPathVisitor"
    ],
    [
      "org.apache.commons.io.file.CounterAssertions",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.file.SimplePathVisitor"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.DeletablePath",
      "org.apache.commons.io.file.DeleteOption"
    ],
    [
      "org.apache.commons.io.file.DeletablePath",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.DeletingPathVisitor",
      "org.apache.commons.io.file.DeleteOption"
    ],
    [
      "org.apache.commons.io.file.DeletingPathVisitor",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.DeletingPathVisitor",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.DeletingPathVisitor",
      "org.apache.commons.io.file.StandardDeleteOption"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.DeleteOption"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.AccumulatorPathVisitor"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.StandardDeleteOption"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.CountingPathVisitor"
    ],
    [
      "org.apache.commons.io.file.TestArguments",
      "org.apache.commons.io.file.CleaningPathVisitor"
    ],
    [
      "org.apache.commons.io.file.TestArguments",
      "org.apache.commons.io.file.CountingPathVisitor"
    ],
    [
      "org.apache.commons.io.file.TestArguments",
      "org.apache.commons.io.file.DeletingPathVisitor"
    ],
    [
      "org.apache.commons.io.file.TestArguments",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.DirectoryStreamFilter",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.DirectoryStreamFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.StandardDeleteOption",
      "org.apache.commons.io.file.DeleteOption"
    ],
    [
      "org.apache.commons.io.file.CleaningPathVisitor",
      "org.apache.commons.io.file.CountingPathVisitor"
    ],
    [
      "org.apache.commons.io.file.CleaningPathVisitor",
      "org.apache.commons.io.file.DeleteOption"
    ],
    [
      "org.apache.commons.io.file.CleaningPathVisitor",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.CleaningPathVisitor",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.file.CleaningPathVisitor",
      "org.apache.commons.io.file.StandardDeleteOption"
    ],
    [
      "org.apache.commons.io.file.CopyDirectoryVisitor",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.CopyDirectoryVisitor",
      "org.apache.commons.io.file.PathUtils"
    ]
  ],
  "incoming_deps": [
    [
      "org.apache.commons.io.output.DeferredFileOutputStream",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.filefilter.PrefixFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.filefilter.NameFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor.AbstractBuilder",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor.AbstractBuilder",
      "org.apache.commons.io.file.SimplePathVisitor"
    ],
    [
      "org.apache.commons.io.filefilter.PathVisitorFileFilter",
      "org.apache.commons.io.file.PathVisitor"
    ],
    [
      "org.apache.commons.io.filefilter.PathVisitorFileFilter",
      "org.apache.commons.io.file.NoopPathVisitor"
    ],
    [
      "org.apache.commons.io.filefilter.PathVisitorFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.jmh.PathUtilsContentEqualsBenchmark",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.build.AbstractStreamBuilder",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.filefilter.WildcardFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.filefilter.WildcardFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.file.Counters"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.file.PathFilter"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.file.AccumulatorPathVisitor"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.file.StandardDeleteOption"
    ],
    [
      "org.apache.commons.io.filefilter.AgeFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ],
    [
      "org.apache.commons.io.filefilter.SuffixFileFilter",
      "org.apache.commons.io.file.PathUtils"
    ]
  ],
  "outgoing_deps": [
    [
      "org.apache.commons.io.file.Counters",
      "org.apache.commons.io.file.Counters.Counter"
    ],
    [
      "org.apache.commons.io.file.Counters",
      "org.apache.commons.io.file.Counters.NoopCounter"
    ],
    [
      "org.apache.commons.io.file.Counters",
      "org.apache.commons.io.file.Counters.NoopPathCounters"
    ],
    [
      "org.apache.commons.io.file.Counters",
      "org.apache.commons.io.file.Counters.PathCounters"
    ],
    [
      "org.apache.commons.io.file.NoopPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.file.CountingPathVisitor.AbstractBuilder"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.filefilter.TrueFileFilter"
    ],
    [
      "org.apache.commons.io.file.FilesUncheck",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.PathUtils.RelativeSortedPaths"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.RandomAccessFileMode"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.FilenameUtils"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.RandomAccessFiles"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.IOUtils"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.FileUtils"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.Charsets"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.file.attribute.FileTimes"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.ThreadUtils"
    ],
    [
      "org.apache.commons.io.file.SimplePathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.file.SimplePathVisitor",
      "org.apache.commons.io.file.SimplePathVisitor.AbstractBuilder"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.file.AccumulatorPathVisitor.Builder"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.file.StandardDeleteOption",
      "org.apache.commons.io.IOUtils"
    ]
  ]
}
```