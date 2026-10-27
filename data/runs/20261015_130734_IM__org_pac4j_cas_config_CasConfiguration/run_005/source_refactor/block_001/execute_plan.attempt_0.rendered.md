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
    "id": 1,
    "goal": "Reduce the public-method count in CasConfiguration by relocating the cohesive URL configuration API to CasUrlConfiguration.",
    "files": [
      "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java"
    ],
    "ops": [
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.getLoginUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.getLoginUrl()"
        ],
        "outputs": [],
        "details": "Move the login URL accessor to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.setLoginUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.setLoginUrl()"
        ],
        "outputs": [],
        "details": "Move the login URL mutator to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.computeFinalLoginUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.computeFinalLoginUrl()"
        ],
        "outputs": [],
        "details": "Move final login URL computation to CasUrlConfiguration while preserving initialization behavior.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.getPrefixUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.getPrefixUrl()"
        ],
        "outputs": [],
        "details": "Move the prefix URL accessor to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.setPrefixUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.setPrefixUrl()"
        ],
        "outputs": [],
        "details": "Move the prefix URL mutator to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.computeFinalPrefixUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.computeFinalPrefixUrl()"
        ],
        "outputs": [],
        "details": "Move final prefix URL computation to CasUrlConfiguration while preserving initialization behavior.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.getRestUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.getRestUrl()"
        ],
        "outputs": [],
        "details": "Move the REST URL accessor to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.setRestUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.setRestUrl()"
        ],
        "outputs": [],
        "details": "Move the REST URL mutator to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.computeFinalRestUrl()",
          "org.pac4j.cas.config.CasUrlConfiguration.computeFinalRestUrl()"
        ],
        "outputs": [],
        "details": "Move final REST URL computation to CasUrlConfiguration while preserving initialization behavior.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.getUrlResolver()",
          "org.pac4j.cas.config.CasUrlConfiguration.getUrlResolver()"
        ],
        "outputs": [],
        "details": "Move the URL resolver accessor to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "MOVE_METHOD",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.setUrlResolver()",
          "org.pac4j.cas.config.CasUrlConfiguration.setUrlResolver()"
        ],
        "outputs": [],
        "details": "Move the URL resolver mutator to the existing URL configuration component.",
        "risk": "medium"
      },
      {
        "op": "UPDATE_CALL_SITES",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.getLoginUrl()",
          "org.pac4j.cas.config.CasConfiguration.setLoginUrl()",
          "org.pac4j.cas.config.CasConfiguration.computeFinalLoginUrl()",
          "org.pac4j.cas.config.CasConfiguration.getPrefixUrl()",
          "org.pac4j.cas.config.CasConfiguration.setPrefixUrl()",
          "org.pac4j.cas.config.CasConfiguration.computeFinalPrefixUrl()",
          "org.pac4j.cas.config.CasConfiguration.getRestUrl()",
          "org.pac4j.cas.config.CasConfiguration.setRestUrl()",
          "org.pac4j.cas.config.CasConfiguration.computeFinalRestUrl()",
          "org.pac4j.cas.config.CasConfiguration.getUrlResolver()",
          "org.pac4j.cas.config.CasConfiguration.setUrlResolver()"
        ],
        "outputs": [],
        "details": "Update callers to use the corresponding methods on CasUrlConfiguration.",
        "risk": "high"
      }
    ]
  },
  "allowed_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java"
  ],
  "executor_existing_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java"
  ],
  "executor_new_files": [],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
      "exists": "true",
      "content": "package org.pac4j.cas.config;\n\nimport org.apereo.cas.client.validation.ProxyList;\nimport org.apereo.cas.client.validation.TicketValidator;\nimport org.pac4j.cas.client.CasProxyReceptor;\nimport org.pac4j.core.client.config.BaseClientConfiguration;\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.exception.TechnicalException;\nimport org.pac4j.core.logout.handler.DefaultLogoutHandler;\nimport org.pac4j.core.logout.handler.LogoutHandler;\nimport org.pac4j.core.util.CommonHelper;\n\nimport javax.net.ssl.HostnameVerifier;\nimport javax.net.ssl.SSLSocketFactory;\nimport java.nio.charset.StandardCharsets;\nimport java.security.PrivateKey;\nimport java.util.ArrayList;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\n/**\n * CAS configuration.\n *\n * @author Jerome Leleu\n * @since 1.9.2\n */\npublic class CasConfiguration extends BaseClientConfiguration {\n\n    public static final String TICKET_PARAMETER = \"ticket\";\n\n    public static final String SERVICE_PARAMETER = \"service\";\n\n    public final static String LOGOUT_REQUEST_PARAMETER = \"logoutRequest\";\n\n    public final static String SESSION_INDEX_TAG = \"SessionIndex\";\n\n    public final static String RELAY_STATE_PARAMETER = \"RelayState\";\n\n    private String encoding = StandardCharsets.UTF_8.name();\n\n    private long timeTolerance = 1000L;\n\n    private CasProtocol protocol = CasProtocol.CAS30;\n\n    private boolean renew = false;\n\n    private boolean gateway = false;\n\n    private boolean acceptAnyProxy = false;\n\n    private ProxyList allowedProxyChains = new ProxyList();\n\n    private LogoutHandler logoutHandler;\n\n    private TicketValidator defaultTicketValidator;\n\n    private CasProxyReceptor proxyReceptor;\n\n    private String postLogoutUrlParameter = SERVICE_PARAMETER;\n\n    /* Map containing user defined parameters */\n    private Map<String, String> customParams = new HashMap<>();\n\n    private String method;\n\n    private final CasSecurityConfiguration securityConfiguration = new CasSecurityConfiguration();\n\n    private final CasUrlConfiguration urlConfiguration = new CasUrlConfiguration();\n\n    public CasConfiguration() {}\n\n    public CasConfiguration(final String loginUrl) {\n        setLoginUrl(loginUrl);\n    }\n\n    public CasConfiguration(final String loginUrl, final CasProtocol protocol) {\n        setLoginUrl(loginUrl);\n        this.protocol = protocol;\n    }\n\n    public CasConfiguration(final String loginUrl, final String prefixUrl) {\n        setLoginUrl(loginUrl);\n        setPrefixUrl(prefixUrl);\n    }\n\n    @Override\n    protected void internalInit(final boolean forceReinit) {\n        if (CommonHelper.isBlank(getLoginUrl()) && CommonHelper.isBlank(getPrefixUrl()) && CommonHelper.isBlank(getRestUrl())) {\n            throw new TechnicalException(\"loginUrl, prefixUrl and restUrl cannot be all blank\");\n        }\n\n        initializeClientConfiguration();\n\n        initializeLogoutHandler();\n\n        securityConfiguration.initializePrivateKey();\n    }\n\n    protected void initializeClientConfiguration() {\n        urlConfiguration.initializeClientConfiguration();\n    }\n\n    protected void initializeLogoutHandler() {\n        if (this.logoutHandler == null) {\n            this.logoutHandler = new DefaultLogoutHandler();\n        }\n    }\n\n    public TicketValidator retrieveTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).retrieveTicketValidator(context);\n    }\n\n    PrivateKey getPrivateKey() {\n        return securityConfiguration.getPrivateKey();\n    }\n\n    public String getEncoding() {\n        return encoding;\n    }\n\n    public void setEncoding(final String encoding) {\n        this.encoding = encoding;\n    }\n\n    public String computeFinalLoginUrl(final WebContext context) {\n        init();\n\n        return urlConfiguration.computeFinalLoginUrl(context);\n    }\n\n    public String getLoginUrl() {\n        return urlConfiguration.getLoginUrl();\n    }\n\n    public void setLoginUrl(final String loginUrl) {\n        urlConfiguration.setLoginUrl(loginUrl);\n    }\n\n    public String getPrefixUrl() {\n        return urlConfiguration.getPrefixUrl();\n    }\n\n    public String computeFinalPrefixUrl(final WebContext context) {\n        init();\n\n        return urlConfiguration.computeFinalPrefixUrl(context);\n    }\n\n    public void setPrefixUrl(final String prefixUrl) {\n        urlConfiguration.setPrefixUrl(prefixUrl);\n    }\n\n    public HostnameVerifier getHostnameVerifier() {\n        return securityConfiguration.getHostnameVerifier();\n    }\n\n    public void setHostnameVerifier(final HostnameVerifier hostnameVerifier) {\n        securityConfiguration.setHostnameVerifier(hostnameVerifier);\n    }\n\n    public SSLSocketFactory getSslSocketFactory() {\n        return securityConfiguration.getSslSocketFactory();\n    }\n\n    public void setSslSocketFactory(final SSLSocketFactory sslSocketFactory) {\n        securityConfiguration.setSslSocketFactory(sslSocketFactory);\n    }\n\n    public Map<String, String> getCustomParams() {\n        return customParams;\n    }\n\n    public void setCustomParams(final Map<String, String> customParams) {\n        this.customParams = customParams;\n    }\n\n    public long getTimeTolerance() {\n        return timeTolerance;\n    }\n\n    public void setTimeTolerance(final long timeTolerance) {\n        this.timeTolerance = timeTolerance;\n    }\n\n    public CasProtocol getProtocol() {\n        return protocol;\n    }\n\n    public void setProtocol(final CasProtocol protocol) {\n        this.protocol = protocol;\n    }\n\n    public boolean isRenew() {\n        return renew;\n    }\n\n    public void setRenew(final boolean renew) {\n        this.renew = renew;\n    }\n\n    public boolean isGateway() {\n        return gateway;\n    }\n\n    public void setGateway(final boolean gateway) {\n        this.gateway = gateway;\n    }\n\n    public boolean isAcceptAnyProxy() {\n        return acceptAnyProxy;\n    }\n\n    public void setAcceptAnyProxy(final boolean acceptAnyProxy) {\n        this.acceptAnyProxy = acceptAnyProxy;\n    }\n\n    public ProxyList getAllowedProxyChains() {\n        return allowedProxyChains;\n    }\n\n    public void setAllowedProxyChains(final ProxyList allowedProxyChains) {\n        this.allowedProxyChains = allowedProxyChains;\n    }\n\n    public void setAllowedProxies(final List<String> allowedProxies) {\n        final List<String[]> proxyChains = new ArrayList<>();\n        for (final String allowedProxyChain : allowedProxies) {\n            final String[] proxyChain = new String[1];\n            proxyChain[0] = allowedProxyChain;\n            proxyChains.add(proxyChain);\n        }\n        this.allowedProxyChains = new ProxyList(proxyChains);\n    }\n\n    public LogoutHandler getLogoutHandler() {\n        return logoutHandler;\n    }\n\n    public LogoutHandler findLogoutHandler() {\n        init();\n\n        return logoutHandler;\n    }\n\n    public void setLogoutHandler(final LogoutHandler logoutHandler) {\n        this.logoutHandler = logoutHandler;\n    }\n\n    public TicketValidator getDefaultTicketValidator() {\n        return defaultTicketValidator;\n    }\n\n    public void setDefaultTicketValidator(final TicketValidator defaultTicketValidator) {\n        this.defaultTicketValidator = defaultTicketValidator;\n    }\n\n    public CasProxyReceptor getProxyReceptor() {\n        return proxyReceptor;\n    }\n\n    public void setProxyReceptor(final CasProxyReceptor proxyReceptor) {\n        this.proxyReceptor = proxyReceptor;\n    }\n\n    public String getPostLogoutUrlParameter() {\n        return postLogoutUrlParameter;\n    }\n\n    public void setPostLogoutUrlParameter(final String postLogoutUrlParameter) {\n        this.postLogoutUrlParameter = postLogoutUrlParameter;\n    }\n\n    public String getRestUrl() {\n        return urlConfiguration.getRestUrl();\n    }\n\n    public void setRestUrl(final String restUrl) {\n        urlConfiguration.setRestUrl(restUrl);\n    }\n\n    public String computeFinalRestUrl(final WebContext context) {\n        init();\n\n        return urlConfiguration.computeFinalRestUrl(context);\n    }\n\n    public org.pac4j.core.http.url.UrlResolver getUrlResolver() {\n        return urlConfiguration.getUrlResolver();\n    }\n\n    public void setUrlResolver(final org.pac4j.core.http.url.UrlResolver urlResolver) {\n        urlConfiguration.setUrlResolver(urlResolver);\n    }\n\n    public void addCustomParam(final String name, final String value) {\n        this.customParams.put(name, value);\n    }\n\n    public String getMethod() {\n        return method;\n    }\n\n    public void setMethod(final String method) {\n        this.method = method;\n    }\n\n    public String getPrivateKeyPath() {\n        return securityConfiguration.getPrivateKeyPath();\n    }\n\n    public void setPrivateKeyPath(final String privateKeyPath) {\n        securityConfiguration.setPrivateKeyPath(privateKeyPath);\n    }\n\n    public String getPrivateKeyAlgorithm() {\n        return securityConfiguration.getPrivateKeyAlgorithm();\n    }\n\n    public void setPrivateKeyAlgorithm(final String privateKeyAlgorithm) {\n        securityConfiguration.setPrivateKeyAlgorithm(privateKeyAlgorithm);\n    }\n\n    @Override\n    public String toString() {\n        return CommonHelper.toNiceString(this.getClass(), \"loginUrl\", this.getLoginUrl(), \"prefixUrl\", this.getPrefixUrl(), \"restUrl\", this.getRestUrl(),\n                \"protocol\", this.protocol, \"renew\", this.renew, \"gateway\", this.gateway, \"encoding\", this.encoding,\n                \"logoutHandler\", this.logoutHandler, \"acceptAnyProxy\", this.acceptAnyProxy, \"allowedProxyChains\", this.allowedProxyChains,\n                \"proxyReceptor\", this.proxyReceptor, \"timeTolerance\", this.timeTolerance, \"postLogoutUrlParameter\",\n                this.postLogoutUrlParameter, \"defaultTicketValidator\", this.defaultTicketValidator, \"urlResolver\", this.getUrlResolver(),\n                \"method\", this.method, \"privateKeyPath\", this.getPrivateKeyPath(), \"privateKeyAlgorithm\", this.getPrivateKeyAlgorithm());\n    }\n}\n"
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
