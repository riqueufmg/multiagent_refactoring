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
  "repo_path": "/data/henrique/langchain_prototype/new/data/repositories/jsoup",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.jsoup.parser.HtmlTreeBuilderState"
  },
  "block": {
    "id": 4,
    "goal": "Extract the InTemplate state's processing into a focused handler to reduce enum size and keep template-specific transitions and logic separate.",
    "files": [
      "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java",
      "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java",
      "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java"
        ],
        "outputs": [
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java",
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java"
        ],
        "details": "Create org.jsoup.parser.HtmlTreeBuilderStateTemplateHandler with a static method processInTemplate(Token t, HtmlTreeBuilder tb). Move the entire InTemplate enum state's process implementation into that method. Keep any small helper logic local to the new class. Retain package and imports.",
        "risk": "low"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java",
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java"
        ],
        "outputs": [
          "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java"
        ],
        "details": "Update the InTemplate enum element to delegate to HtmlTreeBuilderStateTemplateHandler.processInTemplate(Token, HtmlTreeBuilder).",
        "risk": "low"
      },
      {
        "op": "UPDATE_TESTS",
        "inputs": [
          "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java"
        ],
        "outputs": [],
        "details": "Update related tests affected by this refactoring block so the configured build command passes. Adjust imports, package references, moved class references, constructors, and assertions only when required. Do not change production behavior through tests.",
        "risk": "medium",
        "api_change": false
      }
    ],
    "test_files": [
      "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java"
    ]
  },
  "allowed_files": [
    "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java",
    "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java",
    "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java"
  ],
  "executor_existing_files": [
    "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java",
    "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java"
  ],
  "executor_new_files": [
    "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/org/jsoup/parser/HtmlTreeBuilderState.java",
      "exists": "true",
      "content": "package org.jsoup.parser;\n\nimport org.jsoup.helper.Validate;\nimport org.jsoup.internal.StringUtil;\nimport org.jsoup.nodes.Attribute;\nimport org.jsoup.nodes.Attributes;\nimport org.jsoup.nodes.Document;\nimport org.jsoup.nodes.DocumentType;\nimport org.jsoup.nodes.Element;\nimport org.jsoup.nodes.Node;\nimport org.jsoup.nodes.NodeInternals;\nimport org.jsoup.nodes.Range;\nimport org.jspecify.annotations.Nullable;\n\nimport java.util.ArrayList;\n\nimport static org.jsoup.internal.StringUtil.inSorted;\nimport static org.jsoup.parser.HtmlTreeBuilder.isSpecial;\nimport static org.jsoup.parser.HtmlTreeBuilderStateConstants.*;\n\n/**\n * The Tree Builder's current state. Each state embodies the processing for the state, and transitions to other states.\n */\nenum HtmlTreeBuilderState {\n    Initial {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processInitial(t, tb);\n        }\n    },\n    BeforeHtml {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processBeforeHtml(t, tb);\n        }\n\n        private boolean anythingElse(Token t, HtmlTreeBuilder tb) {\n            tb.processStartTag(\"html\");\n            tb.transition(BeforeHead);\n            return tb.process(t);\n        }\n    },\n    BeforeHead {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processBeforeHead(t, tb);\n        }\n    },\n    InHead {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processInHead(t, tb);\n        }\n\n        private boolean anythingElse(Token t, TreeBuilder tb) {\n            tb.processEndTag(\"head\");\n            return tb.process(t);\n        }\n    },\n    InHeadNoscript {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processInHeadNoscript(t, tb);\n        }\n\n        private boolean anythingElse(Token t, HtmlTreeBuilder tb) {\n            // note that this deviates from spec, which is to pop out of noscript and reprocess in head:\n            // https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inheadnoscript\n            // allows content to be inserted as data\n            tb.error(this);\n            tb.insertCharacterNode(new Token.Character().data(t.toString()));\n            return true;\n        }\n    },\n    AfterHead {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateHeadHandlers.processAfterHead(t, tb);\n        }\n\n        private boolean anythingElse(Token t, HtmlTreeBuilder tb) {\n            tb.processStartTag(\"body\");\n            tb.framesetOk(true);\n            return tb.process(t);\n        }\n    },\n    InBody {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateInBodyHandler.processInBody(t, tb);\n        }\n    },\n    Text {\n        // in script, style etc. normally treated as data tags\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (t.isCharacter()) {\n                tb.insertCharacterNode(t.asCharacter());\n            } else if (t.isEOF()) {\n                tb.error(this);\n                // if current node is script: already started\n                tb.pop();\n                tb.transition(tb.originalState());\n                if (tb.state() == Text) // stack is such that we couldn't transition out; just close\n                    tb.transition(InBody);\n                return tb.process(t);\n            } else if (t.isEndTag()) {\n                // if: An end tag whose tag name is \"script\" -- scripting nesting level, if evaluating scripts\n                tb.pop();\n                tb.transition(tb.originalState());\n            }\n            return true;\n        }\n    },\n    InTable {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInTable(t, tb);\n        }\n    },\n    InTableText {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInTableText(t, tb);\n        }\n    },\n    InCaption {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInCaption(t, tb);\n        }\n    },\n    InColumnGroup {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInColumnGroup(t, tb);\n        }\n    },\n    InTableBody {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInTableBody(t, tb);\n        }\n    },\n    InRow {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInRow(t, tb);\n        }\n    },\n    InCell {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateTableHandlers.processInCell(t, tb);\n        }\n    },\n    InSelect {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateSelectHandler.processInSelect(t, tb);\n        }\n\n    },\n    InSelectInTable {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (t.isStartTag() && inSorted(t.asStartTag().normalName(), InSelectTableEnd)) {\n                tb.error(this);\n                tb.popStackToClose(\"select\");\n                tb.resetInsertionMode();\n                return tb.process(t);\n            } else if (t.isEndTag() && inSorted(t.asEndTag().normalName(), InSelectTableEnd)) {\n                tb.error(this);\n                if (tb.inTableScope(t.asEndTag().normalName())) {\n                    tb.popStackToClose(\"select\");\n                    tb.resetInsertionMode();\n                    return (tb.process(t));\n                } else\n                    return false;\n            } else {\n                return tb.process(t, InSelect);\n            }\n        }\n    },\n    InTemplate {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            final String name;\n            switch (t.type) {\n                case Character:\n                case Comment:\n                case Doctype:\n                    tb.process(t, InBody);\n                    break;\n                case StartTag:\n                    name = t.asStartTag().normalName();\n                    if (inSorted(name, InTemplateToHead))\n                        tb.process(t, InHead);\n                    else if (inSorted(name, InTemplateToTable)) {\n                        tb.popTemplateMode();\n                        tb.pushTemplateMode(InTable);\n                        tb.transition(InTable);\n                        return tb.process(t);\n                    }\n                    else if (name.equals(\"col\")) {\n                        tb.popTemplateMode();\n                        tb.pushTemplateMode(InColumnGroup);\n                        tb.transition(InColumnGroup);\n                        return tb.process(t);\n                    } else if (name.equals(\"tr\")) {\n                        tb.popTemplateMode();\n                        tb.pushTemplateMode(InTableBody);\n                        tb.transition(InTableBody);\n                        return tb.process(t);\n                    } else if (name.equals(\"td\") || name.equals(\"th\")) {\n                        tb.popTemplateMode();\n                        tb.pushTemplateMode(InRow);\n                        tb.transition(InRow);\n                        return tb.process(t);\n                    } else {\n                        tb.popTemplateMode();\n                        tb.pushTemplateMode(InBody);\n                        tb.transition(InBody);\n                        return tb.process(t);\n                    }\n\n                    break;\n                case EndTag:\n                    name = t.asEndTag().normalName();\n                    if (name.equals(\"template\"))\n                        tb.process(t, InHead);\n                    else {\n                        tb.error(this);\n                        return false;\n                    }\n                    break;\n                case EOF:\n                    if (!tb.onStack(\"template\")) {// stop parsing\n                        return true;\n                    }\n                    tb.error(this);\n                    tb.popStackToClose(\"template\");\n                    tb.clearFormattingElementsToLastMarker();\n                    tb.popTemplateMode();\n                    tb.resetInsertionMode();\n                    // spec deviation - if we did not break out of Template, stop processing, and don't worry about cleaning up ultra-deep template stacks\n                    // limited depth because this can recurse and will blow stack if too deep\n                    if (tb.state() != InTemplate && tb.templateModeSize() < 12)\n                        return tb.process(t);\n                    else return true;\n                default:\n                    Validate.wtf(\"Unexpected state: \" + t.type); // XmlDecl only in XmlTreeBuilder\n            }\n            return true;\n        }\n    },\n    AfterBody {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            Element html = tb.getFromStack(\"html\");\n            if (HtmlTreeBuilderStateHelper.isWhitespace(t)) {\n                // spec deviation - currently body is still on stack, but we want this to go to the html node\n                if (html != null)\n                    tb.insertCharacterToElement(t.asCharacter(), html);\n                else\n                    tb.process(t, InBody); // will get into body\n            } else if (t.isComment()) {\n                tb.insertCommentNode(t.asComment()); // into html node\n            } else if (t.isDoctype()) {\n                tb.error(this);\n                return false;\n            } else if (t.isStartTag() && t.asStartTag().normalName().equals(\"html\")) {\n                return tb.process(t, InBody);\n            } else if (t.isEndTag() && t.asEndTag().normalName().equals(\"html\")) {\n                if (tb.isFragmentParsing()) {\n                    tb.error(this);\n                    return false;\n                } else {\n                    if (html != null) tb.trackNodePosition(html, false); // track source position of close; html is left on stack, in case of trailers\n                    tb.transition(AfterAfterBody);\n                }\n            } else if (t.isEOF()) {\n                // chillax! we're done\n            } else {\n                tb.error(this);\n                tb.resetBody();\n                return tb.process(t);\n            }\n            return true;\n        }\n    },\n    InFrameset {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (HtmlTreeBuilderStateHelper.isWhitespace(t)) {\n                tb.insertCharacterNode(t.asCharacter());\n            } else if (t.isComment()) {\n                tb.insertCommentNode(t.asComment());\n            } else if (t.isDoctype()) {\n                tb.error(this);\n                return false;\n            } else if (t.isStartTag()) {\n                Token.StartTag start = t.asStartTag();\n                switch (start.normalName()) {\n                    case \"html\":\n                        return tb.process(start, InBody);\n                    case \"frameset\":\n                        tb.insertElementFor(start);\n                        break;\n                    case \"frame\":\n                        tb.insertEmptyElementFor(start);\n                        break;\n                    case \"noframes\":\n                        return tb.process(start, InHead);\n                    default:\n                        tb.error(this);\n                        return false;\n                }\n            } else if (t.isEndTag() && t.asEndTag().normalName().equals(\"frameset\")) {\n                if (!tb.currentElementIs(\"frameset\")) { // spec checks if el is html; deviate to confirm we are about to pop the frameset el\n                    tb.error(this);\n                    return false;\n                } else {\n                    tb.pop();\n                    if (!tb.isFragmentParsing() && !tb.currentElementIs(\"frameset\")) {\n                        tb.transition(AfterFrameset);\n                    }\n                }\n            } else if (t.isEOF()) {\n                if (!tb.currentElementIs(\"html\")) {\n                    tb.error(this);\n                    return true;\n                }\n            } else {\n                tb.error(this);\n                return false;\n            }\n            return true;\n        }\n    },\n    AfterFrameset {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (HtmlTreeBuilderStateHelper.isWhitespace(t)) {\n                tb.insertCharacterNode(t.asCharacter());\n            } else if (t.isComment()) {\n                tb.insertCommentNode(t.asComment());\n            } else if (t.isDoctype()) {\n                tb.error(this);\n                return false;\n            } else if (t.isStartTag() && t.asStartTag().normalName().equals(\"html\")) {\n                return tb.process(t, InBody);\n            } else if (t.isEndTag() && t.asEndTag().normalName().equals(\"html\")) {\n                tb.transition(AfterAfterFrameset);\n            } else if (t.isStartTag() && t.asStartTag().normalName().equals(\"noframes\")) {\n                return tb.process(t, InHead);\n            } else if (t.isEOF()) {\n                // cool your heels, we're complete\n            } else {\n                tb.error(this);\n                return false;\n            }\n            return true;\n        }\n    },\n    AfterAfterBody {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (t.isComment()) {\n                tb.insertCommentNode(t.asComment());\n            } else if (t.isDoctype() || (t.isStartTag() && t.asStartTag().normalName().equals(\"html\"))) {\n                return tb.process(t, InBody);\n            } else if (HtmlTreeBuilderStateHelper.isWhitespace(t)) {\n                // spec deviation - body and html still on stack, but want this space to go after </html>\n                Element doc = tb.getDocument();\n                tb.insertCharacterToElement(t.asCharacter(), doc);\n            }else if (t.isEOF()) {\n                // nice work chuck\n            } else {\n                tb.error(this);\n                tb.resetBody();\n                return tb.process(t);\n            }\n            return true;\n        }\n    },\n    AfterAfterFrameset {\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            if (t.isComment()) {\n                tb.insertCommentNode(t.asComment());\n            } else if (t.isDoctype() || HtmlTreeBuilderStateHelper.isWhitespace(t) || (t.isStartTag() && t.asStartTag().normalName().equals(\"html\"))) {\n                return tb.process(t, InBody);\n            } else if (t.isEOF()) {\n                // nice work chuck\n            } else if (t.isStartTag() && t.asStartTag().normalName().equals(\"noframes\")) {\n                return tb.process(t, InHead);\n            } else {\n                tb.error(this);\n                return false;\n            }\n            return true;\n        }\n    },\n    ForeignContent {\n        // https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign\n        @Override boolean process(Token t, HtmlTreeBuilder tb) {\n            return HtmlTreeBuilderStateForeignContentHandler.processForeignContent(t, tb);\n        }\n    };\n\n    abstract boolean process(Token t, HtmlTreeBuilder tb);\n\n}\n"
    },
    {
      "path": "src/main/java/org/jsoup/parser/HtmlTreeBuilderStateTemplateHandler.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/test/java/org/jsoup/parser/HtmlTreeBuilderStateTest.java",
      "exists": "true",
      "content": "package org.jsoup.parser;\n\nimport org.jsoup.Jsoup;\nimport org.jsoup.internal.StringUtil;\nimport org.jsoup.parser.HtmlTreeBuilderStateConstants;\nimport org.junit.jupiter.api.Test;\n\nimport java.lang.reflect.Field;\nimport java.lang.reflect.Modifier;\nimport java.util.ArrayList;\nimport java.util.Arrays;\nimport java.util.List;\n\nimport static org.jsoup.parser.HtmlTreeBuilderStateConstants.InBodyStartInputAttribs;\nimport static org.junit.jupiter.api.Assertions.*;\n\npublic class HtmlTreeBuilderStateTest {\n    static List<Object[]> findConstantArrays(Class aClass) {\n        ArrayList<Object[]> array = new ArrayList<>();\n        Field[] fields = aClass.getDeclaredFields();\n\n        for (Field field : fields) {\n            int modifiers = field.getModifiers();\n            if (Modifier.isStatic(modifiers) && !Modifier.isPrivate(modifiers) && field.getType().isArray()) {\n                try {\n                    array.add((Object[]) field.get(null));\n                } catch (IllegalAccessException e) {\n                    throw new IllegalStateException(e);\n                }\n            }\n        }\n\n        return array;\n    }\n\n    static void ensureSorted(List<Object[]> constants) {\n        for (Object[] array : constants) {\n            Object[] copy = Arrays.copyOf(array, array.length);\n            Arrays.sort(array);\n            assertArrayEquals(array, copy);\n        }\n    }\n\n    @Test\n    public void ensureArraysAreSorted() {\n        List<Object[]> constants = findConstantArrays(HtmlTreeBuilderStateConstants.class);\n        ensureSorted(constants);\n        assertEquals(39, constants.size());\n    }\n\n    @Test public void ensureTagSearchesAreKnownTags() {\n        List<Object[]> constants = findConstantArrays(HtmlTreeBuilderStateConstants.class);\n        for (Object[] constant : constants) {\n            String[] tagNames = (String[]) constant;\n            for (String tagName : tagNames) {\n                if (StringUtil.inSorted(tagName, InBodyStartInputAttribs))\n                    continue; // odd one out in the constant\n                assertTrue(Tag.isKnownTag(tagName), String.format(\"Unknown tag name: %s\", tagName));\n            }\n        }\n    }\n\n\n    @Test\n    public void nestedAnchorElements01() {\n        String html = \"<html>\\n\" +\n            \"  <body>\\n\" +\n            \"    <a href='#1'>\\n\" +\n            \"        <div>\\n\" +\n            \"          <a href='#2'>child</a>\\n\" +\n            \"        </div>\\n\" +\n            \"    </a>\\n\" +\n            \"  </body>\\n\" +\n            \"</html>\";\n        String s = Jsoup.parse(html).toString();\n        assertEquals(\"<html>\\n\" +\n            \" <head></head>\\n\" +\n            \" <body>\\n\" +\n            \"  <a href=\\\"#1\\\"> </a>\\n\" +\n            \"  <div>\\n\" +\n            \"   <a href=\\\"#1\\\"> </a><a href=\\\"#2\\\">child</a>\\n\" +\n            \"  </div>\\n\" +\n            \" </body>\\n\" +\n            \"</html>\", s);\n    }\n\n    @Test\n    public void nestedAnchorElements02() {\n        String html = \"<html>\\n\" +\n            \"  <body>\\n\" +\n            \"    <a href='#1'>\\n\" +\n            \"      <div>\\n\" +\n            \"        <div>\\n\" +\n            \"          <a href='#2'>child</a>\\n\" +\n            \"        </div>\\n\" +\n            \"      </div>\\n\" +\n            \"    </a>\\n\" +\n            \"  </body>\\n\" +\n            \"</html>\";\n        String s = Jsoup.parse(html).toString();\n        assertEquals(\"<html>\\n\" +\n            \" <head></head>\\n\" +\n            \" <body>\\n\" +\n            \"  <a href=\\\"#1\\\"> </a>\\n\" +\n            \"  <div>\\n\" +\n            \"   <a href=\\\"#1\\\"> </a>\\n\" +\n            \"   <div>\\n\" +\n            \"    <a href=\\\"#1\\\"> </a><a href=\\\"#2\\\">child</a>\\n\" +\n            \"   </div>\\n\" +\n            \"  </div>\\n\" +\n            \" </body>\\n\" +\n            \"</html>\", s);\n    }\n\n}\n"
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
