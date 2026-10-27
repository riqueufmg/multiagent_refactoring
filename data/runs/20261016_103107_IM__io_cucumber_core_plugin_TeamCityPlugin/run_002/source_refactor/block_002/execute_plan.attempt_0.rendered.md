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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/cucumber-jvm/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "io.cucumber.core.plugin.TeamCityPlugin"
  },
  "block": {
    "id": 2,
    "goal": "Extract cohesive test-step naming and location formatting responsibilities from TeamCityPlugin to reduce general methods and simplify event handling.",
    "files": [
      "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityPlugin.java",
      "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityStepFormatter.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "io.cucumber.core.plugin.TeamCityPlugin",
          "io.cucumber.core.plugin.TeamCityStepFormatter"
        ],
        "outputs": [
          "io.cucumber.core.plugin.TeamCityStepFormatter"
        ],
        "details": "Extract the cohesive step naming and location logic represented by ANNOTATION_GLUE_CODE_LOCATION_PATTERN, LAMBDA_GLUE_CODE_LOCATION_PATTERN, extractLocation(TestStepStarted), javaTestLocationUri(), formatHookStepLocation(HookTestStep,BiFunction<String,String,String>,Function<HookTestStep,String>), getHookName(HookTestStep), extractName(TestStep), and hookNameFormat(HookTestStep) into TeamCityStepFormatter. Preserve the existing handling of PickleStepTestStep, HookTestStep, HookType, Java annotation locations, and Java 8 lambda locations.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "io.cucumber.core.plugin.TeamCityPlugin.extractLocation(TestStepStarted)",
          "io.cucumber.core.plugin.TeamCityPlugin.extractName(TestStep)",
          "io.cucumber.core.plugin.TeamCityPlugin.formatHookStepLocation(HookTestStep,BiFunction<String,String,String>,Function<HookTestStep,String>)",
          "io.cucumber.core.plugin.TeamCityPlugin.getHookName(HookTestStep)"
        ],
        "outputs": [
          "io.cucumber.core.plugin.TeamCityStepFormatter.extractLocation(TestStepStarted)",
          "io.cucumber.core.plugin.TeamCityStepFormatter.extractName(TestStep)",
          "io.cucumber.core.plugin.TeamCityStepFormatter.formatHookStepLocation(HookTestStep,BiFunction<String,String,String>,Function<HookTestStep,String>)",
          "io.cucumber.core.plugin.TeamCityStepFormatter.getHookName(HookTestStep)"
        ],
        "details": "Update printTestStepStarted and printTestStepFinished to delegate step name and location calculation to TeamCityStepFormatter. Remove the duplicated private step-formatting methods and regular expression fields from TeamCityPlugin after all references are updated.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityPlugin.java",
    "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityStepFormatter.java"
  ],
  "executor_existing_files": [
    "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityPlugin.java"
  ],
  "executor_new_files": [
    "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityStepFormatter.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityPlugin.java",
      "exists": "true",
      "content": "package io.cucumber.core.plugin;\n\nimport io.cucumber.plugin.EventListener;\nimport io.cucumber.plugin.event.*;\nimport io.cucumber.plugin.event.SnippetsSuggestedEvent.Suggestion;\n\nimport java.io.PrintStream;\nimport java.net.URI;\nimport java.util.*;\nimport java.util.function.BiFunction;\nimport java.util.function.Function;\nimport java.util.function.Predicate;\nimport java.util.function.Supplier;\nimport java.util.regex.Matcher;\nimport java.util.regex.Pattern;\nimport java.util.stream.Collectors;\n\nimport static io.cucumber.core.exception.ExceptionUtils.printStackTrace;\nimport static java.util.Collections.emptyList;\nimport static java.util.stream.Collectors.joining;\n\n/**\n * Outputs Teamcity services messages to std out.\n *\n * @see <a href=\n *      \"https://www.jetbrains.com/help/teamcity/service-messages.html\">TeamCity\n *      - Service Messages</a>\n */\npublic class TeamCityPlugin implements EventListener {\n    private static final Pattern ANNOTATION_GLUE_CODE_LOCATION_PATTERN = Pattern.compile(\"^(.*)\\\\.(.*)\\\\([^:]*\\\\)\");\n    private static final Pattern LAMBDA_GLUE_CODE_LOCATION_PATTERN = Pattern.compile(\"^(.*)\\\\.(.*)\\\\(.*:.*\\\\)\");\n\n    private final TeamCityMessageFormatter formatter;\n    private final List<SnippetsSuggestedEvent> suggestions = new ArrayList<>();\n    private final Map<URI, Collection<Node>> parsedTestSources = new HashMap<>();\n    private List<Node> currentStack = new ArrayList<>();\n    private TestCase currentTestCase;\n\n    @SuppressWarnings(\"unused\")\n    public TeamCityPlugin() {\n        this(System.out);\n    }\n\n    TeamCityPlugin(PrintStream out) {\n        this.formatter = new TeamCityMessageFormatter(out);\n    }\n\n    @Override\n    public void setEventPublisher(EventPublisher publisher) {\n        publisher.registerHandlerFor(TestRunStarted.class, this::printTestRunStarted);\n        publisher.registerHandlerFor(TestCaseStarted.class, this::printTestCaseStarted);\n        publisher.registerHandlerFor(TestStepStarted.class, this::printTestStepStarted);\n        publisher.registerHandlerFor(TestStepFinished.class, this::printTestStepFinished);\n        publisher.registerHandlerFor(TestCaseFinished.class, this::printTestCaseFinished);\n        publisher.registerHandlerFor(TestRunFinished.class, this::printTestRunFinished);\n        publisher.registerHandlerFor(SnippetsSuggestedEvent.class, this::handleSnippetSuggested);\n        publisher.registerHandlerFor(EmbedEvent.class, this::handleEmbedEvent);\n        publisher.registerHandlerFor(WriteEvent.class, this::handleWriteEvent);\n        publisher.registerHandlerFor(TestSourceParsed.class, this::handleTestSourceParsed);\n    }\n\n    private void handleTestSourceParsed(TestSourceParsed event) {\n        parsedTestSources.put(event.getUri(), event.getNodes());\n    }\n\n    private void printTestRunStarted(TestRunStarted event) {\n        String timestamp = formatter.extractTimeStamp(event);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_ENTER_THE_MATRIX, timestamp);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_RUN_STARTED, timestamp);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_PROGRESS_COUNTING_STARTED, timestamp);\n    }\n\n    private void printTestCaseStarted(TestCaseStarted event) {\n        TestCase testCase = event.getTestCase();\n        URI uri = testCase.getUri();\n        String timestamp = formatter.extractTimeStamp(event);\n        Location location = testCase.getLocation();\n        Predicate<Node> withLocation = candidate -> location.equals(candidate.getLocation());\n        List<Node> path = parsedTestSources.get(uri).stream().map(node -> node.findPathTo(withLocation))\n                .filter(Optional::isPresent).map(Optional::get).findFirst().orElse(emptyList());\n        poppedNodes(path).forEach(node -> finishNode(timestamp, node));\n        pushedNodes(path).forEach(node -> startNode(uri, timestamp, node));\n        currentStack = path;\n        currentTestCase = testCase;\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_PROGRESS_TEST_STARTED, timestamp);\n    }\n\n    private void startNode(URI uri, String timestamp, Node node) {\n        Supplier<String> keyword = () -> node.getKeyword().orElse(\"Unknown\");\n        String name = node.getName().orElseGet(keyword);\n        String location = uri + \":\" + node.getLocation().getLine();\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_SUITE_STARTED, timestamp, location, name);\n    }\n\n    private void finishNode(String timestamp, Node node) {\n        Supplier<String> keyword = () -> node.getKeyword().orElse(\"Unknown\");\n        String name = node.getName().orElseGet(keyword);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_SUITE_FINISHED, timestamp, name);\n    }\n\n    private List<Node> poppedNodes(List<Node> newStack) {\n        List<Node> nodes = new ArrayList<>(reversedPoppedNodes(currentStack, newStack));\n        Collections.reverse(nodes);\n        return nodes;\n    }\n\n    private List<Node> reversedPoppedNodes(List<Node> oldStack, List<Node> newStack) {\n        for (int i = 0; i < oldStack.size() && i < newStack.size(); i++) {\n            if (!oldStack.get(i).equals(newStack.get(i)))\n                return oldStack.subList(i, oldStack.size());\n        }\n        if (newStack.size() < oldStack.size())\n            return oldStack.subList(newStack.size(), oldStack.size());\n        return emptyList();\n    }\n\n    private List<Node> pushedNodes(List<Node> newStack) {\n        for (int i = 0; i < currentStack.size() && i < newStack.size(); i++) {\n            if (!currentStack.get(i).equals(newStack.get(i)))\n                return newStack.subList(i, newStack.size());\n        }\n        if (newStack.size() < currentStack.size())\n            return emptyList();\n        return newStack.subList(currentStack.size(), newStack.size());\n    }\n\n    private void printTestStepStarted(TestStepStarted event) {\n        String timestamp = formatter.extractTimeStamp(event);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_STARTED, timestamp, extractLocation(event),\n            extractName(event.getTestStep()));\n    }\n\n    private String extractLocation(TestStepStarted event) {\n        TestStep step = event.getTestStep();\n        if (step instanceof PickleStepTestStep) {\n            PickleStepTestStep pickle = (PickleStepTestStep) step;\n            return pickle.getUri() + \":\" + pickle.getStep().getLine();\n        }\n        if (step instanceof HookTestStep)\n            return formatHookStepLocation((HookTestStep) step, javaTestLocationUri(), TestStep::getCodeLocation);\n        return step.getCodeLocation();\n    }\n\n    private static BiFunction<String, String, String> javaTestLocationUri() {\n        return (declaringClass, method) -> String.format(\"java:test://%s/%s\", declaringClass, method);\n    }\n\n    private String formatHookStepLocation(\n            HookTestStep hook, BiFunction<String, String, String> format, Function<HookTestStep, String> fallback\n    ) {\n        Matcher matcher = ANNOTATION_GLUE_CODE_LOCATION_PATTERN.matcher(hook.getCodeLocation());\n        if (matcher.matches())\n            return format.apply(matcher.group(1), matcher.group(2));\n        matcher = LAMBDA_GLUE_CODE_LOCATION_PATTERN.matcher(hook.getCodeLocation());\n        if (matcher.matches()) {\n            String declaringClass = matcher.group(1);\n            int separator = declaringClass.lastIndexOf(\".\");\n            String simpleName = separator == -1 ? declaringClass : declaringClass.substring(separator + 1);\n            return format.apply(declaringClass, simpleName);\n        }\n        return fallback.apply(hook);\n    }\n\n    private void printTestStepFinished(TestStepFinished event) {\n        String timestamp = formatter.extractTimeStamp(event);\n        long duration = event.getResult().getDuration().toMillis();\n        String name = extractName(event.getTestStep());\n        Throwable error = event.getResult().getError();\n        switch (event.getResult().getStatus()) {\n            case SKIPPED:\n                formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_IGNORED, timestamp, duration,\n                    error == null ? \"Step skipped\" : error.getMessage(), name);\n                break;\n            case PENDING:\n                formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_FAILED, timestamp, duration, \"Step pending\",\n                    error == null ? \"\" : error.getMessage(), name);\n                break;\n            case UNDEFINED:\n                formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_FAILED, timestamp, duration, \"Step undefined\",\n                    getSnippets(currentTestCase), name);\n                break;\n            case AMBIGUOUS:\n            case FAILED:\n                String details = printStackTrace(error);\n                String message = error.getMessage();\n                if (message == null) {\n                    formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_FAILED, timestamp, duration, \"Step failed\",\n                        details, name);\n                    break;\n                }\n                ComparisonFailure comparison = ComparisonFailure.parse(message.trim());\n                if (comparison == null) {\n                    formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_FAILED, timestamp, duration, \"Step failed\",\n                        details, name);\n                    break;\n                }\n                formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_COMPARISON_FAILED, timestamp, duration,\n                    \"Step failed\", details, comparison.getExpected(), comparison.getActual(), name);\n                break;\n            default:\n                break;\n        }\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_FINISHED, timestamp, duration, name);\n    }\n\n    private String getHookName(HookTestStep hook) {\n        switch (hook.getHookType()) {\n            case BEFORE:\n                return \"Before\";\n            case AFTER:\n                return \"After\";\n            case BEFORE_STEP:\n                return \"BeforeStep\";\n            case AFTER_STEP:\n                return \"AfterStep\";\n            default:\n                return hook.getHookType().name().toLowerCase(Locale.US);\n        }\n    }\n\n    private String extractName(TestStep step) {\n        if (step instanceof PickleStepTestStep)\n            return ((PickleStepTestStep) step).getStep().getText();\n        if (step instanceof HookTestStep) {\n            HookTestStep hook = (HookTestStep) step;\n            return formatHookStepLocation(hook,\n                (declaringClass, method) -> String.format(\"%s(%s)\", getHookName(hook), method), this::getHookName);\n        }\n        return \"Unknown step\";\n    }\n\n    private String getSnippets(TestCase testCase) {\n        URI uri = testCase.getUri();\n        Location location = testCase.getLocation();\n        List<Suggestion> matching = suggestions.stream()\n                .filter(s -> s.getUri().equals(uri) && s.getTestCaseLocation().equals(location))\n                .map(SnippetsSuggestedEvent::getSuggestion).collect(Collectors.toList());\n        if (matching.isEmpty())\n            return \"\";\n        StringBuilder result = new StringBuilder(\"You can implement this step\");\n        if (matching.size() > 1)\n            result.append(\" and \").append(matching.size() - 1).append(\" other step(s)\");\n        result.append(\" using the snippet(s) below:\\n\\n\");\n        result.append(matching.stream().map(Suggestion::getSnippets).flatMap(Collection::stream).distinct()\n                .collect(joining(\"\\n\", \"\", \"\\n\")));\n        return result.toString();\n    }\n\n    private void printTestCaseFinished(TestCaseFinished event) {\n        String timestamp = formatter.extractTimeStamp(event);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_PROGRESS_TEST_FINISHED, timestamp);\n        finishNode(timestamp, currentStack.remove(currentStack.size() - 1));\n        currentTestCase = null;\n    }\n\n    private void printTestRunFinished(TestRunFinished event) {\n        String timestamp = formatter.extractTimeStamp(event);\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_PROGRESS_COUNTING_FINISHED, timestamp);\n        List<Node> emptyStack = new ArrayList<>();\n        poppedNodes(emptyStack).forEach(node -> finishNode(timestamp, node));\n        currentStack = emptyStack;\n        Throwable error = event.getResult().getError();\n        if (error != null) {\n            String name = \"Before All/After All\";\n            formatter.print(TeamCityMessageFormatter.TEMPLATE_BEFORE_ALL_AFTER_ALL_STARTED, timestamp, name);\n            formatter.print(TeamCityMessageFormatter.TEMPLATE_BEFORE_ALL_AFTER_ALL_FAILED, timestamp,\n                \"Before All/After All failed\", printStackTrace(error), name);\n            formatter.print(TeamCityMessageFormatter.TEMPLATE_BEFORE_ALL_AFTER_ALL_FINISHED, timestamp, name);\n        }\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_TEST_RUN_FINISHED, timestamp);\n    }\n\n    private void handleSnippetSuggested(SnippetsSuggestedEvent event) {\n        suggestions.add(event);\n    }\n\n    private void handleEmbedEvent(EmbedEvent event) {\n        String name = event.getName() == null ? \"\" : event.getName() + \" \";\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_ATTACH_WRITE_EVENT,\n            \"Embed event: \" + name + \"[\" + event.getMediaType() + \" \" + event.getData().length + \" bytes]\\n\");\n    }\n\n    private void handleWriteEvent(WriteEvent event) {\n        formatter.print(TeamCityMessageFormatter.TEMPLATE_ATTACH_WRITE_EVENT,\n            \"Write event:\\n\" + event.getText() + \"\\n\");\n    }\n}\n"
    },
    {
      "path": "cucumber-core/src/main/java/io/cucumber/core/plugin/TeamCityStepFormatter.java",
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
