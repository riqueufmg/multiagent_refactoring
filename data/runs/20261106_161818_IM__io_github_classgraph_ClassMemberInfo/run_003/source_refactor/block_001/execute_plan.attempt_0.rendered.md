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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/classgraph/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "io.github.classgraph.ClassMemberInfo"
  },
  "block": {
    "id": 1,
    "goal": "Reduce the public API and implementation size of ClassMemberInfo by extracting its cohesive annotation-query facade into a dedicated class while preserving the existing annotation metadata behavior.",
    "files": [
      "src/main/java/io/github/classgraph/ClassMemberInfo.java",
      "src/main/java/io/github/classgraph/ClassMemberInfoAnnotations.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "io.github.classgraph.ClassMemberInfo"
        ],
        "outputs": [
          "io.github.classgraph.ClassMemberInfoAnnotations"
        ],
        "details": "Extract the annotation-query methods getAllAnnotationInfo(), getDirectAnnotationInfo(), getAllAnnotationInfo(Class<? extends Annotation>), getAllAnnotationInfo(String), getDirectAnnotationInfo(Class<? extends Annotation>), getDirectAnnotationInfo(String), getAllAnnotationInfoRepeatable(Class<? extends Annotation>), getAllAnnotationInfoRepeatable(String), getDirectAnnotationInfoRepeatable(Class<? extends Annotation>), getDirectAnnotationInfoRepeatable(String), hasAnnotation(Class<? extends Annotation>), and hasAnnotation(String), together with the required annotationInfoMetadata dependency. Keep ClassMemberInfo delegating these public operations to the extracted class so existing callers remain compatible.",
        "risk": "medium"
      }
    ],
    "test_files": []
  },
  "allowed_files": [
    "src/main/java/io/github/classgraph/ClassMemberInfo.java",
    "src/main/java/io/github/classgraph/ClassMemberInfoAnnotations.java"
  ],
  "executor_existing_files": [
    "src/main/java/io/github/classgraph/ClassMemberInfo.java"
  ],
  "executor_new_files": [
    "src/main/java/io/github/classgraph/ClassMemberInfoAnnotations.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/io/github/classgraph/ClassMemberInfo.java",
      "exists": "true",
      "content": "/*\n * This file is part of ClassGraph.\n *\n * Author: Luke Hutchison\n *\n * Hosted at: https://github.com/classgraph/classgraph\n *\n * The MIT License (MIT)\n */\npackage io.github.classgraph;\n\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Modifier;\n\nimport org.jspecify.annotations.Nullable;\n\n/**\n * Holds metadata about class members of a class encountered during a scan. All values are taken directly out of the\n * classfile for the class.\n */\npublic abstract class ClassMemberInfo extends ScanResultObject implements HasName {\n    /** Defining class name. */\n    String declaringClassName;\n\n    /** The name of the class member. */\n    String name;\n\n    /** Class member modifiers. */\n    int modifiers;\n\n    /** The JVM-internal type descriptor. */\n    String typeDescriptorStr;\n\n    /** The type signature. */\n    @Nullable\n    String typeSignatureStr;\n\n    /** The annotation metadata for this class member. */\n    @Nullable\n    AnnotationInfoList annotationInfo;\n\n    /** Annotation metadata access and query implementation. */\n    private final ClassMemberAnnotationInfo annotationInfoMetadata;\n\n    ClassMemberInfo(final String definingClassName, final String memberName, final int modifiers,\n            final String typeDescriptorStr, final @Nullable String typeSignatureStr,\n            final @Nullable AnnotationInfoList annotationInfo) {\n        super();\n        this.declaringClassName = definingClassName;\n        this.name = memberName;\n        this.modifiers = modifiers;\n        this.typeDescriptorStr = typeDescriptorStr;\n        this.typeSignatureStr = typeSignatureStr;\n        this.annotationInfo = annotationInfo;\n        this.annotationInfoMetadata = new ClassMemberAnnotationInfo(this, annotationInfo);\n    }\n\n    @Override\n    public @Nullable ClassInfo getClassInfo() {\n        return super.getClassInfo();\n    }\n\n    @Override\n    public String getClassName() {\n        return declaringClassName;\n    }\n\n    @Override\n    public String getName() {\n        return name;\n    }\n\n    public int getModifiers() {\n        return modifiers;\n    }\n\n    public abstract String getModifiersString();\n\n    public boolean isPublic() {\n        return Modifier.isPublic(modifiers);\n    }\n\n    public boolean isPrivate() {\n        return Modifier.isPrivate(modifiers);\n    }\n\n    public boolean isProtected() {\n        return Modifier.isProtected(modifiers);\n    }\n\n    public boolean isStatic() {\n        return Modifier.isStatic(modifiers);\n    }\n\n    public boolean isFinal() {\n        return Modifier.isFinal(modifiers);\n    }\n\n    public boolean isSynthetic() {\n        return (modifiers & 0x1000) != 0;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeDescriptor();\n\n    public String getTypeDescriptorString() {\n        return typeDescriptorStr;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeSignature();\n\n    public @Nullable String getTypeSignatureString() {\n        return typeSignatureStr;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeSignatureOrTypeDescriptor();\n\n    public String getTypeSignatureOrTypeDescriptorString() {\n        return typeSignatureStr != null ? typeSignatureStr : typeDescriptorStr;\n    }\n\n    public AnnotationInfoList getAllAnnotationInfo() {\n        return annotationInfoMetadata.getAllAnnotationInfo();\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfo() {\n        return annotationInfoMetadata.getDirectAnnotationInfo();\n    }\n\n    public @Nullable AnnotationInfo getAllAnnotationInfo(final Class<? extends Annotation> annotation) {\n        return annotationInfoMetadata.getAllAnnotationInfo(annotation);\n    }\n\n    public @Nullable AnnotationInfo getAllAnnotationInfo(final String annotationName) {\n        return annotationInfoMetadata.getAllAnnotationInfo(annotationName);\n    }\n\n    public @Nullable AnnotationInfo getDirectAnnotationInfo(final Class<? extends Annotation> annotation) {\n        return annotationInfoMetadata.getDirectAnnotationInfo(annotation);\n    }\n\n    public @Nullable AnnotationInfo getDirectAnnotationInfo(final String annotationName) {\n        return annotationInfoMetadata.getDirectAnnotationInfo(annotationName);\n    }\n\n    public AnnotationInfoList getAllAnnotationInfoRepeatable(final Class<? extends Annotation> annotation) {\n        return annotationInfoMetadata.getAllAnnotationInfoRepeatable(annotation);\n    }\n\n    public AnnotationInfoList getAllAnnotationInfoRepeatable(final String annotationName) {\n        return annotationInfoMetadata.getAllAnnotationInfoRepeatable(annotationName);\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfoRepeatable(final Class<? extends Annotation> annotation) {\n        return annotationInfoMetadata.getDirectAnnotationInfoRepeatable(annotation);\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfoRepeatable(final String annotationName) {\n        return annotationInfoMetadata.getDirectAnnotationInfoRepeatable(annotationName);\n    }\n\n    public boolean hasAnnotation(final Class<? extends Annotation> annotation) {\n        return annotationInfoMetadata.hasAnnotation(annotation);\n    }\n\n    public boolean hasAnnotation(final String annotationName) {\n        return annotationInfoMetadata.hasAnnotation(annotationName);\n    }\n}\n"
    },
    {
      "path": "src/main/java/io/github/classgraph/ClassMemberInfoAnnotations.java",
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
