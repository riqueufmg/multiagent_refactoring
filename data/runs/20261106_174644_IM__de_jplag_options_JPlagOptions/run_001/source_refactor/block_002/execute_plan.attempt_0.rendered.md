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
    "id": 2,
    "goal": "Extract the cohesive submission and exclusion configuration API from JPlagOptions to further reduce its public API size and separate input-path concerns from comparison concerns.",
    "files": [
      "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "core/src/main/java/de/jplag/options/JPlagSubmissionOptions.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "de.jplag.options.JPlagOptions"
        ],
        "outputs": [
          "de.jplag.options.JPlagSubmissionOptions"
        ],
        "details": "Extract submissionDirectories, oldSubmissionDirectories, baseCodeSubmissionName, exclusionFileName, excludedFiles, subdirectoryName, getBaseCodeSubmissionName(), getExcludedFiles(), getExclusionFileName(), getSubmissionDirectories(), getOldSubmissionDirectories(), getSubdirectoryName(), hasBaseCode(), setBaseCodeSubmissionName(String), setExcludedFiles(Set<String>), setExclusionFileName(String), setSubmissionDirectories(List<String>), setOldSubmissionDirectories(List<String>), and setSubdirectoryName(String) into JPlagSubmissionOptions in the same package. Preserve the existing null, empty-string, and file-separator handling behavior.",
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
          "de.jplag.options.JPlagSubmissionOptions.getBaseCodeSubmissionName()",
          "de.jplag.options.JPlagSubmissionOptions.getExcludedFiles()",
          "de.jplag.options.JPlagSubmissionOptions.getExclusionFileName()",
          "de.jplag.options.JPlagSubmissionOptions.getSubmissionDirectories()",
          "de.jplag.options.JPlagSubmissionOptions.getOldSubmissionDirectories()",
          "de.jplag.options.JPlagSubmissionOptions.getSubdirectoryName()",
          "de.jplag.options.JPlagSubmissionOptions.hasBaseCode()",
          "de.jplag.options.JPlagSubmissionOptions.setBaseCodeSubmissionName(String)",
          "de.jplag.options.JPlagSubmissionOptions.setExcludedFiles(Set<String>)",
          "de.jplag.options.JPlagSubmissionOptions.setExclusionFileName(String)",
          "de.jplag.options.JPlagSubmissionOptions.setSubmissionDirectories(List<String>)",
          "de.jplag.options.JPlagSubmissionOptions.setOldSubmissionDirectories(List<String>)",
          "de.jplag.options.JPlagSubmissionOptions.setSubdirectoryName(String)"
        ],
        "details": "Update callers to use JPlagSubmissionOptions for submission directories, old submission directories, base-code selection, excluded files, exclusion file name, and subdirectory selection. Preserve the existing JPlagOptions construction flow and compatibility behavior while delegating or redirecting access to the extracted object.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "core/src/main/java/de/jplag/options/JPlagOptions.java",
    "core/src/main/java/de/jplag/options/JPlagSubmissionOptions.java"
  ],
  "executor_existing_files": [
    "core/src/main/java/de/jplag/options/JPlagOptions.java"
  ],
  "executor_new_files": [
    "core/src/main/java/de/jplag/options/JPlagSubmissionOptions.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "exists": "true",
      "content": "package de.jplag.options;\n\nimport java.io.File;\nimport java.nio.charset.Charset;\nimport java.nio.charset.StandardCharsets;\nimport java.util.Collections;\nimport java.util.List;\nimport java.util.Optional;\nimport java.util.Set;\n\nimport de.jplag.Language;\nimport de.jplag.clustering.ClusteringOptions;\nimport de.jplag.strategy.ComparisonMode;\n\npublic class JPlagOptions {\n\n    public static final ComparisonMode DEFAULT_COMPARISON_MODE = JPlagComparisonOptions.DEFAULT_COMPARISON_MODE;\n    public static final float DEFAULT_SIMILARITY_THRESHOLD = JPlagComparisonOptions.DEFAULT_SIMILARITY_THRESHOLD;\n    public static final int DEFAULT_SHOWN_COMPARISONS = JPlagComparisonOptions.DEFAULT_SHOWN_COMPARISONS;\n    public static final Charset CHARSET = StandardCharsets.UTF_8;\n\n    /**\n     * The identifier of the language used to parse the submissions.\n     */\n    private final String languageIdentifier;\n\n    /**\n     * Language used to parse the submissions.\n     */\n    private Language language;\n\n    private final JPlagComparisonOptions comparisonOptions = new JPlagComparisonOptions();\n\n    /**\n     * Array of file suffixes that should be included.\n     */\n    private String[] fileSuffixes;\n\n    /**\n     * Name of the file that contains the names of files to exclude from comparison.\n     */\n    private String exclusionFileName;\n\n    /**\n     * Names of the excluded files.\n     */\n    private Set<String> excludedFiles = Collections.emptySet();\n\n    /**\n     * Directories with new submissions. These must be checked for plagiarism.\n     */\n    private List<String> submissionDirectories;\n\n    /**\n     * Directories with old submissions to check against.\n     */\n    private List<String> oldSubmissionDirectories;\n\n    /**\n     * Path name of the directory containing the base code.\n     */\n    private String baseCodeSubmissionName = null;\n\n    /**\n     * Example: If the subdirectoryName is 'src', only the code inside submissionDir/src of each submission will be used for\n     * comparison.\n     */\n    private String subdirectoryName;\n\n    /**\n     * Level of output verbosity.\n     */\n    private Verbosity verbosity;\n\n    /**\n     * Clustering options\n     */\n    private ClusteringOptions clusteringOptions = new ClusteringOptions.Builder().build();\n\n    /**\n     * Constructor with required attributes.\n     * @param languageIdentifier the identifier of the language to use. If set to {@code null} you have to use\n     * {@link #setLanguage(Language)} to set the language programmatically.\n     */\n    public JPlagOptions(List<String> submissionDirectories, List<String> oldSubmissionDirectories, String languageIdentifier) {\n        this.submissionDirectories = submissionDirectories;\n        this.oldSubmissionDirectories = oldSubmissionDirectories;\n        this.languageIdentifier = languageIdentifier;\n    }\n\n    public JPlagComparisonOptions getComparisonOptions() {\n        return comparisonOptions;\n    }\n\n    public Optional<String> getBaseCodeSubmissionName() {\n        return Optional.ofNullable(baseCodeSubmissionName);\n    }\n\n    public ComparisonMode getComparisonMode() {\n        return comparisonOptions.getComparisonMode();\n    }\n\n    public Set<String> getExcludedFiles() {\n        return excludedFiles;\n    }\n\n    public String getExclusionFileName() {\n        return exclusionFileName;\n    }\n\n    public String[] getFileSuffixes() {\n        return fileSuffixes;\n    }\n\n    public String getLanguageIdentifier() {\n        return languageIdentifier;\n    }\n\n    public Language getLanguage() {\n        return language;\n    }\n\n    public int getMaximumNumberOfComparisons() {\n        return comparisonOptions.getMaximumNumberOfComparisons();\n    }\n\n    public Integer getMinimumTokenMatch() {\n        return comparisonOptions.getMinimumTokenMatch();\n    }\n\n    public List<String> getSubmissionDirectories() {\n        return submissionDirectories;\n    }\n\n    public List<String> getOldSubmissionDirectories() {\n        return oldSubmissionDirectories;\n    }\n\n    public SimilarityMetric getSimilarityMetric() {\n        return comparisonOptions.getSimilarityMetric();\n    }\n\n    public float getSimilarityThreshold() {\n        return comparisonOptions.getSimilarityThreshold();\n    }\n\n    public String getSubdirectoryName() {\n        return subdirectoryName;\n    }\n\n    public Verbosity getVerbosity() {\n        return verbosity;\n    }\n\n    public boolean hasBaseCode() {\n        return this.baseCodeSubmissionName != null;\n    }\n\n    public boolean isDebugParser() {\n        return comparisonOptions.isDebugParser();\n    }\n\n    public ClusteringOptions getClusteringOptions() {\n        return this.clusteringOptions;\n    }\n\n    public void setBaseCodeSubmissionName(String baseCodeSubmissionName) {\n        if (baseCodeSubmissionName == null || baseCodeSubmissionName.isEmpty()) {\n            this.baseCodeSubmissionName = null;\n        } else {\n            this.baseCodeSubmissionName = baseCodeSubmissionName;\n        }\n    }\n\n    public void setComparisonMode(ComparisonMode comparisonMode) {\n        comparisonOptions.setComparisonMode(comparisonMode);\n    }\n\n    public void setDebugParser(boolean debugParser) {\n        comparisonOptions.setDebugParser(debugParser);\n    }\n\n    public void setExcludedFiles(Set<String> excludedFiles) {\n        this.excludedFiles = excludedFiles;\n    }\n\n    public void setExclusionFileName(String exclusionFileName) {\n        this.exclusionFileName = exclusionFileName;\n    }\n\n    public void setFileSuffixes(String[] fileSuffixes) {\n        this.fileSuffixes = fileSuffixes;\n    }\n\n    public void setLanguage(Language language) {\n        this.language = language;\n    }\n\n    /**\n     * After the selected language has been initialized, this method is called by JPlag to set default values for options\n     * not set by the user.\n     * @param language - initialized language instance\n     */\n    public void setLanguageDefaults(Language language) {\n        if (!comparisonOptions.hasMinimumTokenMatch()) {\n            setMinimumTokenMatch(language.minimumTokenMatch());\n        }\n\n        if (!hasFileSuffixes()) {\n            fileSuffixes = language.suffixes();\n        }\n    }\n\n    public void setMaximumNumberOfComparisons(int maximumNumberOfComparisons) {\n        comparisonOptions.setMaximumNumberOfComparisons(maximumNumberOfComparisons);\n    }\n\n    public void setMinimumTokenMatch(Integer minimumTokenMatch) {\n        comparisonOptions.setMinimumTokenMatch(minimumTokenMatch);\n    }\n\n    public void setSubmissionDirectories(List<String> submissionDirectories) {\n        this.submissionDirectories = submissionDirectories;\n    }\n\n    public void setOldSubmissionDirectories(List<String> oldSubmissionDirectories) {\n        this.oldSubmissionDirectories = oldSubmissionDirectories;\n    }\n\n    public void setSimilarityMetric(SimilarityMetric similarityMetric) {\n        comparisonOptions.setSimilarityMetric(similarityMetric);\n    }\n\n    public void setSimilarityThreshold(float similarityThreshold) {\n        comparisonOptions.setSimilarityThreshold(similarityThreshold);\n    }\n\n    public void setSubdirectoryName(String subdirectoryName) {\n        // Trim problematic file separators.\n        this.subdirectoryName = (subdirectoryName == null) ? null : subdirectoryName.replace(File.separator, \"\");\n    }\n\n    public void setVerbosity(Verbosity verbosity) {\n        this.verbosity = verbosity;\n    }\n\n    public void setClusteringOptions(ClusteringOptions clusteringOptions) {\n        this.clusteringOptions = clusteringOptions;\n    }\n\n    private boolean hasFileSuffixes() {\n        return fileSuffixes != null && fileSuffixes.length > 0;\n    }\n}\n"
    },
    {
      "path": "core/src/main/java/de/jplag/options/JPlagSubmissionOptions.java",
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
