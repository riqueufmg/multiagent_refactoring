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
  "repo_path": "/data/henrique/multiagent_refactoring/data/repositories/javaparser",
  "target": {
    "smell": "HM",
    "smell_name": "Hub-like Modularization",
    "target_type": "class",
    "target_name": "com.github.javaparser.ast.expr.Expression"
  },
  "block": {
    "id": 2,
    "goal": "Reduce Expression's direct dependencies on several literal expression types by extracting string/number literal type-check, cast, optional-conversion and if-visitor methods into a new helper class. This will remove direct coupling to StringLiteralExpr, IntegerLiteralExpr, DoubleLiteralExpr and LongLiteralExpr from Expression (net reduction: remove 4 deps, add 1 helper dep => net -3).",
    "files": [
      "javaparser-core/src/main/java/com/github/javaparser/ast/expr/Expression.java",
      "javaparser-core/src/main/java/com/github/javaparser/ast/expr/ExpressionLiteralHelper.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS(com.github.javaparser.ast.expr.Expression, com.github.javaparser.ast.expr.ExpressionLiteralHelper)",
        "inputs": [
          "com.github.javaparser.ast.expr.Expression"
        ],
        "outputs": [
          "com.github.javaparser.ast.expr.ExpressionLiteralHelper"
        ],
        "details": "Create a new class ExpressionLiteralHelper in the same package and move literal-related methods (isX/asX/toX/ifX for StringLiteralExpr, IntegerLiteralExpr, DoubleLiteralExpr, LongLiteralExpr) into it. Expression will be updated to delegate those calls to the helper.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.isStringLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.isStringLiteralExpr())",
        "inputs": [
          "isStringLiteralExpr()"
        ],
        "outputs": [
          "isStringLiteralExpr()"
        ],
        "details": "Move string-literal helper methods to the new class.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.asStringLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.asStringLiteralExpr())",
        "inputs": [
          "asStringLiteralExpr()"
        ],
        "outputs": [
          "asStringLiteralExpr()"
        ],
        "details": "Move asStringLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.toStringLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.toStringLiteralExpr())",
        "inputs": [
          "toStringLiteralExpr()"
        ],
        "outputs": [
          "toStringLiteralExpr()"
        ],
        "details": "Move toStringLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.ifStringLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.ifStringLiteralExpr())",
        "inputs": [
          "ifStringLiteralExpr(Consumer<StringLiteralExpr>)"
        ],
        "outputs": [
          "ifStringLiteralExpr(Consumer<StringLiteralExpr>)"
        ],
        "details": "Move ifStringLiteralExpr to helper.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.isIntegerLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.isIntegerLiteralExpr())",
        "inputs": [
          "isIntegerLiteralExpr()"
        ],
        "outputs": [
          "isIntegerLiteralExpr()"
        ],
        "details": "Move integer-literal helper methods to the new class.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.asIntegerLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.asIntegerLiteralExpr())",
        "inputs": [
          "asIntegerLiteralExpr()"
        ],
        "outputs": [
          "asIntegerLiteralExpr()"
        ],
        "details": "Move asIntegerLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.toIntegerLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.toIntegerLiteralExpr())",
        "inputs": [
          "toIntegerLiteralExpr()"
        ],
        "outputs": [
          "toIntegerLiteralExpr()"
        ],
        "details": "Move toIntegerLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.ifIntegerLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.ifIntegerLiteralExpr())",
        "inputs": [
          "ifIntegerLiteralExpr(Consumer<IntegerLiteralExpr>)"
        ],
        "outputs": [
          "ifIntegerLiteralExpr(Consumer<IntegerLiteralExpr>)"
        ],
        "details": "Move ifIntegerLiteralExpr to helper.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.isDoubleLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.isDoubleLiteralExpr())",
        "inputs": [
          "isDoubleLiteralExpr()"
        ],
        "outputs": [
          "isDoubleLiteralExpr()"
        ],
        "details": "Move double-literal helper methods to the new class.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.asDoubleLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.asDoubleLiteralExpr())",
        "inputs": [
          "asDoubleLiteralExpr()"
        ],
        "outputs": [
          "asDoubleLiteralExpr()"
        ],
        "details": "Move asDoubleLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.toDoubleLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.toDoubleLiteralExpr())",
        "inputs": [
          "toDoubleLiteralExpr()"
        ],
        "outputs": [
          "toDoubleLiteralExpr()"
        ],
        "details": "Move toDoubleLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.ifDoubleLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.ifDoubleLiteralExpr())",
        "inputs": [
          "ifDoubleLiteralExpr(Consumer<DoubleLiteralExpr>)"
        ],
        "outputs": [
          "ifDoubleLiteralExpr(Consumer<DoubleLiteralExpr>)"
        ],
        "details": "Move ifDoubleLiteralExpr to helper.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.isLongLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.isLongLiteralExpr())",
        "inputs": [
          "isLongLiteralExpr()"
        ],
        "outputs": [
          "isLongLiteralExpr()"
        ],
        "details": "Move long-literal helper methods to the new class.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.asLongLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.asLongLiteralExpr())",
        "inputs": [
          "asLongLiteralExpr()"
        ],
        "outputs": [
          "asLongLiteralExpr()"
        ],
        "details": "Move asLongLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.toLongLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.toLongLiteralExpr())",
        "inputs": [
          "toLongLiteralExpr()"
        ],
        "outputs": [
          "toLongLiteralExpr()"
        ],
        "details": "Move toLongLiteralExpr() to helper.",
        "risk": "low"
      },
      {
        "op": "MOVE_METHOD(com.github.javaparser.ast.expr.Expression.ifLongLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.ifLongLiteralExpr())",
        "inputs": [
          "ifLongLiteralExpr(Consumer<LongLiteralExpr>)"
        ],
        "outputs": [
          "ifLongLiteralExpr(Consumer<LongLiteralExpr>)"
        ],
        "details": "Move ifLongLiteralExpr to helper.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS(com.github.javaparser.ast.expr.ExpressionLiteralHelper)",
        "inputs": [
          "java.util.function.Consumer",
          "java.util.Optional"
        ],
        "outputs": [
          "imports updated in ExpressionLiteralHelper"
        ],
        "details": "Add required imports for the helper. The literal expression types are in the same package.",
        "risk": "low"
      },
      {
        "op": "UPDATE_CALL_SITES(com.github.javaparser.ast.expr.Expression.isStringLiteralExpr(), com.github.javaparser.ast.expr.ExpressionLiteralHelper.isStringLiteralExpr())",
        "inputs": [
          "call sites inside Expression that invoked isX()/asX()/toX()/ifX() for moved literal types"
        ],
        "outputs": [
          "call sites updated to delegate to ExpressionLiteralHelper"
        ],
        "details": "Update internal Expression call sites to delegate to the literal helper. External behavior and public API will be preserved via delegating methods in Expression.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/expr/Expression.java",
    "javaparser-core/src/main/java/com/github/javaparser/ast/expr/ExpressionLiteralHelper.java"
  ],
  "executor_existing_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/expr/Expression.java"
  ],
  "executor_new_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/expr/ExpressionLiteralHelper.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/ast/expr/Expression.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2026 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.ast.expr;\n\nimport static com.github.javaparser.utils.CodeGenerationUtils.f;\n\nimport com.github.javaparser.TokenRange;\nimport com.github.javaparser.ast.AllFieldsConstructor;\nimport com.github.javaparser.ast.Generated;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.nodeTypes.NodeWithOptionalScope;\nimport com.github.javaparser.ast.nodeTypes.NodeWithTypeArguments;\nimport com.github.javaparser.ast.visitor.CloneVisitor;\nimport com.github.javaparser.metamodel.ExpressionMetaModel;\nimport com.github.javaparser.metamodel.JavaParserMetaModel;\nimport com.github.javaparser.resolution.types.ResolvedType;\nimport java.util.Optional;\nimport java.util.function.Consumer;\nimport java.util.function.Function;\nimport java.util.function.Predicate;\n\n/**\n * A base class for all expressions.\n *\n * @author Julio Vilmar Gesser\n */\npublic abstract class Expression extends Node {\n\n    /**\n     * Returns {@code true} when the Node to be tested is not an\n     * {@link EnclosedExpr}, {@code false} otherwise.\n     */\n    public static final Predicate<Node> IS_NOT_ENCLOSED_EXPR = n -> !(n instanceof EnclosedExpr);\n\n    /**\n     * A {@link Function} that returns its argument (an {@link Expression}) when\n     * the argument is not an {@link EnclosedExpr}, otherwise the first\n     * {@link Expression} down the argument's 'inner' path that is not an\n     * {@link EnclosedExpr}.\n     */\n    public static final Function<Expression, Expression> EXCLUDE_ENCLOSED_EXPR = expr -> {\n        while (expr.isEnclosedExpr()) {\n            expr = expr.asEnclosedExpr().getInner();\n        }\n        return expr;\n    };\n\n    @AllFieldsConstructor\n    public Expression() {\n        this(null);\n    }\n\n    /**\n     * This constructor is used by the parser and is considered private.\n     */\n    @Generated(\"com.github.javaparser.generator.core.node.MainConstructorGenerator\")\n    public Expression(TokenRange tokenRange) {\n        super(tokenRange);\n        customInitialization();\n    }\n\n    @Override\n    @Generated(\"com.github.javaparser.generator.core.node.CloneGenerator\")\n    public Expression clone() {\n        return (Expression) accept(new CloneVisitor(), null);\n    }\n\n    @Override\n    @Generated(\"com.github.javaparser.generator.core.node.GetMetaModelGenerator\")\n    public ExpressionMetaModel getMetaModel() {\n        return JavaParserMetaModel.expressionMetaModel;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isAnnotationExpr() {\n        return ExpressionAnnotationsHelper.isAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public AnnotationExpr asAnnotationExpr() {\n        return ExpressionAnnotationsHelper.asAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isArrayAccessExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ArrayAccessExpr asArrayAccessExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not ArrayAccessExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isArrayCreationExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ArrayCreationExpr asArrayCreationExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not ArrayCreationExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isArrayInitializerExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ArrayInitializerExpr asArrayInitializerExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not ArrayInitializerExpr, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isAssignExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public AssignExpr asAssignExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not AssignExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isBinaryExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public BinaryExpr asBinaryExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not BinaryExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isBooleanLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public BooleanLiteralExpr asBooleanLiteralExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not BooleanLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isCastExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public CastExpr asCastExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not CastExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isCharLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public CharLiteralExpr asCharLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not CharLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isClassExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ClassExpr asClassExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not ClassExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isConditionalExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ConditionalExpr asConditionalExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not ConditionalExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isDoubleLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public DoubleLiteralExpr asDoubleLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not DoubleLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isEnclosedExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public EnclosedExpr asEnclosedExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not EnclosedExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isFieldAccessExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public FieldAccessExpr asFieldAccessExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not FieldAccessExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isInstanceOfExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public InstanceOfExpr asInstanceOfExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not InstanceOfExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isIntegerLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public IntegerLiteralExpr asIntegerLiteralExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not IntegerLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLambdaExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LambdaExpr asLambdaExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not LambdaExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LiteralExpr asLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not LiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLiteralStringValueExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LiteralStringValueExpr asLiteralStringValueExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not LiteralStringValueExpr, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLongLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LongLiteralExpr asLongLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not LongLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isMarkerAnnotationExpr() {\n        return ExpressionAnnotationsHelper.isMarkerAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public MarkerAnnotationExpr asMarkerAnnotationExpr() {\n        return ExpressionAnnotationsHelper.asMarkerAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isMethodCallExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public MethodCallExpr asMethodCallExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not MethodCallExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isMethodReferenceExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public MethodReferenceExpr asMethodReferenceExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not MethodReferenceExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isNameExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public NameExpr asNameExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not NameExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isNormalAnnotationExpr() {\n        return ExpressionAnnotationsHelper.isNormalAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public NormalAnnotationExpr asNormalAnnotationExpr() {\n        return ExpressionAnnotationsHelper.asNormalAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isNullLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public NullLiteralExpr asNullLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not NullLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isObjectCreationExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ObjectCreationExpr asObjectCreationExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not ObjectCreationExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isSingleMemberAnnotationExpr() {\n        return ExpressionAnnotationsHelper.isSingleMemberAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public SingleMemberAnnotationExpr asSingleMemberAnnotationExpr() {\n        return ExpressionAnnotationsHelper.asSingleMemberAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isStringLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public StringLiteralExpr asStringLiteralExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not StringLiteralExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isSuperExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public SuperExpr asSuperExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not SuperExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isThisExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ThisExpr asThisExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not ThisExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isTypeExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public TypeExpr asTypeExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not TypeExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isUnaryExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public UnaryExpr asUnaryExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not UnaryExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isVariableDeclarationExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public VariableDeclarationExpr asVariableDeclarationExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not VariableDeclarationExpr, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifAnnotationExpr(Consumer<AnnotationExpr> action) { ExpressionAnnotationsHelper.ifAnnotationExpr(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifArrayAccessExpr(Consumer<ArrayAccessExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifArrayCreationExpr(Consumer<ArrayCreationExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifArrayInitializerExpr(Consumer<ArrayInitializerExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifAssignExpr(Consumer<AssignExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifBinaryExpr(Consumer<BinaryExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifBooleanLiteralExpr(Consumer<BooleanLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifCastExpr(Consumer<CastExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifCharLiteralExpr(Consumer<CharLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifClassExpr(Consumer<ClassExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifConditionalExpr(Consumer<ConditionalExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifDoubleLiteralExpr(Consumer<DoubleLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifEnclosedExpr(Consumer<EnclosedExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifFieldAccessExpr(Consumer<FieldAccessExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifInstanceOfExpr(Consumer<InstanceOfExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifIntegerLiteralExpr(Consumer<IntegerLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLambdaExpr(Consumer<LambdaExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLiteralExpr(Consumer<LiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLiteralStringValueExpr(Consumer<LiteralStringValueExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLongLiteralExpr(Consumer<LongLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifMarkerAnnotationExpr(Consumer<MarkerAnnotationExpr> action) { ExpressionAnnotationsHelper.ifMarkerAnnotationExpr(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifMethodCallExpr(Consumer<MethodCallExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifMethodReferenceExpr(Consumer<MethodReferenceExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifNameExpr(Consumer<NameExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifNormalAnnotationExpr(Consumer<NormalAnnotationExpr> action) { ExpressionAnnotationsHelper.ifNormalAnnotationExpr(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifNullLiteralExpr(Consumer<NullLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifObjectCreationExpr(Consumer<ObjectCreationExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifSingleMemberAnnotationExpr(Consumer<SingleMemberAnnotationExpr> action) { ExpressionAnnotationsHelper.ifSingleMemberAnnotationExpr(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifStringLiteralExpr(Consumer<StringLiteralExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifSuperExpr(Consumer<SuperExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifThisExpr(Consumer<ThisExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifTypeExpr(Consumer<TypeExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifUnaryExpr(Consumer<UnaryExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifVariableDeclarationExpr(Consumer<VariableDeclarationExpr> action) {}\n\n    /**\n     * returns the type associated with the node.\n     */\n    public ResolvedType calculateResolvedType() {\n        return getSymbolResolver().calculateType(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<AnnotationExpr> toAnnotationExpr() {\n        return ExpressionAnnotationsHelper.toAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ArrayAccessExpr> toArrayAccessExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ArrayCreationExpr> toArrayCreationExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ArrayInitializerExpr> toArrayInitializerExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<AssignExpr> toAssignExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<BinaryExpr> toBinaryExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<BooleanLiteralExpr> toBooleanLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<CastExpr> toCastExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<CharLiteralExpr> toCharLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ClassExpr> toClassExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ConditionalExpr> toConditionalExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<DoubleLiteralExpr> toDoubleLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<EnclosedExpr> toEnclosedExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<FieldAccessExpr> toFieldAccessExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<InstanceOfExpr> toInstanceOfExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<IntegerLiteralExpr> toIntegerLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LambdaExpr> toLambdaExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LiteralExpr> toLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LiteralStringValueExpr> toLiteralStringValueExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LongLiteralExpr> toLongLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<MarkerAnnotationExpr> toMarkerAnnotationExpr() {\n        return ExpressionAnnotationsHelper.toMarkerAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<MethodCallExpr> toMethodCallExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<MethodReferenceExpr> toMethodReferenceExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<NameExpr> toNameExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<NormalAnnotationExpr> toNormalAnnotationExpr() {\n        return ExpressionAnnotationsHelper.toNormalAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<NullLiteralExpr> toNullLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ObjectCreationExpr> toObjectCreationExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<SingleMemberAnnotationExpr> toSingleMemberAnnotationExpr() {\n        return ExpressionAnnotationsHelper.toSingleMemberAnnotationExpr(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<StringLiteralExpr> toStringLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<SuperExpr> toSuperExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ThisExpr> toThisExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<TypeExpr> toTypeExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<UnaryExpr> toUnaryExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<VariableDeclarationExpr> toVariableDeclarationExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isSwitchExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public SwitchExpr asSwitchExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not SwitchExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<SwitchExpr> toSwitchExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifSwitchExpr(Consumer<SwitchExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isTextBlockLiteralExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public TextBlockLiteralExpr asTextBlockLiteralExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not TextBlockLiteralExpr, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<TextBlockLiteralExpr> toTextBlockLiteralExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifTextBlockLiteralExpr(Consumer<TextBlockLiteralExpr> action) {}\n\n    /**\n     * See https://docs.oracle.com/javase/specs/jls/se8/html/jls-15.html#jls-15.2\n     * @return true if the expression is a standalone expression\n     */\n    public boolean isStandaloneExpression() {\n        return !isPolyExpression();\n    }\n\n    /**\n     * See https://docs.oracle.com/javase/specs/jls/se8/html/jls-15.html#jls-15.2\n     * @return true if the expression is a poly expression\n     */\n    public boolean isPolyExpression() {\n        return false;\n    }\n\n    /*\n     * 6.5.6.2. Qualified Expression Names\n     * https://docs.oracle.com/javase/specs/jls/se7/html/jls-6.html#jls-6.5.6.2\n     */\n    public boolean isQualified() {\n        return hasScope();\n    }\n\n    /*\n     * Verify if the parent node is an assignment context.\n     */\n    public final boolean appearsInAssignmentContext() {\n        if (getParentNode().isPresent() && getParentNode().get() instanceof Expression) {\n            return ((Expression) getParentNode().get()).isAssignmentContext();\n        }\n        return false;\n    }\n\n    /*\n     * Returns true if the expression is an assignment context. Default is false.\n     * https://docs.oracle.com/javase/specs/jls/se8/html/jls-5.html#jls-5.2\n     * 5.2. Assignment Contexts: Assignment contexts allow the value of an expression to be assigned (§15.26) to a variable;...\n     */\n    protected boolean isAssignmentContext() {\n        return false;\n    }\n\n    /*\n     * Verify if the parent node is an invocation context.\n     */\n    public final boolean appearsInInvocationContext() {\n        if (getParentNode().isPresent() && getParentNode().get() instanceof Expression) {\n            return ((Expression) getParentNode().get()).isInvocationContext();\n        }\n        return false;\n    }\n\n    /*\n     * Returns true if the expression is an invocation context. Default is false.\n     * https://docs.oracle.com/javase/specs/jls/se8/html/jls-5.html#jls-5.3\n     * 5.3. Invocation Contexts\n     */\n    protected boolean isInvocationContext() {\n        return false;\n    }\n\n    /*\n     * returns true if the scope of this expression does not define an type argument or if the expression has not a scope (the expression is not qualified)\n     * or if there is a scope it uses <> to elide class type arguments\n     * For exemple :\n     * m()      ==> true because there is no scope\n     * a.m()    ==> true because the scope has no type arguments\n     * a<>.m()  ==> true because the type argument is elided\n     * a<T>.m() ==> false because the type argument is not elided\n     */\n    public final boolean elidesTypeArguments() {\n        if (!(hasScope() && this instanceof NodeWithTypeArguments)) {\n            return true;\n        }\n        Expression scope =\n                (Expression) ((NodeWithOptionalScope) this).getScope().get();\n        NodeWithTypeArguments nwta = (NodeWithTypeArguments) this;\n        return scope.elidesTypeArguments() && (!nwta.getTypeArguments().isPresent() || nwta.isUsingDiamondOperator());\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isTypePatternExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public TypePatternExpr asTypePatternExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not TypePatternExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<TypePatternExpr> toTypePatternExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifTypePatternExpr(Consumer<TypePatternExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isComponentPatternExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ComponentPatternExpr asComponentPatternExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not ComponentPatternExpr, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ComponentPatternExpr> toComponentPatternExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifComponentPatternExpr(Consumer<ComponentPatternExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isRecordPatternExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public RecordPatternExpr asRecordPatternExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not RecordPatternExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<RecordPatternExpr> toRecordPatternExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifRecordPatternExpr(Consumer<RecordPatternExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isMatchAllPatternExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public MatchAllPatternExpr asMatchAllPatternExpr() {\n        throw new IllegalStateException(f(\n                \"%s is not MatchAllPatternExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<MatchAllPatternExpr> toMatchAllPatternExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifMatchAllPatternExpr(Consumer<MatchAllPatternExpr> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isPatternExpr() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public PatternExpr asPatternExpr() {\n        throw new IllegalStateException(\n                f(\"%s is not PatternExpr, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<PatternExpr> toPatternExpr() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifPatternExpr(Consumer<PatternExpr> action) {}\n}\n"
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/ast/expr/ExpressionLiteralHelper.java",
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
