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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/spring-batch/repository",
  "target": {
    "smell": "GC",
    "smell_name": "God Component",
    "target_type": "package",
    "target_name": "org.springframework.batch.core.configuration.support"
  },
  "block": {
    "id": 1,
    "goal": "Move the cohesive job-loading cluster into a dedicated subpackage.",
    "files": [
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/AutomaticJobRegistrar.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/DefaultJobLoader.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JobLoader.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/AutomaticJobRegistrar.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/DefaultJobLoader.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/JobLoader.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.springframework.batch.core.configuration.support.job"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.springframework.batch.core.configuration.support.JobLoader"
        ],
        "outputs": [
          "org.springframework.batch.core.configuration.support.job.JobLoader"
        ],
        "details": "Move the job-loader contract to the dedicated job-loading subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.springframework.batch.core.configuration.support.DefaultJobLoader"
        ],
        "outputs": [
          "org.springframework.batch.core.configuration.support.job.DefaultJobLoader"
        ],
        "details": "Move the default job-loader implementation together with its contract and registrar collaborators.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.springframework.batch.core.configuration.support.AutomaticJobRegistrar"
        ],
        "outputs": [
          "org.springframework.batch.core.configuration.support.job.AutomaticJobRegistrar"
        ],
        "details": "Move the automatic job registrar together with the job-loading classes it coordinates.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.springframework.batch.core.configuration.support.job.AutomaticJobRegistrar",
          "org.springframework.batch.core.configuration.support.job.DefaultJobLoader",
          "org.springframework.batch.core.configuration.support.job.JobLoader"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/AutomaticJobRegistrar.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/DefaultJobLoader.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JobLoader.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/AutomaticJobRegistrar.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/DefaultJobLoader.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/JobLoader.java"
  ],
  "executor_existing_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/AutomaticJobRegistrar.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/DefaultJobLoader.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JobLoader.java"
  ],
  "executor_new_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/AutomaticJobRegistrar.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/DefaultJobLoader.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/JobLoader.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/AutomaticJobRegistrar.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/DefaultJobLoader.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JobLoader.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/AutomaticJobRegistrar.java",
      "exists": "true",
      "content": "/*\n * Copyright 2006-2025 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\npackage org.springframework.batch.core.configuration.support.job;\n\nimport java.util.ArrayList;\nimport java.util.Arrays;\nimport java.util.Collection;\n\nimport org.jspecify.annotations.NullUnmarked;\nimport org.springframework.batch.core.configuration.support.context.ApplicationContextFactory;\nimport org.springframework.batch.core.configuration.support.job.JobLoader;\nimport org.springframework.batch.core.job.Job;\nimport org.springframework.batch.core.configuration.DuplicateJobException;\nimport org.springframework.batch.core.configuration.JobRegistry;\nimport org.springframework.beans.factory.InitializingBean;\nimport org.springframework.context.ApplicationContext;\nimport org.springframework.context.ApplicationContextAware;\nimport org.springframework.context.Lifecycle;\nimport org.springframework.context.SmartLifecycle;\nimport org.springframework.context.event.ApplicationContextEvent;\nimport org.springframework.core.Ordered;\nimport org.springframework.util.Assert;\n\n/**\n * Loads and unloads {@link Job Jobs} when the application context is created and\n * destroyed. Each provided resource is loaded as an application context with the current\n * context as its parent. Then all the jobs from the child context are registered under\n * their bean names. A {@link JobRegistry} is required.\n *\n * @author Lucas Ward\n * @author Dave Syer\n * @author Mahmoud Ben Hassine\n * @since 2.1\n * @deprecated since 6.0 with no replacement. Scheduled for removal in 6.2 or later.\n */\n@NullUnmarked\n@Deprecated(since = \"6.0\", forRemoval = true)\npublic class AutomaticJobRegistrar implements Ordered, SmartLifecycle, ApplicationContextAware, InitializingBean {\n\n\tprivate final Collection<ApplicationContextFactory> applicationContextFactories = new ArrayList<>();\n\n\tprivate JobLoader jobLoader;\n\n\tprivate ApplicationContext applicationContext;\n\n\tprivate volatile boolean running = false;\n\n\tprivate int phase = Integer.MIN_VALUE + 1000;\n\n\tprivate boolean autoStartup = true;\n\n\tprivate final Object lifecycleMonitor = new Object();\n\n\tprivate int order = Ordered.LOWEST_PRECEDENCE;\n\n\t/**\n\t * The enclosing application context, which you can use to check whether\n\t * {@link ApplicationContextEvent events} come from the expected source.\n\t * @param applicationContext the enclosing application context, if there is one\n\t * @see ApplicationContextAware#setApplicationContext(ApplicationContext)\n\t */\n\t@Override\n\tpublic void setApplicationContext(ApplicationContext applicationContext) {\n\t\tthis.applicationContext = applicationContext;\n\t}\n\n\t/**\n\t * Add a single {@link ApplicationContextFactory} to the set that is used to load\n\t * contexts and jobs.\n\t * @param applicationContextFactory the {@link ApplicationContextFactory} values to\n\t * use\n\t */\n\tpublic void addApplicationContextFactory(ApplicationContextFactory applicationContextFactory) {\n\t\tif (applicationContextFactory instanceof ApplicationContextAware applicationContextAware) {\n\t\t\tapplicationContextAware.setApplicationContext(applicationContext);\n\t\t}\n\t\tthis.applicationContextFactories.add(applicationContextFactory);\n\t}\n\n\t/**\n\t * Add an array of {@link ApplicationContextFactory} instances to the set that is used\n\t * to load contexts and jobs.\n\t * @param applicationContextFactories the {@link ApplicationContextFactory} values to\n\t * use\n\t */\n\tpublic void setApplicationContextFactories(ApplicationContextFactory[] applicationContextFactories) {\n\t\tthis.applicationContextFactories.addAll(Arrays.asList(applicationContextFactories));\n\t}\n\n\t/**\n\t * The job loader that is used to load and manage jobs.\n\t * @param jobLoader the {@link JobLoader} to set\n\t */\n\tpublic void setJobLoader(JobLoader jobLoader) {\n\t\tthis.jobLoader = jobLoader;\n\t}\n\n\t@Override\n\tpublic int getOrder() {\n\t\treturn order;\n\t}\n\n\t/**\n\t * The order in which to start up and shutdown.\n\t * @param order the order (default {@link Ordered#LOWEST_PRECEDENCE}).\n\t * @see Ordered\n\t */\n\tpublic void setOrder(int order) {\n\t\tthis.order = order;\n\t}\n\n\t/**\n\t */\n\t@Override\n\tpublic void afterPropertiesSet() {\n\n\t\tAssert.state(jobLoader != null, \"A JobLoader must be provided\");\n\n\t}\n\n\t/**\n\t * Delegates to {@link JobLoader#clear()}.\n\t *\n\t * @see Lifecycle#stop()\n\t */\n\t@Override\n\tpublic void stop() {\n\t\tsynchronized (this.lifecycleMonitor) {\n\t\t\tjobLoader.clear();\n\t\t\trunning = false;\n\t\t}\n\t}\n\n\t/**\n\t * Take all the contexts from the factories provided and pass them to the\n\t * {@link JobLoader}.\n\t *\n\t * @see Lifecycle#start()\n\t */\n\t@Override\n\tpublic void start() {\n\t\tsynchronized (this.lifecycleMonitor) {\n\t\t\tif (running) {\n\t\t\t\treturn;\n\t\t\t}\n\t\t\tfor (ApplicationContextFactory factory : applicationContextFactories) {\n\t\t\t\ttry {\n\t\t\t\t\tjobLoader.load(factory);\n\t\t\t\t}\n\t\t\t\tcatch (DuplicateJobException e) {\n\t\t\t\t\tthrow new IllegalStateException(e);\n\t\t\t\t}\n\t\t\t}\n\t\t\trunning = true;\n\t\t}\n\t}\n\n\t/**\n\t * Check whether this component has been started.\n\t * @return {@code true} if started successfully and not stopped.\n\t * @see Lifecycle#isRunning()\n\t */\n\t@Override\n\tpublic boolean isRunning() {\n\t\tsynchronized (this.lifecycleMonitor) {\n\t\t\treturn running;\n\t\t}\n\t}\n\n\t@Override\n\tpublic boolean isAutoStartup() {\n\t\treturn autoStartup;\n\t}\n\n\t/**\n\t * @param autoStartup {@code true} for auto start.\n\t * @see #isAutoStartup()\n\t */\n\tpublic void setAutoStartup(boolean autoStartup) {\n\t\tthis.autoStartup = autoStartup;\n\t}\n\n\t@Override\n\tpublic int getPhase() {\n\t\treturn phase;\n\t}\n\n\t/**\n\t * @param phase the phase.\n\t * @see #getPhase()\n\t */\n\tpublic void setPhase(int phase) {\n\t\tthis.phase = phase;\n\t}\n\n\t@Override\n\tpublic void stop(Runnable callback) {\n\t\tstop();\n\t\tcallback.run();\n\t}\n\n}\n"
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/DefaultJobLoader.java",
      "exists": "true",
      "content": "/*\n * Copyright 2006-2025 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.springframework.batch.core.configuration.support.job;\n\nimport java.util.ArrayList;\nimport java.util.Collection;\nimport java.util.HashSet;\nimport java.util.Map;\nimport java.util.concurrent.ConcurrentHashMap;\n\nimport org.apache.commons.logging.Log;\nimport org.apache.commons.logging.LogFactory;\nimport org.jspecify.annotations.NullUnmarked;\nimport org.springframework.batch.core.configuration.support.context.ApplicationContextFactory;\nimport org.springframework.batch.core.configuration.support.job.JobLoader;\nimport org.springframework.batch.core.job.Job;\nimport org.springframework.batch.core.step.ListableStepLocator;\nimport org.springframework.batch.core.step.Step;\nimport org.springframework.batch.core.configuration.DuplicateJobException;\nimport org.springframework.batch.core.configuration.JobRegistry;\nimport org.springframework.batch.core.configuration.StepRegistry;\nimport org.springframework.batch.core.step.StepLocator;\nimport org.springframework.beans.factory.InitializingBean;\nimport org.springframework.context.ApplicationContext;\nimport org.springframework.context.ConfigurableApplicationContext;\nimport org.springframework.lang.Nullable;\nimport org.springframework.util.Assert;\n\n/**\n * Default implementation of {@link JobLoader}. Uses a {@link JobRegistry} to manage a\n * population of loaded jobs and clears them up when asked. An optional\n * {@link StepRegistry} might also be set to register the step(s) available for each\n * registered job.\n *\n * @author Dave Syer\n * @author Stephane Nicoll\n * @author Mahmoud Ben Hassine\n * @deprecated since 6.0 with no replacement. Scheduled for removal in 6.2 or later.\n */\n@NullUnmarked\n@Deprecated(since = \"6.0\", forRemoval = true)\npublic class DefaultJobLoader implements JobLoader, InitializingBean {\n\n\tprivate static final Log logger = LogFactory.getLog(DefaultJobLoader.class);\n\n\tprivate JobRegistry jobRegistry;\n\n\tprivate StepRegistry stepRegistry;\n\n\tprivate final Map<ApplicationContextFactory, ConfigurableApplicationContext> contexts = new ConcurrentHashMap<>();\n\n\tprivate final Map<ConfigurableApplicationContext, Collection<String>> contextToJobNames = new ConcurrentHashMap<>();\n\n\t/**\n\t * Default constructor. Useful for declarative configuration.\n\t */\n\tpublic DefaultJobLoader() {\n\t\tthis(null, null);\n\t}\n\n\t/**\n\t * Creates a job loader with the job registry provided.\n\t * @param jobRegistry a {@link JobRegistry}\n\t */\n\tpublic DefaultJobLoader(JobRegistry jobRegistry) {\n\t\tthis(jobRegistry, null);\n\t}\n\n\t/**\n\t * Creates a job loader with the job and step registries provided.\n\t * @param jobRegistry a {@link JobRegistry}\n\t * @param stepRegistry a {@link StepRegistry} (can be {@code null})\n\t */\n\tpublic DefaultJobLoader(JobRegistry jobRegistry, @Nullable StepRegistry stepRegistry) {\n\t\tthis.jobRegistry = jobRegistry;\n\t\tthis.stepRegistry = stepRegistry;\n\t}\n\n\t/**\n\t * The {@link JobRegistry} to use for jobs created.\n\t * @param jobRegistry the job registry\n\t */\n\tpublic void setJobRegistry(JobRegistry jobRegistry) {\n\t\tthis.jobRegistry = jobRegistry;\n\t}\n\n\t/**\n\t * The {@link StepRegistry} to use for the steps of created jobs.\n\t * @param stepRegistry the step registry\n\t */\n\tpublic void setStepRegistry(StepRegistry stepRegistry) {\n\t\tthis.stepRegistry = stepRegistry;\n\t}\n\n\t/**\n\t * Unregister all the jobs and close all the contexts created by this loader.\n\t *\n\t * @see JobLoader#clear()\n\t */\n\t@Override\n\tpublic void clear() {\n\t\tfor (ConfigurableApplicationContext context : contexts.values()) {\n\t\t\tif (context.isActive()) {\n\t\t\t\tcontext.close();\n\t\t\t}\n\t\t}\n\t\tfor (String jobName : jobRegistry.getJobNames()) {\n\t\t\tdoUnregister(jobName);\n\t\t}\n\t\tcontexts.clear();\n\t\tcontextToJobNames.clear();\n\t}\n\n\t@Override\n\tpublic Collection<Job> reload(ApplicationContextFactory factory) {\n\n\t\t// If the same factory is loaded twice the context can be closed\n\t\tif (contexts.containsKey(factory)) {\n\t\t\tConfigurableApplicationContext context = contexts.get(factory);\n\t\t\tfor (String name : contextToJobNames.get(context)) {\n\t\t\t\tif (logger.isDebugEnabled()) {\n\t\t\t\t\tlogger.debug(\"Unregistering job: \" + name + \" from context: \" + context.getDisplayName());\n\t\t\t\t}\n\t\t\t\tdoUnregister(name);\n\t\t\t}\n\t\t\tcontext.close();\n\t\t}\n\n\t\ttry {\n\t\t\treturn doLoad(factory, true);\n\t\t}\n\t\tcatch (DuplicateJobException e) {\n\t\t\tthrow new IllegalStateException(\"Found duplicate job in reload (it should have been unregistered \"\n\t\t\t\t\t+ \"if it was previously registered in this loader)\", e);\n\t\t}\n\t}\n\n\t@Override\n\tpublic Collection<Job> load(ApplicationContextFactory factory) throws DuplicateJobException {\n\t\treturn doLoad(factory, false);\n\t}\n\n\tprivate Collection<Job> doLoad(ApplicationContextFactory factory, boolean unregister) throws DuplicateJobException {\n\n\t\tCollection<String> jobNamesBefore = jobRegistry.getJobNames();\n\t\tConfigurableApplicationContext context = factory.createApplicationContext();\n\t\tCollection<String> jobNamesAfter = jobRegistry.getJobNames();\n\t\t// Try to detect auto-registration (e.g. through a bean post processor)\n\t\tboolean autoRegistrationDetected = jobNamesAfter.size() > jobNamesBefore.size();\n\n\t\tCollection<String> jobsRegistered = new HashSet<>();\n\t\tif (autoRegistrationDetected) {\n\t\t\tfor (String name : jobNamesAfter) {\n\t\t\t\tif (!jobNamesBefore.contains(name)) {\n\t\t\t\t\tjobsRegistered.add(name);\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\n\t\tcontexts.put(factory, context);\n\t\tString[] names = context.getBeanNamesForType(Job.class);\n\n\t\tfor (String name : names) {\n\n\t\t\tif (!autoRegistrationDetected) {\n\n\t\t\t\tJob job = context.getBean(name, Job.class);\n\t\t\t\tString jobName = job.getName();\n\n\t\t\t\t// On reload try to unregister first\n\t\t\t\tif (unregister) {\n\t\t\t\t\tif (logger.isDebugEnabled()) {\n\t\t\t\t\t\tlogger.debug(\"Unregistering job: \" + jobName + \" from context: \" + context.getDisplayName());\n\t\t\t\t\t}\n\t\t\t\t\tdoUnregister(jobName);\n\t\t\t\t}\n\n\t\t\t\tif (logger.isDebugEnabled()) {\n\t\t\t\t\tlogger.debug(\"Registering job: \" + jobName + \" from context: \" + context.getDisplayName());\n\t\t\t\t}\n\t\t\t\tdoRegister(context, job);\n\t\t\t\tjobsRegistered.add(jobName);\n\t\t\t}\n\n\t\t}\n\n\t\tCollection<Job> result = new ArrayList<>();\n\t\tfor (String name : jobsRegistered) {\n\t\t\tJob job = jobRegistry.getJob(name);\n\t\t\tif (job == null) {\n\t\t\t\tthrow new IllegalStateException(\"Could not retrieve job that was should have been registered\");\n\t\t\t}\n\t\t\tresult.add(job);\n\t\t}\n\n\t\tcontextToJobNames.put(context, jobsRegistered);\n\n\t\treturn result;\n\n\t}\n\n\t/**\n\t * Returns all the {@link Step} instances defined by the specified\n\t * {@link StepLocator}. <br>\n\t * The specified <tt>jobApplicationContext</tt> is used to collect additional steps\n\t * that are not exposed by the step locator\n\t * @param stepLocator the given step locator\n\t * @param jobApplicationContext the application context of the job\n\t * @return all the {@link Step} defined by the given step locator and context\n\t * @see StepLocator\n\t */\n\tprivate Collection<Step> getSteps(final ListableStepLocator stepLocator,\n\t\t\tfinal ApplicationContext jobApplicationContext) {\n\t\tfinal Collection<String> stepNames = stepLocator.getStepNames();\n\t\tfinal Collection<Step> result = new ArrayList<>();\n\t\tfor (String stepName : stepNames) {\n\t\t\tresult.add(stepLocator.getStep(stepName));\n\t\t}\n\n\t\t// Because some steps are referenced by name, we need to look in the context to\n\t\t// see if there\n\t\t// are more Step instances defined. Right now they are registered as being\n\t\t// available in the\n\t\t// context of the job but we have no idea if they are linked to that Job or not.\n\t\tfinal Map<String, Step> allSteps = jobApplicationContext.getBeansOfType(Step.class);\n\t\tfor (Map.Entry<String, Step> entry : allSteps.entrySet()) {\n\t\t\tif (!stepNames.contains(entry.getKey())) {\n\t\t\t\tresult.add(entry.getValue());\n\t\t\t}\n\t\t}\n\t\treturn result;\n\t}\n\n\t/**\n\t * Registers the specified {@link Job} defined in the specified\n\t * {@link ConfigurableApplicationContext}. <br>\n\t * Updates the {@link StepRegistry} if it is available.\n\t * @param context the context in which the job is defined\n\t * @param job the job to register\n\t * @throws DuplicateJobException if that job is already registered\n\t */\n\tprivate void doRegister(ConfigurableApplicationContext context, Job job) throws DuplicateJobException {\n\t\tjobRegistry.register(job);\n\n\t\tif (stepRegistry != null) {\n\t\t\tif (!(job instanceof ListableStepLocator stepLocator)) {\n\t\t\t\tthrow new UnsupportedOperationException(\"Cannot locate steps from a Job that is not a StepLocator: job=\"\n\t\t\t\t\t\t+ job.getName() + \" does not implement StepLocator\");\n\t\t\t}\n\t\t\tstepRegistry.register(job.getName(), getSteps(stepLocator, context));\n\t\t}\n\t}\n\n\t/**\n\t * Unregisters the job identified by the specified <tt>jobName</tt>.\n\t * @param jobName the name of the job to unregister\n\t */\n\tprivate void doUnregister(String jobName) {\n\t\tjobRegistry.unregister(jobName);\n\t\tif (stepRegistry != null) {\n\t\t\tstepRegistry.unregisterStepsFromJob(jobName);\n\t\t}\n\n\t}\n\n\t@Override\n\tpublic void afterPropertiesSet() {\n\t\tAssert.state(jobRegistry != null, \"Job registry could not be null.\");\n\t}\n\n}\n"
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/job/JobLoader.java",
      "exists": "true",
      "content": "/*\n * Copyright 2009-2025 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.springframework.batch.core.configuration.support.job;\n\nimport java.util.Collection;\n\nimport org.jspecify.annotations.NullUnmarked;\nimport org.springframework.batch.core.configuration.support.context.ApplicationContextFactory;\nimport org.springframework.batch.core.job.Job;\nimport org.springframework.batch.core.configuration.DuplicateJobException;\n\n/**\n * @author Dave Syer\n * @author Mahmoud Ben Hassine\n * @since 2.1\n * @deprecated since 6.0 with no replacement. Scheduled for removal in 6.2 or later.\n */\n@NullUnmarked\n@Deprecated(since = \"6.0\", forRemoval = true)\npublic interface JobLoader {\n\n\t/**\n\t * Load an application context and register all the jobs.\n\t * @param factory a factory for an application context (containing jobs)\n\t * @return a collection of the jobs created\n\t * @throws DuplicateJobException if a job with the same name was already registered\n\t */\n\tCollection<Job> load(ApplicationContextFactory factory) throws DuplicateJobException;\n\n\t/**\n\t * Load an application context and register all the jobs, having first unregistered\n\t * them if already registered. Implementations should also close and clean up the\n\t * application context previously created (either from this factory or from one with\n\t * the same jobs), if possible.\n\t * @param factory a factory for an application context (containing jobs)\n\t * @return a collection of the jobs created\n\t */\n\tCollection<Job> reload(ApplicationContextFactory factory);\n\n\t/**\n\t * Unregister all the jobs and close all the contexts created by this loader.\n\t */\n\tvoid clear();\n\n}\n"
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
