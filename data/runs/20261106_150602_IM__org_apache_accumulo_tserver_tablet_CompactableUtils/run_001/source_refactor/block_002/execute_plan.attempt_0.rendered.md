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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/accumulo/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.apache.accumulo.tserver.tablet.CompactableUtils"
  },
  "block": {
    "id": 2,
    "goal": "Extract compaction plugin configuration, selector execution, and compaction helper coordination into a cohesive class, reducing the general-purpose method count and implementation complexity of CompactableUtils.",
    "files": [
      "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java",
      "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.apache.accumulo.tserver.tablet.CompactableUtils",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils"
        ],
        "outputs": [
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.computeOverrides(org.apache.accumulo.tserver.tablet.Tablet,java.util.Set)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.computeOverrides(org.apache.accumulo.tserver.tablet.Tablet,java.util.Set,org.apache.accumulo.core.client.admin.PluginConfig)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.newInstance(org.apache.accumulo.core.conf.AccumuloConfiguration,java.lang.String,java.lang.Class)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.selectFiles(org.apache.accumulo.tserver.tablet.Tablet,java.util.SortedMap,org.apache.accumulo.core.client.admin.PluginConfig)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.getHelper(org.apache.accumulo.core.spi.compaction.CompactionKind,org.apache.accumulo.tserver.tablet.Tablet,java.lang.Long,org.apache.accumulo.core.client.admin.CompactionConfig)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.getOverrides(org.apache.accumulo.core.spi.compaction.CompactionKind,org.apache.accumulo.tserver.tablet.Tablet,org.apache.accumulo.tserver.tablet.CompactableImpl.CompactionHelper,java.util.Set)",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.TableCompactionHelper",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.UserCompactionHelper"
        ],
        "details": "Move the compaction selector and configurer methods, newInstance, getHelper, getOverrides, and both private CompactionHelper implementations together. Preserve package visibility for package-private methods and preserve the existing nested helper behavior. Update references from CompactableUtils.newInstance, CompactableUtils.selectFiles, and computeOverrides to the extracted class within the moved implementation.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils.java",
          "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
        ],
        "outputs": [],
        "details": "Add all imports required by the extracted compaction plugin implementation, including plugin, compaction, summary, configuration, metadata, and Hadoop types. Remove imports from CompactableUtils that are no longer referenced after extraction.",
        "risk": "low"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "org.apache.accumulo.tserver.tablet.CompactableUtils.getHelper()",
          "org.apache.accumulo.tserver.tablet.CompactableUtils.getOverrides()",
          "org.apache.accumulo.tserver.tablet.CompactableUtils.selectFiles()",
          "org.apache.accumulo.tserver.tablet.CompactableUtils.computeOverrides()"
        ],
        "outputs": [
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.getHelper()",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.getOverrides()",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.selectFiles()",
          "org.apache.accumulo.tserver.tablet.CompactableCompactionUtils.computeOverrides()"
        ],
        "details": "Update CompactableImpl and any other callers to use CompactableCompactionUtils. In CompactableUtils.compact, replace the call to getOverrides with CompactableCompactionUtils.getOverrides. Preserve method signatures and package-level accessibility.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/TableCompactionHelper.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/UserCompactionHelper.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set,org/apache/accumulo/core/client/admin/PluginConfig).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getHelper(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,java/lang/Long,org/apache/accumulo/core/client/admin/CompactionConfig).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getOverrides(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,org/apache/accumulo/tserver/tablet/CompactableImpl/CompactionHelper,java/util/Set).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/newInstance(org/apache/accumulo/core/conf/AccumuloConfiguration,java/lang/String,java/lang/Class).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/selectFiles(org/apache/accumulo/tserver/tablet/Tablet,java/util/SortedMap,org/apache/accumulo/core/client/admin/PluginConfig).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
  ],
  "executor_existing_files": [
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java"
  ],
  "executor_new_files": [
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/TableCompactionHelper.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/UserCompactionHelper.java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set,org/apache/accumulo/core/client/admin/PluginConfig).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getHelper(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,java/lang/Long,org/apache/accumulo/core/client/admin/CompactionConfig).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getOverrides(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,org/apache/accumulo/tserver/tablet/CompactableImpl/CompactionHelper,java/util/Set).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/newInstance(org/apache/accumulo/core/conf/AccumuloConfiguration,java/lang/String,java/lang/Class).java",
    "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/selectFiles(org/apache/accumulo/tserver/tablet/Tablet,java/util/SortedMap,org/apache/accumulo/core/client/admin/PluginConfig).java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/TableCompactionHelper.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/UserCompactionHelper.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/computeOverrides(org/apache/accumulo/tserver/tablet/Tablet,java/util/Set,org/apache/accumulo/core/client/admin/PluginConfig).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getHelper(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,java/lang/Long,org/apache/accumulo/core/client/admin/CompactionConfig).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/getOverrides(org/apache/accumulo/core/spi/compaction/CompactionKind,org/apache/accumulo/tserver/tablet/Tablet,org/apache/accumulo/tserver/tablet/CompactableImpl/CompactionHelper,java/util/Set).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/newInstance(org/apache/accumulo/core/conf/AccumuloConfiguration,java/lang/String,java/lang/Class).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableCompactionUtils/selectFiles(org/apache/accumulo/tserver/tablet/Tablet,java/util/SortedMap,org/apache/accumulo/core/client/admin/PluginConfig).java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "server/tserver/src/main/java/org/apache/accumulo/tserver/tablet/CompactableUtils.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.tserver.tablet;\n\nimport java.io.IOException;\nimport java.io.UncheckedIOException;\nimport java.util.Collection;\nimport java.util.Collections;\nimport java.util.Map;\nimport java.util.Objects;\nimport java.util.Optional;\nimport java.util.Set;\nimport java.util.SortedMap;\nimport java.util.function.Predicate;\nimport java.util.stream.Collectors;\n\nimport org.apache.accumulo.core.classloader.ClassLoaderUtil;\nimport org.apache.accumulo.core.client.PluginEnvironment;\nimport org.apache.accumulo.core.client.admin.CompactionConfig;\nimport org.apache.accumulo.core.client.admin.PluginConfig;\nimport org.apache.accumulo.core.client.admin.compaction.CompactableFile;\nimport org.apache.accumulo.core.client.admin.compaction.CompactionConfigurer;\nimport org.apache.accumulo.core.client.admin.compaction.CompactionSelector;\nimport org.apache.accumulo.core.client.admin.compaction.CompactionSelector.Selection;\nimport org.apache.accumulo.core.client.sample.SamplerConfiguration;\nimport org.apache.accumulo.core.client.summary.SummarizerConfiguration;\nimport org.apache.accumulo.core.client.summary.Summary;\nimport org.apache.accumulo.core.clientImpl.UserCompactionUtils;\nimport org.apache.accumulo.core.conf.AccumuloConfiguration;\nimport org.apache.accumulo.core.conf.ConfigurationCopy;\nimport org.apache.accumulo.core.conf.ConfigurationTypeHelper;\nimport org.apache.accumulo.core.conf.Property;\nimport org.apache.accumulo.core.data.Key;\nimport org.apache.accumulo.core.data.TableId;\nimport org.apache.accumulo.core.data.TabletId;\nimport org.apache.accumulo.core.data.Value;\nimport org.apache.accumulo.core.dataImpl.KeyExtent;\nimport org.apache.accumulo.core.dataImpl.TabletIdImpl;\nimport org.apache.accumulo.core.file.FileOperations;\nimport org.apache.accumulo.core.iterators.SortedKeyValueIterator;\nimport org.apache.accumulo.core.metadata.CompactableFileImpl;\nimport org.apache.accumulo.core.metadata.ReferencedTabletFile;\nimport org.apache.accumulo.core.metadata.StoredTabletFile;\nimport org.apache.accumulo.core.metadata.schema.DataFileValue;\nimport org.apache.accumulo.core.sample.impl.SamplerConfigurationImpl;\nimport org.apache.accumulo.core.spi.common.ServiceEnvironment;\nimport org.apache.accumulo.core.spi.compaction.CompactionJob;\nimport org.apache.accumulo.core.spi.compaction.CompactionKind;\nimport org.apache.accumulo.core.summary.Gatherer;\nimport org.apache.accumulo.core.summary.SummarizerFactory;\nimport org.apache.accumulo.core.summary.SummaryCollection;\nimport org.apache.accumulo.core.summary.SummaryReader;\nimport org.apache.accumulo.core.util.Pair;\nimport org.apache.accumulo.server.ServiceEnvironmentImpl;\nimport org.apache.accumulo.server.compaction.CompactionStats;\nimport org.apache.accumulo.server.compaction.FileCompactor;\nimport org.apache.accumulo.server.compaction.FileCompactor.CompactionCanceledException;\nimport org.apache.accumulo.server.compaction.FileCompactor.CompactionEnv;\nimport org.apache.accumulo.server.conf.TableConfiguration;\nimport org.apache.accumulo.server.util.MetadataTableUtil;\nimport org.apache.accumulo.tserver.tablet.CompactableImpl.CompactionHelper;\nimport org.apache.hadoop.conf.Configuration;\nimport org.apache.hadoop.fs.FileSystem;\nimport org.apache.hadoop.fs.Path;\n\nimport com.google.common.collect.Collections2;\n\npublic class CompactableUtils {\n\n  /**\n   * Compatibility delegation for callers not yet migrated to CompactableFileUtils.\n   */\n  public static Map<StoredTabletFile,Pair<Key,Key>> getFirstAndLastKeys(Tablet tablet,\n      Set<StoredTabletFile> allFiles) throws IOException {\n    return CompactableFileUtils.getFirstAndLastKeys(tablet, allFiles);\n  }\n\n  /**\n   * Compatibility delegation for callers not yet migrated to CompactableFileUtils.\n   */\n  public static Set<StoredTabletFile> findChopFiles(KeyExtent extent,\n      Map<StoredTabletFile,Pair<Key,Key>> firstAndLastKeys, Collection<StoredTabletFile> allFiles) {\n    return CompactableFileUtils.findChopFiles(extent, firstAndLastKeys, allFiles);\n  }\n\n  static Map<String,String> computeOverrides(Tablet tablet, Set<CompactableFile> files) {\n    var tconf = tablet.getTableConfiguration();\n\n    var configurorClass = tconf.get(Property.TABLE_COMPACTION_CONFIGURER);\n    if (configurorClass == null || configurorClass.isBlank()) {\n      return null;\n    }\n\n    var opts = tconf.getAllPropertiesWithPrefixStripped(Property.TABLE_COMPACTION_CONFIGURER_OPTS);\n\n    return computeOverrides(tablet, files, new PluginConfig(configurorClass, opts));\n  }\n\n  static Map<String,String> computeOverrides(Tablet tablet, Set<CompactableFile> files,\n      PluginConfig cfg) {\n    CompactionConfigurer configurer = CompactableUtils.newInstance(tablet.getTableConfiguration(),\n        cfg.getClassName(), CompactionConfigurer.class);\n\n    final ServiceEnvironment senv = new ServiceEnvironmentImpl(tablet.getContext());\n\n    configurer.init(new CompactionConfigurer.InitParameters() {\n      @Override\n      public Map<String,String> getOptions() {\n        return cfg.getOptions();\n      }\n\n      @Override\n      public PluginEnvironment getEnvironment() {\n        return senv;\n      }\n\n      @Override\n      public TableId getTableId() {\n        return tablet.getExtent().tableId();\n      }\n    });\n\n    var overrides = configurer.override(new CompactionConfigurer.InputParameters() {\n      @Override\n      public Collection<CompactableFile> getInputFiles() {\n        return files;\n      }\n\n      @Override\n      public PluginEnvironment getEnvironment() {\n        return senv;\n      }\n\n      @Override\n      public TableId getTableId() {\n        return tablet.getExtent().tableId();\n      }\n\n      @Override\n      public TabletId getTabletId() {\n        return new TabletIdImpl(tablet.getExtent());\n      }\n    });\n\n    if (overrides.getOverrides().isEmpty()) {\n      return null;\n    }\n\n    return overrides.getOverrides();\n  }\n\n  static <T> T newInstance(AccumuloConfiguration tableConfig, String className,\n      Class<T> baseClass) {\n    String context = ClassLoaderUtil.tableContext(tableConfig);\n    try {\n      return ConfigurationTypeHelper.getClassInstance(context, className, baseClass);\n    } catch (ReflectiveOperationException e) {\n      throw new IllegalArgumentException(e);\n    }\n  }\n\n  static Set<StoredTabletFile> selectFiles(Tablet tablet,\n      SortedMap<StoredTabletFile,DataFileValue> datafiles, PluginConfig selectorConfig) {\n\n    CompactionSelector selector = newInstance(tablet.getTableConfiguration(),\n        selectorConfig.getClassName(), CompactionSelector.class);\n\n    final ServiceEnvironment senv = new ServiceEnvironmentImpl(tablet.getContext());\n\n    selector.init(new CompactionSelector.InitParameters() {\n      @Override\n      public Map<String,String> getOptions() {\n        return selectorConfig.getOptions();\n      }\n\n      @Override\n      public PluginEnvironment getEnvironment() {\n        return senv;\n      }\n\n      @Override\n      public TableId getTableId() {\n        return tablet.getExtent().tableId();\n      }\n    });\n\n    Selection selection = selector.select(new CompactionSelector.SelectionParameters() {\n      @Override\n      public PluginEnvironment getEnvironment() {\n        return senv;\n      }\n\n      @Override\n      public Collection<CompactableFile> getAvailableFiles() {\n        return Collections2.transform(datafiles.entrySet(),\n            e -> new CompactableFileImpl(e.getKey(), e.getValue()));\n      }\n\n      @Override\n      public Collection<Summary> getSummaries(Collection<CompactableFile> files,\n          Predicate<SummarizerConfiguration> summarySelector) {\n\n        var context = tablet.getContext();\n        var tsrm = tablet.getTabletResources().getTabletServerResourceManager();\n        var tableConf = tablet.getTableConfiguration();\n\n        SummaryCollection sc = new SummaryCollection();\n        SummarizerFactory factory = new SummarizerFactory(tableConf);\n        for (CompactableFile cf : files) {\n          var file = CompactableFileImpl.toStoredTabletFile(cf);\n          FileSystem fs = context.getVolumeManager().getFileSystemByPath(file.getPath());\n          Configuration conf = context.getHadoopConf();\n          SummaryCollection fsc = SummaryReader\n              .load(fs, conf, factory, file.getPath(), summarySelector, tsrm.getSummaryCache(),\n                  tsrm.getIndexCache(), tsrm.getFileLenCache(), tableConf.getCryptoService())\n              .getSummaries(Collections.singletonList(new Gatherer.RowRange(tablet.getExtent())));\n          sc.merge(fsc, factory);\n        }\n\n        return sc.getSummaries();\n      }\n\n      @Override\n      public TableId getTableId() {\n        return tablet.getExtent().tableId();\n      }\n\n      @Override\n      public TabletId getTabletId() {\n        return new TabletIdImpl(tablet.getExtent());\n      }\n\n      @Override\n      public Optional<SortedKeyValueIterator<Key,Value>> getSample(CompactableFile file,\n          SamplerConfiguration sc) {\n        try {\n          FileOperations fileFactory = FileOperations.getInstance();\n          Path path = new Path(file.getUri());\n          FileSystem ns = tablet.getTabletServer().getVolumeManager().getFileSystemByPath(path);\n          var tableConf = tablet.getTableConfiguration();\n          var fiter = fileFactory.newReaderBuilder()\n              .forFile(ReferencedTabletFile.of(path), ns, ns.getConf(),\n                  tableConf.getCryptoService())\n              .withTableConfiguration(tableConf).seekToBeginning().build();\n          return Optional.ofNullable(fiter.getSample(new SamplerConfigurationImpl(sc)));\n        } catch (IOException e) {\n          throw new UncheckedIOException(e);\n        }\n      }\n    });\n\n    return selection.getFilesToCompact().stream().map(CompactableFileImpl::toStoredTabletFile)\n        .collect(Collectors.toSet());\n  }\n\n  private static final class TableCompactionHelper implements CompactionHelper {\n    private final PluginConfig cselCfg2;\n    private final Tablet tablet;\n\n    private TableCompactionHelper(PluginConfig cselCfg2, Tablet tablet) {\n      this.cselCfg2 = Objects.requireNonNull(cselCfg2);\n      this.tablet = Objects.requireNonNull(tablet);\n    }\n\n    @Override\n    public Set<StoredTabletFile> selectFiles(SortedMap<StoredTabletFile,DataFileValue> allFiles) {\n      return CompactableUtils.selectFiles(tablet, allFiles, cselCfg2);\n    }\n\n    @Override\n    public Map<String,String> getConfigOverrides(Set<CompactableFile> files) {\n      return null;\n    }\n  }\n\n  private static final class UserCompactionHelper implements CompactionHelper {\n    private final CompactionConfig compactionConfig;\n    private final Tablet tablet;\n    private final Long compactionId;\n\n    private UserCompactionHelper(CompactionConfig compactionConfig, Tablet tablet,\n        Long compactionId) {\n      this.compactionConfig = compactionConfig;\n      this.tablet = tablet;\n      this.compactionId = compactionId;\n    }\n\n    @Override\n    public Set<StoredTabletFile> selectFiles(SortedMap<StoredTabletFile,DataFileValue> allFiles) {\n      final Set<StoredTabletFile> selectedFiles;\n\n      if (!UserCompactionUtils.isDefault(compactionConfig.getSelector())) {\n        selectedFiles =\n            CompactableUtils.selectFiles(tablet, allFiles, compactionConfig.getSelector());\n      } else {\n        selectedFiles = allFiles.keySet();\n      }\n\n      if (selectedFiles.isEmpty()) {\n        MetadataTableUtil.updateTabletCompactID(tablet.getExtent(), compactionId,\n            tablet.getTabletServer().getContext(), tablet.getTabletServer().getLock());\n        tablet.setLastCompactionID(compactionId);\n      }\n\n      return selectedFiles;\n    }\n\n    @Override\n    public Map<String,String> getConfigOverrides(Set<CompactableFile> files) {\n      if (!UserCompactionUtils.isDefault(compactionConfig.getConfigurer())) {\n        return computeOverrides(tablet, files, compactionConfig.getConfigurer());\n      }\n      return null;\n    }\n  }\n\n  public static CompactionHelper getHelper(CompactionKind kind, Tablet tablet, Long compactionId,\n      CompactionConfig compactionConfig) {\n    if (kind == CompactionKind.USER) {\n      return new UserCompactionHelper(compactionConfig, tablet, compactionId);\n    } else if (kind == CompactionKind.SELECTOR) {\n      var tconf = tablet.getTableConfiguration();\n      var selectorClassName = tconf.get(Property.TABLE_COMPACTION_SELECTOR);\n      PluginConfig cselCfg = null;\n      if (selectorClassName != null && !selectorClassName.isBlank()) {\n        var opts =\n            tconf.getAllPropertiesWithPrefixStripped(Property.TABLE_COMPACTION_SELECTOR_OPTS);\n        cselCfg = new PluginConfig(selectorClassName, opts);\n      }\n      if (cselCfg != null) {\n        return new TableCompactionHelper(cselCfg, tablet);\n      }\n    }\n    return null;\n  }\n\n  public static Map<String,String> getOverrides(CompactionKind kind, Tablet tablet,\n      CompactionHelper driver, Set<CompactableFile> files) {\n    Map<String,String> overrides = null;\n    if (kind == CompactionKind.USER || kind == CompactionKind.SELECTOR) {\n      overrides = driver.getConfigOverrides(files);\n    }\n    if (overrides == null) {\n      overrides = computeOverrides(tablet, files);\n    }\n    if (overrides == null) {\n      return Map.of();\n    }\n    return overrides;\n  }\n\n  private static AccumuloConfiguration getCompactionConfig(TableConfiguration tableConfiguration,\n      Map<String,String> overrides) {\n    if (overrides.isEmpty()) {\n      return tableConfiguration;\n    }\n    ConfigurationCopy copy = new ConfigurationCopy(tableConfiguration);\n    overrides.forEach((k, v) -> copy.set(k, v));\n    return copy;\n  }\n\n  static CompactionStats compact(Tablet tablet, CompactionJob job,\n      CompactableImpl.CompactionInfo cInfo, CompactionEnv cenv,\n      Map<StoredTabletFile,DataFileValue> compactFiles, ReferencedTabletFile tmpFileName)\n      throws IOException, CompactionCanceledException {\n    TableConfiguration tableConf = tablet.getTableConfiguration();\n    AccumuloConfiguration compactionConfig = getCompactionConfig(tableConf,\n        getOverrides(job.getKind(), tablet, cInfo.localHelper, job.getFiles()));\n    FileCompactor compactor = new FileCompactor(tablet.getContext(), tablet.getExtent(),\n        compactFiles, tmpFileName, cInfo.propagateDeletes, cenv, cInfo.iters, compactionConfig,\n        tableConf.getCryptoService(), tablet.getPausedCompactionMetrics());\n    return compactor.call();\n  }\n\n  static Optional<StoredTabletFile> bringOnline(DatafileManager datafileManager,\n      CompactableImpl.CompactionInfo cInfo, CompactionStats stats,\n      Map<StoredTabletFile,DataFileValue> compactFiles, ReferencedTabletFile compactTmpName)\n      throws IOException {\n    var dfv = new DataFileValue(stats.getFileSize(), stats.getEntriesWritten());\n    return datafileManager.bringMajorCompactionOnline(compactFiles.keySet(), compactTmpName,\n        cInfo.checkCompactionId, cInfo.selectedFiles, dfv, Optional.empty());\n  }\n}\n"
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
