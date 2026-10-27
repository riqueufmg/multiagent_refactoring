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

Only top-level classes count toward cluster size and MOVE_CLASS operations. Inner and nested classes move implicitly with their enclosing class.

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
  "target_name": "tools.jackson.core.io",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261019_185202_GC__tools_jackson_core_io/run_001/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/tools/jackson/core/io/BigDecimalParser.java",
    "src/main/java/tools/jackson/core/io/BigIntegerParser.java",
    "src/main/java/tools/jackson/core/io/CharTypes.java",
    "src/main/java/tools/jackson/core/io/CharacterEscapes.java",
    "src/main/java/tools/jackson/core/io/ContentReference.java",
    "src/main/java/tools/jackson/core/io/DataOutputAsStream.java",
    "src/main/java/tools/jackson/core/io/IOContext.java",
    "src/main/java/tools/jackson/core/io/InputDecorator.java",
    "src/main/java/tools/jackson/core/io/JsonStringEncoder.java",
    "src/main/java/tools/jackson/core/io/MergedStream.java",
    "src/main/java/tools/jackson/core/io/NumberInput.java",
    "src/main/java/tools/jackson/core/io/NumberOutput.java",
    "src/main/java/tools/jackson/core/io/OutputDecorator.java",
    "src/main/java/tools/jackson/core/io/SegmentedStringWriter.java",
    "src/main/java/tools/jackson/core/io/SerializedString.java",
    "src/main/java/tools/jackson/core/io/UTF32Reader.java",
    "src/main/java/tools/jackson/core/io/UTF8Writer.java"
  ],
  "internal_deps": [
    [
      "tools.jackson.core.io.NumberInput",
      "tools.jackson.core.io.BigDecimalParser"
    ],
    [
      "tools.jackson.core.io.NumberInput",
      "tools.jackson.core.io.BigIntegerParser"
    ],
    [
      "tools.jackson.core.io.OutputDecorator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.MergedStream",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.io.TestJsonStringEncoder",
      "tools.jackson.core.io.JsonStringEncoder"
    ],
    [
      "tools.jackson.core.io.UTF8Writer",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.io.CharTypes",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.io.UTF32Reader",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.TestCharTypes",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.io.ContentReference",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.io.SerializedString",
      "tools.jackson.core.io.JsonStringEncoder"
    ],
    [
      "tools.jackson.core.io.JsonStringEncoder",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.io.JsonStringEncoder",
      "tools.jackson.core.io.UTF8Writer"
    ],
    [
      "tools.jackson.core.io.InputDecorator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.io.CharacterEscapes",
      "tools.jackson.core.io.CharTypes"
    ]
  ],
  "incoming_deps": [
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.NumberOutput"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingUtf8JsonParserBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingUtf8JsonParserBase",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping.MyEscapes",
      "tools.jackson.core.io.SerializedString"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping.MyEscapes",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.io.CharTypes.AltQuoteEscapes",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.TokenStreamFactory",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.TokenStreamFactory",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingByteArrayJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.base.TextualTSFactory",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.TextualTSFactory",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.TokenStreamContext",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.TokenStreamContext",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingByteBufferJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.TokenStreamLocation",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.util.TextBuffer",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.util.JsonpCharacterEscapes",
      "tools.jackson.core.io.SerializedString"
    ],
    [
      "tools.jackson.core.ObjectWriteContext",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.io.SerializedString"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.base.BinaryTSFactory",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.BinaryTSFactory",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.base.DecorableTSFactory",
      "tools.jackson.core.io.InputDecorator"
    ],
    [
      "tools.jackson.core.base.DecorableTSFactory",
      "tools.jackson.core.io.OutputDecorator"
    ],
    [
      "tools.jackson.core.base.DecorableTSFactory",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.util.JsonGeneratorDelegate",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.util.SimpleStreamReadContext",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.JsonGenerator",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.PrettyPrinter",
      "tools.jackson.core.io.SerializedString"
    ],
    [
      "tools.jackson.core.base.DecorableTSFactory.DecorableTSFBuilder",
      "tools.jackson.core.io.InputDecorator"
    ],
    [
      "tools.jackson.core.base.DecorableTSFactory.DecorableTSFBuilder",
      "tools.jackson.core.io.OutputDecorator"
    ],
    [
      "tools.jackson.core.base.ParserMinimalBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.ParserMinimalBase",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.io.MergedStream"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingJsonParserBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonReadContext",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.GeneratorBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.GeneratorBase",
      "tools.jackson.core.io.UTF8Writer"
    ],
    [
      "tools.jackson.core.base.ParserBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.base.ParserBase",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.base.ParserBase",
      "tools.jackson.core.io.ContentReference"
    ],
    [
      "tools.jackson.core.JsonPointer",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.NumberOutput"
    ],
    [
      "tools.jackson.core.testutil.JacksonTestUtilBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.testutil.JacksonTestUtilBase",
      "tools.jackson.core.io.ContentReference"
    ]
  ],
  "outgoing_deps": [
    [
      "tools.jackson.core.io.OutputDecorator",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.StreamWriteConstraints"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.StreamReadConstraints"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.ErrorReportConfiguration"
    ],
    [
      "tools.jackson.core.io.TestIOContext",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.io.TestJsonStringEncoder",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.io.TestJsonStringEncoder",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.io.TestJsonStringEncoder",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.io.SegmentedStringWriter",
      "tools.jackson.core.util.TextBuffer"
    ],
    [
      "tools.jackson.core.io.SegmentedStringWriter",
      "tools.jackson.core.util.BufferRecycler"
    ],
    [
      "tools.jackson.core.io.SegmentedStringWriter",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.util.BufferRecycler"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.StreamReadConstraints"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.StreamWriteConstraints"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.ErrorReportConfiguration"
    ],
    [
      "tools.jackson.core.io.IOContext",
      "tools.jackson.core.util.TextBuffer"
    ],
    [
      "tools.jackson.core.io.CharTypes",
      "tools.jackson.core.io.CharTypes.AltQuoteEscapes"
    ],
    [
      "tools.jackson.core.io.ContentReference",
      "tools.jackson.core.ErrorReportConfiguration"
    ],
    [
      "tools.jackson.core.io.NumberOutput",
      "tools.jackson.core.io.schubfach.DoubleToDecimal"
    ],
    [
      "tools.jackson.core.io.NumberOutput",
      "tools.jackson.core.io.schubfach.FloatToDecimal"
    ],
    [
      "tools.jackson.core.io.JsonStringEncoder",
      "tools.jackson.core.util.TextBuffer"
    ],
    [
      "tools.jackson.core.io.JsonStringEncoder",
      "tools.jackson.core.util.ByteArrayBuilder"
    ],
    [
      "tools.jackson.core.io.InputDecorator",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.io.CharacterEscapes",
      "tools.jackson.core.SerializableString"
    ]
  ]
}
```