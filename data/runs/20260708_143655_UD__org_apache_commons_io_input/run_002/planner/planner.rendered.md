## CONTEXT

Unstable Dependency (UD) occurs when the target package depends on one or more packages that are less stable than itself.

One way to remove this architecture smell is to remove or reduce the dependencies between the target package and packages that are less stable than it.

## TASK

Your goal is to create a plan that will reduce or (ideally) remove the dependency between a given target package and another package that is less stable than it.

The following input will be provided to inform the decision-making process:

{
  "target": "org.repo.target.package",
  "unstable_packages": [
    "org.repo.packageA",
    "org.repo.packageB",
    "org.repo.packageC",
  ],
  "outgoing_dependencies": [
    {
      "source": "org.repo.target.package.SomeClass",
      "target": "org.repo.packageA.SomeClass",
      "external_calls": [
        "call_1",
        "call_2"
      ]
    }
  ]
}

Based on this data, follow this line of reasoning:
- Evaluate the list of *outgoing_dependencies* and select the simplest package from the *unstable_packages* list for dependency removal or reduction.
- Select exactly one unstable package, no more than that.
- Next, evaluate the external calls from classes in the target package to classes in the selected unstable package. Based on this evaluation, define a refactoring strategy to remove or reduce the dependency between classes.
- Each block of the plan must propose the removal of dependencies between only a single class from the target package and a single class from the unstable package.
- Therefore, if dependencies between N pairs need to be removed, the plan must include N blocks.
- The plan is required to contain a minimum of one block and a maximum of five.

## RULES
- Prefer MOVE_CLASS when a class in the target package depends mostly on one unstable package and semantically belongs closer to that package.
- Prefer MOVE_METHOD or MOVE_FIELD when only a small responsibility causes the dependency.
- Use EXTRACT_INTERFACE only when the target package can depend on a stable abstraction and the concrete unstable dependency can be moved out of the target package.
- Avoid creating new packages/classes unless necessary.
- Do not introduce a facade, interface, or wrapper if it only forwards calls to the unstable package. It must remove the direct dependency from the target package and move a real responsibility.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- - INTRODUCE_FACADE(pkgA.C1, pkgA.Facade): Creates a facade only when it immediately removes direct dependencies from the target package.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT

