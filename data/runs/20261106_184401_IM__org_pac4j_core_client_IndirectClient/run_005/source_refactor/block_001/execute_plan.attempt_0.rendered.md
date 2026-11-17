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
  "repo_path": "/data/henrique/historical-java-repro/benchmark/repositories/pac4j/repository",
  "target": {
    "smell": "IM",
    "smell_name": "Insufficient Modularization",
    "target_type": "class",
    "target_name": "org.pac4j.core.client.IndirectClient"
  },
  "block": {
    "id": 1,
    "goal": "Extract the cohesive callback URL configuration responsibilities from IndirectClient to reduce the number of fields and public accessor methods in the target class while preserving its existing public API.",
    "files": [
      "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClient.java",
      "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClientCallbackConfiguration.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.pac4j.core.client.IndirectClient",
          "org.pac4j.core.client.IndirectClientCallbackConfiguration"
        ],
        "outputs": [
          "org.pac4j.core.client.IndirectClientCallbackConfiguration"
        ],
        "details": "Extract the cohesive callback URL state and behavior consisting of callbackUrl, urlResolver, callbackUrlResolver, computeFinalCallbackUrl(WebContext), setCallbackUrl(String), getCallbackUrl(), getUrlResolver(), setUrlResolver(UrlResolver), getCallbackUrlResolver(), and setCallbackUrlResolver(CallbackUrlResolver). Keep the existing public methods on IndirectClient as delegating facade methods so subclass and external callers remain compatible. Move the corresponding initialization and default resolver handling from beforeInternalInit(boolean) into the extracted configuration while preserving the existing newDefaultCallbackUrlResolver() override behavior. Update toString() to obtain the values through the retained accessors.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClient.java",
    "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClientCallbackConfiguration.java"
  ],
  "executor_existing_files": [
    "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClient.java"
  ],
  "executor_new_files": [
    "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClientCallbackConfiguration.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClient.java",
      "exists": "true",
      "content": "package org.pac4j.core.client;\n\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.context.session.SessionStore;\nimport org.pac4j.core.credentials.Credentials;\nimport org.pac4j.core.exception.http.HttpAction;\nimport org.pac4j.core.exception.http.RedirectionAction;\nimport org.pac4j.core.http.ajax.AjaxRequestResolver;\nimport org.pac4j.core.http.callback.CallbackUrlResolver;\nimport org.pac4j.core.http.callback.QueryParameterCallbackUrlResolver;\nimport org.pac4j.core.http.url.DefaultUrlResolver;\nimport org.pac4j.core.http.url.UrlResolver;\nimport org.pac4j.core.logout.LogoutActionBuilder;\nimport org.pac4j.core.profile.UserProfile;\nimport org.pac4j.core.profile.factory.ProfileManagerFactory;\nimport org.pac4j.core.redirect.RedirectionActionBuilder;\nimport org.pac4j.core.util.HttpActionHelper;\nimport org.pac4j.core.util.Pac4jConstants;\n\nimport java.util.Optional;\n\nimport static org.pac4j.core.util.CommonHelper.*;\n\n/**\n * Indirect client: the requested protected URL is saved, the user is redirected to the identity provider for login and\n * back to the application after the sucessful authentication and finally to the originally requested URL.\n *\n * @author Jerome Leleu\n * @since 1.9.0\n */\npublic abstract class IndirectClient extends BaseClient {\n\n    public static final String ATTEMPTED_AUTHENTICATION_SUFFIX = IndirectClientAuthenticationState.ATTEMPTED_AUTHENTICATION_SUFFIX;\n\n    protected String callbackUrl;\n\n    protected UrlResolver urlResolver;\n\n    protected CallbackUrlResolver callbackUrlResolver;\n\n    private final IndirectClientActionConfiguration actionConfiguration = new IndirectClientActionConfiguration();\n\n    private final IndirectClientAuthenticationState authenticationState = new IndirectClientAuthenticationState(this);\n\n    @Override\n    protected void beforeInternalInit(final boolean forceReinit) {\n        // check configuration\n        assertNotBlank(\"callbackUrl\", this.callbackUrl, \"set it up either on this IndirectClient or on the global Config\");\n        if (this.urlResolver == null) {\n            this.urlResolver = new DefaultUrlResolver();\n        }\n        if (this.callbackUrlResolver == null) {\n            this.callbackUrlResolver = newDefaultCallbackUrlResolver();\n        }\n        actionConfiguration.init();\n        if (saveProfileInSession == null) {\n            saveProfileInSession = true;\n        }\n    }\n\n    @Override\n    protected final void afterInternalInit(final boolean forceReinit) {\n        // ensures components have been properly initialized\n        actionConfiguration.validate();\n        assertNotNull(\"credentialsExtractor\", getCredentialsExtractor());\n        assertNotNull(\"authenticator\", getAuthenticator());\n        assertNotNull(\"profileCreator\", getProfileCreator());\n    }\n\n    protected CallbackUrlResolver newDefaultCallbackUrlResolver() {\n        return new QueryParameterCallbackUrlResolver();\n    }\n\n    /**\n     * <p>If an authentication has already been tried for this client and has failed (<code>null</code> credentials) or if the request is\n     * an AJAX one, an unauthorized response is thrown instead of a \"redirection\".</p>\n     *\n     * @param context context\n     * @return the \"redirection\" action\n     */\n    @Override\n    public final Optional<RedirectionAction> getRedirectionAction(final WebContext context, final SessionStore sessionStore) {\n        init();\n        // it's an AJAX request -> appropriate action\n        if (getAjaxRequestResolver().isAjax(context, sessionStore)) {\n            final var httpAction = getAjaxRequestResolver().buildAjaxResponse(context, sessionStore, getRedirectionActionBuilder());\n            logger.debug(\"AJAX request detected -> returning \" + httpAction + \" for \" + context.getFullRequestURL());\n            cleanRequestedUrl(context, sessionStore);\n            throw httpAction;\n        }\n        // authentication has already been tried -> unauthorized\n        if (authenticationState.isAuthenticationAttempted(context, sessionStore)) {\n            logger.debug(\"authentication already attempted -> 401\");\n            authenticationState.cleanAttemptedAuthentication(context, sessionStore);\n            cleanRequestedUrl(context, sessionStore);\n            throw HttpActionHelper.buildUnauthenticatedAction(context);\n        }\n\n        return getRedirectionActionBuilder().getRedirectionAction(context, sessionStore);\n    }\n\n    private void cleanRequestedUrl(final WebContext context, final SessionStore sessionStore) {\n        logger.debug(\"clean requested URL from session\");\n        sessionStore.set(context, Pac4jConstants.REQUESTED_URL, null);\n    }\n\n    /**\n     * <p>Get the credentials from the web context. In some cases, a {@link HttpAction} may be thrown:</p>\n     * <ul>\n     * <li>if the <code>CasClient</code> receives a logout request, it returns a 200 HTTP status code</li>\n     * <li>for the <code>IndirectBasicAuthClient</code>, if no credentials are sent to the callback url, an unauthorized response\n     * (401 HTTP status code) is returned to request credentials through a popup.</li>\n     * </ul>\n     *\n     * @param context the current web context\n     * @return the credentials\n     */\n    @Override\n    public final Optional<Credentials> getCredentials(final WebContext context, final SessionStore sessionStore,\n                                                      final ProfileManagerFactory profileManagerFactory) {\n        init();\n        final var optCredentials = retrieveCredentials(context, sessionStore, profileManagerFactory);\n        // no credentials and no profile returned -> save this authentication has already been tried and failed\n        if (!optCredentials.isPresent() && getProfileFactoryWhenNotAuthenticated() == null) {\n            logger.debug(\"no credentials and profile returned -> remember the authentication attempt\");\n            authenticationState.saveAttemptedAuthentication(context, sessionStore);\n        } else {\n            authenticationState.cleanAttemptedAuthentication(context, sessionStore);\n        }\n        return optCredentials;\n    }\n\n    @Override\n    public final Optional<RedirectionAction> getLogoutAction(final WebContext context, final SessionStore sessionStore,\n                                                             final UserProfile currentProfile, final String targetUrl) {\n        init();\n        return getLogoutActionBuilder().getLogoutAction(context, sessionStore, currentProfile, targetUrl);\n    }\n\n    public String computeFinalCallbackUrl(final WebContext context) {\n        init();\n        return callbackUrlResolver.compute(this.urlResolver, this.callbackUrl, this.getName(), context);\n    }\n\n    public void setCallbackUrl(final String callbackUrl) {\n        this.callbackUrl = callbackUrl;\n    }\n\n    public String getCallbackUrl() { return this.callbackUrl; }\n\n    public UrlResolver getUrlResolver() {\n        return urlResolver;\n    }\n\n    public void setUrlResolver(final UrlResolver urlResolver) {\n        this.urlResolver = urlResolver;\n    }\n\n    public CallbackUrlResolver getCallbackUrlResolver() {\n        return callbackUrlResolver;\n    }\n\n    public void setCallbackUrlResolver(final CallbackUrlResolver callbackUrlResolver) {\n        this.callbackUrlResolver = callbackUrlResolver;\n    }\n\n    public AjaxRequestResolver getAjaxRequestResolver() {\n        return actionConfiguration.getAjaxRequestResolver();\n    }\n\n    public void setAjaxRequestResolver(final AjaxRequestResolver ajaxRequestResolver) {\n        actionConfiguration.setAjaxRequestResolver(ajaxRequestResolver);\n    }\n\n    public RedirectionActionBuilder getRedirectionActionBuilder() {\n        return actionConfiguration.getRedirectionActionBuilder();\n    }\n\n    protected void defaultRedirectionActionBuilder(final RedirectionActionBuilder redirectActionBuilder) {\n        actionConfiguration.defaultRedirectionActionBuilder(redirectActionBuilder);\n    }\n\n    public LogoutActionBuilder getLogoutActionBuilder() {\n        return actionConfiguration.getLogoutActionBuilder();\n    }\n\n    protected void defaultLogoutActionBuilder(final LogoutActionBuilder logoutActionBuilder) {\n        actionConfiguration.defaultLogoutActionBuilder(logoutActionBuilder);\n    }\n\n    public void setRedirectionActionBuilder(final RedirectionActionBuilder redirectionActionBuilder) {\n        actionConfiguration.setRedirectionActionBuilder(redirectionActionBuilder);\n    }\n\n    public void setLogoutActionBuilder(final LogoutActionBuilder logoutActionBuilder) {\n        actionConfiguration.setLogoutActionBuilder(logoutActionBuilder);\n    }\n\n    public String getStateSessionAttributeName() {\n        return authenticationState.getStateSessionAttributeName();\n    }\n\n    public String getNonceSessionAttributeName() {\n        return authenticationState.getNonceSessionAttributeName();\n    }\n\n    public String getCodeVerifierSessionAttributeName() {\n        return authenticationState.getCodeVerifierSessionAttributeName();\n    }\n\n    public boolean isCheckAuthenticationAttempt() {\n        return authenticationState.isCheckAuthenticationAttempt();\n    }\n\n    public void setCheckAuthenticationAttempt(final boolean checkAuthenticationAttempt) {\n        authenticationState.setCheckAuthenticationAttempt(checkAuthenticationAttempt);\n    }\n\n    @Override\n    public String toString() {\n        return toNiceString(this.getClass(), \"name\", getName(), \"callbackUrl\", this.callbackUrl,\n                \"urlResolver\", this.urlResolver, \"callbackUrlResolver\", this.callbackUrlResolver, \"ajaxRequestResolver\",\n                this.getAjaxRequestResolver(), \"redirectionActionBuilder\", this.getRedirectionActionBuilder(), \"credentialsExtractor\",\n                getCredentialsExtractor(), \"authenticator\", getAuthenticator(), \"profileCreator\", getProfileCreator(),\n                \"logoutActionBuilder\", this.getLogoutActionBuilder(), \"authorizationGenerators\", getAuthorizationGenerators(),\n                \"checkAuthenticationAttempt\", isCheckAuthenticationAttempt());\n    }\n}\n"
    },
    {
      "path": "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClientCallbackConfiguration.java",
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
