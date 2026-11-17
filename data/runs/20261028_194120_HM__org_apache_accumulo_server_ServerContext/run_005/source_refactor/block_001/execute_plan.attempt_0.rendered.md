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
    "smell": "HM",
    "smell_name": "Hub-like Modularization",
    "target_type": "class",
    "target_name": "org.apache.accumulo.server.ServerContext"
  },
  "block": {
    "id": 1,
    "goal": "Extract the data-version compatibility responsibility from ServerContext while preserving the public ensureDataVersionCompatible(int) API.",
    "files": [
      "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
      "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.apache.accumulo.server.ServerContext",
          "org.apache.accumulo.server.ServerContextDataVersionSupport"
        ],
        "outputs": [
          "org.apache.accumulo.server.ServerContextDataVersionSupport"
        ],
        "details": "Extract the body and data-version-specific collaborators of ServerContext.ensureDataVersionCompatible(int) into the new same-package class ServerContextDataVersionSupport. The extracted class should contain the existing compatibility check using AccumuloDataVersion.CAN_RUN, AccumuloDataVersion.oldestUpgradeableVersionName(), and Constants.VERSION. Retain ServerContext.ensureDataVersionCompatible(int) as a public compatibility wrapper delegating to ServerContextDataVersionSupport, so callers and behavior remain unchanged. Remove the direct Constants and AccumuloDataVersion references from ServerContext; the target gains only the new ServerContextDataVersionSupport dependency. The expected net Fan-Out change is positive: two outgoing dependencies, Constants and AccumuloDataVersion, disappear from ServerContext and one new helper dependency is introduced, for an estimated net reduction of one distinct dependency.",
        "risk": "low"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
          "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java"
        ],
        "outputs": [
          "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
          "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java"
        ],
        "details": "Remove the Constants import from ServerContext after the compatibility logic is extracted, and add the Constants import to ServerContextDataVersionSupport. Do not remove or alter dependencies that remain required by ServerContext fields, method signatures, inheritance, constructors, or other methods.",
        "risk": "low"
      }
    ]
  },
  "allowed_files": [
    "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
    "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java"
  ],
  "executor_existing_files": [
    "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java"
  ],
  "executor_new_files": [
    "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.server;\n\nimport static com.google.common.base.Suppliers.memoize;\n\nimport java.util.Map;\nimport java.util.Set;\nimport java.util.concurrent.ScheduledThreadPoolExecutor;\nimport java.util.concurrent.atomic.AtomicBoolean;\nimport java.util.concurrent.atomic.AtomicReference;\nimport java.util.function.Supplier;\n\nimport org.apache.accumulo.core.Constants;\nimport org.apache.accumulo.core.client.ConditionalWriter;\nimport org.apache.accumulo.core.clientImpl.ClientContext;\nimport org.apache.accumulo.core.clientImpl.ClientInfo;\nimport org.apache.accumulo.core.clientImpl.ThriftTransportPool;\nimport org.apache.accumulo.core.conf.AccumuloConfiguration;\nimport org.apache.accumulo.core.conf.DefaultConfiguration;\nimport org.apache.accumulo.core.conf.Property;\nimport org.apache.accumulo.core.conf.SiteConfiguration;\nimport org.apache.accumulo.core.crypto.CryptoFactoryLoader;\nimport org.apache.accumulo.core.data.InstanceId;\nimport org.apache.accumulo.core.data.NamespaceId;\nimport org.apache.accumulo.core.data.ResourceGroupId;\nimport org.apache.accumulo.core.data.TableId;\nimport org.apache.accumulo.core.lock.ServiceLock;\nimport org.apache.accumulo.core.metadata.schema.Ample;\nimport org.apache.accumulo.core.metrics.MetricsInfo;\nimport org.apache.accumulo.core.rpc.SslConnectionParams;\nimport org.apache.accumulo.core.spi.crypto.CryptoServiceFactory;\nimport org.apache.accumulo.core.util.threads.ThreadPools;\nimport org.apache.accumulo.core.util.threads.Threads;\nimport org.apache.accumulo.server.conf.NamespaceConfiguration;\nimport org.apache.accumulo.server.conf.ServerConfigurationFactory;\nimport org.apache.accumulo.server.conf.TableConfiguration;\nimport org.apache.accumulo.server.conf.store.PropStore;\nimport org.apache.accumulo.server.conf.store.impl.ZooPropStore;\nimport org.apache.accumulo.server.fs.VolumeManager;\nimport org.apache.accumulo.server.mem.LowMemoryDetector;\nimport org.apache.accumulo.server.metadata.ServerAmpleImpl;\nimport org.apache.accumulo.server.metrics.MetricsInfoImpl;\nimport org.apache.accumulo.server.rpc.SaslServerConnectionParams;\nimport org.apache.accumulo.server.rpc.ThriftServerType;\nimport org.apache.accumulo.server.security.AuditedSecurityOperation;\nimport org.apache.accumulo.server.security.SecurityOperation;\nimport org.apache.accumulo.server.security.delegation.AuthenticationTokenSecretManager;\nimport org.apache.accumulo.server.tables.TableManager;\nimport org.apache.accumulo.server.tablets.UniqueNameAllocator;\nimport org.apache.hadoop.fs.Path;\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\nimport com.google.common.base.Preconditions;\n\n/**\n * Provides a server context for Accumulo server components that operate with the system credentials\n * and have access to the system files and configuration.\n */\npublic class ServerContext extends ClientContext {\n  private static final Logger log = LoggerFactory.getLogger(ServerContext.class);\n\n  private final ServerInfo info;\n  private final ServerDirs serverDirs;\n  private final Supplier<ZooPropStore> propStore;\n  private final ServerContextStartupSupport startupSupport;\n  private final ServerContextConditionalWriterSupport conditionalWriterSupport;\n  private final Supplier<TableManager> tableManager;\n  private final Supplier<UniqueNameAllocator> nameAllocator;\n  private final Supplier<ServerConfigurationFactory> serverConfFactory;\n  private final Supplier<AuthenticationTokenSecretManager> secretManager;\n  private final Supplier<ScheduledThreadPoolExecutor> sharedScheduledThreadPool;\n  private final Supplier<AuditedSecurityOperation> securityOperation;\n  private final Supplier<CryptoServiceFactory> cryptoFactorySupplier;\n  private final Supplier<LowMemoryDetector> lowMemoryDetector;\n  private final AtomicReference<ServiceLock> serverLock = new AtomicReference<>();\n  private final Supplier<MetricsInfo> metricsInfoSupplier;\n  private final AtomicBoolean metricsInfoCreated = new AtomicBoolean(false);\n  private final AtomicBoolean sharedSchedExecutorCreated = new AtomicBoolean(false);\n\n  public ServerContext(SiteConfiguration siteConfig) {\n    this(ServerInfo.fromServerConfig(siteConfig), ResourceGroupId.DEFAULT);\n  }\n\n  public ServerContext(SiteConfiguration siteConfig, ResourceGroupId rgid) {\n    this(ServerInfo.fromServerConfig(siteConfig), rgid);\n  }\n\n  private ServerContext(ServerInfo info, ResourceGroupId rgid) {\n    super(info, info.getSiteConfiguration(), Threads.UEH);\n    this.info = info;\n    serverDirs = info.getServerDirs();\n    @SuppressWarnings(\"resource\")\n    var tmpPropStore = memoize(() -> ZooPropStore.initialize(getZooSession()));\n    propStore = tmpPropStore;\n    tableManager = memoize(() -> new TableManager(this));\n    nameAllocator = memoize(() -> new UniqueNameAllocator(this));\n    serverConfFactory =\n        memoize(() -> new ServerConfigurationFactory(this, getSiteConfiguration(), rgid));\n    secretManager = memoize(() -> new AuthenticationTokenSecretManager(getInstanceID(),\n        getConfiguration().getTimeInMillis(Property.GENERAL_DELEGATION_TOKEN_LIFETIME)));\n    cryptoFactorySupplier = memoize(() -> CryptoFactoryLoader.newInstance(getConfiguration()));\n    sharedScheduledThreadPool = memoize(() -> ThreadPools.getServerThreadPools()\n        .createGeneralScheduledExecutorService(getConfiguration()));\n    securityOperation =\n        memoize(() -> new AuditedSecurityOperation(this, SecurityOperation.getAuthorizor(this),\n            SecurityOperation.getAuthenticator(this), SecurityOperation.getPermHandler(this)));\n    lowMemoryDetector = memoize(() -> new LowMemoryDetector());\n    metricsInfoSupplier = memoize(() -> new MetricsInfoImpl(this));\n    conditionalWriterSupport = new ServerContextConditionalWriterSupport(this);\n    startupSupport = new ServerContextStartupSupport(this);\n  }\n\n  public static ServerContext initialize(SiteConfiguration siteConfig, String instanceName,\n      InstanceId instanceID) {\n    return new ServerContext(ServerInfo.initialize(siteConfig, instanceName, instanceID),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public static ServerContext withClientInfo(SiteConfiguration siteConfig, ClientInfo info) {\n    return new ServerContext(ServerInfo.fromServerAndClientConfig(siteConfig, info),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public static ServerContext forTesting(SiteConfiguration siteConfig, String instanceName,\n      String zooKeepers, int zkSessionTimeOut) {\n    return new ServerContext(\n        ServerInfo.forTesting(siteConfig, instanceName, zooKeepers, zkSessionTimeOut),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public SiteConfiguration getSiteConfiguration() {\n    return info.getSiteConfiguration();\n  }\n\n  @Override\n  public AccumuloConfiguration getConfiguration() {\n    return serverConfFactory.get().getResourceGroupConfiguration();\n  }\n\n  public AccumuloConfiguration getSystemConfiguration() {\n    return serverConfFactory.get().getSystemConfiguration();\n  }\n\n  public TableConfiguration getTableConfiguration(TableId id) {\n    return serverConfFactory.get().getTableConfiguration(id);\n  }\n\n  public NamespaceConfiguration getNamespaceConfiguration(NamespaceId namespaceId) {\n    return serverConfFactory.get().getNamespaceConfiguration(namespaceId);\n  }\n\n  public DefaultConfiguration getDefaultConfiguration() {\n    return DefaultConfiguration.getInstance();\n  }\n\n  public ServerDirs getServerDirs() {\n    return serverDirs;\n  }\n\n  void enforceKerberosLogin() {\n    startupSupport.enforceKerberosLogin();\n  }\n\n  public VolumeManager getVolumeManager() {\n    return info.getVolumeManager();\n  }\n\n  public SslConnectionParams getServerSslParams() {\n    return SslConnectionParams.forServer(getConfiguration());\n  }\n\n  @Override\n  public SaslServerConnectionParams getSaslParams() {\n    AccumuloConfiguration conf = getSiteConfiguration();\n    if (!conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n      return null;\n    }\n    return new SaslServerConnectionParams(conf, getCredentials().getToken(), getSecretManager());\n  }\n\n  public ThriftServerType getThriftServerType() {\n    AccumuloConfiguration conf = getConfiguration();\n    if (conf.getBoolean(Property.INSTANCE_RPC_SSL_ENABLED)) {\n      if (conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n        throw new IllegalStateException(\n            \"Cannot create a Thrift server capable of both SASL and SSL\");\n      }\n      return ThriftServerType.SSL;\n    } else if (conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n      if (conf.getBoolean(Property.INSTANCE_RPC_SSL_ENABLED)) {\n        throw new IllegalStateException(\n            \"Cannot create a Thrift server capable of both SASL and SSL\");\n      }\n      return ThriftServerType.SASL;\n    } else {\n      return ThriftServerType.get(conf.get(Property.GENERAL_RPC_SERVER_TYPE));\n    }\n  }\n\n  public AuthenticationTokenSecretManager getSecretManager() {\n    return secretManager.get();\n  }\n\n  public TableManager getTableManager() {\n    return tableManager.get();\n  }\n\n  public UniqueNameAllocator getUniqueNameAllocator() {\n    return nameAllocator.get();\n  }\n\n  public CryptoServiceFactory getCryptoFactory() {\n    return cryptoFactorySupplier.get();\n  }\n\n  @Override\n  public Ample getAmple() {\n    return new ServerAmpleImpl(this);\n  }\n\n  public Set<String> getBaseUris() {\n    return serverDirs.getBaseUris();\n  }\n\n  public Map<Path,Path> getVolumeReplacements() {\n    return serverDirs.getVolumeReplacements();\n  }\n\n  public Set<String> getTablesDirs() {\n    return serverDirs.getTablesDirs();\n  }\n\n  public Set<String> getRecoveryDirs() {\n    return serverDirs.getRecoveryDirs();\n  }\n\n  public static void ensureDataVersionCompatible(int dataVersion) {\n    if (!AccumuloDataVersion.CAN_RUN.contains(dataVersion)) {\n      throw new IllegalStateException(\"This version of accumulo (\" + Constants.VERSION\n          + \") is not compatible with files stored using data version \" + dataVersion\n          + \". Please upgrade from \" + AccumuloDataVersion.oldestUpgradeableVersionName()\n          + \" or later.\");\n    }\n  }\n\n  public void waitForZookeeperAndHdfs() {\n    startupSupport.waitForZookeeperAndHdfs();\n  }\n\n  public void init(String application) {\n    startupSupport.init(application);\n  }\n\n  public ScheduledThreadPoolExecutor getScheduledExecutor() {\n    sharedSchedExecutorCreated.set(true);\n    return sharedScheduledThreadPool.get();\n  }\n\n  public PropStore getPropStore() {\n    return propStore.get();\n  }\n\n  @Override\n  protected long getTransportPoolMaxAgeMillis() {\n    return getClientTimeoutInMillis();\n  }\n\n  @Override\n  public synchronized ThriftTransportPool getTransportPool() {\n    return getTransportPoolImpl(true);\n  }\n\n  public AuditedSecurityOperation getSecurityOperation() {\n    return securityOperation.get();\n  }\n\n  public LowMemoryDetector getLowMemoryDetector() {\n    return lowMemoryDetector.get();\n  }\n\n  public void setServiceLock(ServiceLock lock) {\n    if (!serverLock.compareAndSet(null, lock)) {\n      throw new IllegalStateException(\"ServiceLock already set on ServerContext\");\n    }\n  }\n\n  public ServiceLock getServiceLock() {\n    return serverLock.get();\n  }\n\n  public void clearServiceLock() {\n    serverLock.set(null);\n  }\n\n  public MetricsInfo getMetricsInfo() {\n    metricsInfoCreated.set(true);\n    return metricsInfoSupplier.get();\n  }\n\n  public Supplier<ConditionalWriter> getSharedMetadataWriter() {\n    return conditionalWriterSupport.getSharedMetadataWriter();\n  }\n\n  public Supplier<ConditionalWriter> getSharedUserWriter() {\n    return conditionalWriterSupport.getSharedUserWriter();\n  }\n\n  @Override\n  public void close() {\n    Preconditions.checkState(!isClosed(), \"ServerContext.close was already called.\");\n    if (metricsInfoCreated.get()) {\n      getMetricsInfo().close();\n    }\n    if (sharedSchedExecutorCreated.get()) {\n      log.debug(\"Shutting down shared executor pool\");\n      getScheduledExecutor().shutdownNow();\n    }\n    conditionalWriterSupport.close();\n    super.close();\n  }\n}\n"
    },
    {
      "path": "server/base/src/main/java/org/apache/accumulo/server/ServerContextDataVersionSupport.java",
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
