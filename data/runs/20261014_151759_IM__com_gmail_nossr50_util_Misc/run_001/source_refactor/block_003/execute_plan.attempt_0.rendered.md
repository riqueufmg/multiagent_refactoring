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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/mcMMO/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "com.gmail.nossr50.util.Misc"
  },
  "block": {
    "id": 3,
    "goal": "Extract cohesive location, random-offset, and experience-orb utilities from Misc to reduce unrelated general methods and isolate world-related behavior.",
    "files": [
      "src/main/java/com/gmail/nossr50/util/LocationUtil.java",
      "src/main/java/com/gmail/nossr50/util/Misc.java",
      "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "com.gmail.nossr50.util.Misc.isNear(Location, Location, double)",
          "com.gmail.nossr50.util.Misc.getBlockCenter(BlockState)",
          "com.gmail.nossr50.util.Misc.getLocationOffset(Location, double)",
          "com.gmail.nossr50.util.Misc.getRandom()",
          "com.gmail.nossr50.util.Misc.spawnExperienceOrb(Location, int)",
          "com.gmail.nossr50.util.Misc.random"
        ],
        "outputs": [
          "com.gmail.nossr50.util.LocationUtil"
        ],
        "details": "Create LocationUtil in com.gmail.nossr50.util and move the listed location and world utility methods and the random field into it. Preserve static access, random behavior, null/world checks, distance semantics, and experience-orb spawning behavior. Include the required Bukkit, annotation, and java.util.Random imports.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "com.gmail.nossr50.util.Misc.isNear",
          "com.gmail.nossr50.util.Misc.getBlockCenter",
          "com.gmail.nossr50.util.Misc.getLocationOffset",
          "com.gmail.nossr50.util.Misc.getRandom",
          "com.gmail.nossr50.util.Misc.spawnExperienceOrb"
        ],
        "outputs": [
          "All source call sites of the moved location and world utility methods"
        ],
        "details": "Replace calls to the moved methods with calls to the corresponding static methods on LocationUtil. Update direct references to Misc.random only if such references exist.",
        "risk": "medium"
      },
      {
        "op": "ADD_OR_UPDATE_IMPORTS",
        "inputs": [
          "src/main/java/com/gmail/nossr50/util/LocationUtil.java",
          "All files updated by the location utility call-site migration"
        ],
        "outputs": [
          "Compilation-valid imports for LocationUtil and its Bukkit, annotation, and random dependencies"
        ],
        "details": "Remove no-longer-used location, entity, and Random imports from Misc and add LocationUtil imports to migrated callers where required.",
        "risk": "low"
      },
      {
        "op": "UPDATE_TESTS",
        "inputs": [
          "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java"
        ],
        "outputs": [],
        "details": "Update related tests affected by this refactoring block so the configured build command passes. Adjust imports, package references, moved class references, constructors, and assertions only when required. Do not change production behavior through tests.",
        "risk": "medium",
        "api_change": false
      }
    ],
    "test_files": [
      "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java"
    ]
  },
  "allowed_files": [
    "src/main/java/com/gmail/nossr50/util/LocationUtil.java",
    "src/main/java/com/gmail/nossr50/util/Misc.java",
    "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java"
  ],
  "executor_existing_files": [
    "src/main/java/com/gmail/nossr50/util/Misc.java",
    "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java"
  ],
  "executor_new_files": [
    "src/main/java/com/gmail/nossr50/util/LocationUtil.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "src/main/java/com/gmail/nossr50/util/LocationUtil.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "src/main/java/com/gmail/nossr50/util/Misc.java",
      "exists": "true",
      "content": "package com.gmail.nossr50.util;\n\nimport com.gmail.nossr50.api.ItemSpawnReason;\nimport com.gmail.nossr50.datatypes.player.McMMOPlayer;\nimport com.gmail.nossr50.mcMMO;\nimport com.gmail.nossr50.runnables.player.PlayerProfileLoadingTask;\nimport com.gmail.nossr50.util.player.UserManager;\nimport com.google.common.collect.ImmutableSet;\nimport org.bukkit.Location;\nimport org.bukkit.block.BlockState;\nimport org.bukkit.entity.*;\nimport org.bukkit.inventory.ItemStack;\nimport org.jetbrains.annotations.NotNull;\nimport org.jetbrains.annotations.Nullable;\n\nimport java.util.Collection;\nimport java.util.Locale;\nimport java.util.Random;\nimport java.util.Set;\nimport java.util.function.Predicate;\n\npublic final class Misc {\n    private static final @NotNull Random random = new Random();\n\n    public static final int TIME_CONVERSION_FACTOR = 1000;\n    public static final int TICK_CONVERSION_FACTOR = 20;\n\n    public static final int PLAYER_RESPAWN_COOLDOWN_SECONDS = 5;\n    public static final double SKILL_MESSAGE_MAX_SENDING_DISTANCE = 10.0;\n\n    public static final @NotNull Set<String> modNames = ImmutableSet.of(\"LOTR\", \"BUILDCRAFT\", \"ENDERIO\", \"ENHANCEDBIOMES\", \"IC2\", \"METALLURGY\", \"FORESTRY\", \"GALACTICRAFT\", \"RAILCRAFT\", \"TWILIGHTFOREST\", \"THAUMCRAFT\", \"GRAVESTONEMOD\", \"GROWTHCRAFT\", \"ARCTICMOBS\", \"DEMONMOBS\", \"INFERNOMOBS\", \"SWAMPMOBS\", \"MARICULTURE\", \"MINESTRAPPOLATION\");\n\n    private Misc() {}\n\n    public static boolean isNear(@NotNull Location first, @NotNull Location second, double maxDistance) {\n        return (first.getWorld() == second.getWorld()) && (first.distanceSquared(second) < (maxDistance * maxDistance) || maxDistance == 0);\n    }\n\n    public static Location getBlockCenter(BlockState blockState) {\n        return blockState.getLocation().add(0.5, 0.5, 0.5);\n    }\n\n    public static void profileCleanup(@NotNull String playerName) {\n        Player player = mcMMO.p.getServer().getPlayerExact(playerName);\n\n        if (player != null) {\n            UserManager.remove(player);\n            mcMMO.p.getFoliaLib().getImpl().runLaterAsync(new PlayerProfileLoadingTask(player), 1);\n        }\n    }\n\n    public static void printProgress(int convertedUsers, int progressInterval, long startMillis) {\n        if ((convertedUsers % progressInterval) == 0) {\n            mcMMO.p.getLogger().info(String.format(\"Conversion progress: %d users at %.2f users/second\", convertedUsers, convertedUsers / (double) ((System.currentTimeMillis() - startMillis) / TIME_CONVERSION_FACTOR)));\n        }\n    }\n\n    public static String getModName(@NotNull String materialName) {\n        for (String mod : modNames) {\n            if (materialName.contains(mod)) {\n                return mod;\n            }\n        }\n\n        String[] materialSplit = materialName.split(\"_\");\n        if (materialSplit.length > 1) {\n            return materialSplit[0].toLowerCase(Locale.ENGLISH);\n        }\n\n        return \"UnknownMods\";\n    }\n\n    public static Location getLocationOffset(@NotNull Location location, double strength) {\n        double blockX = location.getBlockX();\n        double blockZ = location.getBlockZ();\n\n        double distance = strength * random.nextDouble();\n        blockX = random.nextBoolean() ? blockX + distance : blockX - distance;\n\n        distance = strength * random.nextDouble();\n        blockZ = random.nextBoolean() ? blockZ + distance : blockZ - distance;\n\n        return new Location(location.getWorld(), blockX, location.getY(), blockZ);\n    }\n\n    public static @NotNull Random getRandom() {\n        return random;\n    }\n\n    public static boolean isPartyLeader(@NotNull McMMOPlayer mmoPlayer) {\n        return mmoPlayer.getParty().getLeader().getUniqueId().equals(mmoPlayer.getPlayer().getUniqueId());\n    }\n\n    public static void spawnExperienceOrb(@NotNull Location location, int experienceValue) {\n        if (location.getWorld() == null)\n            return;\n\n        ExperienceOrb experienceOrb = (ExperienceOrb) location.getWorld().spawnEntity(location, EntityType.EXPERIENCE_ORB);\n        experienceOrb.setExperience(experienceValue);\n    }\n\n    public static void spawnItemsFromCollection(@NotNull Player player, @NotNull Location location, @NotNull Collection<ItemStack> drops, @NotNull ItemSpawnReason itemSpawnReason) {\n        ItemSpawnUtil.spawnItemsFromCollection(player, location, drops, itemSpawnReason);\n    }\n\n    public static void spawnItemsFromCollection(@Nullable Player player, @NotNull Location location, @NotNull Collection<ItemStack> drops, @NotNull ItemSpawnReason itemSpawnReason, int sizeLimit) {\n        ItemSpawnUtil.spawnItemsFromCollection(player, location, drops, itemSpawnReason, sizeLimit);\n    }\n\n    public static void spawnItem(@NotNull Collection<ItemStack> potentialItemDrops, @NotNull ItemSpawnReason itemSpawnReason, @NotNull Location spawnLocation, @NotNull Predicate<String> predicate, @NotNull Player player) {\n        ItemSpawnUtil.spawnItem(potentialItemDrops, itemSpawnReason, spawnLocation, predicate, player);\n    }\n\n    public static void spawnItem(@NotNull ItemStack potentialItemSpawn, @NotNull ItemSpawnReason itemSpawnReason, @NotNull Location spawnLocation, @NotNull Predicate<String> predicate, @NotNull Player player) {\n        ItemSpawnUtil.spawnItem(potentialItemSpawn, itemSpawnReason, spawnLocation, predicate, player);\n    }\n\n    public static void spawnItems(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, int quantity, @NotNull ItemSpawnReason itemSpawnReason) {\n        ItemSpawnUtil.spawnItems(player, location, itemStack, quantity, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItem(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, @NotNull ItemSpawnReason itemSpawnReason) {\n        return ItemSpawnUtil.spawnItem(player, location, itemStack, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItemNaturally(@Nullable Player player, @NotNull Location location, @NotNull ItemStack itemStack, @NotNull ItemSpawnReason itemSpawnReason) {\n        return ItemSpawnUtil.spawnItemNaturally(player, location, itemStack, itemSpawnReason);\n    }\n\n    public static void spawnItemsTowardsLocation(@Nullable Player player, @NotNull Location fromLocation, @NotNull Location toLocation, @NotNull ItemStack itemStack, int quantity, double speed, @NotNull ItemSpawnReason itemSpawnReason) {\n        ItemSpawnUtil.spawnItemsTowardsLocation(player, fromLocation, toLocation, itemStack, quantity, speed, itemSpawnReason);\n    }\n\n    public static @Nullable Item spawnItemTowardsLocation(@Nullable Player player, @NotNull Location fromLocation, @NotNull Location toLocation, @NotNull ItemStack itemStack, double speed, @NotNull ItemSpawnReason itemSpawnReason) {\n        return ItemSpawnUtil.spawnItemTowardsLocation(player, fromLocation, toLocation, itemStack, speed, itemSpawnReason);\n    }\n\n    /**\n     * Compatibility delegates for callers not migrated in this refactoring block.\n     */\n    public static boolean isNPCEntityExcludingVillagers(Entity entity) {\n        return NPCUtil.isNPCEntityExcludingVillagers(entity);\n    }\n\n    public static boolean isNPCClassType(Entity entity) {\n        return NPCUtil.isNPCClassType(entity);\n    }\n\n    public static boolean hasNPCMetadataTag(Entity entity) {\n        return NPCUtil.hasNPCMetadataTag(entity);\n    }\n\n    public static boolean isVillager(Entity entity) {\n        return NPCUtil.isVillager(entity);\n    }\n\n    public static boolean isNPCIncludingVillagers(@Nullable Entity entity) {\n        return NPCUtil.isNPCIncludingVillagers(entity);\n    }\n\n    private static class SpawnOrbTask implements Runnable {\n        private final Location location;\n        private int orbExpValue;\n\n        private SpawnOrbTask(Location location, int orbExpValue) {\n            this.location = location;\n            this.orbExpValue = orbExpValue;\n        }\n\n        @Override\n        public void run() {\n            if (location == null || location.getWorld() == null)\n                return;\n\n            ExperienceOrb experienceOrb = (ExperienceOrb) location.getWorld().spawnEntity(location, EntityType.EXPERIENCE_ORB);\n            experienceOrb.setExperience(orbExpValue);\n        }\n    }\n}\n"
    },
    {
      "path": "src/test/java/com/gmail/nossr50/MMOTestEnvironment.java",
      "exists": "true",
      "content": "package com.gmail.nossr50;\n\nimport com.gmail.nossr50.api.exceptions.InvalidSkillException;\nimport com.gmail.nossr50.config.AdvancedConfig;\nimport com.gmail.nossr50.config.ChatConfig;\nimport com.gmail.nossr50.config.GeneralConfig;\nimport com.gmail.nossr50.config.RankConfig;\nimport com.gmail.nossr50.config.experience.ExperienceConfig;\nimport com.gmail.nossr50.config.party.PartyConfig;\nimport com.gmail.nossr50.datatypes.player.McMMOPlayer;\nimport com.gmail.nossr50.datatypes.player.PlayerProfile;\nimport com.gmail.nossr50.datatypes.skills.PrimarySkillType;\nimport com.gmail.nossr50.datatypes.skills.SubSkillType;\nimport com.gmail.nossr50.util.*;\nimport com.gmail.nossr50.util.blockmeta.ChunkManager;\nimport com.gmail.nossr50.util.player.UserManager;\nimport com.gmail.nossr50.util.skills.RankUtils;\nimport com.gmail.nossr50.util.skills.SkillTools;\nimport org.bukkit.*;\nimport org.bukkit.entity.Player;\nimport org.bukkit.inventory.ItemFactory;\nimport org.bukkit.inventory.ItemStack;\nimport org.bukkit.inventory.PlayerInventory;\nimport org.bukkit.plugin.PluginManager;\nimport org.mockito.MockedStatic;\nimport org.mockito.Mockito;\n\nimport java.util.UUID;\nimport java.util.logging.Logger;\n\nimport static org.mockito.ArgumentMatchers.any;\nimport static org.mockito.Mockito.*;\n\npublic abstract class MMOTestEnvironment {\n    protected MockedStatic<Bukkit> mockedBukkit;\n    protected MockedStatic<mcMMO> mockedMcMMO;\n    protected MockedStatic<ChatConfig> mockedChatConfig;\n    protected MockedStatic<ExperienceConfig> experienceConfig;\n    protected MockedStatic<Permissions> mockedPermissions;\n    protected MockedStatic<RankUtils> mockedRankUtils;\n    protected MockedStatic<UserManager> mockedUserManager;\n    protected MockedStatic<Misc> mockedMisc;\n    protected MockedStatic<SkillTools> mockedSkillTools;\n    protected MockedStatic<EventUtils> mockedEventUtils;\n    protected TransientEntityTracker transientEntityTracker;\n    protected AdvancedConfig advancedConfig;\n    protected PartyConfig partyConfig;\n    protected GeneralConfig generalConfig;\n    protected RankConfig rankConfig;\n    protected SkillTools skillTools;\n    protected Server server;\n    protected PluginManager pluginManager;\n    protected World world;\n\n    /* Mocks */\n    protected Player player;\n\n    protected UUID playerUUID = UUID.randomUUID();\n    protected ItemStack itemInMainHand;\n\n    protected PlayerInventory playerInventory;\n    protected PlayerProfile playerProfile;\n    protected McMMOPlayer mmoPlayer;\n    protected String playerName = \"testPlayer\";\n    protected ItemFactory itemFactory;\n\n    protected ChunkManager chunkManager;\n    protected MaterialMapStore materialMapStore;\n\n    protected void mockBaseEnvironment(Logger logger) throws InvalidSkillException {\n        mockedMcMMO = mockStatic(mcMMO.class);\n        mcMMO.p = mock(mcMMO.class);\n        when(mcMMO.p.getLogger()).thenReturn(logger);\n\n        // place store\n        chunkManager = mock(ChunkManager.class);\n        when(mcMMO.getUserBlockTracker()).thenReturn(chunkManager);\n\n        // shut off mod manager for woodcutting\n        when(mcMMO.getModManager()).thenReturn(mock(ModManager.class));\n        when(mcMMO.getModManager().isCustomLog(any())).thenReturn(false);\n\n        // chat config\n        mockedChatConfig = mockStatic(ChatConfig.class);\n        when(ChatConfig.getInstance()).thenReturn(mock(ChatConfig.class));\n\n        // general config\n        mockGeneralConfig();\n\n        // party config\n        mockPartyConfig();\n\n        // rank config\n        mockRankConfig();\n\n        // wire advanced config\n        mockAdvancedConfig();\n\n        // wire experience config\n        mockExperienceConfig();\n\n        // wire skill tools\n        this.skillTools = new SkillTools(mcMMO.p);\n        when(mcMMO.p.getSkillTools()).thenReturn(skillTools);\n\n        this.transientEntityTracker = new TransientEntityTracker();\n        when(mcMMO.getTransientEntityTracker()).thenReturn(transientEntityTracker);\n\n        mockPermissions();\n\n        mockedRankUtils = mockStatic(RankUtils.class);\n\n        // wire server\n        this.server = mock(Server.class);\n        when(mcMMO.p.getServer()).thenReturn(server);\n\n        mockedBukkit = mockStatic(Bukkit.class);\n        when(Bukkit.getItemFactory()).thenReturn(itemFactory);\n        itemFactory = mock(ItemFactory.class);\n        // when(itemFactory.getItemMeta(any())).thenReturn(mock(ItemMeta.class));\n\n        // wire plugin manager\n        this.pluginManager = mock(PluginManager.class);\n        when(server.getPluginManager()).thenReturn(pluginManager);\n\n        // wire world\n        this.world = mock(World.class);\n\n        // wire Misc\n        this.mockedMisc = mockStatic(Misc.class);\n        when(Misc.getBlockCenter(any())).thenReturn(new Location(world, 0, 0, 0));\n\n        // setup player and player related mocks after everything else\n        this.player = mock(Player.class);\n        when(player.getUniqueId()).thenReturn(playerUUID);\n\n        // wire inventory\n        this.playerInventory = mock(PlayerInventory.class);\n        when(player.getInventory()).thenReturn(playerInventory);\n\n        // PlayerProfile and McMMOPlayer are partially mocked\n        playerProfile = new PlayerProfile(\"testPlayer\", player.getUniqueId(), 0);\n        mmoPlayer = Mockito.spy(new McMMOPlayer(player, playerProfile));\n\n        // wire user manager\n        this.mockedUserManager = mockStatic(UserManager.class);\n        when(UserManager.getPlayer(player)).thenReturn(mmoPlayer);\n\n        this.materialMapStore = new MaterialMapStore();\n        when(mcMMO.getMaterialMapStore()).thenReturn(materialMapStore);\n    }\n\n    private void mockPermissions() {\n        mockedPermissions = mockStatic(Permissions.class);\n        when(Permissions.isSubSkillEnabled(any(Player.class), any(SubSkillType.class))).thenReturn(true);\n        when(Permissions.canUseSubSkill(any(Player.class), any(SubSkillType.class))).thenReturn(true);\n        when(Permissions.isSubSkillEnabled(any(Player.class), any(SubSkillType.class))).thenReturn(true);\n        when(Permissions.canUseSubSkill(any(Player.class), any(SubSkillType.class))).thenReturn(true);\n        when(Permissions.lucky(player, PrimarySkillType.WOODCUTTING)).thenReturn(false); // player is not lucky\n    }\n\n    private void mockRankConfig() {\n        rankConfig = mock(RankConfig.class);\n    }\n\n    private void mockAdvancedConfig() {\n        this.advancedConfig = mock(AdvancedConfig.class);\n        when(mcMMO.p.getAdvancedConfig()).thenReturn(advancedConfig);\n    }\n\n    private void mockGeneralConfig() {\n        generalConfig = mock(GeneralConfig.class);\n        when(generalConfig.getTreeFellerThreshold()).thenReturn(100);\n        when(generalConfig.getDoubleDropsEnabled(PrimarySkillType.WOODCUTTING, Material.OAK_LOG)).thenReturn(true);\n        when(generalConfig.getLocale()).thenReturn(\"en_US\");\n        when(mcMMO.p.getGeneralConfig()).thenReturn(generalConfig);\n    }\n\n    private void mockPartyConfig() {\n        partyConfig = mock(PartyConfig.class);\n        when(partyConfig.isPartyEnabled()).thenReturn(false);\n        when(mcMMO.p.getPartyConfig()).thenReturn(partyConfig);\n    }\n\n    private void mockExperienceConfig() {\n        experienceConfig = mockStatic(ExperienceConfig.class);\n\n        when(ExperienceConfig.getInstance()).thenReturn(mock(ExperienceConfig.class));\n\n        // Combat\n        when(ExperienceConfig.getInstance().getCombatXP(\"Cow\")).thenReturn(1D);\n    }\n\n    protected void cleanupBaseEnvironment() {\n        // Clean up resources here if needed.\n        if (mockedMcMMO != null) {\n            mockedMcMMO.close();\n        }\n        if (experienceConfig != null) {\n            experienceConfig.close();\n        }\n        if (mockedChatConfig != null) {\n            mockedChatConfig.close();\n        }\n        if (mockedPermissions != null) {\n            mockedPermissions.close();\n        }\n        if (mockedRankUtils != null) {\n            mockedRankUtils.close();\n        }\n        if (mockedUserManager != null) {\n            mockedUserManager.close();\n        }\n        if (mockedMisc != null) {\n            mockedMisc.close();\n        }\n        if (mockedEventUtils != null) {\n            mockedEventUtils.close();\n        }\n        if (mockedBukkit != null) {\n            mockedBukkit.close();\n        }\n    }\n}\n"
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
