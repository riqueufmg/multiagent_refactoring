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
    "target_name": "org.pac4j.cas.config.CasConfiguration"
  },
  "block": {
    "id": 2,
    "goal": "Extract logout lifecycle and logout-specific state from CasConfiguration to reduce the number of unrelated public methods and simplify internal initialization.",
    "files": [
      "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
      "pac4j-cas/src/main/java/org/pac4j/cas/config/CasLogoutConfiguration.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.initializeLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.getLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.findLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.setLogoutHandler(LogoutHandler)",
          "org.pac4j.cas.config.CasConfiguration.getPostLogoutUrlParameter()",
          "org.pac4j.cas.config.CasConfiguration.setPostLogoutUrlParameter(String)",
          "org.pac4j.cas.config.CasConfiguration.logoutHandler",
          "org.pac4j.cas.config.CasConfiguration.postLogoutUrlParameter"
        ],
        "outputs": [
          "org.pac4j.cas.config.CasLogoutConfiguration",
          "org.pac4j.cas.config.CasConfiguration"
        ],
        "details": "Create CasLogoutConfiguration in the same package. Move logoutHandler, postLogoutUrlParameter, initializeLogoutHandler, and their accessors into the extracted class. Retain CasConfiguration methods with their existing signatures as delegating adapters. Preserve the existing default initialization with DefaultLogoutHandler and the init behavior of findLogoutHandler.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.internalInit(boolean)",
          "org.pac4j.cas.config.CasConfiguration.initializeLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.getLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.findLogoutHandler()",
          "org.pac4j.cas.config.CasConfiguration.setLogoutHandler(LogoutHandler)",
          "org.pac4j.cas.config.CasConfiguration.getPostLogoutUrlParameter()",
          "org.pac4j.cas.config.CasConfiguration.setPostLogoutUrlParameter(String)",
          "org.pac4j.cas.config.CasConfiguration.toString()"
        ],
        "outputs": [
          "org.pac4j.cas.config.CasConfiguration"
        ],
        "details": "Add a CasLogoutConfiguration instance to CasConfiguration, delegate logout initialization and accessors to it, and update internalInit and toString to obtain logout values through the extracted component. Preserve the existing public API and output values.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasLogoutConfiguration.java"
  ],
  "executor_existing_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java"
  ],
  "executor_new_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasLogoutConfiguration.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
      "exists": "true",
      "content": "package org.pac4j.cas.config;\n\nimport org.apereo.cas.client.validation.*;\nimport org.pac4j.cas.client.CasProxyReceptor;\nimport org.pac4j.core.client.config.BaseClientConfiguration;\nimport org.pac4j.core.logout.handler.LogoutHandler;\nimport org.pac4j.core.logout.handler.DefaultLogoutHandler;\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.exception.TechnicalException;\nimport org.pac4j.core.http.url.UrlResolver;\nimport org.pac4j.core.util.CommonHelper;\n\nimport javax.net.ssl.HostnameVerifier;\nimport javax.net.ssl.SSLSocketFactory;\nimport java.nio.charset.StandardCharsets;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\n/**\n * CAS configuration.\n *\n * @author Jerome Leleu\n * @since 1.9.2\n */\npublic class CasConfiguration extends BaseClientConfiguration {\n\n    public static final String TICKET_PARAMETER = \"ticket\";\n\n    public static final String SERVICE_PARAMETER = \"service\";\n\n    public final static String LOGOUT_REQUEST_PARAMETER = \"logoutRequest\";\n\n    public final static String SESSION_INDEX_TAG = \"SessionIndex\";\n\n    public final static String RELAY_STATE_PARAMETER = \"RelayState\";\n\n    private String encoding = StandardCharsets.UTF_8.name();\n\n    private final CasProtocolConfiguration protocolConfiguration = new CasProtocolConfiguration();\n\n    private LogoutHandler logoutHandler;\n\n    private CasProxyReceptor proxyReceptor;\n\n    private String postLogoutUrlParameter = SERVICE_PARAMETER;\n\n    /* Map containing user defined parameters */\n    private Map<String, String> customParams = new HashMap<>();\n\n    private String method;\n\n    private final CasSecurityConfiguration securityConfiguration = new CasSecurityConfiguration();\n\n    private final CasTicketValidatorConfiguration ticketValidatorConfiguration =\n            new CasTicketValidatorConfiguration(this, securityConfiguration);\n\n    private CasUrlConfiguration urlConfiguration = new CasUrlConfiguration();\n\n    public CasConfiguration() {}\n\n    public CasConfiguration(final String loginUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n    }\n\n    public CasConfiguration(final String loginUrl, final CasProtocol protocol) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n        this.protocolConfiguration.setProtocol(protocol);\n    }\n\n    public CasConfiguration(final String loginUrl, final String prefixUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl, prefixUrl);\n    }\n\n    @Override\n    protected void internalInit(final boolean forceReinit) {\n        if (CommonHelper.isBlank(getLoginUrl()) && CommonHelper.isBlank(getPrefixUrl()) && CommonHelper.isBlank(getRestUrl())) {\n            throw new TechnicalException(\"loginUrl, prefixUrl and restUrl cannot be all blank\");\n        }\n\n        initializeClientConfiguration();\n\n        initializeLogoutHandler();\n\n        securityConfiguration.internalInit();\n    }\n\n    protected void initializeClientConfiguration() {\n        urlConfiguration.initializeClientConfiguration();\n    }\n\n    protected void initializeLogoutHandler() {\n        if (this.logoutHandler == null) {\n            this.logoutHandler = new DefaultLogoutHandler();\n        }\n    }\n\n    public TicketValidator retrieveTicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.retrieveTicketValidator(context);\n    }\n\n    protected TicketValidator buildSAMLTicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildSAMLTicketValidator(context);\n    }\n\n    protected void addPrivateKey(final Cas20ServiceTicketValidator validator) {\n        ticketValidatorConfiguration.addPrivateKey(validator);\n    }\n\n    protected TicketValidator buildCas30ProxyTicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildCas30ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas30TicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildCas30TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20ProxyTicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildCas20ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20TicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildCas20TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas10TicketValidator(final WebContext context) {\n        return ticketValidatorConfiguration.buildCas10TicketValidator(context);\n    }\n\n    public String getEncoding() {\n        return encoding;\n    }\n\n    public void setEncoding(final String encoding) {\n        this.encoding = encoding;\n    }\n\n    public String computeFinalLoginUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalLoginUrl(context);\n    }\n\n    public String getLoginUrl() {\n        return urlConfiguration.getLoginUrl();\n    }\n\n    public void setLoginUrl(final String loginUrl) {\n        urlConfiguration.setLoginUrl(loginUrl);\n    }\n\n    public String getPrefixUrl() {\n        return urlConfiguration.getPrefixUrl();\n    }\n\n    public String computeFinalPrefixUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalPrefixUrl(context);\n    }\n\n    public void setPrefixUrl(final String prefixUrl) {\n        urlConfiguration.setPrefixUrl(prefixUrl);\n    }\n\n    public HostnameVerifier getHostnameVerifier() {\n        return securityConfiguration.getHostnameVerifier();\n    }\n\n    public void setHostnameVerifier(final HostnameVerifier hostnameVerifier) {\n        securityConfiguration.setHostnameVerifier(hostnameVerifier);\n    }\n\n    public SSLSocketFactory getSslSocketFactory() {\n        return securityConfiguration.getSslSocketFactory();\n    }\n\n    public void setSslSocketFactory(final SSLSocketFactory sslSocketFactory) {\n        securityConfiguration.setSslSocketFactory(sslSocketFactory);\n    }\n\n    public Map<String, String> getCustomParams() {\n        return customParams;\n    }\n\n    public void setCustomParams(final Map<String, String> customParams) {\n        this.customParams = customParams;\n    }\n\n    public long getTimeTolerance() {\n        return protocolConfiguration.getTimeTolerance();\n    }\n\n    public void setTimeTolerance(final long timeTolerance) {\n        protocolConfiguration.setTimeTolerance(timeTolerance);\n    }\n\n    public CasProtocol getProtocol() {\n        return protocolConfiguration.getProtocol();\n    }\n\n    public void setProtocol(final CasProtocol protocol) {\n        protocolConfiguration.setProtocol(protocol);\n    }\n\n    public boolean isRenew() {\n        return protocolConfiguration.isRenew();\n    }\n\n    public void setRenew(final boolean renew) {\n        protocolConfiguration.setRenew(renew);\n    }\n\n    public boolean isGateway() {\n        return protocolConfiguration.isGateway();\n    }\n\n    public void setGateway(final boolean gateway) {\n        protocolConfiguration.setGateway(gateway);\n    }\n\n    public boolean isAcceptAnyProxy() {\n        return protocolConfiguration.isAcceptAnyProxy();\n    }\n\n    public void setAcceptAnyProxy(final boolean acceptAnyProxy) {\n        protocolConfiguration.setAcceptAnyProxy(acceptAnyProxy);\n    }\n\n    public ProxyList getAllowedProxyChains() {\n        return protocolConfiguration.getAllowedProxyChains();\n    }\n\n    public void setAllowedProxyChains(final ProxyList allowedProxyChains) {\n        protocolConfiguration.setAllowedProxyChains(allowedProxyChains);\n    }\n\n    public void setAllowedProxies(final List<String> allowedProxies) {\n        protocolConfiguration.setAllowedProxies(allowedProxies);\n    }\n\n    public LogoutHandler getLogoutHandler() {\n        return logoutHandler;\n    }\n\n    public LogoutHandler findLogoutHandler() {\n        init();\n        return logoutHandler;\n    }\n\n    public void setLogoutHandler(final LogoutHandler logoutHandler) {\n        this.logoutHandler = logoutHandler;\n    }\n\n    public TicketValidator getDefaultTicketValidator() {\n        return ticketValidatorConfiguration.getDefaultTicketValidator();\n    }\n\n    public void setDefaultTicketValidator(final TicketValidator defaultTicketValidator) {\n        ticketValidatorConfiguration.setDefaultTicketValidator(defaultTicketValidator);\n    }\n\n    public CasProxyReceptor getProxyReceptor() {\n        return proxyReceptor;\n    }\n\n    public void setProxyReceptor(final CasProxyReceptor proxyReceptor) {\n        this.proxyReceptor = proxyReceptor;\n    }\n\n    public String getPostLogoutUrlParameter() {\n        return postLogoutUrlParameter;\n    }\n\n    public void setPostLogoutUrlParameter(final String postLogoutUrlParameter) {\n        this.postLogoutUrlParameter = postLogoutUrlParameter;\n    }\n\n    public String getRestUrl() {\n        return urlConfiguration.getRestUrl();\n    }\n\n    public void setRestUrl(final String restUrl) {\n        urlConfiguration.setRestUrl(restUrl);\n    }\n\n    public String computeFinalRestUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalRestUrl(context);\n    }\n\n    public UrlResolver getUrlResolver() {\n        return urlConfiguration.getUrlResolver();\n    }\n\n    public void setUrlResolver(final UrlResolver urlResolver) {\n        urlConfiguration.setUrlResolver(urlResolver);\n    }\n\n    public void addCustomParam(final String name, final String value) {\n        this.customParams.put(name, value);\n    }\n\n    public String getMethod() {\n        return method;\n    }\n\n    public void setMethod(final String method) {\n        this.method = method;\n    }\n\n    public String getPrivateKeyPath() {\n        return securityConfiguration.getPrivateKeyPath();\n    }\n\n    public void setPrivateKeyPath(final String privateKeyPath) {\n        securityConfiguration.setPrivateKeyPath(privateKeyPath);\n    }\n\n    public String getPrivateKeyAlgorithm() {\n        return securityConfiguration.getPrivateKeyAlgorithm();\n    }\n\n    public void setPrivateKeyAlgorithm(final String privateKeyAlgorithm) {\n        securityConfiguration.setPrivateKeyAlgorithm(privateKeyAlgorithm);\n    }\n\n    @Override\n    public String toString() {\n        return CommonHelper.toNiceString(this.getClass(), \"loginUrl\", this.getLoginUrl(), \"prefixUrl\", this.getPrefixUrl(), \"restUrl\", this.getRestUrl(),\n                \"protocol\", this.getProtocol(), \"renew\", this.isRenew(), \"gateway\", this.isGateway(), \"encoding\", this.encoding,\n                \"logoutHandler\", this.logoutHandler, \"acceptAnyProxy\", this.isAcceptAnyProxy(), \"allowedProxyChains\", this.getAllowedProxyChains(),\n                \"proxyReceptor\", this.proxyReceptor, \"timeTolerance\", this.getTimeTolerance(), \"postLogoutUrlParameter\",\n                this.postLogoutUrlParameter, \"defaultTicketValidator\", this.getDefaultTicketValidator(), \"urlResolver\", this.getUrlResolver(),\n                \"method\", this.method, \"privateKeyPath\", this.getPrivateKeyPath(), \"privateKeyAlgorithm\", this.getPrivateKeyAlgorithm());\n    }\n}\n"
    },
    {
      "path": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasLogoutConfiguration.java",
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
