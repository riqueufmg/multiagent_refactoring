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
  "target_name": "org.apache.accumulo.manager.tableOps.Utils",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261028_162242_HM__org_apache_accumulo_manager_tableOps_Utils/run_002/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java",
  "target_source_root": "server/manager/src/main/java",
  "target_code": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.manager.tableOps;\n\nimport static java.nio.charset.StandardCharsets.UTF_8;\n\nimport java.io.IOException;\nimport java.math.BigInteger;\nimport java.util.Base64;\nimport java.util.NoSuchElementException;\nimport java.util.Objects;\nimport java.util.SortedMap;\nimport java.util.SortedSet;\nimport java.util.TreeMap;\nimport java.util.TreeSet;\nimport java.util.function.Function;\n\nimport org.apache.accumulo.core.Constants;\nimport org.apache.accumulo.core.client.admin.TabletMergeability;\nimport org.apache.accumulo.core.clientImpl.AcceptableThriftTableOperationException;\nimport org.apache.accumulo.core.clientImpl.TableOperationsImpl;\nimport org.apache.accumulo.core.clientImpl.TabletMergeabilityUtil;\nimport org.apache.accumulo.core.clientImpl.thrift.TableOperation;\nimport org.apache.accumulo.core.clientImpl.thrift.TableOperationExceptionType;\nimport org.apache.accumulo.core.data.AbstractId;\nimport org.apache.accumulo.core.data.Key;\nimport org.apache.accumulo.core.data.NamespaceId;\nimport org.apache.accumulo.core.data.PartialKey;\nimport org.apache.accumulo.core.data.TableId;\nimport org.apache.accumulo.core.dataImpl.KeyExtent;\nimport org.apache.accumulo.core.fate.FateId;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.DistributedLock;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.LockType;\nimport org.apache.accumulo.core.fate.zookeeper.FateLock;\nimport org.apache.accumulo.core.fate.zookeeper.LockRange;\nimport org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter;\nimport org.apache.accumulo.core.fate.zookeeper.ZooReservation;\nimport org.apache.accumulo.core.metadata.schema.Ample;\nimport org.apache.accumulo.core.metadata.schema.TabletMetadata;\nimport org.apache.accumulo.manager.Manager;\nimport org.apache.accumulo.server.ServerContext;\nimport org.apache.hadoop.fs.FileSystem;\nimport org.apache.hadoop.fs.Path;\nimport org.apache.hadoop.io.Text;\nimport org.apache.zookeeper.KeeperException;\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\nimport com.google.common.base.Preconditions;\nimport com.google.common.collect.MoreCollectors;\n\npublic class Utils {\n  private static final byte[] ZERO_BYTE = {'0'};\n  private static final Logger log = LoggerFactory.getLogger(Utils.class);\n\n  public static <T extends AbstractId<T>> T getNextId(String name, ServerContext context,\n      Function<String,T> newIdFunction) throws AcceptableThriftTableOperationException {\n    try {\n      ZooReaderWriter zoo = context.getZooSession().asReaderWriter();\n      byte[] nid = zoo.mutateOrCreate(Constants.ZTABLES, ZERO_BYTE, currentValue -> {\n        BigInteger nextId = new BigInteger(new String(currentValue, UTF_8), Character.MAX_RADIX);\n        nextId = nextId.add(BigInteger.ONE);\n        return nextId.toString(Character.MAX_RADIX).getBytes(UTF_8);\n      });\n      return newIdFunction.apply(new String(nid, UTF_8));\n    } catch (Exception e1) {\n      log.error(\"Failed to assign id to \" + name, e1);\n      throw new AcceptableThriftTableOperationException(null, name, TableOperation.CREATE,\n          TableOperationExceptionType.OTHER, e1.getMessage());\n    }\n  }\n\n  private static KeyExtent findContaining(Ample ample, TableId tableId, Text row) {\n    Objects.requireNonNull(row);\n    try (var tablets = ample.readTablets().forTable(tableId).overlapping(row, true, row)\n        .fetch(TabletMetadata.ColumnType.PREV_ROW).build()) {\n      return tablets.stream().collect(MoreCollectors.onlyElement()).getExtent();\n    }\n  }\n\n  /**\n   * Widen a range to the greatest table split that is before the range and least table split that\n   * is after the range.\n   */\n  public static KeyExtent widen(Ample ample, KeyExtent extent) {\n    Text prevRowOfStartRowTablet = extent.prevEndRow();\n    Text endRowOfEndRowTablet = extent.endRow();\n\n    if (extent.prevEndRow() != null) {\n      // The startRow is not inclusive, so do not want to find the tablet containing startRow but\n      // instead find the tablet that contains the next possible row after startRow\n      Text nextPossibleRow = new Key(extent.prevEndRow()).followingKey(PartialKey.ROW).getRow();\n      prevRowOfStartRowTablet =\n          findContaining(ample, extent.tableId(), nextPossibleRow).prevEndRow();\n    }\n\n    if (extent.endRow() != null) {\n      // find the tablet containing endRow and use its endRow\n      endRowOfEndRowTablet = findContaining(ample, extent.tableId(), extent.endRow()).endRow();\n    }\n\n    return new KeyExtent(extent.tableId(), endRowOfEndRowTablet, prevRowOfStartRowTablet);\n  }\n\n  public static LockRange widen(Ample ample, TableId tableId, LockRange range, TableOperation op,\n      boolean tableMustExists) throws AcceptableThriftTableOperationException {\n    if (range.isInfinite()) {\n      return range;\n    }\n    try {\n      var wext = widen(ample, new KeyExtent(tableId, range.getEndRow(), range.getStartRow()));\n      return LockRange.of(wext.prevEndRow(), wext.endRow());\n    } catch (NoSuchElementException nse) {\n      if (tableMustExists) {\n        throw new AcceptableThriftTableOperationException(tableId.canonical(), \"\", op,\n            TableOperationExceptionType.NOTFOUND, \"Table does not exist\");\n      } else {\n        log.debug(\"Attempted to widen range {} but no metadata entries found for table {}\", range,\n            tableId);\n        return LockRange.infinite();\n      }\n    }\n\n  }\n\n  public static long reserveTable(Manager env, TableId tableId, FateId fateId, LockType lockType,\n      boolean tableMustExist, TableOperation op) throws Exception {\n    return reserveTable(env, tableId, fateId, lockType, tableMustExist, op, LockRange.infinite());\n  }\n\n  public static long reserveTable(Manager env, TableId tableId, FateId fateId, LockType lockType,\n      boolean tableMustExist, TableOperation op, final LockRange range) throws Exception {\n    final LockRange widenedRange;\n\n    boolean shouldWiden = lockType == LockType.WRITE || op == TableOperation.COMPACT;\n\n    if (shouldWiden) {\n      /*\n       * Write locks are widened to table split points to avoid non-overlapping ranges operating on\n       * the same tablet. For example assume a table has splits at c,e and two fate operations need\n       * write locks on ranges (a1,c2] and (d1,d9]. The fate ranges do not overlap, however both\n       * will operate on the tablet (c,e]. When the ranges are widened, (a1,c2] turns into (null,e]\n       * and (d1,d9] turns into (c,e]. The widened ranges for the fate operations overlap which\n       * prevents both from operating on the same tablet.\n       *\n       * Widening is done for write locks because those need to work on mutually exclusive sets of\n       * tablets w/ other write or read locks. Read locks do not need to be mutually exclusive w/\n       * each other and it does not matter if they operate on the same tablet so widening is not\n       * needed for that case. Widening write locks is sufficient for detecting overlap w/ any\n       * tablets that read locks need to use. For example if a write locks is obtained on (a1,c2]\n       * and it widens to (null,e] then a read lock on (d1,d9] would overlap with the widened range.\n       *\n       * Mostly widening for write locks is nice because fate operations that get read locks are\n       * probably more frequent. So the work of widening is not done on most fate operations. Also\n       * widening an infinite range is a quick operation, so create/delete table will not be slowed\n       * down by widening.\n       *\n       * Widening is done for compactions because those operations widen their range.\n       */\n      widenedRange = widen(env.getContext().getAmple(), tableId, range, op, tableMustExist);\n      log.debug(\"{} widened write lock range from {} to {}\", fateId, range, widenedRange);\n    } else {\n      widenedRange = range;\n    }\n\n    var lock = getLock(env.getContext(), tableId, fateId, lockType, widenedRange);\n    if (shouldWiden && !widenedRange.equals(lock.getRange())) {\n      // It is possible the range changed since the lock entry was created. Pre existing locks are\n      // found using the fate id and could have a different range.\n      lock.unlock();\n      // This should be a rare event, log at info in case it happens a lot.\n      log.info(\n          \"{} widened range {} differs from existing lock range {}, deleted lock and will retry\",\n          fateId, widenedRange, lock.getRange());\n      return 100;\n    } else if (lockType == LockType.READ) {\n      // Not expecting the lock range on a read lock to change.\n      Preconditions.checkState(widenedRange.equals(lock.getRange()));\n    }\n\n    if (lock.tryLock()) {\n      if (shouldWiden) {\n        // Now that table lock is acquired see if the range still widens to the same thing. If not\n        // it means the table splits changed so release the lock and try again later. The table\n        // splits in this range can not change once the lock is acquired, so this recheck is done\n        // after getting the lock.\n        var widenedRange2 = widen(env.getContext().getAmple(), tableId, range, op, tableMustExist);\n        if (!widenedRange.equals(widenedRange2)) {\n          lock.unlock();\n          log.info(\n              \"{} widened range {} changed to {} after acquiring lock, deleted lock and will retry\",\n              fateId, widenedRange, widenedRange2);\n          return 100;\n        }\n      }\n\n      if (tableMustExist) {\n        ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n        if (!zk.exists(Constants.ZTABLES + \"/\" + tableId)) {\n          throw new AcceptableThriftTableOperationException(tableId.canonical(), \"\", op,\n              TableOperationExceptionType.NOTFOUND, \"Table does not exist\");\n        }\n      }\n\n      if (widenedRange.equals(range)) {\n        log.info(\"table {} {} locked for {} operation: {} range:{}\", tableId, fateId, lockType, op,\n            range);\n      } else {\n        log.info(\"table {} {} locked for {} operation: {} range:{} widenedRange:{}\", tableId,\n            fateId, lockType, op, range, widenedRange);\n      }\n      return 0;\n    } else {\n      return 100;\n    }\n  }\n\n  public static void unreserveTable(Manager env, TableId tableId, FateId fateId,\n      LockType lockType) {\n    getLock(env.getContext(), tableId, fateId, lockType, LockRange.infinite()).unlock();\n    log.info(\"table {} {} unlocked for {}\", tableId, fateId, lockType);\n  }\n\n  public static void unreserveNamespace(Manager env, NamespaceId namespaceId, FateId fateId,\n      LockType lockType) {\n    getLock(env.getContext(), namespaceId, fateId, lockType, LockRange.infinite()).unlock();\n    log.info(\"namespace {} {} unlocked for {}\", namespaceId, fateId, lockType);\n  }\n\n  public static long reserveNamespace(Manager env, NamespaceId namespaceId, FateId fateId,\n      LockType lockType, boolean mustExist, TableOperation op) throws Exception {\n    if (getLock(env.getContext(), namespaceId, fateId, lockType, LockRange.infinite()).tryLock()) {\n      if (mustExist) {\n        ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n        if (!zk.exists(Constants.ZNAMESPACES + \"/\" + namespaceId)) {\n          throw new AcceptableThriftTableOperationException(namespaceId.canonical(), \"\", op,\n              TableOperationExceptionType.NAMESPACE_NOTFOUND, \"Namespace does not exist\");\n        }\n      }\n      log.info(\"namespace {} {} locked for {} operation: {}\", namespaceId, fateId, lockType, op);\n      return 0;\n    } else {\n      return 100;\n    }\n  }\n\n  public static long reserveHdfsDirectory(Manager env, String directory, FateId fateId)\n      throws KeeperException, InterruptedException {\n\n    ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n\n    if (ZooReservation.attempt(zk, Constants.ZHDFS_RESERVATIONS + \"/\"\n        + Base64.getEncoder().encodeToString(directory.getBytes(UTF_8)), fateId, \"\")) {\n      log.trace(\"{} reserved bulk dir {}\", fateId, directory);\n      return 0;\n    } else {\n      log.trace(\"{} could not reserve bulk dir {} that is already reserved\", fateId, directory);\n      return 50;\n    }\n  }\n\n  public static void unreserveHdfsDirectory(Manager env, String directory, FateId fateId)\n      throws KeeperException, InterruptedException {\n    ZooReservation.release(env.getContext().getZooSession().asReaderWriter(),\n        Constants.ZHDFS_RESERVATIONS + \"/\"\n            + Base64.getEncoder().encodeToString(directory.getBytes(UTF_8)),\n        fateId);\n    log.trace(\"{} unreserved bulk dir {}\", fateId, directory);\n  }\n\n  private static DistributedLock getLock(ServerContext context, AbstractId<?> id, FateId fateId,\n      LockType lockType, LockRange range) {\n    FateLock qlock = new FateLock(context.getZooSession().asReaderWriter(),\n        FateLock.path(Constants.ZTABLE_LOCKS + \"/\" + id.canonical()));\n    DistributedLock lock = DistributedReadWriteLock.recoverLock(qlock, fateId);\n    if (lock != null) {\n\n      // Validate the recovered lock type\n      if (lock.getType() != lockType) {\n        throw new IllegalStateException(\n            \"Unexpected lock type \" + lock.getType() + \" recovered for transaction \" + fateId\n                + \" on object \" + id + \". Expected \" + lockType + \" lock instead.\");\n      }\n    } else {\n      DistributedReadWriteLock locker = new DistributedReadWriteLock(qlock, fateId, range);\n      lock = switch (lockType) {\n        case WRITE -> locker.writeLock();\n        case READ -> locker.readLock();\n      };\n    }\n    return lock;\n  }\n\n  public static DistributedLock getReadLock(Manager env, AbstractId<?> id, FateId fateId,\n      LockRange range) {\n    return Utils.getLock(env.getContext(), id, fateId, LockType.READ, range);\n  }\n\n  /**\n   * Given a fully-qualified Path and a flag indicating if the file info is base64 encoded or not,\n   * retrieve the data from a file on the file system. It is assumed that the file is textual and\n   * not binary data.\n   *\n   * @param path the fully-qualified path\n   */\n  public static SortedSet<Text> getSortedSetFromFile(Manager manager, Path path, boolean encoded)\n      throws IOException {\n    FileSystem fs = path.getFileSystem(manager.getContext().getHadoopConf());\n    var data = new TreeSet<Text>();\n    try (var file = new java.util.Scanner(fs.open(path), UTF_8)) {\n      while (file.hasNextLine()) {\n        String line = file.nextLine();\n        data.add(encoded ? new Text(Base64.getDecoder().decode(line)) : new Text(line));\n      }\n    }\n    return data;\n  }\n\n  public static SortedMap<Text,TabletMergeability> getSortedSplitsFromFile(ServerContext ctx,\n      Path path) throws IOException {\n    FileSystem fs = path.getFileSystem(ctx.getHadoopConf());\n    var data = new TreeMap<Text,TabletMergeability>();\n    try (var file = new java.util.Scanner(fs.open(path), UTF_8)) {\n      while (file.hasNextLine()) {\n        String line = file.nextLine();\n        log.trace(\"split line: {}\", line);\n        TableOperationsImpl.SplitMergeability splitTm = TabletMergeabilityUtil.decode(line);\n        data.put(splitTm.split(), splitTm.mergeability());\n      }\n    }\n    return data;\n  }\n\n}\n",
  "observed_external_calls": {
    "Base64": [
      "getDecoder",
      "getEncoder"
    ],
    "DistributedReadWriteLock": [
      "recoverLock"
    ],
    "FateLock": [
      "path"
    ],
    "LockRange": [
      "infinite",
      "of"
    ],
    "LoggerFactory": [
      "getLogger"
    ],
    "MoreCollectors": [
      "onlyElement"
    ],
    "Objects": [
      "requireNonNull"
    ],
    "Preconditions": [
      "checkState"
    ],
    "TabletMergeabilityUtil": [
      "decode"
    ],
    "Utils": [
      "getLock"
    ],
    "ZooReservation": [
      "attempt",
      "release"
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
