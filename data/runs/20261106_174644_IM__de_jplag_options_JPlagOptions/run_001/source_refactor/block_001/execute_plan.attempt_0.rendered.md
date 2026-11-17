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
    "goal": "Extract the cohesive comparison configuration API and its validation logic from JPlagOptions to reduce the number of public methods and isolate comparison-related state.",
    "files": [
      "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "core/src/main/java/de/jplag/options/JPlagComparisonOptions.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "de.jplag.options.JPlagOptions"
        ],
        "outputs": [
          "de.jplag.options.JPlagComparisonOptions"
        ],
        "details": "Extract DEFAULT_COMPARISON_MODE, DEFAULT_SIMILARITY_THRESHOLD, DEFAULT_SHOWN_COMPARISONS, comparisonMode, similarityThreshold, maximumNumberOfComparisons, similarityMetric, minimumTokenMatch, logger, getComparisonMode(), getMaximumNumberOfComparisons(), getMinimumTokenMatch(), getSimilarityMetric(), getSimilarityThreshold(), isDebugParser(), setComparisonMode(ComparisonMode), setMaximumNumberOfComparisons(int), setMinimumTokenMatch(Integer), setSimilarityMetric(SimilarityMetric), setSimilarityThreshold(float), hasMinimumTokenMatch(), and the associated validation and warning behavior into JPlagComparisonOptions in the same package. Preserve the existing defaults and setter behavior.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "de.jplag.options.JPlagOptions.getComparisonMode()",
          "de.jplag.options.JPlagOptions.getMaximumNumberOfComparisons()",
          "de.jplag.options.JPlagOptions.getMinimumTokenMatch()",
          "de.jplag.options.JPlagOptions.getSimilarityMetric()",
          "de.jplag.options.JPlagOptions.getSimilarityThreshold()",
          "de.jplag.options.JPlagOptions.setComparisonMode(ComparisonMode)",
          "de.jplag.options.JPlagOptions.setMaximumNumberOfComparisons(int)",
          "de.jplag.options.JPlagOptions.setMinimumTokenMatch(Integer)",
          "de.jplag.options.JPlagOptions.setSimilarityMetric(SimilarityMetric)",
          "de.jplag.options.JPlagOptions.setSimilarityThreshold(float)"
        ],
        "outputs": [
          "de.jplag.options.JPlagComparisonOptions.getComparisonMode()",
          "de.jplag.options.JPlagComparisonOptions.getMaximumNumberOfComparisons()",
          "de.jplag.options.JPlagComparisonOptions.getMinimumTokenMatch()",
          "de.jplag.options.JPlagComparisonOptions.getSimilarityMetric()",
          "de.jplag.options.JPlagComparisonOptions.getSimilarityThreshold()",
          "de.jplag.options.JPlagComparisonOptions.setComparisonMode(ComparisonMode)",
          "de.jplag.options.JPlagComparisonOptions.setMaximumNumberOfComparisons(int)",
          "de.jplag.options.JPlagComparisonOptions.setMinimumTokenMatch(Integer)",
          "de.jplag.options.JPlagComparisonOptions.setSimilarityMetric(SimilarityMetric)",
          "de.jplag.options.JPlagComparisonOptions.setSimilarityThreshold(float)"
        ],
        "details": "Update callers to access the extracted comparison configuration through JPlagComparisonOptions. Preserve JPlagOptions compatibility through the extraction mechanism where required, and update direct field or method references to the new class.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "core/src/main/java/de/jplag/options/JPlagComparisonOptions.java",
    "core/src/main/java/de/jplag/options/JPlagOptions.java"
  ],
  "executor_existing_files": [
    "core/src/main/java/de/jplag/options/JPlagOptions.java"
  ],
  "executor_new_files": [
    "core/src/main/java/de/jplag/options/JPlagComparisonOptions.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "core/src/main/java/de/jplag/options/JPlagComparisonOptions.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "core/src/main/java/de/jplag/options/JPlagOptions.java",
      "exists": "true",
      "content": "package de.jplag.options;\n\nimport static de.jplag.strategy.ComparisonMode.NORMAL;\n\nimport java.io.File;\nimport java.nio.charset.Charset;\nimport java.nio.charset.StandardCharsets;\nimport java.util.Collections;\nimport java.util.List;\nimport java.util.Optional;\nimport java.util.Set;\n\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\nimport de.jplag.Language;\nimport de.jplag.clustering.ClusteringOptions;\nimport de.jplag.strategy.ComparisonMode;\n\npublic class JPlagOptions {\n\n    private static final Logger logger = LoggerFactory.getLogger(\"JPlag\");\n    public static final ComparisonMode DEFAULT_COMPARISON_MODE = NORMAL;\n    public static final float DEFAULT_SIMILARITY_THRESHOLD = 0;\n    public static final int DEFAULT_SHOWN_COMPARISONS = 30;\n\n    public static final Charset CHARSET = StandardCharsets.UTF_8;\n\n    /**\n     * The identifier of the language used to parse the submissions.\n     */\n    private final String languageIdentifier;\n\n    /**\n     * Language used to parse the submissions.\n     */\n    private Language language;\n\n    /**\n     * Determines which strategy to use for the comparison of submissions.\n     */\n    private ComparisonMode comparisonMode = DEFAULT_COMPARISON_MODE;\n\n    /**\n     * If true, submissions that cannot be parsed will be stored in a separate directory.\n     */\n    private boolean debugParser = false;\n\n    /**\n     * Array of file suffixes that should be included.\n     */\n    private String[] fileSuffixes;\n\n    /**\n     * Percentage value (must be between 0 and 100). Comparisons (of submissions pairs) with a similarity below this\n     * threshold will be ignored. The default value of 0 allows all matches to be stored. This affects which comparisons are\n     * stored and thus make it into the result object.\n     * @see JPlagOptions#similarityMetric\n     */\n    private float similarityThreshold = DEFAULT_SIMILARITY_THRESHOLD;\n\n    /**\n     * The maximum number of comparisons that will be shown in the generated report. If set to -1 all comparisons will be\n     * shown.\n     */\n    private int maximumNumberOfComparisons = DEFAULT_SHOWN_COMPARISONS;\n\n    /**\n     * The similarity metric determines how the minimum similarity threshold required for a comparison (of two submissions)\n     * is calculated. This affects which comparisons are stored and thus make it into the result object.\n     * @see JPlagOptions#similarityThreshold\n     */\n    private SimilarityMetric similarityMetric = SimilarityMetric.AVG;\n\n    /**\n     * Tunes the comparison sensitivity by adjusting the minimum token required to be counted as matching section. A smaller\n     * <n> increases the sensitivity but might lead to more false-positives.\n     */\n    private Integer minimumTokenMatch;\n\n    /**\n     * Name of the file that contains the names of files to exclude from comparison.\n     */\n    private String exclusionFileName;\n\n    /**\n     * Names of the excluded files.\n     */\n    private Set<String> excludedFiles = Collections.emptySet();\n\n    /**\n     * Directories with new submissions. These must be checked for plagiarism.\n     */\n    private List<String> submissionDirectories;\n\n    /**\n     * Directories with old submissions to check against.\n     */\n    private List<String> oldSubmissionDirectories;\n\n    /**\n     * Path name of the directory containing the base code.\n     * <p>\n     * For backwards compatibility it may also be a directory name inside the root directory. Condition for the latter is\n     * <ul>\n     * <li>Specified path does not exist.</li>\n     * <li>Name has not have a separator character after trimming them from both ends (leaving at least a one-character\n     * name).</li>\n     * <li>A submission with the specified name exists in the root directory.</li>\n     * </ul>\n     * It's an error if a string has been provided but it is neither an existing path nor does it fulfill all the conditions\n     * of the compatibility fallback listed above.\n     * </p>\n     */\n    private String baseCodeSubmissionName = null;\n\n    /**\n     * Example: If the subdirectoryName is 'src', only the code inside submissionDir/src of each submission will be used for\n     * comparison.\n     */\n    private String subdirectoryName;\n\n    /**\n     * Level of output verbosity.\n     */\n    private Verbosity verbosity;\n\n    /**\n     * Clustering options\n     */\n    private ClusteringOptions clusteringOptions = new ClusteringOptions.Builder().build();\n\n    /**\n     * Constructor with required attributes.\n     * @param languageIdentifier the identifier of the language to use. If set to {@code null} you have to use\n     * {@link #setLanguage(Language)} to set the language programmatically.\n     */\n    public JPlagOptions(List<String> submissionDirectories, List<String> oldSubmissionDirectories, String languageIdentifier) {\n        this.submissionDirectories = submissionDirectories;\n        this.oldSubmissionDirectories = oldSubmissionDirectories;\n        this.languageIdentifier = languageIdentifier;\n    }\n\n    public Optional<String> getBaseCodeSubmissionName() {\n        return Optional.ofNullable(baseCodeSubmissionName);\n    }\n\n    public ComparisonMode getComparisonMode() {\n        return comparisonMode;\n    }\n\n    public Set<String> getExcludedFiles() {\n        return excludedFiles;\n    }\n\n    public String getExclusionFileName() {\n        return exclusionFileName;\n    }\n\n    public String[] getFileSuffixes() {\n        return fileSuffixes;\n    }\n\n    public String getLanguageIdentifier() {\n        return languageIdentifier;\n    }\n\n    public Language getLanguage() {\n        return language;\n    }\n\n    public int getMaximumNumberOfComparisons() {\n        return this.maximumNumberOfComparisons;\n    }\n\n    public Integer getMinimumTokenMatch() {\n        return minimumTokenMatch;\n    }\n\n    public List<String> getSubmissionDirectories() {\n        return submissionDirectories;\n    }\n\n    public List<String> getOldSubmissionDirectories() {\n        return oldSubmissionDirectories;\n    }\n\n    public SimilarityMetric getSimilarityMetric() {\n        return similarityMetric;\n    }\n\n    public float getSimilarityThreshold() {\n        return similarityThreshold;\n    }\n\n    public String getSubdirectoryName() {\n        return subdirectoryName;\n    }\n\n    public Verbosity getVerbosity() {\n        return verbosity;\n    }\n\n    public boolean hasBaseCode() {\n        return this.baseCodeSubmissionName != null;\n    }\n\n    public boolean isDebugParser() {\n        return debugParser;\n    }\n\n    public ClusteringOptions getClusteringOptions() {\n        return this.clusteringOptions;\n    }\n\n    public void setBaseCodeSubmissionName(String baseCodeSubmissionName) {\n        if (baseCodeSubmissionName == null || baseCodeSubmissionName.isEmpty()) {\n            this.baseCodeSubmissionName = null;\n        } else {\n            this.baseCodeSubmissionName = baseCodeSubmissionName;\n        }\n    }\n\n    public void setComparisonMode(ComparisonMode comparisonMode) {\n        this.comparisonMode = comparisonMode;\n    }\n\n    public void setDebugParser(boolean debugParser) {\n        this.debugParser = debugParser;\n    }\n\n    public void setExcludedFiles(Set<String> excludedFiles) {\n        this.excludedFiles = excludedFiles;\n    }\n\n    public void setExclusionFileName(String exclusionFileName) {\n        this.exclusionFileName = exclusionFileName;\n    }\n\n    public void setFileSuffixes(String[] fileSuffixes) {\n        this.fileSuffixes = fileSuffixes;\n    }\n\n    public void setLanguage(Language language) {\n        this.language = language;\n    }\n\n    /**\n     * After the selected language has been initialized, this method is called by JPlag to set default values for options\n     * not set by the user.\n     * @param language - initialized language instance\n     */\n    public void setLanguageDefaults(Language language) {\n        if (!hasMinimumTokenMatch()) {\n            setMinimumTokenMatch(language.minimumTokenMatch());\n        }\n\n        if (!hasFileSuffixes()) {\n            fileSuffixes = language.suffixes();\n        }\n    }\n\n    public void setMaximumNumberOfComparisons(int maximumNumberOfComparisons) {\n        this.maximumNumberOfComparisons = Math.max(maximumNumberOfComparisons, -1);\n    }\n\n    public void setMinimumTokenMatch(Integer minimumTokenMatch) {\n        if (minimumTokenMatch != null && minimumTokenMatch < 1) {\n            this.minimumTokenMatch = 1;\n        } else {\n            this.minimumTokenMatch = minimumTokenMatch;\n        }\n    }\n\n    public void setSubmissionDirectories(List<String> submissionDirectories) {\n        this.submissionDirectories = submissionDirectories;\n    }\n\n    public void setOldSubmissionDirectories(List<String> oldSubmissionDirectories) {\n        this.oldSubmissionDirectories = oldSubmissionDirectories;\n    }\n\n    public void setSimilarityMetric(SimilarityMetric similarityMetric) {\n        this.similarityMetric = similarityMetric;\n    }\n\n    public void setSimilarityThreshold(float similarityThreshold) {\n        if (similarityThreshold > 100) {\n            logger.warn(\"Maximum threshold of 100 used instead of {}\", similarityThreshold);\n            this.similarityThreshold = 100;\n        } else if (similarityThreshold < 0) {\n            logger.warn(\"Minimum threshold of 0 used instead of {}\", similarityThreshold);\n            this.similarityThreshold = 0;\n        } else {\n            this.similarityThreshold = similarityThreshold;\n        }\n    }\n\n    public void setSubdirectoryName(String subdirectoryName) {\n        // Trim problematic file separators.\n        this.subdirectoryName = (subdirectoryName == null) ? null : subdirectoryName.replace(File.separator, \"\");\n    }\n\n    public void setVerbosity(Verbosity verbosity) {\n        this.verbosity = verbosity;\n    }\n\n    public void setClusteringOptions(ClusteringOptions clusteringOptions) {\n        this.clusteringOptions = clusteringOptions;\n    }\n\n    private boolean hasFileSuffixes() {\n        return fileSuffixes != null && fileSuffixes.length > 0;\n    }\n\n    private boolean hasMinimumTokenMatch() {\n        return minimumTokenMatch != null;\n    }\n\n}\n"
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
