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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/javaparser/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "com.github.javaparser.symbolsolver.javaparser.Navigator"
  },
  "block": {
    "id": 2,
    "goal": "Remove node-navigation delegation methods from Navigator and use the existing NavigatorNodeLookup component as their owner.",
    "files": [
      "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/Navigator.java",
      "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/NavigatorNodeLookup.java"
    ],
    "ops": [
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandNodeOfGivenClass(Node, Class)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandParentNode(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandReturnStmt(MethodDeclaration)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandSwitch(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandVariableDeclaration(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findMethodCall(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findNameExpression(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findNodeOfGivenClass(Node, Class)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findReturnStmt(MethodDeclaration)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findSimpleName(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findSwitch(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.requireParentNode(Node)"
        ],
        "outputs": [
          "com.github.javaparser.symbolsolver.javaparser.NavigatorNodeLookup"
        ],
        "details": "Transfer the node-oriented public operations to the existing NavigatorNodeLookup component. Preserve the deprecated status and documentation of findNodeOfGivenClass, findReturnStmt, findSwitch, and requireParentNode.",
        "risk": "high"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandNodeOfGivenClass(Node, Class)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandParentNode(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandReturnStmt(MethodDeclaration)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandSwitch(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.demandVariableDeclaration(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findMethodCall(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findNameExpression(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findNodeOfGivenClass(Node, Class)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findReturnStmt(MethodDeclaration)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findSimpleName(Node, String)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.findSwitch(Node)",
          "com.github.javaparser.symbolsolver.javaparser.Navigator.requireParentNode(Node)"
        ],
        "outputs": [
          "com.github.javaparser.symbolsolver.javaparser.NavigatorNodeLookup"
        ],
        "details": "Update all callers to use NavigatorNodeLookup after the methods are removed from Navigator. Retain equivalent generic signatures and Optional return types.",
        "risk": "high"
      }
    ]
  },
  "allowed_files": [
    "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/Navigator.java",
    "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/NavigatorNodeLookup.java"
  ],
  "executor_existing_files": [
    "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/Navigator.java",
    "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/NavigatorNodeLookup.java"
  ],
  "executor_new_files": [],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/Navigator.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2015-2016 Federico Tomassetti\n * Copyright (C) 2017-2020 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\n\npackage com.github.javaparser.symbolsolver.javaparser;\n\nimport com.github.javaparser.ast.CompilationUnit;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.body.*;\n\nimport java.util.Optional;\n\n/**\n * This class can be used to easily retrieve nodes from a JavaParser AST.\n *\n * Note that methods with the prefix `demand` indicate that if the search value is not found, an exception will be thrown.\n *\n * @author Federico Tomassetti\n */\npublic final class Navigator {\n\n    private Navigator() {\n        // prevent instantiation\n    }\n\n    /**\n     * Returns the {@code (i+1)}'th constructor of the given type declaration, in textual order. The constructor that\n     * appears first has the index 0, the second one the index 1, and so on.\n     *\n     * @param td    The type declaration to search in. Note that only classes and enums have constructors.\n     * @param index The index of the desired constructor.\n     * @return The desired ConstructorDeclaration if it was found, else an exception is thrown.\n     */\n    public static ConstructorDeclaration demandConstructor(TypeDeclaration<?> td, int index) {\n        return NavigatorDeclarationLookup.demandConstructor(td, index);\n    }\n\n    public static VariableDeclarator demandField(ClassOrInterfaceDeclaration cd, String name) {\n        return NavigatorDeclarationLookup.demandField(cd, name);\n    }\n\n    public static MethodDeclaration demandMethod(TypeDeclaration<?> cd, String name) {\n        return NavigatorDeclarationLookup.demandMethod(cd, name);\n    }\n\n    public static ClassOrInterfaceDeclaration demandClass(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandClass(cu, qualifiedName);\n    }\n\n    public static ClassOrInterfaceDeclaration demandClassOrInterface(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandClassOrInterface(cu, qualifiedName);\n    }\n\n    public static EnumDeclaration demandEnum(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandEnum(cu, qualifiedName);\n    }\n\n    public static ClassOrInterfaceDeclaration demandInterface(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandInterface(cu, qualifiedName);\n    }\n\n    public static <N extends Node> N demandNodeOfGivenClass(Node node, Class<N> clazz) {\n        return NavigatorNodeLookup.demandNodeOfGivenClass(node, clazz);\n    }\n\n    public static Node demandParentNode(Node node) {\n        return NavigatorNodeLookup.demandParentNode(node);\n    }\n\n    public static com.github.javaparser.ast.stmt.ReturnStmt demandReturnStmt(MethodDeclaration method) {\n        return NavigatorNodeLookup.demandReturnStmt(method);\n    }\n\n    public static com.github.javaparser.ast.stmt.SwitchStmt demandSwitch(Node node) {\n        return NavigatorNodeLookup.demandSwitch(node);\n    }\n\n    public static Optional<VariableDeclarator> demandVariableDeclaration(Node node, String name) {\n        return NavigatorNodeLookup.demandVariableDeclaration(node, name);\n    }\n\n    public static Optional<com.github.javaparser.ast.expr.MethodCallExpr> findMethodCall(Node node, String methodName) {\n        return NavigatorNodeLookup.findMethodCall(node, methodName);\n    }\n\n    public static Optional<com.github.javaparser.ast.expr.NameExpr> findNameExpression(Node node, String name) {\n        return NavigatorNodeLookup.findNameExpression(node, name);\n    }\n\n    /**\n     * @deprecated Use {@link #demandNodeOfGivenClass(Node, Class)}\n     */\n    @Deprecated\n    public static <N extends Node> N findNodeOfGivenClass(Node node, Class<N> clazz) {\n        return NavigatorNodeLookup.findNodeOfGivenClass(node, clazz);\n    }\n\n    /**\n     * @deprecated Use {@link #demandReturnStmt(MethodDeclaration)}\n     */\n    @Deprecated\n    public static com.github.javaparser.ast.stmt.ReturnStmt findReturnStmt(MethodDeclaration method) {\n        return NavigatorNodeLookup.findReturnStmt(method);\n    }\n\n    public static Optional<com.github.javaparser.ast.expr.SimpleName> findSimpleName(Node node, String name) {\n        return NavigatorNodeLookup.findSimpleName(node, name);\n    }\n\n    /**\n     * @deprecated Use {@link #demandSwitch(Node)}\n     */\n    @Deprecated\n    public static com.github.javaparser.ast.stmt.SwitchStmt findSwitch(Node node) {\n        return NavigatorNodeLookup.findSwitch(node);\n    }\n\n    /**\n     * Looks among the type declared in the Compilation Unit for one having the specified name.\n     * The name can be qualified with respect to the compilation unit. For example, if the compilation\n     * unit is in package a.b; and it contains two top level classes named C and D, with class E being defined inside D\n     * then the qualifiedName that can be resolved are \"C\", \"D\", and \"D.E\".\n     */\n    public static Optional<TypeDeclaration<?>> findType(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.findType(cu, qualifiedName);\n    }\n\n    /**\n     * Looks among the type declared in the TypeDeclaration for one having the specified name.\n     * The name can be qualified with respect to the TypeDeclaration. For example, if the class declaration defines\n     * class D and class D contains an internal class named E then the qualifiedName that can be resolved are \"D\", and\n     * \"D.E\".\n     */\n    public static Optional<TypeDeclaration<?>> findType(TypeDeclaration<?> td, String qualifiedName) {\n        return NavigatorTypeLookup.findType(td, qualifiedName);\n    }\n\n    /**\n     * @deprecated Use {@link #demandParentNode(Node)}\n     */\n    @Deprecated\n    public static Node requireParentNode(Node node) {\n        return NavigatorNodeLookup.requireParentNode(node);\n    }\n\n}\n"
    },
    {
      "path": "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/NavigatorNodeLookup.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2015-2016 Federico Tomassetti\n * Copyright (C) 2017-2020 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\n\npackage com.github.javaparser.symbolsolver.javaparser;\n\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.body.MethodDeclaration;\nimport com.github.javaparser.ast.body.VariableDeclarator;\nimport com.github.javaparser.ast.expr.MethodCallExpr;\nimport com.github.javaparser.ast.expr.NameExpr;\nimport com.github.javaparser.ast.expr.SimpleName;\nimport com.github.javaparser.ast.stmt.ReturnStmt;\nimport com.github.javaparser.ast.stmt.SwitchStmt;\n\nimport java.util.Optional;\n\n/**\n * Utility methods for searching and demanding nodes in a JavaParser AST.\n */\npublic final class NavigatorNodeLookup {\n\n    private NavigatorNodeLookup() {\n        // prevent instantiation\n    }\n\n    public static <N extends Node> N demandNodeOfGivenClass(Node node, Class<N> clazz) {\n        return node.findFirst(clazz).orElseThrow(IllegalArgumentException::new);\n    }\n\n    public static Node demandParentNode(Node node) {\n        return node.getParentNode().orElseThrow(() -> new IllegalStateException(\"Parent not found, the node does not appear to be inserted in a correct AST\"));\n    }\n\n    public static ReturnStmt demandReturnStmt(MethodDeclaration method) {\n        return demandNodeOfGivenClass(method, ReturnStmt.class);\n    }\n\n    public static SwitchStmt demandSwitch(Node node) {\n        return findSwitchHelper(node).orElseThrow(IllegalArgumentException::new);\n    }\n\n    public static Optional<VariableDeclarator> demandVariableDeclaration(Node node, String name) {\n        return node.findFirst(VariableDeclarator.class, n -> n.getNameAsString().equals(name));\n    }\n\n    public static Optional<MethodCallExpr> findMethodCall(Node node, String methodName) {\n        return node.findFirst(MethodCallExpr.class, n -> n.getNameAsString().equals(methodName));\n    }\n\n    public static Optional<NameExpr> findNameExpression(Node node, String name) {\n        return node.findFirst(NameExpr.class, n -> n.getNameAsString().equals(name));\n    }\n\n    /**\n     * @deprecated Use {@link #demandNodeOfGivenClass(Node, Class)}\n     */\n    @Deprecated\n    public static <N extends Node> N findNodeOfGivenClass(Node node, Class<N> clazz) {\n        return demandNodeOfGivenClass(node, clazz);\n    }\n\n    /**\n     * @deprecated Use {@link #demandReturnStmt(MethodDeclaration)}\n     */\n    @Deprecated\n    public static ReturnStmt findReturnStmt(MethodDeclaration method) {\n        return demandReturnStmt(method);\n    }\n\n    public static Optional<SimpleName> findSimpleName(Node node, String name) {\n        return node.findFirst(SimpleName.class, n -> n.asString().equals(name));\n    }\n\n    /**\n     * @deprecated Use {@link #demandSwitch(Node)}\n     */\n    @Deprecated\n    public static SwitchStmt findSwitch(Node node) {\n        return demandSwitch(node);\n    }\n\n    private static Optional<SwitchStmt> findSwitchHelper(Node node) {\n        if (node instanceof SwitchStmt) {\n            return Optional.of((SwitchStmt) node);\n        }\n\n        return node.findFirst(SwitchStmt.class);\n    }\n\n    /**\n     * @deprecated Use {@link #demandParentNode(Node)}\n     */\n    @Deprecated\n    public static Node requireParentNode(Node node) {\n        return demandParentNode(node);\n    }\n}\n"
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
