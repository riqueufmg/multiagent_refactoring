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
  "target_name": "tools.jackson.core.json",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261019_181949_GC__tools_jackson_core_json/run_005/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/tools/jackson/core/json/ByteSourceJsonBootstrapper.java",
    "src/main/java/tools/jackson/core/json/JsonFactory.java",
    "src/main/java/tools/jackson/core/json/JsonFactoryBuilder.java",
    "src/main/java/tools/jackson/core/json/JsonGeneratorBase.java",
    "src/main/java/tools/jackson/core/json/JsonParserBase.java",
    "src/main/java/tools/jackson/core/json/JsonReadFeature.java",
    "src/main/java/tools/jackson/core/json/JsonWriteFeature.java",
    "src/main/java/tools/jackson/core/json/ReaderBasedJsonParser.java",
    "src/main/java/tools/jackson/core/json/UTF8DataInputJsonParser.java",
    "src/main/java/tools/jackson/core/json/UTF8JsonGenerator.java",
    "src/main/java/tools/jackson/core/json/UTF8StreamJsonParser.java",
    "src/main/java/tools/jackson/core/json/WriterBasedJsonGenerator.java",
    "src/main/java/tools/jackson/core/json/package-info.java"
  ],
  "internal_deps": [
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.TestWithTonsaSymbols",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.json.PackageVersion"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.json.JsonWriteFeature"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.json.JsonWriteFeature"
    ],
    [
      "tools.jackson.core.json.TestUnicode",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.json.JsonWriteFeature"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.json.PackageVersion"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.TestMaxErrorSize",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.json.JsonFactoryBuilder"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.json.JsonWriteFeature"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.json.ByteSourceJsonBootstrapper"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.json.PackageVersion"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.json.JsonWriteFeature"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.json.JsonWriteFeature"
    ]
  ],
  "incoming_deps": [
    [
      "tools.jackson.core.sym.TestSymbolTables",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.sym.TestByteBasedSymbols",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingJsonParserBase",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.io.TestJsonStringEncoder",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "perf.ManualFuzzUTF32",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.json.async.NonBlockingUtf8JsonParserBase",
      "tools.jackson.core.json.JsonReadFeature"
    ],
    [
      "tools.jackson.core.sym.TestHashCollisionChars",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "perf.ManualIntRead",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.async.AsyncTestBase",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.sym.CharsToNameCanonicalizer",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "perf.MediaItem",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "perf.ManualReadPerfWithMedia",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.read.TestReadHumongousString",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.sym.TestSymbolsWithMediaItem",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.sym.ByteQuadsCanonicalizer",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.JacksonCoreTestBase",
      "tools.jackson.core.json.JsonFactory"
    ],
    [
      "tools.jackson.core.JacksonCoreTestBase",
      "tools.jackson.core.json.JsonFactoryBuilder"
    ],
    [
      "perf.ManualSmallTokenRead",
      "tools.jackson.core.json.JsonFactory"
    ]
  ],
  "outgoing_deps": [
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.sym.CharsToNameCanonicalizer"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.Base64Variant"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.util.ByteArrayBuilder"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.util.TextBuffer"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.TokenStreamLocation"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.exc.StreamReadException"
    ],
    [
      "tools.jackson.core.json.ReaderBasedJsonParser",
      "tools.jackson.core.StreamReadFeature"
    ],
    [
      "tools.jackson.core.json.TestWithTonsaSymbols",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.TestWithTonsaSymbols",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.TestWithTonsaSymbols",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.json.context.JsonReadContext"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.json.context.DupDetector"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.Version"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.util.JacksonFeatureSet"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.TokenStreamContext"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.io.NumberInput"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.exc.InputCoercionException"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.base.ParserMinimalBase"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.exc.StreamReadException"
    ],
    [
      "tools.jackson.core.json.JsonParserBase",
      "tools.jackson.core.StreamReadFeature"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.json.TestDecorators.SimpleInputDecorator"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.json.TestDecorators.SimpleOutputDecorator"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.json.TestDecorators.SimpleGeneratorDecorator"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.TestDecorators",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.PrettyPrinter"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.json.context.JsonWriteContext"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.Base64Variant"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.io.NumberOutput"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.TokenStreamContext"
    ],
    [
      "tools.jackson.core.json.WriterBasedJsonGenerator",
      "tools.jackson.core.StreamWriteFeature"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.StreamReadConstraints"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.StreamWriteConstraints"
    ],
    [
      "tools.jackson.core.json.JsonFactoryBuilder",
      "tools.jackson.core.ErrorReportConfiguration"
    ],
    [
      "tools.jackson.core.json.TestUnicode",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.TestUnicode",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.TestUnicode",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.TestCharEscaping",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.json.TestRootValues.Issue516InputStream"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.json.TestRootValues.Issue516Reader"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.TestRootValues",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.util.VersionUtil"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.io.MergedStream"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.sym.ByteQuadsCanonicalizer"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.sym.CharsToNameCanonicalizer"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.ByteSourceJsonBootstrapper",
      "tools.jackson.core.exc.JacksonIOException"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.PrettyPrinter"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.json.context.JsonWriteContext"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.json.context.DupDetector"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.Version"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.util.JacksonFeatureSet"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.TokenStreamContext"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.JsonGeneratorBase",
      "tools.jackson.core.StreamWriteFeature"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.sym.ByteQuadsCanonicalizer"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.Base64Variant"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.util.ByteArrayBuilder"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.base.ParserBase"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.exc.StreamReadException"
    ],
    [
      "tools.jackson.core.json.UTF8DataInputJsonParser",
      "tools.jackson.core.TokenStreamLocation"
    ],
    [
      "tools.jackson.core.json.TestMaxErrorSize",
      "tools.jackson.core.JsonParser"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.sym.CharsToNameCanonicalizer"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.sym.ByteQuadsCanonicalizer"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.StreamReadConstraints"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.StreamWriteConstraints"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.ErrorReportConfiguration"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.TokenStreamFactory"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.Version"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.FormatSchema"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.JsonParser"
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
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.sym.PropertyNameMatcher"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.sym.BinaryNameMatcher"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.util.DefaultPrettyPrinter"
    ],
    [
      "tools.jackson.core.json.JsonFactory",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.io.SerializedString"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.util.JsonpCharacterEscapes"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.json.TestCustomEscaping.MyEscapes"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.TestCustomEscaping",
      "tools.jackson.core.JsonEncoding"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.sym.ByteQuadsCanonicalizer"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.ObjectReadContext"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.JsonToken"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.Base64Variant"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.util.ByteArrayBuilder"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.sym.PropertyNameMatcher"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.base.ParserBase"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.exc.StreamReadException"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.util.InternalJacksonUtil"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.TokenStreamLocation"
    ],
    [
      "tools.jackson.core.json.UTF8StreamJsonParser",
      "tools.jackson.core.StreamReadFeature"
    ],
    [
      "tools.jackson.core.json.PackageVersion",
      "tools.jackson.core.Version"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.ObjectWriteContext"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.IOContext"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.SerializableString"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.CharacterEscapes"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.PrettyPrinter"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.JsonGenerator"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.CharTypes"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.JacksonException"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.json.context.JsonWriteContext"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.Base64Variant"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.io.NumberOutput"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.TokenStreamContext"
    ],
    [
      "tools.jackson.core.json.UTF8JsonGenerator",
      "tools.jackson.core.StreamWriteFeature"
    ]
  ]
}
```