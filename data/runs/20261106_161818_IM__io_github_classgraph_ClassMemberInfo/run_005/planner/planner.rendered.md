## CONTEXT

Insufficient Modularization is a design smell that occurs when a class exists that has not been completely decomposed, and a further decomposition could reduce its size, implementation complexity, or both.

The factors that characterize Insufficient Modularization are considered in the following priority order:
- Too many public methods (poorly cohesive API).
- Too many general methods.
- Overly complex methods.

## TASK

Evaluate the input elements and create a plan in JSON format with the goal of removing (or reducing) Insufficient Modularization.

Strategy:
- Reduce the size and complexity of the class by grouping cohesive attributes and methods.
- MOVE and CREATE refactorings are only allowed at the same level as the entry or at a sub-level.
- When the smell is caused by too many public methods, prefer plans that move a cohesive group of public and private methods out of the target class.
- Test refactoring does not need to be included, as this will be done later.

## ALLOWED REFACTORINGS
A list of refactorings allowed in the refactoring plan is presented as following:
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "io.github.classgraph.ClassMemberInfo",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261106_161818_IM__io_github_classgraph_ClassMemberInfo/run_005/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "src/main/java/io/github/classgraph/ClassMemberInfo.java",
  "target_source_root": "src/main/java",
  "target_code": "/*\n * This file is part of ClassGraph.\n *\n * Author: Luke Hutchison\n *\n * Hosted at: https://github.com/classgraph/classgraph\n *\n * The MIT License (MIT)\n */\npackage io.github.classgraph;\n\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Modifier;\n\nimport org.jspecify.annotations.Nullable;\n\n/**\n * Holds metadata about class members of a class encountered during a scan. All values are taken directly out of the\n * classfile for the class.\n */\npublic abstract class ClassMemberInfo extends ScanResultObject implements HasName {\n    /** Defining class name. */\n    String declaringClassName;\n\n    /** The name of the class member. */\n    String name;\n\n    /** Class member modifiers. */\n    int modifiers;\n\n    /** The JVM-internal type descriptor. */\n    String typeDescriptorStr;\n\n    /** The type signature. */\n    @Nullable\n    String typeSignatureStr;\n\n    /** The annotation metadata for this class member. */\n    @Nullable\n    AnnotationInfoList annotationInfo;\n\n    /** Annotation metadata access and query facade. */\n    private final ClassMemberInfoAnnotations annotations;\n\n    ClassMemberInfo(final String definingClassName, final String memberName, final int modifiers,\n            final String typeDescriptorStr, final @Nullable String typeSignatureStr,\n            final @Nullable AnnotationInfoList annotationInfo) {\n        super();\n        this.declaringClassName = definingClassName;\n        this.name = memberName;\n        this.modifiers = modifiers;\n        this.typeDescriptorStr = typeDescriptorStr;\n        this.typeSignatureStr = typeSignatureStr;\n        this.annotationInfo = annotationInfo;\n        this.annotations = new ClassMemberInfoAnnotations(this, annotationInfo);\n    }\n\n    @Override\n    public @Nullable ClassInfo getClassInfo() {\n        return super.getClassInfo();\n    }\n\n    @Override\n    public String getClassName() {\n        return declaringClassName;\n    }\n\n    @Override\n    public String getName() {\n        return name;\n    }\n\n    public int getModifiers() {\n        return modifiers;\n    }\n\n    public abstract String getModifiersString();\n\n    public boolean isPublic() {\n        return Modifier.isPublic(modifiers);\n    }\n\n    public boolean isPrivate() {\n        return Modifier.isPrivate(modifiers);\n    }\n\n    public boolean isProtected() {\n        return Modifier.isProtected(modifiers);\n    }\n\n    public boolean isStatic() {\n        return Modifier.isStatic(modifiers);\n    }\n\n    public boolean isFinal() {\n        return Modifier.isFinal(modifiers);\n    }\n\n    public boolean isSynthetic() {\n        return (modifiers & 0x1000) != 0;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeDescriptor();\n\n    public String getTypeDescriptorString() {\n        return typeDescriptorStr;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeSignature();\n\n    public @Nullable String getTypeSignatureString() {\n        return typeSignatureStr;\n    }\n\n    public abstract @Nullable HierarchicalTypeSignature getTypeSignatureOrTypeDescriptor();\n\n    public String getTypeSignatureOrTypeDescriptorString() {\n        return typeSignatureStr != null ? typeSignatureStr : typeDescriptorStr;\n    }\n\n    public AnnotationInfoList getAllAnnotationInfo() {\n        return annotations.getAllAnnotationInfo();\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfo() {\n        return annotations.getDirectAnnotationInfo();\n    }\n\n    public @Nullable AnnotationInfo getAllAnnotationInfo(final Class<? extends Annotation> annotation) {\n        return annotations.getAllAnnotationInfo(annotation);\n    }\n\n    public @Nullable AnnotationInfo getAllAnnotationInfo(final String annotationName) {\n        return annotations.getAllAnnotationInfo(annotationName);\n    }\n\n    public @Nullable AnnotationInfo getDirectAnnotationInfo(final Class<? extends Annotation> annotation) {\n        return annotations.getDirectAnnotationInfo(annotation);\n    }\n\n    public @Nullable AnnotationInfo getDirectAnnotationInfo(final String annotationName) {\n        return annotations.getDirectAnnotationInfo(annotationName);\n    }\n\n    public AnnotationInfoList getAllAnnotationInfoRepeatable(final Class<? extends Annotation> annotation) {\n        return annotations.getAllAnnotationInfoRepeatable(annotation);\n    }\n\n    public AnnotationInfoList getAllAnnotationInfoRepeatable(final String annotationName) {\n        return annotations.getAllAnnotationInfoRepeatable(annotationName);\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfoRepeatable(final Class<? extends Annotation> annotation) {\n        return annotations.getDirectAnnotationInfoRepeatable(annotation);\n    }\n\n    public AnnotationInfoList getDirectAnnotationInfoRepeatable(final String annotationName) {\n        return annotations.getDirectAnnotationInfoRepeatable(annotationName);\n    }\n\n    public boolean hasAnnotation(final Class<? extends Annotation> annotation) {\n        return annotations.hasAnnotation(annotation);\n    }\n\n    public boolean hasAnnotation(final String annotationName) {\n        return annotations.hasAnnotation(annotationName);\n    }\n}\n"
}

## OUTPUT

The expected output format and contraints for that output are presented below.

{
  "smell_type": "Insufficient Modularization",
  "target_level": "class",
  "target": "<class FQN from input>",
  "blocks": [
    {
      "id": 1,
      "goal": "...",
      "files": ["..."],
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

Contraints:
- Reference only packages, classes, methods, and fields present in the input.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.