# GOAL
Refactor ONE cohesive cluster from the TARGET PACKAGE to reduce the God Component smell.

A single run must move only ONE cluster. All classes in the selected cluster must be moved to the SAME new subpackage.

# INPUT DATA
- `target_files`: files currently in the target package.
- `internal_deps`: dependencies between classes inside the target package.
- `incoming_deps`: external classes that depend on classes in the target package.
- `outgoing_deps`: target package classes depending on external classes.

# TASK
Choose exactly ONE cohesive cluster of classes from the target package.

Then generate a refactoring plan where:
- all classes in the cluster move to the same new subpackage;
- the plan contains exactly ONE block;
- that block moves all classes in the selected cluster together;
- the block contains 2 to 10 MOVE_CLASS operations.

# CLUSTER MOVEMENT STRATEGY

For God Component refactoring, each block must move one cohesive cluster, not a single isolated class.

A cluster must contain 2 to 4 classes.

All classes in the selected cluster must be moved to the same destination package.

Prefer clusters whose classes have strong internal relationships and many package-private interactions with each other.

Avoid moving highly central parser/state-machine classes alone.

Avoid selecting clusters that would require exposing many package-private members from classes that remain in the original package.

Each block must contain:
- optionally one CREATE_PACKAGE operation;
- two to four MOVE_CLASS operations;
- no UPDATE_VISIBILITY operation. UPDATE_VISIBILITY will be added automatically later.

Do not create one block per class.

Do not move all package classes in one block.

Prefer small cohesive clusters that can compile after limited visibility updates.

Only top-level classes count toward cluster size and MOVE_CLASS operations. Inner and nested classes move implicitly with their enclosing class.

# PACKAGE RULES
- Move classes only from the TARGET PACKAGE to a subpackage of the TARGET PACKAGE.
- All moved classes must use the same destination package.
- Do not move classes to unrelated packages.
- Do not introduce facades.
- API changes are allowed.

# BLOCK RULES
- The plan must contain exactly ONE block.
- This single block represents the whole selected cluster.
- The block must contain 2 to 4 MOVE_CLASS operations.
- All MOVE_CLASS operations must move classes to the same destination package.
- The block may include one CREATE_PACKAGE operation before the MOVE_CLASS operations.
- The block files list must include the original source file path of every moved class.
- Do not create one block per class.
- Do not split the selected cluster across multiple blocks.
- Do not update external files in the plan; OpenRewrite will handle references/imports later.
- The executor will handle minimal package-private visibility changes in related internal files.

# ALLOWED OPS
CREATE_PACKAGE, MOVE_CLASS, ADD_OR_UPDATE_IMPORTS, UPDATE_CALL_SITES, UPDATE_VISIBILITY, NO_OP.

# OUTPUT
Return ONLY valid JSON.

{
  "smell_type": "<copied from input>",
  "target_level": "package",
  "target": "<target_name from input>",
  "selected_cluster": [
    "<class FQN>"
  ],
  "destination_package": "<new subpackage FQN>",
  "cluster_reason": "<why this cluster is cohesive and relatively safe>",
  "risk": "low|medium|high",
  "blocks": [
    {
      "id": 1,
      "goal": "Move one class from the selected cluster.",
      "files": [
        "<source file path from target_files>"
      ],
      "ops": [
        {
          "op": "CREATE_PACKAGE",
          "inputs": [],
          "outputs": ["<destination package FQN>"],
          "details": "Create the destination subpackage if it does not exist.",
          "risk": "low",
          "api_change": false
        },
        {
          "op": "MOVE_CLASS",
          "inputs": ["<old class FQN>"],
          "outputs": ["<new class FQN>"],
          "details": "Move this class to the destination package.",
          "risk": "low|medium|high",
          "api_change": true
        }
      ]
    }
  ]
}

