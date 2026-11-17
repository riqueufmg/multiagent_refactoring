## CONTEXT

Hub-like Modularization (HM) is a class-level design smell that occurs when **both** the target class's Fan-In and Fan-Out are high. If either metric is medium or low, HM is absent.

This refactoring targets **Fan-Out only**. Reducing the number of distinct outgoing class dependencies sufficiently to bring Fan-Out below the high category can remove HM even when Fan-In remains high. Do not optimize Fan-In as a substitute for reducing Fan-Out.

## TASK

The goal is to reduce the target class's Fan-Out while preserving its behavior, responsibilities' cohesion, and public compatibility. Aim to remove 2 to 4 net outgoing dependencies when feasible; the actual reduction needed to eliminate HM depends on the target's metrics and the detector's thresholds, if provided in the input.

Based on the target class's code and its outgoing dependencies, follow this reasoning:
- Identify coherent responsibilities implemented by methods and fields of the target class. Group elements by their behavior, shared state, and collaboration, **not** simply because they use the same dependency.
- For each candidate responsibility, identify the distinct external classes it references and check whether those classes are also referenced elsewhere in the target class.
- Favor changes that eliminate **all direct references** from the target class to several outgoing dependency classes. A dependency is not removed from Fan-Out if any direct reference to it remains in the target class.
- Consider the effects of the target's fields, constructors, methods, inheritance, annotations, parameter and return types, and required compatibility wrappers. Do not assume that moving a method or deleting an import removes a dependency.
- Select the most suitable combination of allowed refactorings. Extract Class is one possible strategy, not a mandatory one; moving cohesive methods or fields to an appropriate existing class may be better. Avoid unnecessary new classes, forwarding layers, circular dependencies, and dependency replacements that merely disguise coupling.
- Account for **new outgoing dependencies** introduced into the target class (such as a newly extracted helper). Estimate the **net Fan-Out change** as the number of distinct outgoing dependencies genuinely eliminated minus the number of new distinct outgoing dependencies introduced.
- Prefer a small, cohesive change with a credible positive net reduction over a larger refactoring that only redistributes code. Do not sacrifice behavior or design quality to force a numeric reduction.
- Before producing the plan, verify for each proposed removed dependency why the target class will no longer reference it. Identify dependencies that must remain, and do not count them toward the expected reduction.
- The plan must consist of 1 to 3 small blocks, each independently compilable. A block may prepare a transformation without immediately reducing Fan-Out, provided the overall plan has a credible net reduction.

