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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/dropwizard/repository",
  "target": {
    "smell": "GC",
    "smell_name": "God Component",
    "target_type": "package",
    "target_name": "io.dropwizard.jersey.optional"
  },
  "block": {
    "id": 1,
    "goal": "Move the cohesive optional exception-handling cluster into a dedicated subpackage.",
    "files": [
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalException.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalExceptionMapper.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalNoContentExceptionMapper.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleMessageBodyWriter.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntMessageBodyWriter.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongMessageBodyWriter.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalMessageBodyWriter.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalException.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalExceptionMapper.java",
      "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalNoContentExceptionMapper.java"
    ],
    "ops": [
      {
        "op": "CREATE_PACKAGE",
        "inputs": [],
        "outputs": [
          "io.dropwizard.jersey.optional.exception"
        ],
        "details": "Create the destination subpackage if it does not exist.",
        "risk": "low",
        "api_change": false
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.EmptyOptionalException"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.exception.EmptyOptionalException"
        ],
        "details": "Move the exception class to the dedicated optional exception subpackage.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.EmptyOptionalExceptionMapper"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.exception.EmptyOptionalExceptionMapper"
        ],
        "details": "Move the exception mapper alongside the exception it handles.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "MOVE_CLASS",
        "inputs": [
          "io.dropwizard.jersey.optional.EmptyOptionalNoContentExceptionMapper"
        ],
        "outputs": [
          "io.dropwizard.jersey.optional.exception.EmptyOptionalNoContentExceptionMapper"
        ],
        "details": "Move the no-content exception mapper alongside the exception it handles.",
        "risk": "medium",
        "api_change": true
      },
      {
        "op": "UPDATE_VISIBILITY",
        "inputs": [
          "io.dropwizard.jersey.optional.OptionalDoubleMessageBodyWriter",
          "io.dropwizard.jersey.optional.OptionalIntMessageBodyWriter",
          "io.dropwizard.jersey.optional.OptionalLongMessageBodyWriter",
          "io.dropwizard.jersey.optional.OptionalMessageBodyWriter",
          "io.dropwizard.jersey.optional.exception.EmptyOptionalException",
          "io.dropwizard.jersey.optional.exception.EmptyOptionalExceptionMapper",
          "io.dropwizard.jersey.optional.exception.EmptyOptionalNoContentExceptionMapper"
        ],
        "outputs": [],
        "details": "After moving the whole cluster to the destination package, update only the minimum required visibility in moved classes and related remaining classes so the project can compile. Do not change behavior. Do not move additional classes.",
        "risk": "medium",
        "api_change": true
      }
    ]
  },
  "allowed_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalException.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalNoContentExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalException.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalNoContentExceptionMapper.java"
  ],
  "executor_existing_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalException.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalNoContentExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongMessageBodyWriter.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalMessageBodyWriter.java"
  ],
  "executor_new_files": [
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalException.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalExceptionMapper.java",
    "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalNoContentExceptionMapper.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalException.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalExceptionMapper.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/EmptyOptionalNoContentExceptionMapper.java",
      "exists": "false",
      "content": ""
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalDoubleMessageBodyWriter.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\n\nimport javax.ws.rs.Produces;\nimport javax.ws.rs.core.MediaType;\nimport javax.ws.rs.core.MultivaluedMap;\nimport javax.ws.rs.ext.MessageBodyWriter;\nimport javax.ws.rs.ext.Provider;\nimport java.io.IOException;\nimport java.io.OutputStream;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.nio.charset.StandardCharsets;\nimport java.util.OptionalDouble;\n\n@Provider\n@Produces(MediaType.WILDCARD)\npublic class OptionalDoubleMessageBodyWriter implements MessageBodyWriter<OptionalDouble> {\n    // Jersey ignores this\n    @Override\n    public long getSize(OptionalDouble entity, Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return -1;\n    }\n\n    @Override\n    public boolean isWriteable(Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return OptionalDouble.class.isAssignableFrom(type);\n    }\n\n    @Override\n    public void writeTo(OptionalDouble entity,\n                        Class<?> type,\n                        Type genericType,\n                        Annotation[] annotations,\n                        MediaType mediaType,\n                        MultivaluedMap<String, Object> httpHeaders,\n                        OutputStream entityStream) throws IOException {\n        if (!entity.isPresent()) {\n            throw EmptyOptionalException.INSTANCE;\n        }\n\n        entityStream.write(Double.toString(entity.getAsDouble()).getBytes(StandardCharsets.US_ASCII));\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalIntMessageBodyWriter.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\n\nimport javax.ws.rs.Produces;\nimport javax.ws.rs.core.MediaType;\nimport javax.ws.rs.core.MultivaluedMap;\nimport javax.ws.rs.ext.MessageBodyWriter;\nimport javax.ws.rs.ext.Provider;\nimport java.io.IOException;\nimport java.io.OutputStream;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.nio.charset.StandardCharsets;\nimport java.util.OptionalInt;\n\n@Provider\n@Produces(MediaType.WILDCARD)\npublic class OptionalIntMessageBodyWriter implements MessageBodyWriter<OptionalInt> {\n    // Jersey ignores this\n    @Override\n    public long getSize(OptionalInt entity, Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return -1;\n    }\n\n    @Override\n    public boolean isWriteable(Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return OptionalInt.class.isAssignableFrom(type);\n    }\n\n    @Override\n    public void writeTo(OptionalInt entity,\n                        Class<?> type,\n                        Type genericType,\n                        Annotation[] annotations,\n                        MediaType mediaType,\n                        MultivaluedMap<String, Object> httpHeaders,\n                        OutputStream entityStream) throws IOException {\n        if (!entity.isPresent()) {\n            throw EmptyOptionalException.INSTANCE;\n        }\n\n        entityStream.write(Integer.toString(entity.getAsInt()).getBytes(StandardCharsets.US_ASCII));\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalLongMessageBodyWriter.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\n\nimport javax.ws.rs.Produces;\nimport javax.ws.rs.core.MediaType;\nimport javax.ws.rs.core.MultivaluedMap;\nimport javax.ws.rs.ext.MessageBodyWriter;\nimport javax.ws.rs.ext.Provider;\nimport java.io.IOException;\nimport java.io.OutputStream;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.Type;\nimport java.nio.charset.StandardCharsets;\nimport java.util.OptionalLong;\n\n@Provider\n@Produces(MediaType.WILDCARD)\npublic class OptionalLongMessageBodyWriter implements MessageBodyWriter<OptionalLong> {\n    // Jersey ignores this\n    @Override\n    public long getSize(OptionalLong entity, Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return -1;\n    }\n\n    @Override\n    public boolean isWriteable(Class<?> type, Type genericType, Annotation[] annotations, MediaType mediaType) {\n        return OptionalLong.class.isAssignableFrom(type);\n    }\n\n    @Override\n    public void writeTo(OptionalLong entity,\n                        Class<?> type,\n                        Type genericType,\n                        Annotation[] annotations,\n                        MediaType mediaType,\n                        MultivaluedMap<String, Object> httpHeaders,\n                        OutputStream entityStream) throws IOException {\n        if (!entity.isPresent()) {\n            throw EmptyOptionalException.INSTANCE;\n        }\n\n        entityStream.write(Long.toString(entity.getAsLong()).getBytes(StandardCharsets.US_ASCII));\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/OptionalMessageBodyWriter.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\nimport org.glassfish.jersey.message.MessageBodyWorkers;\n\nimport javax.annotation.Nullable;\nimport javax.inject.Inject;\nimport javax.ws.rs.Produces;\nimport javax.ws.rs.core.MediaType;\nimport javax.ws.rs.core.MultivaluedMap;\nimport javax.ws.rs.ext.MessageBodyWriter;\nimport javax.ws.rs.ext.Provider;\nimport java.io.IOException;\nimport java.io.OutputStream;\nimport java.lang.annotation.Annotation;\nimport java.lang.reflect.ParameterizedType;\nimport java.lang.reflect.Type;\nimport java.util.Optional;\n\nimport static java.util.Objects.requireNonNull;\n\n@Provider\n@Produces(MediaType.WILDCARD)\npublic class OptionalMessageBodyWriter implements MessageBodyWriter<Optional<?>> {\n\n    @Inject\n    @Nullable\n    private javax.inject.Provider<MessageBodyWorkers> mbw;\n\n    // Jersey ignores this\n    @Override\n    public long getSize(Optional<?> entity, Class<?> type, Type genericType,\n                        Annotation[] annotations, MediaType mediaType) {\n        return 0;\n    }\n\n    @Override\n    public boolean isWriteable(Class<?> type, Type genericType,\n                               Annotation[] annotations, MediaType mediaType) {\n        return Optional.class.isAssignableFrom(type);\n    }\n\n    @SuppressWarnings({\"rawtypes\", \"unchecked\"})\n    @Override\n    public void writeTo(Optional<?> entity,\n                        Class<?> type,\n                        Type genericType,\n                        Annotation[] annotations,\n                        MediaType mediaType,\n                        MultivaluedMap<String, Object> httpHeaders,\n                        OutputStream entityStream)\n            throws IOException {\n        if (!entity.isPresent()) {\n            throw EmptyOptionalException.INSTANCE;\n        }\n\n        final Type innerGenericType = (genericType instanceof ParameterizedType) ?\n            ((ParameterizedType) genericType).getActualTypeArguments()[0] : entity.get().getClass();\n\n        final MessageBodyWriter writer = requireNonNull(mbw).get().getMessageBodyWriter(entity.get().getClass(),\n            innerGenericType, annotations, mediaType);\n        writer.writeTo(entity.get(), entity.get().getClass(),\n            innerGenericType, annotations, mediaType, httpHeaders, entityStream);\n    }\n\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalException.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.exception;\n\n/**\n * An exception thrown when a resource endpoint attempts to write out an\n * optional that is empty.\n */\npublic class EmptyOptionalException extends RuntimeException {\n    /**\n     * Auto-generated by Eclipse.\n     */\n    private static final long serialVersionUID = -3398853218754085781L;\n\n    public static final EmptyOptionalException INSTANCE = new EmptyOptionalException();\n\n    private EmptyOptionalException() { }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalExceptionMapper.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.exception;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\n\nimport javax.ws.rs.core.Response;\nimport javax.ws.rs.ext.ExceptionMapper;\n\n/**\n * The default response when an empty optional is returned, is to respond with\n * a 404 NOT FOUND response.\n */\npublic class EmptyOptionalExceptionMapper implements ExceptionMapper<EmptyOptionalException> {\n    @Override\n    public Response toResponse(EmptyOptionalException exception) {\n        return Response.status(Response.Status.NOT_FOUND).build();\n    }\n}\n"
    },
    {
      "path": "dropwizard-jersey/src/main/java/io/dropwizard/jersey/optional/exception/EmptyOptionalNoContentExceptionMapper.java",
      "exists": "true",
      "content": "package io.dropwizard.jersey.optional.exception;\n\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalException;\nimport io.dropwizard.jersey.optional.exception.EmptyOptionalExceptionMapper;\n\nimport javax.ws.rs.core.Response;\nimport javax.ws.rs.ext.ExceptionMapper;\nimport java.util.Optional;\n\n/**\n * Returns a 204 for {@link Optional#empty()}\n * {@link EmptyOptionalExceptionMapper} returns a 404 for {@link Optional#empty()}\n *\n * @since 2.0\n */\npublic class EmptyOptionalNoContentExceptionMapper implements ExceptionMapper<EmptyOptionalException> {\n    @Override\n    public Response toResponse(EmptyOptionalException exception) {\n        return Response.noContent().build();\n    }\n}\n"
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
