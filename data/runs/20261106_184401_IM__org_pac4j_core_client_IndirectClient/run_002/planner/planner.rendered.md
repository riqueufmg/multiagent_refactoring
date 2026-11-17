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
  "smell": "Insufficient Modularization",
  "target_type": "class",
  "target_name": "org.pac4j.core.client.IndirectClient",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261106_184401_IM__org_pac4j_core_client_IndirectClient/run_002/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "pac4j-core/src/main/java/org/pac4j/core/client/IndirectClient.java",
  "target_source_root": "pac4j-core/src/main/java",
  "target_code": "package org.pac4j.core.client;\n\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.context.session.SessionStore;\nimport org.pac4j.core.credentials.Credentials;\nimport org.pac4j.core.exception.http.HttpAction;\nimport org.pac4j.core.exception.http.RedirectionAction;\nimport org.pac4j.core.http.ajax.AjaxRequestResolver;\nimport org.pac4j.core.http.ajax.DefaultAjaxRequestResolver;\nimport org.pac4j.core.http.callback.CallbackUrlResolver;\nimport org.pac4j.core.http.callback.QueryParameterCallbackUrlResolver;\nimport org.pac4j.core.http.url.DefaultUrlResolver;\nimport org.pac4j.core.http.url.UrlResolver;\nimport org.pac4j.core.logout.LogoutActionBuilder;\nimport org.pac4j.core.logout.NoLogoutActionBuilder;\nimport org.pac4j.core.profile.UserProfile;\nimport org.pac4j.core.profile.factory.ProfileManagerFactory;\nimport org.pac4j.core.redirect.RedirectionActionBuilder;\nimport org.pac4j.core.util.HttpActionHelper;\nimport org.pac4j.core.util.Pac4jConstants;\n\nimport java.util.Optional;\n\nimport static org.pac4j.core.util.CommonHelper.*;\n\n/**\n * Indirect client: the requested protected URL is saved, the user is redirected to the identity provider for login and\n * back to the application after the sucessful authentication and finally to the originally requested URL.\n *\n * @author Jerome Leleu\n * @since 1.9.0\n */\npublic abstract class IndirectClient extends BaseClient {\n\n    public static final String ATTEMPTED_AUTHENTICATION_SUFFIX = \"$attemptedAuthentication\";\n    private static final String STATE_SESSION_PARAMETER = \"$stateSessionParameter\";\n    private static final String NONCE_SESSION_PARAMETER = \"$nonceSessionParameter\";\n    private static final String CODE_VERIFIER_SESSION_PARAMETER = \"$codeVerifierSessionParameter\";\n\n    protected String callbackUrl;\n\n    protected UrlResolver urlResolver;\n\n    protected CallbackUrlResolver callbackUrlResolver;\n\n    private AjaxRequestResolver ajaxRequestResolver;\n\n    private RedirectionActionBuilder redirectionActionBuilder;\n\n    private LogoutActionBuilder logoutActionBuilder = NoLogoutActionBuilder.INSTANCE;\n\n    private boolean checkAuthenticationAttempt = true;\n\n    @Override\n    protected void beforeInternalInit(final boolean forceReinit) {\n        // check configuration\n        assertNotBlank(\"callbackUrl\", this.callbackUrl, \"set it up either on this IndirectClient or on the global Config\");\n        if (this.urlResolver == null) {\n            this.urlResolver = new DefaultUrlResolver();\n        }\n        if (this.callbackUrlResolver == null) {\n            this.callbackUrlResolver = newDefaultCallbackUrlResolver();\n        }\n        if (this.ajaxRequestResolver == null) {\n            ajaxRequestResolver = new DefaultAjaxRequestResolver();\n        }\n        if (saveProfileInSession == null) {\n            saveProfileInSession = true;\n        }\n    }\n\n    @Override\n    protected final void afterInternalInit(final boolean forceReinit) {\n        // ensures components have been properly initialized\n        assertNotNull(\"redirectionActionBuilder\", this.redirectionActionBuilder);\n        assertNotNull(\"credentialsExtractor\", getCredentialsExtractor());\n        assertNotNull(\"authenticator\", getAuthenticator());\n        assertNotNull(\"profileCreator\", getProfileCreator());\n        assertNotNull(\"logoutActionBuilder\", this.logoutActionBuilder);\n    }\n\n    protected CallbackUrlResolver newDefaultCallbackUrlResolver() {\n        return new QueryParameterCallbackUrlResolver();\n    }\n\n    /**\n     * <p>If an authentication has already been tried for this client and has failed (<code>null</code> credentials) or if the request is\n     * an AJAX one, an unauthorized response is thrown instead of a \"redirection\".</p>\n     *\n     * @param context context\n     * @return the \"redirection\" action\n     */\n    @Override\n    public final Optional<RedirectionAction> getRedirectionAction(final WebContext context, final SessionStore sessionStore) {\n        init();\n        // it's an AJAX request -> appropriate action\n        if (ajaxRequestResolver.isAjax(context, sessionStore)) {\n            final var httpAction = ajaxRequestResolver.buildAjaxResponse(context, sessionStore, redirectionActionBuilder);\n            logger.debug(\"AJAX request detected -> returning \" + httpAction + \" for \" + context.getFullRequestURL());\n            cleanRequestedUrl(context, sessionStore);\n            throw httpAction;\n        }\n        // authentication has already been tried -> unauthorized\n        final var attemptedAuth = sessionStore.get(context, getName() + ATTEMPTED_AUTHENTICATION_SUFFIX);\n        if (attemptedAuth.isPresent() && !Pac4jConstants.EMPTY_STRING.equals(attemptedAuth.get())) {\n            logger.debug(\"authentication already attempted -> 401\");\n            cleanAttemptedAuthentication(context, sessionStore);\n            cleanRequestedUrl(context, sessionStore);\n            throw HttpActionHelper.buildUnauthenticatedAction(context);\n        }\n\n        return redirectionActionBuilder.getRedirectionAction(context, sessionStore);\n    }\n\n    private void cleanRequestedUrl(final WebContext context, final SessionStore sessionStore) {\n        logger.debug(\"clean requested URL from session\");\n        sessionStore.set(context, Pac4jConstants.REQUESTED_URL, null);\n    }\n\n    private void cleanAttemptedAuthentication(final WebContext context, final SessionStore sessionStore) {\n        logger.debug(\"clean authentication attempt from session\");\n        sessionStore.set(context, getName() + ATTEMPTED_AUTHENTICATION_SUFFIX, null);\n    }\n\n    private void saveAttemptedAuthentication(final WebContext context, final SessionStore sessionStore) {\n        if (checkAuthenticationAttempt) {\n            logger.debug(\"save authentication attempt in session\");\n            sessionStore.set(context, getName() + ATTEMPTED_AUTHENTICATION_SUFFIX, \"true\");\n        }\n    }\n\n    /**\n     * <p>Get the credentials from the web context. In some cases, a {@link HttpAction} may be thrown:</p>\n     * <ul>\n     * <li>if the <code>CasClient</code> receives a logout request, it returns a 200 HTTP status code</li>\n     * <li>for the <code>IndirectBasicAuthClient</code>, if no credentials are sent to the callback url, an unauthorized response\n     * (401 HTTP status code) is returned to request credentials through a popup.</li>\n     * </ul>\n     *\n     * @param context the current web context\n     * @return the credentials\n     */\n    @Override\n    public final Optional<Credentials> getCredentials(final WebContext context, final SessionStore sessionStore,\n                                                      final ProfileManagerFactory profileManagerFactory) {\n        init();\n        final var optCredentials = retrieveCredentials(context, sessionStore, profileManagerFactory);\n        // no credentials and no profile returned -> save this authentication has already been tried and failed\n        if (!optCredentials.isPresent() && getProfileFactoryWhenNotAuthenticated() == null) {\n            logger.debug(\"no credentials and profile returned -> remember the authentication attempt\");\n            saveAttemptedAuthentication(context, sessionStore);\n        } else {\n            cleanAttemptedAuthentication(context, sessionStore);\n        }\n        return optCredentials;\n    }\n\n    @Override\n    public final Optional<RedirectionAction> getLogoutAction(final WebContext context, final SessionStore sessionStore,\n                                                             final UserProfile currentProfile, final String targetUrl) {\n        init();\n        return logoutActionBuilder.getLogoutAction(context, sessionStore, currentProfile, targetUrl);\n    }\n\n    public String computeFinalCallbackUrl(final WebContext context) {\n        init();\n        return callbackUrlResolver.compute(this.urlResolver, this.callbackUrl, this.getName(), context);\n    }\n\n    public void setCallbackUrl(final String callbackUrl) {\n        this.callbackUrl = callbackUrl;\n    }\n\n    public String getCallbackUrl() { return this.callbackUrl; }\n\n    public UrlResolver getUrlResolver() {\n        return urlResolver;\n    }\n\n    public void setUrlResolver(final UrlResolver urlResolver) {\n        this.urlResolver = urlResolver;\n    }\n\n    public CallbackUrlResolver getCallbackUrlResolver() {\n        return callbackUrlResolver;\n    }\n\n    public void setCallbackUrlResolver(final CallbackUrlResolver callbackUrlResolver) {\n        this.callbackUrlResolver = callbackUrlResolver;\n    }\n\n    public AjaxRequestResolver getAjaxRequestResolver() {\n        return ajaxRequestResolver;\n    }\n\n    public void setAjaxRequestResolver(final AjaxRequestResolver ajaxRequestResolver) {\n        this.ajaxRequestResolver = ajaxRequestResolver;\n    }\n\n    public RedirectionActionBuilder getRedirectionActionBuilder() {\n        return redirectionActionBuilder;\n    }\n\n    protected void defaultRedirectionActionBuilder(final RedirectionActionBuilder redirectActionBuilder) {\n        if (this.redirectionActionBuilder == null) {\n            this.redirectionActionBuilder = redirectActionBuilder;\n        }\n    }\n\n    public LogoutActionBuilder getLogoutActionBuilder() {\n        return logoutActionBuilder;\n    }\n\n    protected void defaultLogoutActionBuilder(final LogoutActionBuilder logoutActionBuilder) {\n        if (this.logoutActionBuilder == null || this.logoutActionBuilder == NoLogoutActionBuilder.INSTANCE) {\n            this.logoutActionBuilder = logoutActionBuilder;\n        }\n    }\n\n    public void setRedirectionActionBuilder(final RedirectionActionBuilder redirectionActionBuilder) {\n        this.redirectionActionBuilder = redirectionActionBuilder;\n    }\n\n    public void setLogoutActionBuilder(final LogoutActionBuilder logoutActionBuilder) {\n        this.logoutActionBuilder = logoutActionBuilder;\n    }\n\n    public String getStateSessionAttributeName() {\n        return getName() + STATE_SESSION_PARAMETER;\n    }\n\n    public String getNonceSessionAttributeName() {\n        return getName() + NONCE_SESSION_PARAMETER;\n    }\n\n    public String getCodeVerifierSessionAttributeName() {\n        return getName() + CODE_VERIFIER_SESSION_PARAMETER;\n    }\n\n    public boolean isCheckAuthenticationAttempt() {\n        return checkAuthenticationAttempt;\n    }\n\n    public void setCheckAuthenticationAttempt(final boolean checkAuthenticationAttempt) {\n        this.checkAuthenticationAttempt = checkAuthenticationAttempt;\n    }\n\n    @Override\n    public String toString() {\n        return toNiceString(this.getClass(), \"name\", getName(), \"callbackUrl\", this.callbackUrl,\n                \"urlResolver\", this.urlResolver, \"callbackUrlResolver\", this.callbackUrlResolver, \"ajaxRequestResolver\",\n                this.ajaxRequestResolver, \"redirectionActionBuilder\", this.redirectionActionBuilder, \"credentialsExtractor\",\n                getCredentialsExtractor(), \"authenticator\", getAuthenticator(), \"profileCreator\", getProfileCreator(),\n                \"logoutActionBuilder\", this.logoutActionBuilder, \"authorizationGenerators\", getAuthorizationGenerators(),\n                \"checkAuthenticationAttempt\", checkAuthenticationAttempt);\n    }\n}\n"
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