Observations:
- Moving methods alone does not guarantee a Fan-Out reduction. The target class must stop referring to the outgoing dependency classes being counted as removed.
- If the target class gains one new helper dependency, removing only one existing dependency gives **zero net reduction**. Removing two existing dependencies gives a net reduction of one, assuming no other changes.
- A dependency is still present when the target class references it through fields, method signatures, local variables, object creation, static calls, annotations, inheritance, or other direct type usages. Imports alone are not evidence of a dependency, and removing an import alone does not establish a Fan-Out reduction.
- Preserve necessary public APIs. If compatibility requirements leave the old dependencies in public signatures, account for them rather than claiming they were removed.
- If the input does not provide enough evidence for a reliable reduction, do not invent methods, fields, or dependencies or claim that HM will be removed. Return an empty `blocks` array rather than an unjustified transformation.

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
  "smell": "Hub-like Modularization",
  "target_type": "class",
  "target_name": "org.apache.accumulo.server.ServerContext",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261028_194120_HM__org_apache_accumulo_server_ServerContext/run_005/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "server/base/src/main/java/org/apache/accumulo/server/ServerContext.java",
  "target_source_root": "server/base/src/main/java",
  "target_code": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.server;\n\nimport static com.google.common.base.Suppliers.memoize;\n\nimport java.util.Map;\nimport java.util.Set;\nimport java.util.concurrent.ScheduledThreadPoolExecutor;\nimport java.util.concurrent.atomic.AtomicBoolean;\nimport java.util.concurrent.atomic.AtomicReference;\nimport java.util.function.Supplier;\n\nimport org.apache.accumulo.core.Constants;\nimport org.apache.accumulo.core.client.ConditionalWriter;\nimport org.apache.accumulo.core.clientImpl.ClientContext;\nimport org.apache.accumulo.core.clientImpl.ClientInfo;\nimport org.apache.accumulo.core.clientImpl.ThriftTransportPool;\nimport org.apache.accumulo.core.conf.AccumuloConfiguration;\nimport org.apache.accumulo.core.conf.DefaultConfiguration;\nimport org.apache.accumulo.core.conf.Property;\nimport org.apache.accumulo.core.conf.SiteConfiguration;\nimport org.apache.accumulo.core.crypto.CryptoFactoryLoader;\nimport org.apache.accumulo.core.data.InstanceId;\nimport org.apache.accumulo.core.data.NamespaceId;\nimport org.apache.accumulo.core.data.ResourceGroupId;\nimport org.apache.accumulo.core.data.TableId;\nimport org.apache.accumulo.core.lock.ServiceLock;\nimport org.apache.accumulo.core.metadata.schema.Ample;\nimport org.apache.accumulo.core.metrics.MetricsInfo;\nimport org.apache.accumulo.core.rpc.SslConnectionParams;\nimport org.apache.accumulo.core.spi.crypto.CryptoServiceFactory;\nimport org.apache.accumulo.core.util.threads.ThreadPools;\nimport org.apache.accumulo.core.util.threads.Threads;\nimport org.apache.accumulo.server.conf.NamespaceConfiguration;\nimport org.apache.accumulo.server.conf.ServerConfigurationFactory;\nimport org.apache.accumulo.server.conf.TableConfiguration;\nimport org.apache.accumulo.server.conf.store.PropStore;\nimport org.apache.accumulo.server.conf.store.impl.ZooPropStore;\nimport org.apache.accumulo.server.fs.VolumeManager;\nimport org.apache.accumulo.server.mem.LowMemoryDetector;\nimport org.apache.accumulo.server.metadata.ServerAmpleImpl;\nimport org.apache.accumulo.server.metrics.MetricsInfoImpl;\nimport org.apache.accumulo.server.rpc.SaslServerConnectionParams;\nimport org.apache.accumulo.server.rpc.ThriftServerType;\nimport org.apache.accumulo.server.security.AuditedSecurityOperation;\nimport org.apache.accumulo.server.security.SecurityOperation;\nimport org.apache.accumulo.server.security.delegation.AuthenticationTokenSecretManager;\nimport org.apache.accumulo.server.tables.TableManager;\nimport org.apache.accumulo.server.tablets.UniqueNameAllocator;\nimport org.apache.hadoop.fs.Path;\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\nimport com.google.common.base.Preconditions;\n\n/**\n * Provides a server context for Accumulo server components that operate with the system credentials\n * and have access to the system files and configuration.\n */\npublic class ServerContext extends ClientContext {\n  private static final Logger log = LoggerFactory.getLogger(ServerContext.class);\n\n  private final ServerInfo info;\n  private final ServerDirs serverDirs;\n  private final Supplier<ZooPropStore> propStore;\n  private final ServerContextStartupSupport startupSupport;\n  private final ServerContextConditionalWriterSupport conditionalWriterSupport;\n  private final Supplier<TableManager> tableManager;\n  private final Supplier<UniqueNameAllocator> nameAllocator;\n  private final Supplier<ServerConfigurationFactory> serverConfFactory;\n  private final Supplier<AuthenticationTokenSecretManager> secretManager;\n  private final Supplier<ScheduledThreadPoolExecutor> sharedScheduledThreadPool;\n  private final Supplier<AuditedSecurityOperation> securityOperation;\n  private final Supplier<CryptoServiceFactory> cryptoFactorySupplier;\n  private final Supplier<LowMemoryDetector> lowMemoryDetector;\n  private final AtomicReference<ServiceLock> serverLock = new AtomicReference<>();\n  private final Supplier<MetricsInfo> metricsInfoSupplier;\n  private final AtomicBoolean metricsInfoCreated = new AtomicBoolean(false);\n  private final AtomicBoolean sharedSchedExecutorCreated = new AtomicBoolean(false);\n\n  public ServerContext(SiteConfiguration siteConfig) {\n    this(ServerInfo.fromServerConfig(siteConfig), ResourceGroupId.DEFAULT);\n  }\n\n  public ServerContext(SiteConfiguration siteConfig, ResourceGroupId rgid) {\n    this(ServerInfo.fromServerConfig(siteConfig), rgid);\n  }\n\n  private ServerContext(ServerInfo info, ResourceGroupId rgid) {\n    super(info, info.getSiteConfiguration(), Threads.UEH);\n    this.info = info;\n    serverDirs = info.getServerDirs();\n    @SuppressWarnings(\"resource\")\n    var tmpPropStore = memoize(() -> ZooPropStore.initialize(getZooSession()));\n    propStore = tmpPropStore;\n    tableManager = memoize(() -> new TableManager(this));\n    nameAllocator = memoize(() -> new UniqueNameAllocator(this));\n    serverConfFactory =\n        memoize(() -> new ServerConfigurationFactory(this, getSiteConfiguration(), rgid));\n    secretManager = memoize(() -> new AuthenticationTokenSecretManager(getInstanceID(),\n        getConfiguration().getTimeInMillis(Property.GENERAL_DELEGATION_TOKEN_LIFETIME)));\n    cryptoFactorySupplier = memoize(() -> CryptoFactoryLoader.newInstance(getConfiguration()));\n    sharedScheduledThreadPool = memoize(() -> ThreadPools.getServerThreadPools()\n        .createGeneralScheduledExecutorService(getConfiguration()));\n    securityOperation =\n        memoize(() -> new AuditedSecurityOperation(this, SecurityOperation.getAuthorizor(this),\n            SecurityOperation.getAuthenticator(this), SecurityOperation.getPermHandler(this)));\n    lowMemoryDetector = memoize(() -> new LowMemoryDetector());\n    metricsInfoSupplier = memoize(() -> new MetricsInfoImpl(this));\n    conditionalWriterSupport = new ServerContextConditionalWriterSupport(this);\n    startupSupport = new ServerContextStartupSupport(this);\n  }\n\n  public static ServerContext initialize(SiteConfiguration siteConfig, String instanceName,\n      InstanceId instanceID) {\n    return new ServerContext(ServerInfo.initialize(siteConfig, instanceName, instanceID),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public static ServerContext withClientInfo(SiteConfiguration siteConfig, ClientInfo info) {\n    return new ServerContext(ServerInfo.fromServerAndClientConfig(siteConfig, info),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public static ServerContext forTesting(SiteConfiguration siteConfig, String instanceName,\n      String zooKeepers, int zkSessionTimeOut) {\n    return new ServerContext(\n        ServerInfo.forTesting(siteConfig, instanceName, zooKeepers, zkSessionTimeOut),\n        ResourceGroupId.DEFAULT);\n  }\n\n  public SiteConfiguration getSiteConfiguration() {\n    return info.getSiteConfiguration();\n  }\n\n  @Override\n  public AccumuloConfiguration getConfiguration() {\n    return serverConfFactory.get().getResourceGroupConfiguration();\n  }\n\n  public AccumuloConfiguration getSystemConfiguration() {\n    return serverConfFactory.get().getSystemConfiguration();\n  }\n\n  public TableConfiguration getTableConfiguration(TableId id) {\n    return serverConfFactory.get().getTableConfiguration(id);\n  }\n\n  public NamespaceConfiguration getNamespaceConfiguration(NamespaceId namespaceId) {\n    return serverConfFactory.get().getNamespaceConfiguration(namespaceId);\n  }\n\n  public DefaultConfiguration getDefaultConfiguration() {\n    return DefaultConfiguration.getInstance();\n  }\n\n  public ServerDirs getServerDirs() {\n    return serverDirs;\n  }\n\n  void enforceKerberosLogin() {\n    startupSupport.enforceKerberosLogin();\n  }\n\n  public VolumeManager getVolumeManager() {\n    return info.getVolumeManager();\n  }\n\n  public SslConnectionParams getServerSslParams() {\n    return SslConnectionParams.forServer(getConfiguration());\n  }\n\n  @Override\n  public SaslServerConnectionParams getSaslParams() {\n    AccumuloConfiguration conf = getSiteConfiguration();\n    if (!conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n      return null;\n    }\n    return new SaslServerConnectionParams(conf, getCredentials().getToken(), getSecretManager());\n  }\n\n  public ThriftServerType getThriftServerType() {\n    AccumuloConfiguration conf = getConfiguration();\n    if (conf.getBoolean(Property.INSTANCE_RPC_SSL_ENABLED)) {\n      if (conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n        throw new IllegalStateException(\n            \"Cannot create a Thrift server capable of both SASL and SSL\");\n      }\n      return ThriftServerType.SSL;\n    } else if (conf.getBoolean(Property.INSTANCE_RPC_SASL_ENABLED)) {\n      if (conf.getBoolean(Property.INSTANCE_RPC_SSL_ENABLED)) {\n        throw new IllegalStateException(\n            \"Cannot create a Thrift server capable of both SASL and SSL\");\n      }\n      return ThriftServerType.SASL;\n    } else {\n      return ThriftServerType.get(conf.get(Property.GENERAL_RPC_SERVER_TYPE));\n    }\n  }\n\n  public AuthenticationTokenSecretManager getSecretManager() {\n    return secretManager.get();\n  }\n\n  public TableManager getTableManager() {\n    return tableManager.get();\n  }\n\n  public UniqueNameAllocator getUniqueNameAllocator() {\n    return nameAllocator.get();\n  }\n\n  public CryptoServiceFactory getCryptoFactory() {\n    return cryptoFactorySupplier.get();\n  }\n\n  @Override\n  public Ample getAmple() {\n    return new ServerAmpleImpl(this);\n  }\n\n  public Set<String> getBaseUris() {\n    return serverDirs.getBaseUris();\n  }\n\n  public Map<Path,Path> getVolumeReplacements() {\n    return serverDirs.getVolumeReplacements();\n  }\n\n  public Set<String> getTablesDirs() {\n    return serverDirs.getTablesDirs();\n  }\n\n  public Set<String> getRecoveryDirs() {\n    return serverDirs.getRecoveryDirs();\n  }\n\n  public static void ensureDataVersionCompatible(int dataVersion) {\n    if (!AccumuloDataVersion.CAN_RUN.contains(dataVersion)) {\n      throw new IllegalStateException(\"This version of accumulo (\" + Constants.VERSION\n          + \") is not compatible with files stored using data version \" + dataVersion\n          + \". Please upgrade from \" + AccumuloDataVersion.oldestUpgradeableVersionName()\n          + \" or later.\");\n    }\n  }\n\n  public void waitForZookeeperAndHdfs() {\n    startupSupport.waitForZookeeperAndHdfs();\n  }\n\n  public void init(String application) {\n    startupSupport.init(application);\n  }\n\n  public ScheduledThreadPoolExecutor getScheduledExecutor() {\n    sharedSchedExecutorCreated.set(true);\n    return sharedScheduledThreadPool.get();\n  }\n\n  public PropStore getPropStore() {\n    return propStore.get();\n  }\n\n  @Override\n  protected long getTransportPoolMaxAgeMillis() {\n    return getClientTimeoutInMillis();\n  }\n\n  @Override\n  public synchronized ThriftTransportPool getTransportPool() {\n    return getTransportPoolImpl(true);\n  }\n\n  public AuditedSecurityOperation getSecurityOperation() {\n    return securityOperation.get();\n  }\n\n  public LowMemoryDetector getLowMemoryDetector() {\n    return lowMemoryDetector.get();\n  }\n\n  public void setServiceLock(ServiceLock lock) {\n    if (!serverLock.compareAndSet(null, lock)) {\n      throw new IllegalStateException(\"ServiceLock already set on ServerContext\");\n    }\n  }\n\n  public ServiceLock getServiceLock() {\n    return serverLock.get();\n  }\n\n  public void clearServiceLock() {\n    serverLock.set(null);\n  }\n\n  public MetricsInfo getMetricsInfo() {\n    metricsInfoCreated.set(true);\n    return metricsInfoSupplier.get();\n  }\n\n  public Supplier<ConditionalWriter> getSharedMetadataWriter() {\n    return conditionalWriterSupport.getSharedMetadataWriter();\n  }\n\n  public Supplier<ConditionalWriter> getSharedUserWriter() {\n    return conditionalWriterSupport.getSharedUserWriter();\n  }\n\n  @Override\n  public void close() {\n    Preconditions.checkState(!isClosed(), \"ServerContext.close was already called.\");\n    if (metricsInfoCreated.get()) {\n      getMetricsInfo().close();\n    }\n    if (sharedSchedExecutorCreated.get()) {\n      log.debug(\"Shutting down shared executor pool\");\n      getScheduledExecutor().shutdownNow();\n    }\n    conditionalWriterSupport.close();\n    super.close();\n  }\n}\n",
  "observed_external_calls": {
    "AccumuloDataVersion": [
      "oldestUpgradeableVersionName"
    ],
    "AccumuloDataVersion.CAN_RUN": [
      "contains"
    ],
    "CryptoFactoryLoader": [
      "newInstance"
    ],
    "DefaultConfiguration": [
      "getInstance"
    ],
    "LoggerFactory": [
      "getLogger"
    ],
    "Preconditions": [
      "checkState"
    ],
    "SecurityOperation": [
      "getAuthenticator",
      "getAuthorizor",
      "getPermHandler"
    ],
    "ServerInfo": [
      "forTesting",
      "fromServerAndClientConfig",
      "fromServerConfig",
      "initialize"
    ],
    "SslConnectionParams": [
      "forServer"
    ],
    "ThreadPools": [
      "getServerThreadPools"
    ],
    "ThriftServerType": [
      "get"
    ],
    "ZooPropStore": [
      "initialize"
    ]
  }
}

## OUTPUT

The expected output format and constraints for that output are presented below.

```json
{
  "smell_type": "Hub-like Modularization",
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
```

For each planned block, use `goal` and `details` to explain the cohesive responsibility being redistributed, the **specific outgoing dependency classes expected to disappear from the target**, any newly introduced target dependencies, and why the expected **net Fan-Out change** is positive. Make these claims only when supported by the input. Do not add new JSON fields.

## CONSTRAINTS

- Reference only packages, classes, methods, and fields present in the input, except for names of new classes or packages explicitly created by the plan.
- Each block must be small and independently compilable.
- New classes must be placed in the same package as the target class unless the input clearly justifies otherwise.
- The target class must retain its original fully qualified name (FQN) throughout the refactoring; MOVE_CLASS may be applied to other classes, but not to the target class.
- Preserve behavior and required public interfaces. Do not change tests merely to conceal regressions.
- Do not propose a package reorganization as the primary strategy for reducing class-level HM.
- Never assert that HM has been removed solely from a predicted Fan-Out change; the actual result must be measured after the refactoring.
