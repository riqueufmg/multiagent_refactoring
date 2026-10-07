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
  "target_name": "org.apache.commons.lang3.function",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260730_170432_GC__org_apache_commons_lang3_function/run_001/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/org/apache/commons/lang3/function/BooleanConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/ByteConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/ByteSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/Consumers.java",
    "src/main/java/org/apache/commons/lang3/function/Failable.java",
    "src/main/java/org/apache/commons/lang3/function/FailableBiConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableBiFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableBiPredicate.java",
    "src/main/java/org/apache/commons/lang3/function/FailableBooleanSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableByteConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableByteSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableCallable.java",
    "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleBinaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoublePredicate.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleToIntFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleToLongFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableDoubleUnaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntBinaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntPredicate.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntToDoubleFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntToFloatFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntToLongFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableIntUnaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongBinaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongPredicate.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongToDoubleFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongToIntFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableLongUnaryOperator.java",
    "src/main/java/org/apache/commons/lang3/function/FailableObjDoubleConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableObjIntConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailableObjLongConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/FailablePredicate.java",
    "src/main/java/org/apache/commons/lang3/function/FailableRunnable.java",
    "src/main/java/org/apache/commons/lang3/function/FailableShortSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableSupplier.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToBooleanFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToDoubleBiFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToDoubleFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToIntBiFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToIntFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToLongBiFunction.java",
    "src/main/java/org/apache/commons/lang3/function/FailableToLongFunction.java",
    "src/main/java/org/apache/commons/lang3/function/Functions.java",
    "src/main/java/org/apache/commons/lang3/function/IntToCharFunction.java",
    "src/main/java/org/apache/commons/lang3/function/MethodInvokers.java",
    "src/main/java/org/apache/commons/lang3/function/Predicates.java",
    "src/main/java/org/apache/commons/lang3/function/Suppliers.java",
    "src/main/java/org/apache/commons/lang3/function/ToBooleanBiFunction.java",
    "src/main/java/org/apache/commons/lang3/function/TriConsumer.java",
    "src/main/java/org/apache/commons/lang3/function/TriFunction.java",
    "src/main/java/org/apache/commons/lang3/function/package-info.java"
  ],
  "internal_deps": [
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableDoubleConsumer"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableIntConsumer"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableLongConsumer"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableBiFunction"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableFunction"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableDoubleBinaryOperator"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableBiPredicate"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableCallable"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailablePredicate"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableRunnable"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableBooleanSupplier"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableDoubleSupplier"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableIntSupplier"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableLongSupplier"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.function.FailableShortSupplier"
    ],
    [
      "org.apache.commons.lang3.function.MethodInvokers",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.function.MethodInvokers",
      "org.apache.commons.lang3.function.FailableBiFunction"
    ],
    [
      "org.apache.commons.lang3.function.MethodInvokers",
      "org.apache.commons.lang3.function.FailableFunction"
    ],
    [
      "org.apache.commons.lang3.function.MethodInvokers",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.function.FailableBiFunction",
      "org.apache.commons.lang3.function.FailableFunction"
    ]
  ],
  "incoming_deps": [
    [
      "org.apache.commons.lang3.event.EventListenerSupport.ProxyInvocationHandler",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.AppendableJoiner",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.ObjectUtils",
      "org.apache.commons.lang3.function.Suppliers"
    ],
    [
      "org.apache.commons.lang3.time.StopWatch",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.time.StopWatch",
      "org.apache.commons.lang3.function.FailableRunnable"
    ],
    [
      "org.apache.commons.lang3.concurrent.AbstractConcurrentInitializer.AbstractBuilder",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.concurrent.AbstractConcurrentInitializer.AbstractBuilder",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.ArrayFill",
      "org.apache.commons.lang3.function.FailableIntFunction"
    ],
    [
      "org.apache.commons.lang3.AppendableJoiner.Builder",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.concurrent.AtomicSafeInitializer",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.concurrent.AtomicSafeInitializer",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.SystemProperties",
      "org.apache.commons.lang3.function.Suppliers"
    ],
    [
      "org.apache.commons.lang3.time.DurationUtils",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.time.DurationUtils",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.time.DurationUtils",
      "org.apache.commons.lang3.function.FailableRunnable"
    ],
    [
      "org.apache.commons.lang3.event.EventListenerSupport",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.Strings",
      "org.apache.commons.lang3.function.ToBooleanBiFunction"
    ],
    [
      "org.apache.commons.lang3.ArrayUtils",
      "org.apache.commons.lang3.function.FailableFunction"
    ],
    [
      "org.apache.commons.lang3.AutoCloseables",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.AutoCloseables",
      "org.apache.commons.lang3.function.Consumers"
    ],
    [
      "org.apache.commons.lang3.StringUtils",
      "org.apache.commons.lang3.function.Suppliers"
    ],
    [
      "org.apache.commons.lang3.ThreadUtils",
      "org.apache.commons.lang3.function.Predicates"
    ],
    [
      "org.apache.commons.lang3.concurrent.AbstractConcurrentInitializer",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.concurrent.AbstractConcurrentInitializer",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.concurrent.BackgroundInitializer",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.concurrent.BackgroundInitializer",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.Functions",
      "org.apache.commons.lang3.function.FailableBooleanSupplier"
    ],
    [
      "org.apache.commons.lang3.Functions",
      "org.apache.commons.lang3.function.FailableRunnable"
    ],
    [
      "org.apache.commons.lang3.Functions",
      "org.apache.commons.lang3.function.Failable"
    ],
    [
      "org.apache.commons.lang3.concurrent.AtomicInitializer",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.concurrent.AtomicInitializer",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.concurrent.LazyInitializer",
      "org.apache.commons.lang3.function.FailableSupplier"
    ],
    [
      "org.apache.commons.lang3.concurrent.LazyInitializer",
      "org.apache.commons.lang3.function.FailableConsumer"
    ],
    [
      "org.apache.commons.lang3.tuple.Pair",
      "org.apache.commons.lang3.function.FailableBiConsumer"
    ],
    [
      "org.apache.commons.lang3.tuple.Pair",
      "org.apache.commons.lang3.function.FailableBiFunction"
    ]
  ],
  "outgoing_deps": [
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.exception.ExceptionUtils"
    ],
    [
      "org.apache.commons.lang3.function.Failable",
      "org.apache.commons.lang3.stream.Streams"
    ]
  ]
}
```