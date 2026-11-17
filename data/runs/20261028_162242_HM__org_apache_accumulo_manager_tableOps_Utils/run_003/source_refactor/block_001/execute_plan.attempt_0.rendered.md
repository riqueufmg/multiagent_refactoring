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
    "target_name": "org.apache.accumulo.manager.tableOps.Utils"
  },
  "block": {
    "id": 1,
    "goal": "Extract the cohesive tablet-range widening responsibility while preserving the public Utils.widen methods as compatibility wrappers.",
    "files": [
      "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java",
      "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/UtilsRangeWidening.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.apache.accumulo.manager.tableOps.Utils",
          "org.apache.accumulo.manager.tableOps.UtilsRangeWidening"
        ],
        "outputs": [
          "org.apache.accumulo.manager.tableOps.UtilsRangeWidening"
        ],
        "details": "Move findContaining(org.apache.accumulo.core.metadata.schema.Ample, org.apache.accumulo.core.data.TableId, org.apache.hadoop.io.Text) and the two widen methods' implementation into UtilsRangeWidening. Keep Utils.widen(org.apache.accumulo.core.metadata.schema.Ample, org.apache.accumulo.core.dataImpl.KeyExtent) and Utils.widen(org.apache.accumulo.core.metadata.schema.Ample, org.apache.accumulo.core.data.TableId, org.apache.accumulo.core.fate.zookeeper.LockRange, org.apache.accumulo.core.clientImpl.thrift.TableOperation, boolean) with their existing signatures and delegate to UtilsRangeWidening. This removes Utils's direct references to org.apache.accumulo.core.data.Key, org.apache.accumulo.core.data.PartialKey, java.util.Objects, and com.google.common.collect.MoreCollectors. The target gains only the new UtilsRangeWidening dependency, for an expected net Fan-Out reduction of three removed dependencies minus one introduced dependency, or two. org.apache.accumulo.core.dataImpl.KeyExtent, org.apache.accumulo.core.metadata.schema.Ample, org.apache.accumulo.core.fate.zookeeper.LockRange, org.apache.hadoop.io.Text, and related public signature dependencies remain and are not counted as removed.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java",
          "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/UtilsRangeWidening.java"
        ],
        "outputs": [
          "Updated imports for the moved widening implementation and its compatibility wrappers"
        ],
        "details": "Remove imports used only by the moved implementation from Utils and add the UtilsRangeWidening reference. Preserve imports required by the existing public method signatures and by other Utils methods.",
        "risk": "low"
      }
    ]
  },
  "allowed_files": [
    "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java",
    "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/UtilsRangeWidening.java"
  ],
  "executor_existing_files": [
    "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java"
  ],
  "executor_new_files": [
    "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/UtilsRangeWidening.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/Utils.java",
      "exists": "true",
      "content": "/*\n * Licensed to the Apache Software Foundation (ASF) under one\n * or more contributor license agreements.  See the NOTICE file\n * distributed with this work for additional information\n * regarding copyright ownership.  The ASF licenses this file\n * to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance\n * with the License.  You may obtain a copy of the License at\n *\n *   https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing,\n * software distributed under the License is distributed on an\n * \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n * KIND, either express or implied.  See the License for the\n * specific language governing permissions and limitations\n * under the License.\n */\npackage org.apache.accumulo.manager.tableOps;\n\nimport static java.nio.charset.StandardCharsets.UTF_8;\n\nimport java.io.IOException;\nimport java.math.BigInteger;\nimport java.util.Base64;\nimport java.util.NoSuchElementException;\nimport java.util.Objects;\nimport java.util.SortedMap;\nimport java.util.SortedSet;\nimport java.util.function.Function;\n\nimport org.apache.accumulo.core.Constants;\nimport org.apache.accumulo.core.client.admin.TabletMergeability;\nimport org.apache.accumulo.core.clientImpl.AcceptableThriftTableOperationException;\nimport org.apache.accumulo.core.clientImpl.thrift.TableOperation;\nimport org.apache.accumulo.core.clientImpl.thrift.TableOperationExceptionType;\nimport org.apache.accumulo.core.data.AbstractId;\nimport org.apache.accumulo.core.data.Key;\nimport org.apache.accumulo.core.data.NamespaceId;\nimport org.apache.accumulo.core.data.PartialKey;\nimport org.apache.accumulo.core.data.TableId;\nimport org.apache.accumulo.core.dataImpl.KeyExtent;\nimport org.apache.accumulo.core.fate.FateId;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.DistributedLock;\nimport org.apache.accumulo.core.fate.zookeeper.DistributedReadWriteLock.LockType;\nimport org.apache.accumulo.core.fate.zookeeper.FateLock;\nimport org.apache.accumulo.core.fate.zookeeper.LockRange;\nimport org.apache.accumulo.core.fate.zookeeper.ZooReaderWriter;\nimport org.apache.accumulo.core.fate.zookeeper.ZooReservation;\nimport org.apache.accumulo.core.metadata.schema.Ample;\nimport org.apache.accumulo.core.metadata.schema.TabletMetadata;\nimport org.apache.accumulo.manager.Manager;\nimport org.apache.accumulo.server.ServerContext;\nimport org.apache.hadoop.fs.Path;\nimport org.apache.hadoop.io.Text;\nimport org.apache.zookeeper.KeeperException;\nimport org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n\nimport com.google.common.base.Preconditions;\nimport com.google.common.collect.MoreCollectors;\n\npublic class Utils {\n  private static final byte[] ZERO_BYTE = {'0'};\n  private static final Logger log = LoggerFactory.getLogger(Utils.class);\n\n  public static <T extends AbstractId<T>> T getNextId(String name, ServerContext context,\n      Function<String,T> newIdFunction) throws AcceptableThriftTableOperationException {\n    try {\n      ZooReaderWriter zoo = context.getZooSession().asReaderWriter();\n      byte[] nid = zoo.mutateOrCreate(Constants.ZTABLES, ZERO_BYTE, currentValue -> {\n        BigInteger nextId = new BigInteger(new String(currentValue, UTF_8), Character.MAX_RADIX);\n        nextId = nextId.add(BigInteger.ONE);\n        return nextId.toString(Character.MAX_RADIX).getBytes(UTF_8);\n      });\n      return newIdFunction.apply(new String(nid, UTF_8));\n    } catch (Exception e1) {\n      log.error(\"Failed to assign id to \" + name, e1);\n      throw new AcceptableThriftTableOperationException(null, name, TableOperation.CREATE,\n          TableOperationExceptionType.OTHER, e1.getMessage());\n    }\n  }\n\n  private static KeyExtent findContaining(Ample ample, TableId tableId, Text row) {\n    Objects.requireNonNull(row);\n    try (var tablets = ample.readTablets().forTable(tableId).overlapping(row, true, row)\n        .fetch(TabletMetadata.ColumnType.PREV_ROW).build()) {\n      return tablets.stream().collect(MoreCollectors.onlyElement()).getExtent();\n    }\n  }\n\n  /**\n   * Widen a range to the greatest table split that is before the range and least table split that\n   * is after the range.\n   */\n  public static KeyExtent widen(Ample ample, KeyExtent extent) {\n    Text prevRowOfStartRowTablet = extent.prevEndRow();\n    Text endRowOfEndRowTablet = extent.endRow();\n\n    if (extent.prevEndRow() != null) {\n      Text nextPossibleRow = new Key(extent.prevEndRow()).followingKey(PartialKey.ROW).getRow();\n      prevRowOfStartRowTablet =\n          findContaining(ample, extent.tableId(), nextPossibleRow).prevEndRow();\n    }\n\n    if (extent.endRow() != null) {\n      endRowOfEndRowTablet = findContaining(ample, extent.tableId(), extent.endRow()).endRow();\n    }\n\n    return new KeyExtent(extent.tableId(), endRowOfEndRowTablet, prevRowOfStartRowTablet);\n  }\n\n  public static LockRange widen(Ample ample, TableId tableId, LockRange range, TableOperation op,\n      boolean tableMustExists) throws AcceptableThriftTableOperationException {\n    if (range.isInfinite()) {\n      return range;\n    }\n    try {\n      var wext = widen(ample, new KeyExtent(tableId, range.getEndRow(), range.getStartRow()));\n      return LockRange.of(wext.prevEndRow(), wext.endRow());\n    } catch (NoSuchElementException nse) {\n      if (tableMustExists) {\n        throw new AcceptableThriftTableOperationException(tableId.canonical(), \"\", op,\n            TableOperationExceptionType.NOTFOUND, \"Table does not exist\");\n      } else {\n        log.debug(\"Attempted to widen range {} but no metadata entries found for table {}\", range,\n            tableId);\n        return LockRange.infinite();\n      }\n    }\n  }\n\n  public static long reserveTable(Manager env, TableId tableId, FateId fateId, LockType lockType,\n      boolean tableMustExist, TableOperation op) throws Exception {\n    return reserveTable(env, tableId, fateId, lockType, tableMustExist, op, LockRange.infinite());\n  }\n\n  public static long reserveTable(Manager env, TableId tableId, FateId fateId, LockType lockType,\n      boolean tableMustExist, TableOperation op, final LockRange range) throws Exception {\n    final LockRange widenedRange;\n    boolean shouldWiden = lockType == LockType.WRITE || op == TableOperation.COMPACT;\n\n    if (shouldWiden) {\n      widenedRange = widen(env.getContext().getAmple(), tableId, range, op, tableMustExist);\n      log.debug(\"{} widened write lock range from {} to {}\", fateId, range, widenedRange);\n    } else {\n      widenedRange = range;\n    }\n\n    var lock = getLock(env.getContext(), tableId, fateId, lockType, widenedRange);\n    if (shouldWiden && !widenedRange.equals(lock.getRange())) {\n      lock.unlock();\n      log.info(\n          \"{} widened range {} differs from existing lock range {}, deleted lock and will retry\",\n          fateId, widenedRange, lock.getRange());\n      return 100;\n    } else if (lockType == LockType.READ) {\n      Preconditions.checkState(widenedRange.equals(lock.getRange()));\n    }\n\n    if (lock.tryLock()) {\n      if (shouldWiden) {\n        var widenedRange2 = widen(env.getContext().getAmple(), tableId, range, op, tableMustExist);\n        if (!widenedRange.equals(widenedRange2)) {\n          lock.unlock();\n          log.info(\n              \"{} widened range {} changed to {} after acquiring lock, deleted lock and will retry\",\n              fateId, widenedRange, widenedRange2);\n          return 100;\n        }\n      }\n\n      if (tableMustExist) {\n        ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n        if (!zk.exists(Constants.ZTABLES + \"/\" + tableId)) {\n          throw new AcceptableThriftTableOperationException(tableId.canonical(), \"\", op,\n              TableOperationExceptionType.NOTFOUND, \"Table does not exist\");\n        }\n      }\n\n      if (widenedRange.equals(range)) {\n        log.info(\"table {} {} locked for {} operation: {} range:{}\", tableId, fateId, lockType, op,\n            range);\n      } else {\n        log.info(\"table {} {} locked for {} operation: {} range:{} widenedRange:{}\", tableId,\n            fateId, lockType, op, range, widenedRange);\n      }\n      return 0;\n    } else {\n      return 100;\n    }\n  }\n\n  public static void unreserveTable(Manager env, TableId tableId, FateId fateId,\n      LockType lockType) {\n    getLock(env.getContext(), tableId, fateId, lockType, LockRange.infinite()).unlock();\n    log.info(\"table {} {} unlocked for {}\", tableId, fateId, lockType);\n  }\n\n  public static void unreserveNamespace(Manager env, NamespaceId namespaceId, FateId fateId,\n      LockType lockType) {\n    getLock(env.getContext(), namespaceId, fateId, lockType, LockRange.infinite()).unlock();\n    log.info(\"namespace {} {} unlocked for {}\", namespaceId, fateId, lockType);\n  }\n\n  public static long reserveNamespace(Manager env, NamespaceId namespaceId, FateId fateId,\n      LockType lockType, boolean mustExist, TableOperation op) throws Exception {\n    if (getLock(env.getContext(), namespaceId, fateId, lockType, LockRange.infinite()).tryLock()) {\n      if (mustExist) {\n        ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n        if (!zk.exists(Constants.ZNAMESPACES + \"/\" + namespaceId)) {\n          throw new AcceptableThriftTableOperationException(namespaceId.canonical(), \"\", op,\n              TableOperationExceptionType.NAMESPACE_NOTFOUND, \"Namespace does not exist\");\n        }\n      }\n      log.info(\"namespace {} {} locked for {} operation: {}\", namespaceId, fateId, lockType, op);\n      return 0;\n    } else {\n      return 100;\n    }\n  }\n\n  public static long reserveHdfsDirectory(Manager env, String directory, FateId fateId)\n      throws KeeperException, InterruptedException {\n    ZooReaderWriter zk = env.getContext().getZooSession().asReaderWriter();\n    if (ZooReservation.attempt(zk, Constants.ZHDFS_RESERVATIONS + \"/\"\n        + Base64.getEncoder().encodeToString(directory.getBytes(UTF_8)), fateId, \"\")) {\n      log.trace(\"{} reserved bulk dir {}\", fateId, directory);\n      return 0;\n    } else {\n      log.trace(\"{} could not reserve bulk dir {} that is already reserved\", fateId, directory);\n      return 50;\n    }\n  }\n\n  public static void unreserveHdfsDirectory(Manager env, String directory, FateId fateId)\n      throws KeeperException, InterruptedException {\n    ZooReservation.release(env.getContext().getZooSession().asReaderWriter(),\n        Constants.ZHDFS_RESERVATIONS + \"/\"\n            + Base64.getEncoder().encodeToString(directory.getBytes(UTF_8)),\n        fateId);\n    log.trace(\"{} unreserved bulk dir {}\", fateId, directory);\n  }\n\n  private static DistributedLock getLock(ServerContext context, AbstractId<?> id, FateId fateId,\n      LockType lockType, LockRange range) {\n    FateLock qlock = new FateLock(context.getZooSession().asReaderWriter(),\n        FateLock.path(Constants.ZTABLE_LOCKS + \"/\" + id.canonical()));\n    DistributedLock lock = DistributedReadWriteLock.recoverLock(qlock, fateId);\n    if (lock != null) {\n      if (lock.getType() != lockType) {\n        throw new IllegalStateException(\n            \"Unexpected lock type \" + lock.getType() + \" recovered for transaction \" + fateId\n                + \" on object \" + id + \". Expected \" + lockType + \" lock instead.\");\n      }\n    } else {\n      DistributedReadWriteLock locker = new DistributedReadWriteLock(qlock, fateId, range);\n      lock = switch (lockType) {\n        case WRITE -> locker.writeLock();\n        case READ -> locker.readLock();\n      };\n    }\n    return lock;\n  }\n\n  public static DistributedLock getReadLock(Manager env, AbstractId<?> id, FateId fateId,\n      LockRange range) {\n    return Utils.getLock(env.getContext(), id, fateId, LockType.READ, range);\n  }\n\n  public static SortedSet<Text> getSortedSetFromFile(Manager manager, Path path, boolean encoded)\n      throws IOException {\n    return UtilsFileParser.getSortedSetFromFile(manager, path, encoded);\n  }\n\n  public static SortedMap<Text,TabletMergeability> getSortedSplitsFromFile(ServerContext ctx,\n      Path path) throws IOException {\n    return UtilsFileParser.getSortedSplitsFromFile(ctx, path);\n  }\n\n}\n"
    },
    {
      "path": "server/manager/src/main/java/org/apache/accumulo/manager/tableOps/UtilsRangeWidening.java",
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
