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
- ADD_OR_UPDATE_IMPORTS
- CREATE_PACKAGE
- DEPENDENCY_INVERSION
- EXTRACT_CLASS
- EXTRACT_INTERFACE
- INTRODUCE_FACADE
- MOVE_CLASS
- MOVE_FIELD
- MOVE_METHOD
- REPLACE_DEPENDENCY
- UPDATE_CALL_SITES

## INPUT
{
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "com.gmail.nossr50.util.Misc",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261014_144405_IM__com_gmail_nossr50_util_Misc/run_005/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "src/main/java/com/gmail/nossr50/util/Misc.java",
  "target_source_root": "src/main/java",
  "target_code": "package com.gmail.nossr50.util;\n\nimport com.gmail.nossr50.api.ItemSpawnReason;\nimport com.gmail.nossr50.datatypes.player.McMMOPlayer;\nimport com.gmail.nossr50.mcMMO;\nimport com.gmail.nossr50.runnables.player.PlayerProfileLoadingTask;\nimport com.gmail.nossr50.util.player.UserManager;\nimport com.google.common.collect.ImmutableSet;\nimport org.bukkit.Location;\nimport org.bukkit.block.BlockState;\nimport org.bukkit.entity.EntityType;\nimport org.bukkit.entity.ExperienceOrb;\nimport org.bukkit.entity.Item;\nimport org.bukkit.entity.Player;\nimport org.bukkit.inventory.ItemStack;\nimport org.jetbrains.annotations.NotNull;\nimport org.jetbrains.annotations.Nullable;\n\nimport java.util.Collection;\nimport java.util.Locale;\nimport java.util.Random;\nimport java.util.Set;\nimport java.util.function.Predicate;\n\npublic final class Misc {\n    private static final @NotNull Random random = new Random();\n\n    public static final int TIME_CONVERSION_FACTOR = 1000;\n    public static final int TICK_CONVERSION_FACTOR = 20;\n    public static final int PLAYER_RESPAWN_COOLDOWN_SECONDS = 5;\n    public static final double SKILL_MESSAGE_MAX_SENDING_DISTANCE = 10.0;\n\n    public static final @NotNull Set<String> modNames = ImmutableSet.of(\"LOTR\", \"BUILDCRAFT\", \"ENDERIO\", \"ENHANCEDBIOMES\", \"IC2\", \"METALLURGY\", \"FORESTRY\", \"GALACTICRAFT\", \"RAILCRAFT\", \"TWILIGHTFOREST\", \"THAUMCRAFT\", \"GRAVESTONEMOD\", \"GROWTHCRAFT\", \"ARCTICMOBS\", \"DEMONMOBS\", \"INFERNOMOBS\", \"SWAMPMOBS\", \"MARICULTURE\", \"MINESTRAPPOLATION\");\n\n    private Misc() {\n    }\n\n    public static boolean isNPCEntityExcludingVillagers(@NotNull org.bukkit.entity.Entity entity) {\n        return EntityUtil.isNPCEntityExcludingVillagers(entity);\n    }\n\n    public static boolean isNPCIncludingVillagers(@Nullable org.bukkit.entity.Entity entity) {\n        return EntityUtil.isNPCIncludingVillagers(entity);\n    }\n\n    public static boolean isNear(@NotNull Location first, @NotNull Location second, double maxDistance) {\n        return first.getWorld() == second.getWorld() && (first.distanceSquared(second) < maxDistance * maxDistance || maxDistance == 0);\n    }\n\n    public static Location getBlockCenter(BlockState blockState) {\n        return blockState.getLocation().add(0.5, 0.5, 0.5);\n    }\n\n    public static void profileCleanup(@NotNull String playerName) {\n        Player player = mcMMO.p.getServer().getPlayerExact(playerName);\n        if (player != null) {\n            UserManager.remove(player);\n            mcMMO.p.getFoliaLib().getImpl().runLaterAsync(new PlayerProfileLoadingTask(player), 1);\n        }\n    }\n\n    public static void printProgress(int convertedUsers, int progressInterval, long startMillis) {\n        if (convertedUsers % progressInterval == 0) {\n            mcMMO.p.getLogger().info(String.format(\"Conversion progress: %d users at %.2f users/second\", convertedUsers, convertedUsers / (double) ((System.currentTimeMillis() - startMillis) / TIME_CONVERSION_FACTOR)));\n        }\n    }\n\n    public static String getModName(@NotNull String materialName) {\n        for (String mod : modNames) {\n            if (materialName.contains(mod)) {\n                return mod;\n            }\n        }\n        String[] materialSplit = materialName.split(\"_\");\n        if (materialSplit.length > 1) {\n            return materialSplit[0].toLowerCase(Locale.ENGLISH);\n        }\n        return \"UnknownMods\";\n    }\n\n    public static Location getLocationOffset(@NotNull Location location, double strength) {\n        double blockX = location.getBlockX();\n        double blockZ = location.getBlockZ();\n        double distance = strength * random.nextDouble();\n        blockX = random.nextBoolean() ? blockX + distance : blockX - distance;\n        distance = strength * random.nextDouble();\n        blockZ = random.nextBoolean() ? blockZ + distance : blockZ - distance;\n        return new Location(location.getWorld(), blockX, location.getY(), blockZ);\n    }\n\n    public static @NotNull Random getRandom() {\n        return random;\n    }\n\n    public static boolean isPartyLeader(@NotNull McMMOPlayer mmoPlayer) {\n        return mmoPlayer.getParty().getLeader().getUniqueId().equals(mmoPlayer.getPlayer().getUniqueId());\n    }\n\n    public static void spawnItemsFromCollection(@NotNull Player player, @NotNull Location location, @NotNull Collection<ItemStack> drops, @NotNull ItemSpawnReason itemSpawnReason) {\n        MiscItemSpawnUtil.spawnItemsFromCollection(player, location, drops, itemSpawnReason);\n    }\n\n    public static void spawnItemsFromCollection(@Nullable Player player, @NotNull Location location, @NotNull Collection<ItemStack> drops, @NotNull ItemSpawnReason itemSpawnReason, int sizeLimit) {\n        MiscItemSpawnUtil.spawnItemsFromCollection(player, location, drops, itemSpawnReason, sizeLimit);\n    }\n\n    public static void spawnItem(@NotNull Collection<ItemStack> potentialItemDrops, @NotNull ItemSpawnReason itemSpawnReason, @NotNull Location spawnLocation, @NotNull Predicate<String> predicate, @NotNull Player player) {\n        MiscItemSpawnUtil.spawnItem(potentialItemDrops, itemSpawnReason, spawnLocation, predicate, player);\n    }\n\n    public static void spawnItem(@NotNull ItemStack potentialItemSpawn, @NotNull ItemSpawnReason itemSpawnReason, @NotNull Location spawnLocation, @NotNull Predicate<String> predicate, @NotNull Player player) {\n        MiscItemSpawnUtil.spawnItem(potentialItemSpawn, itemSpawnReason, spawnLocation, predicate, player);\n    }\n\n    public static void spawnItems(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, int quantity, @NotNull ItemSpawnReason itemSpawnReason) {\n        MiscItemSpawnUtil.spawnItems(player, location, itemStack, quantity, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItem(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, @NotNull ItemSpawnReason itemSpawnReason) {\n        return MiscItemSpawnUtil.spawnItem(player, location, itemStack, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItemNaturally(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, @NotNull ItemSpawnReason itemSpawnReason) {\n        return MiscItemSpawnUtil.spawnItemNaturally(player, location, itemStack, itemSpawnReason);\n    }\n\n    public static void spawnItemsTowardsLocation(@Nullable Player player, @NotNull Location fromLocation, @NotNull Location toLocation, @NotNull ItemStack itemStack, int quantity, double speed, @NotNull ItemSpawnReason itemSpawnReason) {\n        MiscItemSpawnUtil.spawnItemsTowardsLocation(player, fromLocation, toLocation, itemStack, quantity, speed, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItemTowardsLocation(@Nullable Player player, @NotNull Location fromLocation, @NotNull Location toLocation, @NotNull ItemStack itemStack, double speed, @NotNull ItemSpawnReason itemSpawnReason) {\n        return MiscItemSpawnUtil.spawnItemTowardsLocation(player, fromLocation, toLocation, itemStack, speed, itemSpawnReason);\n    }\n\n    public static void spawnExperienceOrb(@NotNull Location location, int experienceValue) {\n        if (location.getWorld() == null) {\n            return;\n        }\n        ExperienceOrb experienceOrb = (ExperienceOrb) location.getWorld().spawnEntity(location, EntityType.EXPERIENCE_ORB);\n        experienceOrb.setExperience(experienceValue);\n    }\n\n    private static class SpawnOrbTask implements Runnable {\n        private final Location location;\n        private int orbExpValue;\n\n        private SpawnOrbTask(Location location, int orbExpValue) {\n            this.location = location;\n            this.orbExpValue = orbExpValue;\n        }\n\n        @Override\n        public void run() {\n            if (location == null || location.getWorld() == null) {\n                return;\n            }\n            ExperienceOrb experienceOrb = (ExperienceOrb) location.getWorld().spawnEntity(location, EntityType.EXPERIENCE_ORB);\n            experienceOrb.setExperience(orbExpValue);\n        }\n    }\n}\n"
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