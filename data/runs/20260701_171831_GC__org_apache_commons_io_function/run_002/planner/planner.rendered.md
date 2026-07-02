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
  "target_name": "org.apache.commons.io.function",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260701_171831_GC__org_apache_commons_io_function/run_002/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/org/apache/commons/io/function/Constants.java",
    "src/main/java/org/apache/commons/io/function/Erase.java",
    "src/main/java/org/apache/commons/io/function/IOBaseStream.java",
    "src/main/java/org/apache/commons/io/function/IOBaseStreamAdapter.java",
    "src/main/java/org/apache/commons/io/function/IOBiConsumer.java",
    "src/main/java/org/apache/commons/io/function/IOBiFunction.java",
    "src/main/java/org/apache/commons/io/function/IOBinaryOperator.java",
    "src/main/java/org/apache/commons/io/function/IOBooleanSupplier.java",
    "src/main/java/org/apache/commons/io/function/IOComparator.java",
    "src/main/java/org/apache/commons/io/function/IOConsumer.java",
    "src/main/java/org/apache/commons/io/function/IOFunction.java",
    "src/main/java/org/apache/commons/io/function/IOIntConsumer.java",
    "src/main/java/org/apache/commons/io/function/IOIntSupplier.java",
    "src/main/java/org/apache/commons/io/function/IOIterable.java",
    "src/main/java/org/apache/commons/io/function/IOIterator.java",
    "src/main/java/org/apache/commons/io/function/IOIteratorAdapter.java",
    "src/main/java/org/apache/commons/io/function/IOLongSupplier.java",
    "src/main/java/org/apache/commons/io/function/IOPredicate.java",
    "src/main/java/org/apache/commons/io/function/IOQuadFunction.java",
    "src/main/java/org/apache/commons/io/function/IORunnable.java",
    "src/main/java/org/apache/commons/io/function/IOSpliterator.java",
    "src/main/java/org/apache/commons/io/function/IOSpliteratorAdapter.java",
    "src/main/java/org/apache/commons/io/function/IOStream.java",
    "src/main/java/org/apache/commons/io/function/IOStreamAdapter.java",
    "src/main/java/org/apache/commons/io/function/IOStreams.java",
    "src/main/java/org/apache/commons/io/function/IOSupplier.java",
    "src/main/java/org/apache/commons/io/function/IOTriConsumer.java",
    "src/main/java/org/apache/commons/io/function/IOTriFunction.java",
    "src/main/java/org/apache/commons/io/function/IOUnaryOperator.java",
    "src/main/java/org/apache/commons/io/function/Uncheck.java",
    "src/main/java/org/apache/commons/io/function/UncheckedIOBaseStream.java",
    "src/main/java/org/apache/commons/io/function/UncheckedIOIterable.java",
    "src/main/java/org/apache/commons/io/function/UncheckedIOIterator.java",
    "src/main/java/org/apache/commons/io/function/UncheckedIOSpliterator.java",
    "src/main/java/org/apache/commons/io/function/package-info.java"
  ],
  "internal_deps": [
    [
      "org.apache.commons.io.function.UncheckedIOSpliterator",
      "org.apache.commons.io.function.IOSpliterator"
    ],
    [
      "org.apache.commons.io.function.UncheckedIOSpliterator",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOIntSupplier",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOComparator",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.Constants",
      "org.apache.commons.io.function.IOTriConsumer"
    ],
    [
      "org.apache.commons.io.function.IOUnaryOperator",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOBinaryOperator",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.IOBinaryOperator",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOIntConsumer"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOTriConsumer"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOQuadFunction"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOTriFunction"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOBooleanSupplier"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOIntSupplier"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOLongSupplier"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.Uncheck",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.IOConsumer",
      "org.apache.commons.io.function.IOStreams"
    ],
    [
      "org.apache.commons.io.function.IOConsumer",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOIterable",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOIterable",
      "org.apache.commons.io.function.IOIterator"
    ],
    [
      "org.apache.commons.io.function.IOIterable",
      "org.apache.commons.io.function.IOSpliterator"
    ],
    [
      "org.apache.commons.io.function.IOIterable",
      "org.apache.commons.io.function.IOSpliteratorAdapter"
    ],
    [
      "org.apache.commons.io.function.IOIntStreamAdapter",
      "org.apache.commons.io.function.IOIntStream"
    ],
    [
      "org.apache.commons.io.function.IORunnable",
      "org.apache.commons.io.function.Constants"
    ],
    [
      "org.apache.commons.io.function.IORunnable",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.Erase",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.IOIterator"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.IOSpliterator"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.IOIteratorAdapter"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.function.IOBaseStream",
      "org.apache.commons.io.function.IOSpliteratorAdapter"
    ],
    [
      "org.apache.commons.io.function.IOBiConsumer",
      "org.apache.commons.io.function.Constants"
    ],
    [
      "org.apache.commons.io.function.IOBiConsumer",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOBinaryOperator"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOBooleanSupplier"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOIntConsumer"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOIntSupplier"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOLongSupplier"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOQuadFunction"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOTriConsumer"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOTriFunction"
    ],
    [
      "org.apache.commons.io.function.TestConstants",
      "org.apache.commons.io.function.IOUnaryOperator"
    ],
    [
      "org.apache.commons.io.function.UncheckedIOBaseStream",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOFunction",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOFunction",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.IOFunction",
      "org.apache.commons.io.function.Constants"
    ],
    [
      "org.apache.commons.io.function.IOFunction",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOStreams",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOStreams",
      "org.apache.commons.io.function.IOStream"
    ],
    [
      "org.apache.commons.io.function.IOStreams",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.function.UncheckedIOIterable",
      "org.apache.commons.io.function.IOIterable"
    ],
    [
      "org.apache.commons.io.function.IOSpliterator",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOSpliterator",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.IOSpliterator",
      "org.apache.commons.io.function.IOSpliteratorAdapter"
    ],
    [
      "org.apache.commons.io.function.IOBiFunction",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.IOBiFunction",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOUnaryOperator"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOBinaryOperator"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOStreams"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.IOStreamAdapter"
    ],
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.function.UncheckedIOIterator",
      "org.apache.commons.io.function.IOIterator"
    ],
    [
      "org.apache.commons.io.function.UncheckedIOIterator",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOBooleanSupplier",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOSupplier",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOIntConsumer",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOTriConsumer",
      "org.apache.commons.io.function.Constants"
    ],
    [
      "org.apache.commons.io.function.IOTriFunction",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.IOLongSupplier",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOPredicate",
      "org.apache.commons.io.function.Constants"
    ],
    [
      "org.apache.commons.io.function.IOPredicate",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.function.IOQuadFunction",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.IOStreamAdapter",
      "org.apache.commons.io.function.IOStream"
    ],
    [
      "org.apache.commons.io.function.IOIterator",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.IOIterator",
      "org.apache.commons.io.function.IOIteratorAdapter"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOBinaryOperator"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOComparator"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOIntConsumer"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOPredicate"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IORunnable"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.IOUnaryOperator"
    ],
    [
      "org.apache.commons.io.function.TestUtils",
      "org.apache.commons.io.function.TestConstants"
    ]
  ],
  "incoming_deps": [
    [
      "org.apache.commons.io.input.ProxyInputStream",
      "org.apache.commons.io.function.IOIntConsumer"
    ],
    [
      "org.apache.commons.io.output.FilterCollectionWriter",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.input.CloseShieldInputStream",
      "org.apache.commons.io.function.IOUnaryOperator"
    ],
    [
      "org.apache.commons.io.file.FilesUncheck",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.input.XmlStreamReader",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.output.UnsynchronizedByteArrayOutputStream",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.input.CharSequenceInputStream",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.file.SimplePathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.input.UncheckedFilterReader",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.file.AccumulatorPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.input.SequenceReader",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.input.ObservableInputStream",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.file.CountingPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.file.PathUtils",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.input.ProxyInputStream.AbstractBuilder",
      "org.apache.commons.io.function.IOIntConsumer"
    ],
    [
      "org.apache.commons.io.output.UncheckedAppendableImpl",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.IOUtils",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.IOUtils",
      "org.apache.commons.io.function.IOTriFunction"
    ],
    [
      "org.apache.commons.io.IOUtils",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.input.BrokenInputStream",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.input.BoundedInputStream.AbstractBuilder",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.filefilter.AbstractFileFilter",
      "org.apache.commons.io.function.IOSupplier"
    ],
    [
      "org.apache.commons.io.file.SimplePathVisitor.AbstractBuilder",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.input.BoundedInputStream",
      "org.apache.commons.io.function.IOBiConsumer"
    ],
    [
      "org.apache.commons.io.output.UncheckedFilterWriter",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.output.BrokenOutputStream",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.input.UncheckedBufferedReader",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.input.CloseShieldInputStream.Builder",
      "org.apache.commons.io.function.IOUnaryOperator"
    ],
    [
      "org.apache.commons.io.output.UncheckedFilterOutputStream",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.output.BrokenWriter",
      "org.apache.commons.io.function.Erase"
    ],
    [
      "org.apache.commons.io.output.ThresholdingOutputStream",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.output.ThresholdingOutputStream",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.file.NoopPathVisitor",
      "org.apache.commons.io.function.IOBiFunction"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.FileUtils",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.input.UncheckedFilterInputStream",
      "org.apache.commons.io.function.Uncheck"
    ],
    [
      "org.apache.commons.io.RandomAccessFileMode",
      "org.apache.commons.io.function.IOConsumer"
    ],
    [
      "org.apache.commons.io.RandomAccessFileMode",
      "org.apache.commons.io.function.IOFunction"
    ],
    [
      "org.apache.commons.io.input.BrokenReader",
      "org.apache.commons.io.function.Erase"
    ]
  ],
  "outgoing_deps": [
    [
      "org.apache.commons.io.function.IOStream",
      "org.apache.commons.io.IOExceptionList"
    ]
  ]
}
```