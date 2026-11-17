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
- ADD_OR_UPDATE_IMPORTS(file): Adds, removes, or updates imports required by the refactoring.
- CREATE_PACKAGE(pkgA.subpkg): Creates a new package under the current source root.
- EXTRACT_CLASS(pkgA.C1, pkgA.C2): Extracts part of class C1 into a new class C2.
- EXTRACT_INTERFACE(pkgA.C1, pkgA.I1): Extracts an interface I1 from class C1.
- MOVE_CLASS(pkgA.C1, pkgB.C1): Moves class C1 from package A to package B.
- MOVE_FIELD(pkgA.C1.field, pkgA.C2.field): Moves a field from class C1 to class C2.
- MOVE_METHOD(pkgA.C1.m(), pkgA.C2.m()): Moves a method from class C1 to class C2.
- REPLACE_DEPENDENCY(pkgA.C1, pkgA.C2): Replaces a direct dependency in C1 with a different dependency C2.
- UPDATE_CALL_SITES(pkgA.C1.m(), pkgA.C2.m()): Updates callers to use the new method or class location.

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "de.jplag.options.JPlagOptions",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261106_174644_IM__de_jplag_options_JPlagOptions/run_002/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "core/src/main/java/de/jplag/options/JPlagOptions.java",
  "target_source_root": "core/src/main/java",
  "target_code": "package de.jplag.options;\n\nimport java.nio.charset.Charset;\nimport java.nio.charset.StandardCharsets;\nimport java.util.List;\nimport java.util.Optional;\nimport java.util.Set;\n\nimport de.jplag.Language;\nimport de.jplag.clustering.ClusteringOptions;\nimport de.jplag.strategy.ComparisonMode;\n\npublic class JPlagOptions {\n\n    public static final ComparisonMode DEFAULT_COMPARISON_MODE = JPlagComparisonOptions.DEFAULT_COMPARISON_MODE;\n    public static final float DEFAULT_SIMILARITY_THRESHOLD = JPlagComparisonOptions.DEFAULT_SIMILARITY_THRESHOLD;\n    public static final int DEFAULT_SHOWN_COMPARISONS = JPlagComparisonOptions.DEFAULT_SHOWN_COMPARISONS;\n    public static final Charset CHARSET = StandardCharsets.UTF_8;\n\n    /**\n     * The identifier of the language used to parse the submissions.\n     */\n    private final String languageIdentifier;\n\n    /**\n     * Language used to parse the submissions.\n     */\n    private Language language;\n\n    private final JPlagComparisonOptions comparisonOptions = new JPlagComparisonOptions();\n    private final JPlagSubmissionOptions submissionOptions;\n\n    /**\n     * Array of file suffixes that should be included.\n     */\n    private String[] fileSuffixes;\n\n    /**\n     * Level of output verbosity.\n     */\n    private Verbosity verbosity;\n\n    /**\n     * Clustering options\n     */\n    private ClusteringOptions clusteringOptions = new ClusteringOptions.Builder().build();\n\n    /**\n     * Constructor with required attributes.\n     * @param languageIdentifier the identifier of the language to use. If set to {@code null} you have to use\n     * {@link #setLanguage(Language)} to set the language programmatically.\n     */\n    public JPlagOptions(List<String> submissionDirectories, List<String> oldSubmissionDirectories, String languageIdentifier) {\n        this.submissionOptions = new JPlagSubmissionOptions(submissionDirectories, oldSubmissionDirectories);\n        this.languageIdentifier = languageIdentifier;\n    }\n\n    public JPlagComparisonOptions getComparisonOptions() {\n        return comparisonOptions;\n    }\n\n    public JPlagSubmissionOptions getSubmissionOptions() {\n        return submissionOptions;\n    }\n\n    public Optional<String> getBaseCodeSubmissionName() {\n        return submissionOptions.getBaseCodeSubmissionName();\n    }\n\n    public ComparisonMode getComparisonMode() {\n        return comparisonOptions.getComparisonMode();\n    }\n\n    public Set<String> getExcludedFiles() {\n        return submissionOptions.getExcludedFiles();\n    }\n\n    public String getExclusionFileName() {\n        return submissionOptions.getExclusionFileName();\n    }\n\n    public String[] getFileSuffixes() {\n        return fileSuffixes;\n    }\n\n    public String getLanguageIdentifier() {\n        return languageIdentifier;\n    }\n\n    public Language getLanguage() {\n        return language;\n    }\n\n    public int getMaximumNumberOfComparisons() {\n        return comparisonOptions.getMaximumNumberOfComparisons();\n    }\n\n    public Integer getMinimumTokenMatch() {\n        return comparisonOptions.getMinimumTokenMatch();\n    }\n\n    public List<String> getSubmissionDirectories() {\n        return submissionOptions.getSubmissionDirectories();\n    }\n\n    public List<String> getOldSubmissionDirectories() {\n        return submissionOptions.getOldSubmissionDirectories();\n    }\n\n    public SimilarityMetric getSimilarityMetric() {\n        return comparisonOptions.getSimilarityMetric();\n    }\n\n    public float getSimilarityThreshold() {\n        return comparisonOptions.getSimilarityThreshold();\n    }\n\n    public String getSubdirectoryName() {\n        return submissionOptions.getSubdirectoryName();\n    }\n\n    public Verbosity getVerbosity() {\n        return verbosity;\n    }\n\n    public boolean hasBaseCode() {\n        return submissionOptions.hasBaseCode();\n    }\n\n    public boolean isDebugParser() {\n        return comparisonOptions.isDebugParser();\n    }\n\n    public ClusteringOptions getClusteringOptions() {\n        return this.clusteringOptions;\n    }\n\n    public void setBaseCodeSubmissionName(String baseCodeSubmissionName) {\n        submissionOptions.setBaseCodeSubmissionName(baseCodeSubmissionName);\n    }\n\n    public void setComparisonMode(ComparisonMode comparisonMode) {\n        comparisonOptions.setComparisonMode(comparisonMode);\n    }\n\n    public void setDebugParser(boolean debugParser) {\n        comparisonOptions.setDebugParser(debugParser);\n    }\n\n    public void setExcludedFiles(Set<String> excludedFiles) {\n        submissionOptions.setExcludedFiles(excludedFiles);\n    }\n\n    public void setExclusionFileName(String exclusionFileName) {\n        submissionOptions.setExclusionFileName(exclusionFileName);\n    }\n\n    public void setFileSuffixes(String[] fileSuffixes) {\n        this.fileSuffixes = fileSuffixes;\n    }\n\n    public void setLanguage(Language language) {\n        this.language = language;\n    }\n\n    /**\n     * After the selected language has been initialized, this method is called by JPlag to set default values for options\n     * not set by the user.\n     * @param language - initialized language instance\n     */\n    public void setLanguageDefaults(Language language) {\n        if (!comparisonOptions.hasMinimumTokenMatch()) {\n            setMinimumTokenMatch(language.minimumTokenMatch());\n        }\n\n        if (!hasFileSuffixes()) {\n            fileSuffixes = language.suffixes();\n        }\n    }\n\n    public void setMaximumNumberOfComparisons(int maximumNumberOfComparisons) {\n        comparisonOptions.setMaximumNumberOfComparisons(maximumNumberOfComparisons);\n    }\n\n    public void setMinimumTokenMatch(Integer minimumTokenMatch) {\n        comparisonOptions.setMinimumTokenMatch(minimumTokenMatch);\n    }\n\n    public void setSubmissionDirectories(List<String> submissionDirectories) {\n        submissionOptions.setSubmissionDirectories(submissionDirectories);\n    }\n\n    public void setOldSubmissionDirectories(List<String> oldSubmissionDirectories) {\n        submissionOptions.setOldSubmissionDirectories(oldSubmissionDirectories);\n    }\n\n    public void setSimilarityMetric(SimilarityMetric similarityMetric) {\n        comparisonOptions.setSimilarityMetric(similarityMetric);\n    }\n\n    public void setSimilarityThreshold(float similarityThreshold) {\n        comparisonOptions.setSimilarityThreshold(similarityThreshold);\n    }\n\n    public void setSubdirectoryName(String subdirectoryName) {\n        submissionOptions.setSubdirectoryName(subdirectoryName);\n    }\n\n    public void setVerbosity(Verbosity verbosity) {\n        this.verbosity = verbosity;\n    }\n\n    public void setClusteringOptions(ClusteringOptions clusteringOptions) {\n        this.clusteringOptions = clusteringOptions;\n    }\n\n    private boolean hasFileSuffixes() {\n        return fileSuffixes != null && fileSuffixes.length > 0;\n    }\n}\n"
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