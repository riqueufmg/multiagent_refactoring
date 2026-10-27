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
    "goal": "Move the cohesive database-specific batch configuration cluster to a dedicated subpackage.",
    "files": [
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JdbcDefaultBatchConfiguration.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/MongoDefaultBatchConfiguration.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/JdbcDefaultBatchConfiguration.java",
      "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/MongoDefaultBatchConfiguration.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "org.springframework.batch.core.configuration.support.database"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.springframework.batch.core.configuration.support.JdbcDefaultBatchConfiguration"
        ],
        "outputs": [
          "org.springframework.batch.core.configuration.support.database.JdbcDefaultBatchConfiguration"
        ],
        "details": "Move the JDBC-specific batch configuration class to the database subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "org.springframework.batch.core.configuration.support.MongoDefaultBatchConfiguration"
        ],
        "outputs": [
          "org.springframework.batch.core.configuration.support.database.MongoDefaultBatchConfiguration"
        ],
        "details": "Move the MongoDB-specific batch configuration class to the database subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "org.springframework.batch.core.configuration.support.database.JdbcDefaultBatchConfiguration",
          "org.springframework.batch.core.configuration.support.database.MongoDefaultBatchConfiguration"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JdbcDefaultBatchConfiguration.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/MongoDefaultBatchConfiguration.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/JdbcDefaultBatchConfiguration.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/MongoDefaultBatchConfiguration.java"
  ],
  "executor_existing_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JdbcDefaultBatchConfiguration.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/MongoDefaultBatchConfiguration.java"
  ],
  "executor_new_files": [
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/JdbcDefaultBatchConfiguration.java",
    "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/MongoDefaultBatchConfiguration.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/JdbcDefaultBatchConfiguration.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/MongoDefaultBatchConfiguration.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/JdbcDefaultBatchConfiguration.java",
      "exists": "true",
      "content": "/*\n * Copyright 2012-2025 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.springframework.batch.core.configuration.support.database;\n\nimport org.springframework.batch.core.configuration.BatchConfigurationException;\nimport org.springframework.batch.core.converter.DateToStringConverter;\nimport org.springframework.batch.core.converter.LocalDateTimeToStringConverter;\nimport org.springframework.batch.core.converter.LocalDateToStringConverter;\nimport org.springframework.batch.core.converter.LocalTimeToStringConverter;\nimport org.springframework.batch.core.converter.StringToDateConverter;\nimport org.springframework.batch.core.converter.StringToLocalDateConverter;\nimport org.springframework.batch.core.converter.StringToLocalDateTimeConverter;\nimport org.springframework.batch.core.converter.StringToLocalTimeConverter;\nimport org.springframework.batch.core.job.DefaultJobKeyGenerator;\nimport org.springframework.batch.core.job.JobInstance;\nimport org.springframework.batch.core.job.JobKeyGenerator;\nimport org.springframework.batch.core.launch.JobOperator;\nimport org.springframework.batch.core.repository.ExecutionContextSerializer;\nimport org.springframework.batch.core.repository.JobRepository;\nimport org.springframework.batch.core.repository.dao.AbstractJdbcBatchMetadataDao;\nimport org.springframework.batch.core.repository.dao.DefaultExecutionContextSerializer;\nimport org.springframework.batch.core.repository.dao.jdbc.JdbcExecutionContextDao;\nimport org.springframework.batch.core.repository.dao.jdbc.JdbcJobExecutionDao;\nimport org.springframework.batch.core.repository.dao.jdbc.JdbcStepExecutionDao;\nimport org.springframework.batch.core.repository.support.JdbcJobRepositoryFactoryBean;\nimport org.springframework.batch.infrastructure.item.database.support.DataFieldMaxValueIncrementerFactory;\nimport org.springframework.batch.infrastructure.item.database.support.DefaultDataFieldMaxValueIncrementerFactory;\nimport org.springframework.batch.infrastructure.support.DatabaseType;\nimport org.springframework.context.annotation.Bean;\nimport org.springframework.context.annotation.Configuration;\nimport org.springframework.core.convert.support.ConfigurableConversionService;\nimport org.springframework.core.convert.support.DefaultConversionService;\nimport org.springframework.jdbc.core.JdbcOperations;\nimport org.springframework.jdbc.core.JdbcTemplate;\nimport org.springframework.jdbc.support.MetaDataAccessException;\nimport org.springframework.jdbc.support.incrementer.DataFieldMaxValueIncrementer;\nimport org.springframework.transaction.PlatformTransactionManager;\nimport org.springframework.transaction.annotation.Isolation;\n\nimport javax.sql.DataSource;\nimport java.nio.charset.Charset;\nimport java.nio.charset.StandardCharsets;\nimport java.sql.Types;\n\n/**\n * Base {@link Configuration} class that provides common JDBC-based infrastructure beans\n * for enabling and using Spring Batch.\n * <p>\n * This configuration class configures and registers the following beans in the\n * application context:\n *\n * <ul>\n * <li>a {@link JobRepository} named \"jobRepository\"</li>\n * <li>a {@link JobOperator} named \"jobOperator\"</li>\n * <li>a {@link org.springframework.batch.core.scope.StepScope} named \"stepScope\"</li>\n * <li>a {@link org.springframework.batch.core.scope.JobScope} named \"jobScope\"</li>\n * </ul>\n *\n * Customization is possible by extending the class and overriding getters.\n * <p>\n * A typical usage of this class is as follows: <pre class=\"code\">\n * &#064;Configuration\n * public class MyJobConfiguration extends JdbcDefaultBatchConfiguration {\n *\n *     &#064;Bean\n *     public Job job(JobRepository jobRepository) {\n *         return new JobBuilder(\"myJob\", jobRepository)\n *                 // define job flow as needed\n *                 .build();\n *     }\n *\n * }\n * </pre>\n *\n * @author Mahmoud Ben Hassine\n * @since 6.0\n */\n@Configuration(proxyBeanMethods = false)\npublic class JdbcDefaultBatchConfiguration extends DefaultBatchConfiguration {\n\n\t@Bean\n\t@Override\n\tpublic JobRepository jobRepository() throws BatchConfigurationException {\n\t\tJdbcJobRepositoryFactoryBean jobRepositoryFactoryBean = new JdbcJobRepositoryFactoryBean();\n\t\ttry {\n\t\t\tjobRepositoryFactoryBean.setDataSource(getDataSource());\n\t\t\tjobRepositoryFactoryBean.setTransactionManager(getTransactionManager());\n\t\t\tjobRepositoryFactoryBean.setDatabaseType(getDatabaseType());\n\t\t\tjobRepositoryFactoryBean.setIncrementerFactory(getIncrementerFactory());\n\t\t\tjobRepositoryFactoryBean.setJobKeyGenerator(getJobKeyGenerator());\n\t\t\tjobRepositoryFactoryBean.setClobType(getClobType());\n\t\t\tjobRepositoryFactoryBean.setTablePrefix(getTablePrefix());\n\t\t\tjobRepositoryFactoryBean.setSerializer(getExecutionContextSerializer());\n\t\t\tjobRepositoryFactoryBean.setConversionService(getConversionService());\n\t\t\tjobRepositoryFactoryBean.setJdbcOperations(getJdbcOperations());\n\t\t\tjobRepositoryFactoryBean.setCharset(getCharset());\n\t\t\tjobRepositoryFactoryBean.setMaxVarCharLength(getMaxVarCharLength());\n\t\t\tjobRepositoryFactoryBean.setIsolationLevelForCreateEnum(getIsolationLevelForCreate());\n\t\t\tjobRepositoryFactoryBean.setValidateTransactionState(getValidateTransactionState());\n\t\t\tjobRepositoryFactoryBean.afterPropertiesSet();\n\t\t\treturn jobRepositoryFactoryBean.getObject();\n\t\t}\n\t\tcatch (Exception e) {\n\t\t\tthrow new BatchConfigurationException(\"Unable to configure the default job repository\", e);\n\t\t}\n\t}\n\n\t/*\n\t * Getters to customize the configuration of infrastructure beans\n\t */\n\n\t/**\n\t * Return the data source to use for Batch meta-data. Defaults to the bean of type\n\t * {@link DataSource} and named \"dataSource\" in the application context.\n\t * @return The data source to use for Batch meta-data\n\t */\n\tprotected DataSource getDataSource() {\n\t\tString errorMessage = \" To use the default configuration, a data source bean named 'dataSource'\"\n\t\t\t\t+ \" should be defined in the application context but none was found. Override getDataSource()\"\n\t\t\t\t+ \" to provide the data source to use for Batch meta-data.\";\n\t\tif (this.applicationContext.getBeansOfType(DataSource.class).isEmpty()) {\n\t\t\tthrow new BatchConfigurationException(\n\t\t\t\t\t\"Unable to find a DataSource bean in the application context.\" + errorMessage);\n\t\t}\n\t\telse {\n\t\t\tif (!this.applicationContext.containsBean(\"dataSource\")) {\n\t\t\t\tthrow new BatchConfigurationException(errorMessage);\n\t\t\t}\n\t\t}\n\t\treturn this.applicationContext.getBean(\"dataSource\", DataSource.class);\n\t}\n\n\t@Override\n\tprotected PlatformTransactionManager getTransactionManager() {\n\t\tString errorMessage = \" To use the default configuration, a PlatformTransactionManager bean named 'transactionManager'\"\n\t\t\t\t+ \" should be defined in the application context but none was found. Override getTransactionManager()\"\n\t\t\t\t+ \" to provide the transaction manager to use for the job repository.\";\n\t\tif (this.applicationContext.getBeansOfType(PlatformTransactionManager.class).isEmpty()) {\n\t\t\tthrow new BatchConfigurationException(\n\t\t\t\t\t\"Unable to find a PlatformTransactionManager bean in the application context.\" + errorMessage);\n\t\t}\n\t\telse {\n\t\t\tif (!this.applicationContext.containsBean(\"transactionManager\")) {\n\t\t\t\tthrow new BatchConfigurationException(errorMessage);\n\t\t\t}\n\t\t}\n\t\treturn this.applicationContext.getBean(\"transactionManager\", PlatformTransactionManager.class);\n\t}\n\n\t/**\n\t * Return the length of long string columns in database. Do not override this if you\n\t * haven't modified the schema. Note this value will be used for the exit message in\n\t * both {@link JdbcJobExecutionDao} and {@link JdbcStepExecutionDao} and also the\n\t * short version of the execution context in {@link JdbcExecutionContextDao} . For\n\t * databases with multi-byte character sets this number can be smaller (by up to a\n\t * factor of 2 for 2-byte characters) than the declaration of the column length in the\n\t * DDL for the tables. Defaults to\n\t * {@link AbstractJdbcBatchMetadataDao#DEFAULT_EXIT_MESSAGE_LENGTH}\n\t */\n\tprotected int getMaxVarCharLength() {\n\t\treturn AbstractJdbcBatchMetadataDao.DEFAULT_EXIT_MESSAGE_LENGTH;\n\t}\n\n\t/**\n\t * Return the prefix of Batch meta-data tables. Defaults to\n\t * {@link AbstractJdbcBatchMetadataDao#DEFAULT_TABLE_PREFIX}.\n\t * @return the prefix of meta-data tables\n\t */\n\tprotected String getTablePrefix() {\n\t\treturn AbstractJdbcBatchMetadataDao.DEFAULT_TABLE_PREFIX;\n\t}\n\n\t/**\n\t * Return the {@link Charset} to use when serializing/deserializing the execution\n\t * context. Defaults to \"UTF-8\".\n\t * @return the charset to use when serializing/deserializing the execution context\n\t */\n\tprotected Charset getCharset() {\n\t\treturn StandardCharsets.UTF_8;\n\t}\n\n\t/**\n\t * Return the {@link JdbcOperations}. If this property is not overridden, a new\n\t * {@link JdbcTemplate} will be created for the configured data source by default.\n\t * @return the {@link JdbcOperations} to use\n\t */\n\tprotected JdbcOperations getJdbcOperations() {\n\t\treturn new JdbcTemplate(getDataSource());\n\t}\n\n\t/**\n\t * A custom implementation of the {@link ExecutionContextSerializer}. The default, if\n\t * not injected, is the {@link DefaultExecutionContextSerializer}.\n\t * @return the serializer to use to serialize/deserialize the execution context\n\t */\n\tprotected ExecutionContextSerializer getExecutionContextSerializer() {\n\t\treturn new DefaultExecutionContextSerializer();\n\t}\n\n\t/**\n\t * Return the value from {@link Types} class to indicate the type to use for a CLOB\n\t * @return the value from {@link Types} class to indicate the type to use for a CLOB\n\t */\n\tprotected int getClobType() {\n\t\treturn Types.CLOB;\n\t}\n\n\t/**\n\t * Return the factory for creating {@link DataFieldMaxValueIncrementer}\n\t * implementations used to increment entity IDs in meta-data tables.\n\t * @return the factory for creating {@link DataFieldMaxValueIncrementer}\n\t * implementations.\n\t */\n\tprotected DataFieldMaxValueIncrementerFactory getIncrementerFactory() {\n\t\treturn new DefaultDataFieldMaxValueIncrementerFactory(getDataSource());\n\t}\n\n\t/**\n\t * Return the database type. The default will be introspected from the JDBC meta-data\n\t * of the data source.\n\t * @return the database type\n\t * @throws MetaDataAccessException if an error occurs when trying to get the database\n\t * type of JDBC meta-data\n\t *\n\t */\n\tprotected String getDatabaseType() throws MetaDataAccessException {\n\t\treturn DatabaseType.fromMetaData(getDataSource()).name();\n\t}\n\n\t/**\n\t * Return the conversion service to use in the job repository and job explorer. This\n\t * service is used to convert job parameters from String literal to typed values and\n\t * vice versa.\n\t * @return the {@link ConfigurableConversionService} to use.\n\t */\n\tprotected ConfigurableConversionService getConversionService() {\n\t\tDefaultConversionService conversionService = new DefaultConversionService();\n\t\tconversionService.addConverter(new DateToStringConverter());\n\t\tconversionService.addConverter(new StringToDateConverter());\n\t\tconversionService.addConverter(new LocalDateToStringConverter());\n\t\tconversionService.addConverter(new StringToLocalDateConverter());\n\t\tconversionService.addConverter(new LocalTimeToStringConverter());\n\t\tconversionService.addConverter(new StringToLocalTimeConverter());\n\t\tconversionService.addConverter(new LocalDateTimeToStringConverter());\n\t\tconversionService.addConverter(new StringToLocalDateTimeConverter());\n\t\treturn conversionService;\n\t}\n\n\t/**\n\t * Return the value of the {@code validateTransactionState} parameter. Defaults to\n\t * {@code true}.\n\t * @return true if the transaction state should be validated, false otherwise\n\t */\n\tprotected boolean getValidateTransactionState() {\n\t\treturn true;\n\t}\n\n\t/**\n\t * Return the transaction isolation level when creating job executions. Defaults to\n\t * {@link Isolation#SERIALIZABLE}.\n\t * @return the transaction isolation level when creating job executions\n\t */\n\tprotected Isolation getIsolationLevelForCreate() {\n\t\treturn Isolation.SERIALIZABLE;\n\t}\n\n\t/**\n\t * A custom implementation of the {@link JobKeyGenerator}. The default, if not\n\t * injected, is the {@link DefaultJobKeyGenerator}.\n\t * @return the generator that creates the key used in identifying {@link JobInstance}\n\t * objects\n\t * @since 5.1\n\t */\n\tprotected JobKeyGenerator getJobKeyGenerator() {\n\t\treturn new DefaultJobKeyGenerator();\n\t}\n\n}\n"
    },
    {
      "path": "spring-batch-core/src/main/java/org/springframework/batch/core/configuration/support/database/MongoDefaultBatchConfiguration.java",
      "exists": "true",
      "content": "/*\n * Copyright 2012-2025 the original author or authors.\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *      https://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\npackage org.springframework.batch.core.configuration.support.database;\n\nimport org.springframework.batch.core.configuration.BatchConfigurationException;\nimport org.springframework.batch.core.job.DefaultJobKeyGenerator;\nimport org.springframework.batch.core.job.JobInstance;\nimport org.springframework.batch.core.job.JobKeyGenerator;\nimport org.springframework.batch.core.launch.JobOperator;\nimport org.springframework.batch.core.repository.JobRepository;\nimport org.springframework.batch.core.repository.dao.mongodb.MongoSequenceIncrementer;\nimport org.springframework.batch.core.repository.support.MongoJobRepositoryFactoryBean;\nimport org.springframework.context.annotation.Bean;\nimport org.springframework.context.annotation.Configuration;\nimport org.springframework.data.mongodb.MongoTransactionManager;\nimport org.springframework.data.mongodb.core.MongoOperations;\nimport org.springframework.jdbc.support.incrementer.DataFieldMaxValueIncrementer;\nimport org.springframework.transaction.annotation.Isolation;\n\n/**\n * Base {@link Configuration} class that provides common MongoDB-based infrastructure\n * beans for enabling and using Spring Batch.\n * <p>\n * This configuration class configures and registers the following beans in the\n * application context:\n *\n * <ul>\n * <li>a {@link JobRepository} named \"jobRepository\"</li>\n * <li>a {@link JobOperator} named \"jobOperator\"</li>\n * <li>a {@link org.springframework.batch.core.scope.StepScope} named \"stepScope\"</li>\n * <li>a {@link org.springframework.batch.core.scope.JobScope} named \"jobScope\"</li>\n * </ul>\n *\n * Customization is possible by extending the class and overriding getters.\n * <p>\n * A typical usage of this class is as follows: <pre class=\"code\">\n * &#064;Configuration\n * public class MyJobConfiguration extends MongoDefaultBatchConfiguration {\n *\n *     &#064;Bean\n *     public Job job(JobRepository jobRepository) {\n *         return new JobBuilder(\"myJob\", jobRepository)\n *                 // define job flow as needed\n *                 .build();\n *     }\n *\n * }\n * </pre>\n *\n * @author Mahmoud Ben Hassine\n * @since 6.0\n */\n@Configuration(proxyBeanMethods = false)\npublic class MongoDefaultBatchConfiguration extends DefaultBatchConfiguration {\n\n\t@Bean\n\t@Override\n\tpublic JobRepository jobRepository() throws BatchConfigurationException {\n\t\tMongoJobRepositoryFactoryBean jobRepositoryFactoryBean = new MongoJobRepositoryFactoryBean();\n\t\ttry {\n\t\t\tjobRepositoryFactoryBean.setMongoOperations(getMongoOperations());\n\t\t\tjobRepositoryFactoryBean.setTransactionManager(getTransactionManager());\n\t\t\tjobRepositoryFactoryBean.setIsolationLevelForCreateEnum(getIsolationLevelForCreate());\n\t\t\tjobRepositoryFactoryBean.setValidateTransactionState(getValidateTransactionState());\n\t\t\tjobRepositoryFactoryBean.setJobKeyGenerator(getJobKeyGenerator());\n\t\t\tjobRepositoryFactoryBean.setJobInstanceIncrementer(getJobInstanceIncrementer());\n\t\t\tjobRepositoryFactoryBean.setJobExecutionIncrementer(getJobExecutionIncrementer());\n\t\t\tjobRepositoryFactoryBean.setStepExecutionIncrementer(getStepExecutionIncrementer());\n\t\t\tjobRepositoryFactoryBean.afterPropertiesSet();\n\t\t\treturn jobRepositoryFactoryBean.getObject();\n\t\t}\n\t\tcatch (Exception e) {\n\t\t\tthrow new BatchConfigurationException(\"Unable to configure the default job repository\", e);\n\t\t}\n\t}\n\n\t/*\n\t * Getters to customize the configuration of infrastructure beans\n\t */\n\n\tprotected MongoOperations getMongoOperations() {\n\t\tString errorMessage = \" To use the default configuration, a MongoOperations bean named 'mongoTemplate'\"\n\t\t\t\t+ \" should be defined in the application context but none was found. Override getMongoOperations()\"\n\t\t\t\t+ \" to provide the MongoOperations for Batch meta-data.\";\n\t\tif (this.applicationContext.getBeansOfType(MongoOperations.class).isEmpty()) {\n\t\t\tthrow new BatchConfigurationException(\n\t\t\t\t\t\"Unable to find a MongoOperations bean in the application context.\" + errorMessage);\n\t\t}\n\t\telse {\n\t\t\tif (!this.applicationContext.containsBean(\"mongoTemplate\")) {\n\t\t\t\tthrow new BatchConfigurationException(errorMessage);\n\t\t\t}\n\t\t}\n\t\treturn this.applicationContext.getBean(\"mongoTemplate\", MongoOperations.class);\n\t}\n\n\t@Override\n\tprotected MongoTransactionManager getTransactionManager() {\n\t\tString errorMessage = \" To use the default configuration, a MongoTransactionManager bean named 'transactionManager'\"\n\t\t\t\t+ \" should be defined in the application context but none was found. Override getTransactionManager()\"\n\t\t\t\t+ \" to provide the transaction manager to use for the job repository.\";\n\t\tif (this.applicationContext.getBeansOfType(MongoTransactionManager.class).isEmpty()) {\n\t\t\tthrow new BatchConfigurationException(\n\t\t\t\t\t\"Unable to find a MongoTransactionManager bean in the application context.\" + errorMessage);\n\t\t}\n\t\telse {\n\t\t\tif (!this.applicationContext.containsBean(\"transactionManager\")) {\n\t\t\t\tthrow new BatchConfigurationException(errorMessage);\n\t\t\t}\n\t\t}\n\t\treturn this.applicationContext.getBean(\"transactionManager\", MongoTransactionManager.class);\n\t}\n\n\t/**\n\t * Return the value of the {@code validateTransactionState} parameter. Defaults to\n\t * {@code true}.\n\t * @return true if the transaction state should be validated, false otherwise\n\t */\n\tprotected boolean getValidateTransactionState() {\n\t\treturn true;\n\t}\n\n\t/**\n\t * Return the transaction isolation level when creating job executions. Defaults to\n\t * {@link Isolation#SERIALIZABLE}.\n\t * @return the transaction isolation level when creating job executions\n\t */\n\tprotected Isolation getIsolationLevelForCreate() {\n\t\treturn Isolation.SERIALIZABLE;\n\t}\n\n\t/**\n\t * A custom implementation of the {@link JobKeyGenerator}. The default, if not\n\t * injected, is the {@link DefaultJobKeyGenerator}.\n\t * @return the generator that creates the key used in identifying {@link JobInstance}\n\t * objects\n\t * @since 5.1\n\t */\n\tprotected JobKeyGenerator getJobKeyGenerator() {\n\t\treturn new DefaultJobKeyGenerator();\n\t}\n\n\t/**\n\t * Return the incrementer to be used to generate ids for new job instances.\n\t * @return the incrementer to be used to generate ids for new job instances\n\t * @since 6.0\n\t */\n\tprotected DataFieldMaxValueIncrementer getJobInstanceIncrementer() {\n\t\treturn new MongoSequenceIncrementer(getMongoOperations(), \"BATCH_JOB_INSTANCE_SEQ\");\n\t}\n\n\t/**\n\t * Return the incrementer to be used to generate ids for new job executions.\n\t * @return the incrementer to be used to generate ids for new job executions\n\t * @since 6.0\n\t */\n\tprotected DataFieldMaxValueIncrementer getJobExecutionIncrementer() {\n\t\treturn new MongoSequenceIncrementer(getMongoOperations(), \"BATCH_JOB_EXECUTION_SEQ\");\n\t}\n\n\t/**\n\t * Return the incrementer to be used to generate ids for new step executions.\n\t * @return the incrementer to be used to generate ids for new step executions\n\t * @since 6.0\n\t */\n\tprotected DataFieldMaxValueIncrementer getStepExecutionIncrementer() {\n\t\treturn new MongoSequenceIncrementer(getMongoOperations(), \"BATCH_STEP_EXECUTION_SEQ\");\n\t}\n\n}\n"
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
