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
    "goal": "Reduce the number of public methods and fields in CasConfiguration by extracting the cohesive CAS protocol, proxy, and validation policy settings while preserving the existing CasConfiguration API through delegation.",
    "files": [
      "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
      "pac4j-cas/src/main/java/org/pac4j/cas/config/CasProtocolConfiguration.java"
    ],
    "ops": [
      {
        "op": "EXTRACT_CLASS",
        "inputs": [
          "org.pac4j.cas.config.CasConfiguration.protocol",
          "org.pac4j.cas.config.CasConfiguration.timeTolerance",
          "org.pac4j.cas.config.CasConfiguration.renew",
          "org.pac4j.cas.config.CasConfiguration.gateway",
          "org.pac4j.cas.config.CasConfiguration.acceptAnyProxy",
          "org.pac4j.cas.config.CasConfiguration.allowedProxyChains",
          "org.pac4j.cas.config.CasConfiguration.getTimeTolerance()",
          "org.pac4j.cas.config.CasConfiguration.setTimeTolerance(long)",
          "org.pac4j.cas.config.CasConfiguration.getProtocol()",
          "org.pac4j.cas.config.CasConfiguration.setProtocol(CasProtocol)",
          "org.pac4j.cas.config.CasConfiguration.isRenew()",
          "org.pac4j.cas.config.CasConfiguration.setRenew(boolean)",
          "org.pac4j.cas.config.CasConfiguration.isGateway()",
          "org.pac4j.cas.config.CasConfiguration.setGateway(boolean)",
          "org.pac4j.cas.config.CasConfiguration.isAcceptAnyProxy()",
          "org.pac4j.cas.config.CasConfiguration.setAcceptAnyProxy(boolean)",
          "org.pac4j.cas.config.CasConfiguration.getAllowedProxyChains()",
          "org.pac4j.cas.config.CasConfiguration.setAllowedProxyChains(ProxyList)",
          "org.pac4j.cas.config.CasConfiguration.setAllowedProxies(List<String>)"
        ],
        "outputs": [
          "org.pac4j.cas.config.CasProtocolConfiguration",
          "org.pac4j.cas.config.CasConfiguration"
        ],
        "details": "Create CasProtocolConfiguration in the same package and move the listed fields and methods into it. Preserve the existing public methods on CasConfiguration as delegating methods backed by a private CasProtocolConfiguration field, so existing callers and CasTicketValidatorFactory interactions remain source-compatible. Preserve the existing default values: timeTolerance=1000L, protocol=CasProtocol.CAS30, renew=false, gateway=false, acceptAnyProxy=false, and allowedProxyChains=new ProxyList(). Keep setAllowedProxies(List<String>) conversion behavior unchanged.",
        "risk": "medium"
      }
    ]
  },
  "allowed_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasProtocolConfiguration.java"
  ],
  "executor_existing_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java"
  ],
  "executor_new_files": [
    "pac4j-cas/src/main/java/org/pac4j/cas/config/CasProtocolConfiguration.java"
  ],
  "executor_rejected_files": [],
  "files_context": [
    {
      "path": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
      "exists": "true",
      "content": "package org.pac4j.cas.config;\n\nimport org.apereo.cas.client.util.PrivateKeyUtils;\nimport org.apereo.cas.client.validation.*;\nimport org.pac4j.cas.client.CasProxyReceptor;\nimport org.pac4j.core.client.config.BaseClientConfiguration;\nimport org.pac4j.core.logout.handler.LogoutHandler;\nimport org.pac4j.core.logout.handler.DefaultLogoutHandler;\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.exception.TechnicalException;\nimport org.pac4j.core.http.url.UrlResolver;\nimport org.pac4j.core.util.CommonHelper;\n\nimport javax.net.ssl.HostnameVerifier;\nimport javax.net.ssl.SSLSocketFactory;\nimport java.nio.charset.StandardCharsets;\nimport java.security.PrivateKey;\nimport java.util.ArrayList;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\n/**\n * CAS configuration.\n *\n * @author Jerome Leleu\n * @since 1.9.2\n */\npublic class CasConfiguration extends BaseClientConfiguration {\n\n    public static final String TICKET_PARAMETER = \"ticket\";\n\n    public static final String SERVICE_PARAMETER = \"service\";\n\n    public final static String LOGOUT_REQUEST_PARAMETER = \"logoutRequest\";\n\n    public final static String SESSION_INDEX_TAG = \"SessionIndex\";\n\n    public final static String RELAY_STATE_PARAMETER = \"RelayState\";\n\n    private String encoding = StandardCharsets.UTF_8.name();\n\n    private long timeTolerance = 1000L;\n\n    private CasProtocol protocol = CasProtocol.CAS30;\n\n    private boolean renew = false;\n\n    private boolean gateway = false;\n\n    private boolean acceptAnyProxy = false;\n\n    private ProxyList allowedProxyChains = new ProxyList();\n\n    private LogoutHandler logoutHandler;\n\n    private TicketValidator defaultTicketValidator;\n\n    private CasProxyReceptor proxyReceptor;\n\n    private String postLogoutUrlParameter = SERVICE_PARAMETER;\n\n    /* Map containing user defined parameters */\n    private Map<String, String> customParams = new HashMap<>();\n\n    private String method;\n\n    private String privateKeyPath;\n\n    private String privateKeyAlgorithm;\n\n    private PrivateKey privateKey;\n\n    private HostnameVerifier hostnameVerifier;\n\n    private SSLSocketFactory sslSocketFactory;\n\n    private CasUrlConfiguration urlConfiguration = new CasUrlConfiguration();\n\n    public CasConfiguration() {}\n\n    public CasConfiguration(final String loginUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n    }\n\n    public CasConfiguration(final String loginUrl, final CasProtocol protocol) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n        this.protocol = protocol;\n    }\n\n    public CasConfiguration(final String loginUrl, final String prefixUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl, prefixUrl);\n    }\n\n    @Override\n    protected void internalInit(final boolean forceReinit) {\n        if (CommonHelper.isBlank(getLoginUrl()) && CommonHelper.isBlank(getPrefixUrl()) && CommonHelper.isBlank(getRestUrl())) {\n            throw new TechnicalException(\"loginUrl, prefixUrl and restUrl cannot be all blank\");\n        }\n\n        initializeClientConfiguration();\n\n        initializeLogoutHandler();\n\n        if (privateKeyPath != null) {\n            final String algo;\n            if (privateKeyAlgorithm != null) {\n                algo = privateKeyAlgorithm;\n            } else {\n                algo = \"RSA\";\n            }\n            this.privateKey = PrivateKeyUtils.createKey(privateKeyPath, algo);\n        }\n    }\n\n    protected void initializeClientConfiguration() {\n        urlConfiguration.initializeClientConfiguration();\n    }\n\n    protected void initializeLogoutHandler() {\n        if (this.logoutHandler == null) {\n            this.logoutHandler = new DefaultLogoutHandler();\n        }\n    }\n\n    public TicketValidator retrieveTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).retrieveTicketValidator(context);\n    }\n\n    protected TicketValidator buildSAMLTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildSAMLTicketValidator(context);\n    }\n\n    protected void addPrivateKey(final Cas20ServiceTicketValidator validator) {\n        if (this.privateKey != null) {\n            validator.setPrivateKey(this.privateKey);\n        }\n    }\n\n    protected TicketValidator buildCas30ProxyTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas30ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas30TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas30TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20ProxyTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas20ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas20TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas10TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas10TicketValidator(context);\n    }\n\n    public String getEncoding() {\n        return encoding;\n    }\n\n    public void setEncoding(final String encoding) {\n        this.encoding = encoding;\n    }\n\n    public String computeFinalLoginUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalLoginUrl(context);\n    }\n\n    public String getLoginUrl() {\n        return urlConfiguration.getLoginUrl();\n    }\n\n    public void setLoginUrl(final String loginUrl) {\n        urlConfiguration.setLoginUrl(loginUrl);\n    }\n\n    public String getPrefixUrl() {\n        return urlConfiguration.getPrefixUrl();\n    }\n\n    public String computeFinalPrefixUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalPrefixUrl(context);\n    }\n\n    public void setPrefixUrl(final String prefixUrl) {\n        urlConfiguration.setPrefixUrl(prefixUrl);\n    }\n\n    public HostnameVerifier getHostnameVerifier() {\n        return hostnameVerifier;\n    }\n\n    public void setHostnameVerifier(final HostnameVerifier hostnameVerifier) {\n        this.hostnameVerifier = hostnameVerifier;\n    }\n\n    public SSLSocketFactory getSslSocketFactory() {\n        return sslSocketFactory;\n    }\n\n    public void setSslSocketFactory(final SSLSocketFactory sslSocketFactory) {\n        this.sslSocketFactory = sslSocketFactory;\n    }\n\n    public Map<String, String> getCustomParams() {\n        return customParams;\n    }\n\n    public void setCustomParams(final Map<String, String> customParams) {\n        this.customParams = customParams;\n    }\n\n    public long getTimeTolerance() {\n        return timeTolerance;\n    }\n\n    public void setTimeTolerance(final long timeTolerance) {\n        this.timeTolerance = timeTolerance;\n    }\n\n    public CasProtocol getProtocol() {\n        return protocol;\n    }\n\n    public void setProtocol(final CasProtocol protocol) {\n        this.protocol = protocol;\n    }\n\n    public boolean isRenew() {\n        return renew;\n    }\n\n    public void setRenew(final boolean renew) {\n        this.renew = renew;\n    }\n\n    public boolean isGateway() {\n        return gateway;\n    }\n\n    public void setGateway(final boolean gateway) {\n        this.gateway = gateway;\n    }\n\n    public boolean isAcceptAnyProxy() {\n        return acceptAnyProxy;\n    }\n\n    public void setAcceptAnyProxy(final boolean acceptAnyProxy) {\n        this.acceptAnyProxy = acceptAnyProxy;\n    }\n\n    public ProxyList getAllowedProxyChains() {\n        return allowedProxyChains;\n    }\n\n    public void setAllowedProxyChains(final ProxyList allowedProxyChains) {\n        this.allowedProxyChains = allowedProxyChains;\n    }\n\n    public void setAllowedProxies(final List<String> allowedProxies) {\n        final List<String[]> proxyChains = new ArrayList<>();\n        for (final String allowedProxyChain : allowedProxies) {\n            final String[] proxyChain = new String[1];\n            proxyChain[0] = allowedProxyChain;\n            proxyChains.add(proxyChain);\n        }\n        this.allowedProxyChains = new ProxyList(proxyChains);\n    }\n\n    public LogoutHandler getLogoutHandler() {\n        return logoutHandler;\n    }\n\n    public LogoutHandler findLogoutHandler() {\n        init();\n        return logoutHandler;\n    }\n\n    public void setLogoutHandler(final LogoutHandler logoutHandler) {\n        this.logoutHandler = logoutHandler;\n    }\n\n    public TicketValidator getDefaultTicketValidator() {\n        return defaultTicketValidator;\n    }\n\n    public void setDefaultTicketValidator(final TicketValidator defaultTicketValidator) {\n        this.defaultTicketValidator = defaultTicketValidator;\n    }\n\n    public CasProxyReceptor getProxyReceptor() {\n        return proxyReceptor;\n    }\n\n    public void setProxyReceptor(final CasProxyReceptor proxyReceptor) {\n        this.proxyReceptor = proxyReceptor;\n    }\n\n    public String getPostLogoutUrlParameter() {\n        return postLogoutUrlParameter;\n    }\n\n    public void setPostLogoutUrlParameter(final String postLogoutUrlParameter) {\n        this.postLogoutUrlParameter = postLogoutUrlParameter;\n    }\n\n    public String getRestUrl() {\n        return urlConfiguration.getRestUrl();\n    }\n\n    public void setRestUrl(final String restUrl) {\n        urlConfiguration.setRestUrl(restUrl);\n    }\n\n    public String computeFinalRestUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalRestUrl(context);\n    }\n\n    public UrlResolver getUrlResolver() {\n        return urlConfiguration.getUrlResolver();\n    }\n\n    public void setUrlResolver(final UrlResolver urlResolver) {\n        urlConfiguration.setUrlResolver(urlResolver);\n    }\n\n    public void addCustomParam(final String name, final String value) {\n        this.customParams.put(name, value);\n    }\n\n    public String getMethod() {\n        return method;\n    }\n\n    public void setMethod(final String method) {\n        this.method = method;\n    }\n\n    public String getPrivateKeyPath() {\n        return privateKeyPath;\n    }\n\n    public void setPrivateKeyPath(final String privateKeyPath) {\n        this.privateKeyPath = privateKeyPath;\n    }\n\n    public String getPrivateKeyAlgorithm() {\n        return privateKeyAlgorithm;\n    }\n\n    public void setPrivateKeyAlgorithm(final String privateKeyAlgorithm) {\n        this.privateKeyAlgorithm = privateKeyAlgorithm;\n    }\n\n    @Override\n    public String toString() {\n        return CommonHelper.toNiceString(this.getClass(), \"loginUrl\", this.getLoginUrl(), \"prefixUrl\", this.getPrefixUrl(), \"restUrl\", this.getRestUrl(),\n                \"protocol\", this.protocol, \"renew\", this.renew, \"gateway\", this.gateway, \"encoding\", this.encoding,\n                \"logoutHandler\", this.logoutHandler, \"acceptAnyProxy\", this.acceptAnyProxy, \"allowedProxyChains\", this.allowedProxyChains,\n                \"proxyReceptor\", this.proxyReceptor, \"timeTolerance\", this.timeTolerance, \"postLogoutUrlParameter\",\n                this.postLogoutUrlParameter, \"defaultTicketValidator\", this.defaultTicketValidator, \"urlResolver\", this.getUrlResolver(),\n                \"method\", this.method, \"privateKeyPath\", this.privateKeyPath, \"privateKeyAlgorithm\", this.privateKeyAlgorithm);\n    }\n}\n"
    },
    {
      "path": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasProtocolConfiguration.java",
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