{
  "smell": "Unstable Dependency",
  "target_type": "package",
  "target_name": "org.apache.commons.io.input",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20260708_143655_UD__org_apache_commons_io_input/run_002/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "src/main/java",
  "target_files": [
    "src/main/java/org/apache/commons/io/input/AbstractCharacterFilterReader.java",
    "src/main/java/org/apache/commons/io/input/AbstractInputStream.java",
    "src/main/java/org/apache/commons/io/input/AbstractLineEndingInputStream.java",
    "src/main/java/org/apache/commons/io/input/AutoCloseInputStream.java",
    "src/main/java/org/apache/commons/io/input/BOMInputStream.java",
    "src/main/java/org/apache/commons/io/input/BoundedInputStream.java",
    "src/main/java/org/apache/commons/io/input/BoundedReader.java",
    "src/main/java/org/apache/commons/io/input/BrokenInputStream.java",
    "src/main/java/org/apache/commons/io/input/BrokenReader.java",
    "src/main/java/org/apache/commons/io/input/BufferedFileChannelInputStream.java",
    "src/main/java/org/apache/commons/io/input/ByteBufferCleaner.java",
    "src/main/java/org/apache/commons/io/input/CharSequenceInputStream.java",
    "src/main/java/org/apache/commons/io/input/CharSequenceReader.java",
    "src/main/java/org/apache/commons/io/input/CharacterFilterReader.java",
    "src/main/java/org/apache/commons/io/input/CharacterSetFilterReader.java",
    "src/main/java/org/apache/commons/io/input/ChecksumInputStream.java",
    "src/main/java/org/apache/commons/io/input/CircularInputStream.java",
    "src/main/java/org/apache/commons/io/input/ClassLoaderObjectInputStream.java",
    "src/main/java/org/apache/commons/io/input/CloseShieldInputStream.java",
    "src/main/java/org/apache/commons/io/input/CloseShieldReader.java",
    "src/main/java/org/apache/commons/io/input/ClosedInputStream.java",
    "src/main/java/org/apache/commons/io/input/ClosedReader.java",
    "src/main/java/org/apache/commons/io/input/CountingInputStream.java",
    "src/main/java/org/apache/commons/io/input/DemuxInputStream.java",
    "src/main/java/org/apache/commons/io/input/InfiniteCircularInputStream.java",
    "src/main/java/org/apache/commons/io/input/Input.java",
    "src/main/java/org/apache/commons/io/input/MarkShieldInputStream.java",
    "src/main/java/org/apache/commons/io/input/MemoryMappedFileInputStream.java",
    "src/main/java/org/apache/commons/io/input/MessageDigestCalculatingInputStream.java",
    "src/main/java/org/apache/commons/io/input/MessageDigestInputStream.java",
    "src/main/java/org/apache/commons/io/input/NullInputStream.java",
    "src/main/java/org/apache/commons/io/input/NullReader.java",
    "src/main/java/org/apache/commons/io/input/ObservableInputStream.java",
    "src/main/java/org/apache/commons/io/input/ProxyInputStream.java",
    "src/main/java/org/apache/commons/io/input/ProxyReader.java",
    "src/main/java/org/apache/commons/io/input/QueueInputStream.java",
    "src/main/java/org/apache/commons/io/input/RandomAccessFileInputStream.java",
    "src/main/java/org/apache/commons/io/input/ReadAheadInputStream.java",
    "src/main/java/org/apache/commons/io/input/ReaderInputStream.java",
    "src/main/java/org/apache/commons/io/input/ReversedLinesFileReader.java",
    "src/main/java/org/apache/commons/io/input/SequenceReader.java",
    "src/main/java/org/apache/commons/io/input/SwappedDataInputStream.java",
    "src/main/java/org/apache/commons/io/input/TaggedInputStream.java",
    "src/main/java/org/apache/commons/io/input/TaggedReader.java",
    "src/main/java/org/apache/commons/io/input/Tailer.java",
    "src/main/java/org/apache/commons/io/input/TailerListener.java",
    "src/main/java/org/apache/commons/io/input/TailerListenerAdapter.java",
    "src/main/java/org/apache/commons/io/input/TeeInputStream.java",
    "src/main/java/org/apache/commons/io/input/TeeReader.java",
    "src/main/java/org/apache/commons/io/input/ThrottledInputStream.java",
    "src/main/java/org/apache/commons/io/input/TimestampedObserver.java",
    "src/main/java/org/apache/commons/io/input/UncheckedBufferedReader.java",
    "src/main/java/org/apache/commons/io/input/UncheckedFilterInputStream.java",
    "src/main/java/org/apache/commons/io/input/UncheckedFilterReader.java",
    "src/main/java/org/apache/commons/io/input/UnixLineEndingInputStream.java",
    "src/main/java/org/apache/commons/io/input/UnsupportedOperationExceptions.java",
    "src/main/java/org/apache/commons/io/input/UnsynchronizedBufferedInputStream.java",
    "src/main/java/org/apache/commons/io/input/UnsynchronizedBufferedReader.java",
    "src/main/java/org/apache/commons/io/input/UnsynchronizedByteArrayInputStream.java",
    "src/main/java/org/apache/commons/io/input/UnsynchronizedFilterInputStream.java",
    "src/main/java/org/apache/commons/io/input/UnsynchronizedReader.java",
    "src/main/java/org/apache/commons/io/input/WindowsLineEndingInputStream.java",
    "src/main/java/org/apache/commons/io/input/XmlStreamReader.java",
    "src/main/java/org/apache/commons/io/input/XmlStreamReaderException.java",
    "src/main/java/org/apache/commons/io/input/package-info.java"
  ],
  "target": "org.apache.commons.io.input",
  "unstable_packages": [
    "org.apache.commons.io.build"
  ],
  "outgoing_dependencies": []
}

## OUTPUT

Return ONLY valid JSON in the following format:

{
  "smell_type": "Unstable Dependency",
  "target_level": "package",
  "target": "<package FQN from input>",
  "selected_unstable_package": "<selected package FQN>",
  "blocks": [
    {
      "id": 1,
      "goal": "...",
      "dependency_pair": {
        "source": "<class from target package>",
        "target": "<class from selected unstable package>"
      },
      "files": ["src/main/java/..."],
      "ops": [
        {
          "op": "<allowed op>",
          "inputs": ["..."],
          "outputs": ["..."],
          "details": "...",
          "risk": "low|medium|high"
        }
      ]
    }
  ]
}

## CONSTRAINTS

- Return only valid JSON.
- Reference only packages, classes, methods, fields, and calls present in the input.
- Select exactly one unstable package.
- Each block must address only one source class from the target package and one target class from the selected unstable package.
- Each block must be small and independently compilable.
- Each block must have an immediate expected effect on reducing dependencies from the target package to the selected unstable package.
- Do not introduce a facade, interface, wrapper, or helper if it only forwards calls to the unstable package.
- Avoid creating new packages/classes unless necessary.
- If a new class is necessary, place it in an existing package present in the input.
- Do not include optional, preparatory, future, or follow-up blocks.
- The plan must contain at least one block and at most five blocks.
- If no safe block can reduce the dependency under these constraints, return an empty "blocks" list and explain why in "notes".