# INPUT
```json
{
  "smell": "God Component",
  "target_type": "package",
  "target_name": "org.apache.accumulo.core.fate.zookeeper",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261019_151154_GC__org_apache_accumulo_core_fate_zookeeper/run_004/planner/designite",
    "smells_csv": "ArchitectureSmells.csv",
    "target_has_smell": true
  },
  "target_source_root": "core/src/main/java",
  "target_files": [
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/DistributedReadWriteLock.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/FateLock.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/MetaFateStore.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/ZooReader.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/ZooReaderWriter.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/ZooReservation.java",
    "core/src/main/java/org/apache/accumulo/core/fate/zookeeper/ZooUtil.java"
  ],
  "internal_deps": [
    [
      "org.apache.accumulo.core.fate.zookeeper.FateLock",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReservation",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ]
  ],
  "incoming_deps": [
    [
      "org.apache.accumulo.gc.GCRun",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.core.lock.ServiceLock",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.lock.ServiceLock",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.compactor.Compactor",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.clientImpl.ClientContext",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.fate.FateStore.FateReservation",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.util.ChangeSecret",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.security.delegation.ZooAuthenticationKeyWatcher",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.manager.ManagerClientServiceHandler",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.monitor.Monitor",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.tableOps.availability.LockTable",
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock"
    ],
    [
      "org.apache.accumulo.server.util.DumpZookeeper",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.util.checkCommand.TableLocksCheckRunner",
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore"
    ],
    [
      "org.apache.accumulo.server.init.Initialize",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.tserver.TabletServer",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.store.impl.ZooPropLoader",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.MockServerContext",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.fate.user.UserFateStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.compaction.coordinator.CompactionCoordinator",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.tableOps.rename.RenameTable",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.ServerContext",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.tableOps.Utils",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.tableOps.Utils",
      "org.apache.accumulo.core.fate.zookeeper.FateLock"
    ],
    [
      "org.apache.accumulo.manager.tableOps.Utils",
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock"
    ],
    [
      "org.apache.accumulo.manager.tableOps.Utils",
      "org.apache.accumulo.core.fate.zookeeper.ZooReservation"
    ],
    [
      "org.apache.accumulo.core.fate.AbstractFateStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.security.handler.ZKAuthorizor",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.ManagerTime",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.Manager",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.Manager",
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore"
    ],
    [
      "org.apache.accumulo.manager.Manager",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.upgrade.Upgrader11to12",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.constraints.MetadataConstraints",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.conf.store.PropStoreKey",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.clientImpl.ClientInfoImpl",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.util.ZooZap",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.zookeeper.ZooSession",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.zookeeper.ZooSession",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.util.RestoreZookeeper",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.compaction.CompactionConfigStorage",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.security.handler.ZKAuthenticator",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.log.WalStateManager",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.miniclusterImpl.MiniAccumuloClusterImpl",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.util.Admin",
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore"
    ],
    [
      "org.apache.accumulo.server.util.Admin",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.lock.ServiceLockSupport",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.core.util.MonitorUtil",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.manager.state.DeadServerList",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.store.TablePropKey",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.upgrade.Upgrader10to11",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.upgrade.Upgrader10to11",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.ServerInfo",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.fate.FateStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.clientImpl.NamespaceMapping",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.store.SystemPropKey",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.tableOps.delete.PreDeleteTable",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.tableOps.delete.PreDeleteTable",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.manager.tableOps.compact.CompactionDriver",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.security.handler.KerberosAuthenticator",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.util.DeleteZooInstance",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.util.ZooInfoViewer",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.conf.util.ZooInfoViewer",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.security.handler.ZKPermHandler",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.tserver.TabletClientHandler",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.upgrade.Upgrader12to13",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.upgrade.Upgrader12to13",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.util.TabletServerLocks",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.security.delegation.ZooAuthenticationKeyDistributor",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.security.delegation.ZooAuthenticationKeyDistributor",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.util.ServiceStatusCmd",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.manager.tserverOps.ShutdownTServer",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.metadata.ServerAmpleImpl",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.core.fate.AdminUtil",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.core.fate.AdminUtil",
      "org.apache.accumulo.core.fate.zookeeper.FateLock"
    ],
    [
      "org.apache.accumulo.server.tables.TableManager",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.tables.TableManager",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.util.ListInstances",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.util.ListInstances",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.conf.store.impl.ZooPropStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.store.impl.ZooPropStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.server.conf.store.impl.ZooPropStore",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.conf.store.NamespacePropKey",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.core.metadata.schema.RootTabletMetadata",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.init.ZooKeeperInitializer",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.init.ZooKeeperInitializer",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil"
    ],
    [
      "org.apache.accumulo.manager.tableOps.namespace.rename.RenameNamespace",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.conf.util.ZooPropEditor",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader"
    ],
    [
      "org.apache.accumulo.server.util.RestoreZookeeper.Restore",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.server.zookeeper.DistributedWorkQueue",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ],
    [
      "org.apache.accumulo.tserver.ScanServer",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter"
    ]
  ],
  "outgoing_deps": [
    [
      "org.apache.accumulo.core.fate.zookeeper.FateLock",
      "org.apache.accumulo.core.fate.zookeeper.FateLock.FateLockPath"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.FateLock",
      "org.apache.accumulo.core.fate.FateId"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.FateLock",
      "org.apache.accumulo.core.fate.zookeeper.FateLock.FateLockEntry"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.FateLock",
      "org.apache.accumulo.core.fate.zookeeper.FateLock.NodeName"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock",
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.QueueLock"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock",
      "org.apache.accumulo.core.fate.FateId"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock",
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.DistributedLock"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock",
      "org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.LockType"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil",
      "org.apache.accumulo.core.data.InstanceId"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil",
      "org.apache.accumulo.core.zookeeper.ZooSession"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil",
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil.NodeMissingPolicy"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooUtil",
      "org.apache.accumulo.core.Constants"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.zookeeper.ZooSession"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.util.Stat"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader.ZKFunction"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.fate.zookeeper.ZooReader.ZKFunctionMutator"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.util.Retry"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReader",
      "org.apache.accumulo.core.clientImpl.AcceptableThriftTableOperationException"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReservation",
      "org.apache.accumulo.core.fate.FateId"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.FateInstanceType"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.zookeeper.ZooSession"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.FateId"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.FateKey"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore.FateData"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.Repo"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.MetaFateStore",
      "org.apache.accumulo.core.fate.Fate"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter",
      "org.apache.accumulo.core.zookeeper.ZooSession"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter",
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter.Mutator"
    ],
    [
      "org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter",
      "org.apache.accumulo.core.clientImpl.AcceptableThriftTableOperationException"
    ]
  ]
}
```