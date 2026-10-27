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
    "smell": "HM",
    "smell_name": "Hub-like Modularization",
    "target_type": "class",
    "target_name": "com.github.javaparser.printer.lexicalpreservation.LexicalPreservingPrinter"
  },
  "block": {
    "id": 1,
    "goal": "Move one cohesive lexical text-model cluster to a dedicated subpackage.",
    "files": [
      "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/NodeText.java",
      "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TextElement.java",
      "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TokenTextElement.java",
      "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/ChildTextElement.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "com.github.javaparser.printer.lexicalpreservation.text"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "com.github.javaparser.printer.lexicalpreservation.NodeText"
        ],
        "outputs": [
          "com.github.javaparser.printer.lexicalpreservation.text.NodeText"
        ],
        "details": "Move NodeText to the dedicated lexical text-model subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "com.github.javaparser.printer.lexicalpreservation.TextElement"
        ],
        "outputs": [
          "com.github.javaparser.printer.lexicalpreservation.text.TextElement"
        ],
        "details": "Move the common text-element abstraction to the dedicated lexical text-model subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "com.github.javaparser.printer.lexicalpreservation.TokenTextElement"
        ],
        "outputs": [
          "com.github.javaparser.printer.lexicalpreservation.text.TokenTextElement"
        ],
        "details": "Move TokenTextElement with the text-element model classes it specializes.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "com.github.javaparser.printer.lexicalpreservation.ChildTextElement"
        ],
        "outputs": [
          "com.github.javaparser.printer.lexicalpreservation.text.ChildTextElement"
        ],
        "details": "Move ChildTextElement with the text-element model classes it specializes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/ChildTextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/NodeText.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TokenTextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/ChildTextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/NodeText.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TokenTextElement.java"
  ],
  "executor_existing_files": [
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/ChildTextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/NodeText.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TokenTextElement.java"
  ],
  "executor_new_files": [
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/ChildTextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/NodeText.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TextElement.java",
    "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TokenTextElement.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/ChildTextElement.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/NodeText.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TextElement.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/TokenTextElement.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/ChildTextElement.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2023 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.printer.lexicalpreservation.text;\n\nimport com.github.javaparser.Range;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.ast.comments.Comment;\nimport com.github.javaparser.printer.lexicalpreservation.text.NodeText;\nimport com.github.javaparser.printer.lexicalpreservation.text.TextElement;\n\nimport java.util.Optional;\n\n/**\n * Represent the position of a child node in the NodeText of its parent.\n */\nclass ChildTextElement extends TextElement {\n\n    private final Node child;\n\n    ChildTextElement(Node child) {\n        this.child = child;\n    }\n\n    String expand() {\n        return LexicalPreservingPrinter.print(child);\n    }\n\n    Node getChild() {\n        return child;\n    }\n\n    @Override\n    boolean isToken(int tokenKind) {\n        return false;\n    }\n\n    @Override\n    boolean isNode(Node node) {\n        return node == child;\n    }\n\n    NodeText getNodeTextForWrappedNode() {\n        return LexicalPreservingPrinter.getOrCreateNodeText(child);\n    }\n\n    @Override\n    public boolean equals(Object o) {\n        if (this == o)\n            return true;\n        if (o == null || getClass() != o.getClass())\n            return false;\n        ChildTextElement that = (ChildTextElement) o;\n        return child.equals(that.child);\n    }\n\n    @Override\n    public int hashCode() {\n        return child.hashCode();\n    }\n\n    @Override\n    public String toString() {\n        return \"ChildTextElement{\" + child + '}';\n    }\n\n    @Override\n    public boolean isWhiteSpace() {\n        return false;\n    }\n\n    @Override\n    public boolean isSpaceOrTab() {\n        return false;\n    }\n\n    @Override\n    public boolean isNewline() {\n        return false;\n    }\n\n    @Override\n    public boolean isComment() {\n        return child instanceof Comment;\n    }\n\n    @Override\n    public boolean isSeparator() {\n        return false;\n    }\n\n    @Override\n    public boolean isIdentifier() {\n        return false;\n    }\n\n    @Override\n    public boolean isKeyword() {\n        return false;\n    }\n\n    @Override\n    public boolean isPrimitive() {\n        return false;\n    }\n\n    @Override\n    public boolean isLiteral() {\n        return false;\n    }\n\n    @Override\n    public boolean isChildOfClass(Class<? extends Node> nodeClass) {\n        return nodeClass.isInstance(child);\n    }\n\n    @Override\n    Optional<Range> getRange() {\n        return child.getRange();\n    }\n\n\t@Override\n\tpublic void accept(LexicalPreservingVisitor visitor) {\n\t\tNodeText nodeText = getNodeTextForWrappedNode();\n\t\tnodeText.getElements().forEach(element -> element.accept(visitor));\n\t}\n}\n"
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/NodeText.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2023 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.printer.lexicalpreservation.text;\n\nimport com.github.javaparser.ast.Node;\n\nimport java.util.LinkedList;\nimport java.util.List;\n\n/**\n * This contains the lexical information for a single node.\n * It is basically a list of tokens and children.\n */\nclass NodeText {\n\n    private final List<TextElement> elements;\n\n    public static final int NOT_FOUND = -1;\n\n    // \n    // Constructors\n    // \n    NodeText(List<TextElement> elements) {\n        this.elements = elements;\n    }\n\n    /**\n     * Initialize with an empty list of elements.\n     */\n    NodeText() {\n        this(new LinkedList<>());\n    }\n\n    // \n    // Adding elements\n    // \n    /**\n     * Add an element at the end.\n     */\n    void addElement(TextElement nodeTextElement) {\n        this.elements.add(nodeTextElement);\n    }\n\n    /**\n     * Add an element at the given position.\n     */\n    void addElement(int index, TextElement nodeTextElement) {\n        this.elements.add(index, nodeTextElement);\n    }\n\n    void addChild(Node child) {\n        addElement(new ChildTextElement(child));\n    }\n\n    void addChild(int index, Node child) {\n        addElement(index, new ChildTextElement(child));\n    }\n\n    void addToken(int tokenKind, String text) {\n        elements.add(new TokenTextElement(tokenKind, text));\n    }\n\n    void addToken(int index, int tokenKind, String text) {\n        elements.add(index, new TokenTextElement(tokenKind, text));\n    }\n\n    // \n    // Finding elements\n    // \n    int findElement(TextElementMatcher matcher) {\n        return findElement(matcher, 0);\n    }\n\n    int findElement(TextElementMatcher matcher, int from) {\n        int res = tryToFindElement(matcher, from);\n        if (res == NOT_FOUND) {\n            throw new IllegalArgumentException(String.format(\"I could not find child '%s' from position %d. Elements: %s\", matcher, from, elements));\n        }\n        return res;\n    }\n\n    int tryToFindElement(TextElementMatcher matcher, int from) {\n        for (int i = from; i < elements.size(); i++) {\n            TextElement element = elements.get(i);\n            if (matcher.match(element)) {\n                return i;\n            }\n        }\n        return NOT_FOUND;\n    }\n\n    int findChild(Node child) {\n        return findChild(child, 0);\n    }\n\n    int findChild(Node child, int from) {\n        return findElement(TextElementMatchers.byNode(child), from);\n    }\n\n    int tryToFindChild(Node child) {\n        return tryToFindChild(child, 0);\n    }\n\n    int tryToFindChild(Node child, int from) {\n        return tryToFindElement(TextElementMatchers.byNode(child), from);\n    }\n\n    // \n    // Removing single elements\n    // \n    public void remove(TextElementMatcher matcher, boolean potentiallyFollowingWhitespace) {\n        int i = 0;\n        for (TextElement e : elements) {\n            if (matcher.match(e)) {\n                elements.remove(e);\n                if (potentiallyFollowingWhitespace) {\n                    if (i < elements.size()) {\n                        if (elements.get(i).isWhiteSpace()) {\n                            elements.remove(i);\n                        }\n                    } else {\n                        throw new UnsupportedOperationException();\n                    }\n                }\n                return;\n            }\n        }\n        throw new IllegalArgumentException();\n    }\n\n    // \n    // Removing sequences\n    // \n    void removeElement(int index) {\n        elements.remove(index);\n    }\n\n    // \n    // Replacing elements\n    // \n    void replace(TextElementMatcher position, TextElement newElement) {\n        int index = findElement(position, 0);\n        elements.remove(index);\n        elements.add(index, newElement);\n    }\n\n    // \n    // Other methods\n    // \n    /**\n     * Generate the corresponding string.\n     */\n    String expand() {\n        StringBuffer sb = new StringBuffer();\n        elements.forEach(e -> sb.append(e.expand()));\n        return sb.toString();\n    }\n\n    // Visible for testing\n    int numberOfElements() {\n        return elements.size();\n    }\n\n    // Visible for testing\n    TextElement getTextElement(int index) {\n        return elements.get(index);\n    }\n\n    // Visible for testing\n    List<TextElement> getElements() {\n        return elements;\n    }\n\n    @Override\n    public String toString() {\n        return \"NodeText{\" + elements + '}';\n    }\n}\n"
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TextElement.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2023 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.printer.lexicalpreservation.text;\n\nimport com.github.javaparser.GeneratedJavaParserConstants;\nimport com.github.javaparser.Range;\nimport com.github.javaparser.ast.Node;\n\nimport java.util.Optional;\n\npublic abstract class TextElement implements TextElementMatcher, PrintableTextElement {\n\n    abstract String expand();\n\n    abstract boolean isToken(int tokenKind);\n\n    final boolean isCommentToken() {\n        return isToken(GeneratedJavaParserConstants.JAVADOC_COMMENT) || isToken(GeneratedJavaParserConstants.SINGLE_LINE_COMMENT) || isToken(GeneratedJavaParserConstants.MULTI_LINE_COMMENT);\n    }\n\n    @Override\n    public boolean match(TextElement textElement) {\n        return this.equals(textElement);\n    }\n\n    abstract boolean isNode(Node node);\n\n    public abstract boolean isLiteral();\n\n    public abstract boolean isWhiteSpace();\n\n    public abstract boolean isSpaceOrTab();\n\n    public abstract boolean isNewline();\n\n    public abstract boolean isComment();\n\n    public abstract boolean isSeparator();\n\n    public abstract boolean isIdentifier();\n\n    public abstract boolean isKeyword();\n\n    public abstract boolean isPrimitive();\n\n    public final boolean isWhiteSpaceOrComment() {\n        return isWhiteSpace() || isComment();\n    }\n\n    /**\n     * Is this TextElement representing a child of the given class?\n     */\n    public abstract boolean isChildOfClass(Class<? extends Node> nodeClass);\n\n    public boolean isChild() {\n        return isChildOfClass(Node.class);\n    }\n\n    abstract Optional<Range> getRange();\n\n    /**\n     * Creates a {@link TextElementMatcher} that matches any TextElement with the same range as this TextElement.<br>\n     * This can be used to curry another TextElementMatcher.<br>\n     * e.g. {@code someTextElementMatcher.and(textElement.matchByRange());}\n     *\n     * @return TextElementMatcher that matches any TextElement with the same Range\n     */\n    TextElementMatcher matchByRange() {\n        return (TextElement textElement) -> getRange().flatMap(r1 -> textElement.getRange().map(r1::equals)).// We're missing range information. This may happen when a node is manually instantiated. Don't be too harsh on that:\n        orElse(true);\n    }\n}\n"
    },
    {
      "path": "javaparser-core/src/main/java/com/github/javaparser/printer/lexicalpreservation/text/TokenTextElement.java",
      "exists": "true",
      "content": "/*\n * Copyright (C) 2007-2010 Júlio Vilmar Gesser.\n * Copyright (C) 2011, 2013-2023 The JavaParser Team.\n *\n * This file is part of JavaParser.\n *\n * JavaParser can be used either under the terms of\n * a) the GNU Lesser General Public License as published by\n *     the Free Software Foundation, either version 3 of the License, or\n *     (at your option) any later version.\n * b) the terms of the Apache License\n *\n * You should have received a copy of both licenses in LICENCE.LGPL and\n * LICENCE.APACHE. Please refer to those files for details.\n *\n * JavaParser is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU Lesser General Public License for more details.\n */\npackage com.github.javaparser.printer.lexicalpreservation.text;\n\nimport com.github.javaparser.JavaToken;\nimport com.github.javaparser.JavaToken.Kind;\nimport com.github.javaparser.Range;\nimport com.github.javaparser.ast.Node;\nimport com.github.javaparser.printer.lexicalpreservation.text.TextElement;\n\nimport java.util.Optional;\n\nclass TokenTextElement extends TextElement {\n\n    private final JavaToken token;\n\n    TokenTextElement(JavaToken token) {\n        this.token = token;\n    }\n\n    TokenTextElement(int tokenKind, String text) {\n        this(new JavaToken(tokenKind, text));\n    }\n\n    TokenTextElement(int tokenKind) {\n        this(new JavaToken(tokenKind));\n    }\n\n    @Override\n    String expand() {\n        return token.getText();\n    }\n\n    // Visible for testing\n    String getText() {\n        return token.getText();\n    }\n\n    int getTokenKind() {\n        return token.getKind();\n    }\n\n    public JavaToken getToken() {\n        return token;\n    }\n\n    @Override\n    public boolean equals(Object o) {\n        if (this == o)\n            return true;\n        if (o == null || getClass() != o.getClass())\n            return false;\n        TokenTextElement that = (TokenTextElement) o;\n        return token.equals(that.token);\n    }\n\n    @Override\n    public int hashCode() {\n        return token.hashCode();\n    }\n\n    @Override\n    public String toString() {\n        return token.toString();\n    }\n\n    @Override\n    boolean isToken(int tokenKind) {\n        return token.getKind() == tokenKind;\n    }\n\n    @Override\n    boolean isNode(Node node) {\n        return false;\n    }\n\n    @Override\n    public boolean isWhiteSpace() {\n        return token.getCategory().isWhitespace();\n    }\n\n    @Override\n    public boolean isSpaceOrTab() {\n        return token.getCategory().isWhitespaceButNotEndOfLine();\n    }\n\n    @Override\n    public boolean isComment() {\n        return token.getCategory().isComment();\n    }\n\n    @Override\n    public boolean isSeparator() {\n        return token.getCategory().isSeparator();\n    }\n\n    @Override\n    public boolean isNewline() {\n        return token.getCategory().isEndOfLine();\n    }\n\n    @Override\n    public boolean isChildOfClass(Class<? extends Node> nodeClass) {\n        return false;\n    }\n\n    @Override\n    public boolean isIdentifier() {\n        return getToken().getCategory().isIdentifier();\n    }\n\n    @Override\n    public boolean isKeyword() {\n        return getToken().getCategory().isKeyword();\n    }\n\n    @Override\n    public boolean isLiteral() {\n        return getToken().getCategory().isLiteral();\n    }\n\n    @Override\n    public boolean isPrimitive() {\n        return Kind.valueOf(getTokenKind()).isPrimitive();\n    }\n\n    @Override\n    Optional<Range> getRange() {\n        return token.getRange();\n    }\n\n\t@Override\n\tpublic void accept(LexicalPreservingVisitor visitor) {\n\t\tvisitor.visit(this);\n\t}\n}\n"
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
