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
    "target_name": "com.github.javaparser.ast.stmt.Statement"
  },
  "block": {
    "id": 1,
    "goal": "Reduce Statement's output coupling by removing direct references to four concrete statement subtype classes (AssertStmt, BlockStmt, BreakStmt, ContinueStmt). Extract the subtype-specific type-casting and accessor methods into a new helper class in the same package so that Statement no longer declares or implements these methods, reducing its fan-out by 3 (four dependencies removed, no new dependency introduced on the target).",
    "files": [
      "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/Statement.java",
      "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS(com.github.javaparser.ast.stmt.Statement, com.github.javaparser.ast.stmt.StatementTypeAccessors)",
        "inputs": [
          "com.github.javaparser.ast.stmt.Statement.isAssertStmt()",
          "com.github.javaparser.ast.stmt.Statement.asAssertStmt()",
          "com.github.javaparser.ast.stmt.Statement.ifAssertStmt(java.util.function.Consumer<AssertStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toAssertStmt()",
          "com.github.javaparser.ast.stmt.Statement.isBlockStmt()",
          "com.github.javaparser.ast.stmt.Statement.asBlockStmt()",
          "com.github.javaparser.ast.stmt.Statement.ifBlockStmt(java.util.function.Consumer<BlockStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toBlockStmt()",
          "com.github.javaparser.ast.stmt.Statement.isBreakStmt()",
          "com.github.javaparser.ast.stmt.Statement.asBreakStmt()",
          "com.github.javaparser.ast.stmt.Statement.ifBreakStmt(java.util.function.Consumer<BreakStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toBreakStmt()",
          "com.github.javaparser.ast.stmt.Statement.isContinueStmt()",
          "com.github.javaparser.ast.stmt.Statement.asContinueStmt()",
          "com.github.javaparser.ast.stmt.Statement.ifContinueStmt(java.util.function.Consumer<ContinueStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toContinueStmt()"
        ],
        "outputs": [
          "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java"
        ],
        "details": "Create a new class StatementTypeAccessors in package com.github.javaparser.ast.stmt and move the 16 methods listed above into it. Implement them as static helper methods that accept a Statement instance when needed or as instance methods on the new helper specialized for these casts. The implementations are unchanged aside from being relocated. Remove the moved method declarations from Statement so that Statement no longer references AssertStmt, BlockStmt, BreakStmt, or ContinueStmt in its own method signatures or bodies.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS(javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java)",
        "inputs": [
          "com.github.javaparser.ast.stmt.AssertStmt",
          "com.github.javaparser.ast.stmt.BlockStmt",
          "com.github.javaparser.ast.stmt.BreakStmt",
          "com.github.javaparser.ast.stmt.ContinueStmt",
          "com.github.javaparser.ast.stmt.StatementTypeCasting",
          "java.util.Optional",
          "java.util.function.Consumer",
          "static com.github.javaparser.utils.CodeGenerationUtils.f"
        ],
        "outputs": [
          "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java (updated imports)"
        ],
        "details": "Add or update imports required by the new class. The original Statement file should have the imports for AssertStmt/BlockStmt/BreakStmt/ContinueStmt removed if they are no longer used there.",
        "risk": "low"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "com.github.javaparser.ast.stmt.Statement.isAssertStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.isAssertStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.asAssertStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.asAssertStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.ifAssertStmt(java.util.function.Consumer<AssertStmt>) -> com.github.javaparser.ast.stmt.StatementTypeAccessors.ifAssertStmt(Statement, java.util.function.Consumer<AssertStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toAssertStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.toAssertStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.isBlockStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.isBlockStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.asBlockStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.asBlockStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.ifBlockStmt(java.util.function.Consumer<BlockStmt>) -> com.github.javaparser.ast.stmt.StatementTypeAccessors.ifBlockStmt(Statement, java.util.function.Consumer<BlockStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toBlockStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.toBlockStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.isBreakStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.isBreakStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.asBreakStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.asBreakStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.ifBreakStmt(java.util.function.Consumer<BreakStmt>) -> com.github.javaparser.ast.stmt.StatementTypeAccessors.ifBreakStmt(Statement, java.util.function.Consumer<BreakStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toBreakStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.toBreakStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.isContinueStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.isContinueStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.asContinueStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.asContinueStmt(Statement)",
          "com.github.javaparser.ast.stmt.Statement.ifContinueStmt(java.util.function.Consumer<ContinueStmt>) -> com.github.javaparser.ast.stmt.StatementTypeAccessors.ifContinueStmt(Statement, java.util.function.Consumer<ContinueStmt>)",
          "com.github.javaparser.ast.stmt.Statement.toContinueStmt() -> com.github.javaparser.ast.stmt.StatementTypeAccessors.toContinueStmt(Statement)"
        ],
        "outputs": [
          "Codebase call sites updated to invoke the moved methods on StatementTypeAccessors, passing the Statement instance where required."
        ],
        "details": "Replace direct calls of the moved instance methods with calls to the new helper class methods. Update static imports/usages accordingly. This preserves external behavior while allowing Statement to drop direct references to the four subtype classes. Update any internal references in the Statement class already moved.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/Statement.java",
    "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java"
  ],
  "executor_existing_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/Statement.java"
  ],
  "executor_new_files": [
    "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/Statement.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2026 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.ast.stmt;\n\nimport static com.github.javaparser.utils.CodeGenerationUtils.f;\n\nimport com.github.javaparser.TokenRange;\nimport com.github.javaparser.ast.AllFieldsConstructor;\nimport com.github.javaparser.ast.Generated;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.visitor.CloneVisitor;\nimport com.github.javaparser.metamodel.JavaParserMetaModel;\nimport com.github.javaparser.metamodel.StatementMetaModel;\nimport java.util.Optional;\nimport java.util.function.Consumer;\n\n/**\n * A base class for all statements.\n *\n * @author Julio Vilmar Gesser\n */\npublic abstract class Statement extends Node {\n\n    @AllFieldsConstructor\n    public Statement() {\n        this(null);\n    }\n\n    /**\n     * This constructor is used by the parser and is considered private.\n     */\n    @Generated(\"com.github.javaparser.generator.core.node.MainConstructorGenerator\")\n    public Statement(TokenRange tokenRange) {\n        super(tokenRange);\n        customInitialization();\n    }\n\n    @Override\n    @Generated(\"com.github.javaparser.generator.core.node.CloneGenerator\")\n    public Statement clone() {\n        return (Statement) accept(new CloneVisitor(), null);\n    }\n\n    @Override\n    @Generated(\"com.github.javaparser.generator.core.node.GetMetaModelGenerator\")\n    public StatementMetaModel getMetaModel() {\n        return JavaParserMetaModel.statementMetaModel;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isAssertStmt() {\n        return StatementTypeCasting.isAssertStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public AssertStmt asAssertStmt() {\n        return StatementTypeCasting.asAssertStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isBlockStmt() {\n        return StatementTypeCasting.isBlockStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public BlockStmt asBlockStmt() {\n        return StatementTypeCasting.asBlockStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isBreakStmt() {\n        return StatementTypeCasting.isBreakStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public BreakStmt asBreakStmt() {\n        return StatementTypeCasting.asBreakStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isContinueStmt() {\n        return StatementTypeCasting.isContinueStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ContinueStmt asContinueStmt() {\n        return StatementTypeCasting.asContinueStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isDoStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public DoStmt asDoStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not DoStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isEmptyStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public EmptyStmt asEmptyStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not EmptyStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isExplicitConstructorInvocationStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ExplicitConstructorInvocationStmt asExplicitConstructorInvocationStmt() {\n        throw new IllegalStateException(f(\n                \"%s is not ExplicitConstructorInvocationStmt, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isExpressionStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ExpressionStmt asExpressionStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not ExpressionStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isForStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ForStmt asForStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not ForStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isIfStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public IfStmt asIfStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not IfStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLabeledStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LabeledStmt asLabeledStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not LabeledStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLocalClassDeclarationStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isLocalRecordDeclarationStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LocalClassDeclarationStmt asLocalClassDeclarationStmt() {\n        throw new IllegalStateException(f(\n                \"%s is not LocalClassDeclarationStmt, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public LocalRecordDeclarationStmt asLocalRecordDeclarationStmt() {\n        throw new IllegalStateException(f(\n                \"%s is not LocalRecordDeclarationStmt, it is %s\",\n                this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isReturnStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ReturnStmt asReturnStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not ReturnStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isSwitchStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public SwitchStmt asSwitchStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not SwitchStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isSynchronizedStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public SynchronizedStmt asSynchronizedStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not SynchronizedStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isThrowStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ThrowStmt asThrowStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not ThrowStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isTryStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public TryStmt asTryStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not TryStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isUnparsableStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public UnparsableStmt asUnparsableStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not UnparsableStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isWhileStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public WhileStmt asWhileStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not WhileStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifAssertStmt(Consumer<AssertStmt> action) { StatementTypeCasting.ifAssertStmt(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifBlockStmt(Consumer<BlockStmt> action) { StatementTypeCasting.ifBlockStmt(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifBreakStmt(Consumer<BreakStmt> action) { StatementTypeCasting.ifBreakStmt(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifContinueStmt(Consumer<ContinueStmt> action) { StatementTypeCasting.ifContinueStmt(this, action); }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifDoStmt(Consumer<DoStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifEmptyStmt(Consumer<EmptyStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifExplicitConstructorInvocationStmt(Consumer<ExplicitConstructorInvocationStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifExpressionStmt(Consumer<ExpressionStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifForStmt(Consumer<ForStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifIfStmt(Consumer<IfStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLabeledStmt(Consumer<LabeledStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLocalClassDeclarationStmt(Consumer<LocalClassDeclarationStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifLocalRecordDeclarationStmt(Consumer<LocalRecordDeclarationStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifReturnStmt(Consumer<ReturnStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifSwitchStmt(Consumer<SwitchStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifSynchronizedStmt(Consumer<SynchronizedStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifThrowStmt(Consumer<ThrowStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifTryStmt(Consumer<TryStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifUnparsableStmt(Consumer<UnparsableStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifWhileStmt(Consumer<WhileStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<AssertStmt> toAssertStmt() {\n        return StatementTypeCasting.toAssertStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<BlockStmt> toBlockStmt() {\n        return StatementTypeCasting.toBlockStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<BreakStmt> toBreakStmt() {\n        return StatementTypeCasting.toBreakStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ContinueStmt> toContinueStmt() {\n        return StatementTypeCasting.toContinueStmt(this);\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<DoStmt> toDoStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<EmptyStmt> toEmptyStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ExplicitConstructorInvocationStmt> toExplicitConstructorInvocationStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ExpressionStmt> toExpressionStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ForStmt> toForStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<IfStmt> toIfStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LabeledStmt> toLabeledStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LocalClassDeclarationStmt> toLocalClassDeclarationStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<LocalRecordDeclarationStmt> toLocalRecordDeclarationStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ReturnStmt> toReturnStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<SwitchStmt> toSwitchStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<SynchronizedStmt> toSynchronizedStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ThrowStmt> toThrowStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<TryStmt> toTryStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<UnparsableStmt> toUnparsableStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<WhileStmt> toWhileStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isForEachStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public ForEachStmt asForEachStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not ForEachStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<ForEachStmt> toForEachStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifForEachStmt(Consumer<ForEachStmt> action) {}\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public boolean isYieldStmt() {\n        return false;\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public YieldStmt asYieldStmt() {\n        throw new IllegalStateException(\n                f(\"%s is not YieldStmt, it is %s\", this, this.getClass().getSimpleName()));\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public Optional<YieldStmt> toYieldStmt() {\n        return Optional.empty();\n    }\n\n    @Generated(\"com.github.javaparser.generator.core.node.TypeCastingGenerator\")\n    public void ifYieldStmt(Consumer<YieldStmt> action) {}\n}\n"
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/ast/stmt/StatementTypeAccessors.java",
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
