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
- ADD_OR_UPDATE_IMPORTS
- CREATE_PACKAGE
- DEPENDENCY_INVERSION
- EXTRACT_CLASS
- EXTRACT_INTERFACE
- INTRODUCE_FACADE
- MOVE_CLASS
- MOVE_FIELD
- MOVE_METHOD
- REPLACE_DEPENDENCY
- UPDATE_CALL_SITES

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "com.github.javaparser.symbolsolver.javaparser.Navigator",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261013_103652_IM__com_github_javaparser_symbolsolver_javaparser_Navigator/run_003/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "javaparser-symbol-solver-core/src/main/java/com/github/javaparser/symbolsolver/javaparser/Navigator.java",
  "target_source_root": "javaparser-symbol-solver-core/src/main/java",
  "target_code": "/*\n * Copyright (C) 2015-2016 Federico Tomassetti\n * Copyright (C) 2017-2020 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\n\npackage com.github.javaparser.symbolsolver.javaparser;\n\nimport com.github.javaparser.ast.CompilationUnit;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;\nimport com.github.javaparser.ast.body.ConstructorDeclaration;\nimport com.github.javaparser.ast.body.EnumDeclaration;\nimport com.github.javaparser.ast.body.MethodDeclaration;\nimport com.github.javaparser.ast.body.TypeDeclaration;\nimport com.github.javaparser.ast.body.VariableDeclarator;\nimport com.github.javaparser.ast.expr.MethodCallExpr;\nimport com.github.javaparser.ast.expr.NameExpr;\nimport com.github.javaparser.ast.expr.SimpleName;\nimport com.github.javaparser.ast.stmt.ReturnStmt;\nimport com.github.javaparser.ast.stmt.SwitchStmt;\n\nimport java.util.Optional;\n\n/**\n * This class can be used to easily retrieve nodes from a JavaParser AST.\n *\n * Note that methods with the prefix `demand` indicate that if the search value is not found, an exception will be thrown.\n *\n * @author Federico Tomassetti\n */\npublic final class Navigator {\n\n    private Navigator() {\n        // prevent instantiation\n    }\n\n    public static <N extends Node> N demandNodeOfGivenClass(Node node, Class<N> clazz) {\n        return NavigatorNodeLookup.demandNodeOfGivenClass(node, clazz);\n    }\n\n    public static Node demandParentNode(Node node) {\n        return NavigatorNodeLookup.demandParentNode(node);\n    }\n\n    public static ReturnStmt demandReturnStmt(MethodDeclaration method) {\n        return NavigatorNodeLookup.demandReturnStmt(method);\n    }\n\n    public static SwitchStmt demandSwitch(Node node) {\n        return NavigatorNodeLookup.demandSwitch(node);\n    }\n\n    public static Optional<VariableDeclarator> demandVariableDeclaration(Node node, String name) {\n        return NavigatorNodeLookup.demandVariableDeclaration(node, name);\n    }\n\n    public static Optional<MethodCallExpr> findMethodCall(Node node, String methodName) {\n        return NavigatorNodeLookup.findMethodCall(node, methodName);\n    }\n\n    public static Optional<NameExpr> findNameExpression(Node node, String name) {\n        return NavigatorNodeLookup.findNameExpression(node, name);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorNodeLookup#demandNodeOfGivenClass(Node, Class)}\n     */\n    @Deprecated\n    public static <N extends Node> N findNodeOfGivenClass(Node node, Class<N> clazz) {\n        return NavigatorNodeLookup.findNodeOfGivenClass(node, clazz);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorNodeLookup#demandReturnStmt(MethodDeclaration)}\n     */\n    @Deprecated\n    public static ReturnStmt findReturnStmt(MethodDeclaration method) {\n        return NavigatorNodeLookup.findReturnStmt(method);\n    }\n\n    public static Optional<SimpleName> findSimpleName(Node node, String name) {\n        return NavigatorNodeLookup.findSimpleName(node, name);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorNodeLookup#demandSwitch(Node)}\n     */\n    @Deprecated\n    public static SwitchStmt findSwitch(Node node) {\n        return NavigatorNodeLookup.findSwitch(node);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorNodeLookup#demandParentNode(Node)}\n     */\n    @Deprecated\n    public static Node requireParentNode(Node node) {\n        return NavigatorNodeLookup.requireParentNode(node);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorDeclarationLookup#demandConstructor(TypeDeclaration, int)}\n     */\n    @Deprecated\n    public static ConstructorDeclaration demandConstructor(TypeDeclaration<?> td, int index) {\n        return NavigatorDeclarationLookup.demandConstructor(td, index);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorDeclarationLookup#demandField(ClassOrInterfaceDeclaration, String)}\n     */\n    @Deprecated\n    public static VariableDeclarator demandField(ClassOrInterfaceDeclaration cd, String name) {\n        return NavigatorDeclarationLookup.demandField(cd, name);\n    }\n\n    /**\n     * @deprecated Use {@link NavigatorDeclarationLookup#demandMethod(TypeDeclaration, String)}\n     */\n    @Deprecated\n    public static MethodDeclaration demandMethod(TypeDeclaration<?> cd, String name) {\n        return NavigatorDeclarationLookup.demandMethod(cd, name);\n    }\n\n    public static ClassOrInterfaceDeclaration demandClass(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandClass(cu, qualifiedName);\n    }\n\n    public static ClassOrInterfaceDeclaration demandClassOrInterface(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandClassOrInterface(cu, qualifiedName);\n    }\n\n    public static EnumDeclaration demandEnum(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandEnum(cu, qualifiedName);\n    }\n\n    public static ClassOrInterfaceDeclaration demandInterface(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.demandInterface(cu, qualifiedName);\n    }\n\n    /**\n     * Looks among the type declared in the Compilation Unit for one having the specified name.\n     * The name can be qualified with respect to the compilation unit. For example, if the compilation\n     * unit is in package a.b; and it contains two top level classes named C and D, with class E being defined inside D\n     * then the qualifiedName that can be resolved are \"C\", \"D\", and \"D.E\".\n     */\n    public static Optional<TypeDeclaration<?>> findType(CompilationUnit cu, String qualifiedName) {\n        return NavigatorTypeLookup.findType(cu, qualifiedName);\n    }\n\n    /**\n     * Looks among the type declared in the TypeDeclaration for one having the specified name.\n     * The name can be qualified with respect to the TypeDeclaration. For example, if the class declaration defines\n     * class D and class D contains an internal class named E then the qualifiedName that can be resolved are \"D\", and\n     * \"D.E\".\n     */\n    public static Optional<TypeDeclaration<?>> findType(TypeDeclaration<?> td, String qualifiedName) {\n        return NavigatorTypeLookup.findType(td, qualifiedName);\n    }\n\n}\n"
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