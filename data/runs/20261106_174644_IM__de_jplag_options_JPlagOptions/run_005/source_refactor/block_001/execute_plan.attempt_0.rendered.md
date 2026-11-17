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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/jplag/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "de.jplag.options.JPlagOptions"
  },
  "block": {
    "id": 1,
    "goal": "Extract the cohesive submission-related forwarding API from JPlagOptions so that submission configuration access is modularized separately.",
    "files": [
      "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "core/src/main/java/de/jplag/options/JPlagSubmissionOptionAccess.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "de.jplag.options.JPlagOptions",
          "de.jplag.options.JPlagSubmissionOptionAccess"
        ],
        "outputs": [
          "de.jplag.options.JPlagSubmissionOptionAccess"
        ],
        "details": "Extract the submission-related methods getBaseCodeSubmissionName(), getExcludedFiles(), getExclusionFileName(), getSubmissionDirectories(), getOldSubmissionDirectories(), getSubdirectoryName(), hasBaseCode(), setBaseCodeSubmissionName(String), setExcludedFiles(Set<String>), setExclusionFileName(String), setSubmissionDirectories(List<String>), setOldSubmissionDirectories(List<String>), and setSubdirectoryName(String), together with their required submissionOptions dependency.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "de.jplag.options.JPlagOptions.getBaseCodeSubmissionName()",
          "de.jplag.options.JPlagOptions.getExcludedFiles()",
          "de.jplag.options.JPlagOptions.getExclusionFileName()",
          "de.jplag.options.JPlagOptions.getSubmissionDirectories()",
          "de.jplag.options.JPlagOptions.getOldSubmissionDirectories()",
          "de.jplag.options.JPlagOptions.getSubdirectoryName()",
          "de.jplag.options.JPlagOptions.hasBaseCode()",
          "de.jplag.options.JPlagOptions.setBaseCodeSubmissionName(String)",
          "de.jplag.options.JPlagOptions.setExcludedFiles(Set<String>)",
          "de.jplag.options.JPlagOptions.setExclusionFileName(String)",
          "de.jplag.options.JPlagOptions.setSubmissionDirectories(List<String>)",
          "de.jplag.options.JPlagOptions.setOldSubmissionDirectories(List<String>)",
          "de.jplag.options.JPlagOptions.setSubdirectoryName(String)"
        ],
        "outputs": [
          "de.jplag.options.JPlagSubmissionOptionAccess"
        ],
        "details": "Update callers to use the extracted submission option access class or the existing JPlagSubmissionOptions instance instead of the removed forwarding methods on JPlagOptions.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "core/src/main/java/de/jplag/options/JPlagOptions.java",
    "core/src/main/java/de/jplag/options/JPlagSubmissionOptionAccess.java"
  ],
  "executor_existing_files": [
    "core/src/main/java/de/jplag/options/JPlagOptions.java"
  ],
  "executor_new_files": [
    "core/src/main/java/de/jplag/options/JPlagSubmissionOptionAccess.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "exists": "true",
      "content": "package de.jplag.options;\n\nimport java.nio.charset.Charset;\nimport java.nio.charset.StandardCharsets;\nimport java.util.List;\nimport java.util.Optional;\nimport java.util.Set;\n\nimport de.jplag.Language;\nimport de.jplag.clustering.ClusteringOptions;\nimport de.jplag.strategy.ComparisonMode;\n\npublic class JPlagOptions {\n\n    public static final ComparisonMode DEFAULT_COMPARISON_MODE = JPlagComparisonOptions.DEFAULT_COMPARISON_MODE;\n    public static final float DEFAULT_SIMILARITY_THRESHOLD = JPlagComparisonOptions.DEFAULT_SIMILARITY_THRESHOLD;\n    public static final int DEFAULT_SHOWN_COMPARISONS = JPlagComparisonOptions.DEFAULT_SHOWN_COMPARISONS;\n    public static final Charset CHARSET = StandardCharsets.UTF_8;\n\n    private final JPlagComparisonOptions comparisonOptions = new JPlagComparisonOptions();\n    private final JPlagSubmissionOptions submissionOptions;\n    private final JPlagLanguageOptions languageOptions;\n    private final JPlagClusteringOptions clusteringOptions = new JPlagClusteringOptions();\n\n    /**\n     * Constructor with required attributes.\n     * @param languageIdentifier the identifier of the language to use. If set to {@code null} you have to use\n     * {@link #setLanguage(Language)} to set the language programmatically.\n     */\n    public JPlagOptions(List<String> submissionDirectories, List<String> oldSubmissionDirectories, String languageIdentifier) {\n        this.submissionOptions = new JPlagSubmissionOptions(submissionDirectories, oldSubmissionDirectories);\n        this.languageOptions = new JPlagLanguageOptions(languageIdentifier, comparisonOptions);\n    }\n\n    public JPlagComparisonOptions getComparisonOptions() {\n        return comparisonOptions;\n    }\n\n    public JPlagSubmissionOptions getSubmissionOptions() {\n        return submissionOptions;\n    }\n\n    public JPlagLanguageOptions getLanguageOptions() {\n        return languageOptions;\n    }\n\n    public Optional<String> getBaseCodeSubmissionName() {\n        return submissionOptions.getBaseCodeSubmissionName();\n    }\n\n    public ComparisonMode getComparisonMode() {\n        return comparisonOptions.getComparisonMode();\n    }\n\n    public Set<String> getExcludedFiles() {\n        return submissionOptions.getExcludedFiles();\n    }\n\n    public String getExclusionFileName() {\n        return submissionOptions.getExclusionFileName();\n    }\n\n    public String[] getFileSuffixes() {\n        return languageOptions.getFileSuffixes();\n    }\n\n    public String getLanguageIdentifier() {\n        return languageOptions.getLanguageIdentifier();\n    }\n\n    public Language getLanguage() {\n        return languageOptions.getLanguage();\n    }\n\n    public int getMaximumNumberOfComparisons() {\n        return comparisonOptions.getMaximumNumberOfComparisons();\n    }\n\n    public Integer getMinimumTokenMatch() {\n        return comparisonOptions.getMinimumTokenMatch();\n    }\n\n    public List<String> getSubmissionDirectories() {\n        return submissionOptions.getSubmissionDirectories();\n    }\n\n    public List<String> getOldSubmissionDirectories() {\n        return submissionOptions.getOldSubmissionDirectories();\n    }\n\n    public SimilarityMetric getSimilarityMetric() {\n        return comparisonOptions.getSimilarityMetric();\n    }\n\n    public float getSimilarityThreshold() {\n        return comparisonOptions.getSimilarityThreshold();\n    }\n\n    public String getSubdirectoryName() {\n        return submissionOptions.getSubdirectoryName();\n    }\n\n    public Verbosity getVerbosity() {\n        return languageOptions.getVerbosity();\n    }\n\n    public boolean hasBaseCode() {\n        return submissionOptions.hasBaseCode();\n    }\n\n    public boolean isDebugParser() {\n        return comparisonOptions.isDebugParser();\n    }\n\n    public ClusteringOptions getClusteringOptions() {\n        return clusteringOptions.getClusteringOptions();\n    }\n\n    public void setBaseCodeSubmissionName(String baseCodeSubmissionName) {\n        submissionOptions.setBaseCodeSubmissionName(baseCodeSubmissionName);\n    }\n\n    public void setComparisonMode(ComparisonMode comparisonMode) {\n        comparisonOptions.setComparisonMode(comparisonMode);\n    }\n\n    public void setDebugParser(boolean debugParser) {\n        comparisonOptions.setDebugParser(debugParser);\n    }\n\n    public void setExcludedFiles(Set<String> excludedFiles) {\n        submissionOptions.setExcludedFiles(excludedFiles);\n    }\n\n    public void setExclusionFileName(String exclusionFileName) {\n        submissionOptions.setExclusionFileName(exclusionFileName);\n    }\n\n    public void setFileSuffixes(String[] fileSuffixes) {\n        languageOptions.setFileSuffixes(fileSuffixes);\n    }\n\n    public void setLanguage(Language language) {\n        languageOptions.setLanguage(language);\n    }\n\n    public void setLanguageDefaults(Language language) {\n        languageOptions.setLanguageDefaults(language);\n    }\n\n    public void setMaximumNumberOfComparisons(int maximumNumberOfComparisons) {\n        comparisonOptions.setMaximumNumberOfComparisons(maximumNumberOfComparisons);\n    }\n\n    public void setMinimumTokenMatch(Integer minimumTokenMatch) {\n        comparisonOptions.setMinimumTokenMatch(minimumTokenMatch);\n    }\n\n    public void setSubmissionDirectories(List<String> submissionDirectories) {\n        submissionOptions.setSubmissionDirectories(submissionDirectories);\n    }\n\n    public void setOldSubmissionDirectories(List<String> oldSubmissionDirectories) {\n        submissionOptions.setOldSubmissionDirectories(oldSubmissionDirectories);\n    }\n\n    public void setSimilarityMetric(SimilarityMetric similarityMetric) {\n        comparisonOptions.setSimilarityMetric(similarityMetric);\n    }\n\n    public void setSimilarityThreshold(float similarityThreshold) {\n        comparisonOptions.setSimilarityThreshold(similarityThreshold);\n    }\n\n    public void setSubdirectoryName(String subdirectoryName) {\n        submissionOptions.setSubdirectoryName(subdirectoryName);\n    }\n\n    public void setVerbosity(Verbosity verbosity) {\n        languageOptions.setVerbosity(verbosity);\n    }\n\n    public void setClusteringOptions(ClusteringOptions clusteringOptions) {\n        this.clusteringOptions.setClusteringOptions(clusteringOptions);\n    }\n}\n"
    },
    {
      "path": "core/src/main/java/de/jplag/options/JPlagSubmissionOptionAccess.java",
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
