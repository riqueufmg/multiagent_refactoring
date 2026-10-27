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
  "target_name": "org.pac4j.cas.config.CasConfiguration",
  "designite": {
    "dir": "/data/henrique/multiagent_refactoring/data/runs/20261014_164848_IM__org_pac4j_cas_config_CasConfiguration/run_004/planner/designite",
    "smells_csv": "DesignSmells.csv",
    "target_has_smell": true
  },
  "target_file": "pac4j-cas/src/main/java/org/pac4j/cas/config/CasConfiguration.java",
  "target_source_root": "pac4j-cas/src/main/java",
  "target_code": "package org.pac4j.cas.config;\n\nimport org.apereo.cas.client.util.PrivateKeyUtils;\nimport org.apereo.cas.client.validation.*;\nimport org.pac4j.cas.client.CasProxyReceptor;\nimport org.pac4j.core.client.config.BaseClientConfiguration;\nimport org.pac4j.core.logout.handler.LogoutHandler;\nimport org.pac4j.core.logout.handler.DefaultLogoutHandler;\nimport org.pac4j.core.context.WebContext;\nimport org.pac4j.core.exception.TechnicalException;\nimport org.pac4j.core.http.url.UrlResolver;\nimport org.pac4j.core.util.CommonHelper;\n\nimport javax.net.ssl.HostnameVerifier;\nimport javax.net.ssl.SSLSocketFactory;\nimport java.nio.charset.StandardCharsets;\nimport java.security.PrivateKey;\nimport java.util.HashMap;\nimport java.util.List;\nimport java.util.Map;\n\n/**\n * CAS configuration.\n *\n * @author Jerome Leleu\n * @since 1.9.2\n */\npublic class CasConfiguration extends BaseClientConfiguration {\n\n    public static final String TICKET_PARAMETER = \"ticket\";\n\n    public static final String SERVICE_PARAMETER = \"service\";\n\n    public final static String LOGOUT_REQUEST_PARAMETER = \"logoutRequest\";\n\n    public final static String SESSION_INDEX_TAG = \"SessionIndex\";\n\n    public final static String RELAY_STATE_PARAMETER = \"RelayState\";\n\n    private String encoding = StandardCharsets.UTF_8.name();\n\n    private final CasProtocolConfiguration protocolConfiguration = new CasProtocolConfiguration();\n\n    private LogoutHandler logoutHandler;\n\n    private TicketValidator defaultTicketValidator;\n\n    private CasProxyReceptor proxyReceptor;\n\n    private String postLogoutUrlParameter = SERVICE_PARAMETER;\n\n    /* Map containing user defined parameters */\n    private Map<String, String> customParams = new HashMap<>();\n\n    private String method;\n\n    private String privateKeyPath;\n\n    private String privateKeyAlgorithm;\n\n    private PrivateKey privateKey;\n\n    private HostnameVerifier hostnameVerifier;\n\n    private SSLSocketFactory sslSocketFactory;\n\n    private CasUrlConfiguration urlConfiguration = new CasUrlConfiguration();\n\n    public CasConfiguration() {}\n\n    public CasConfiguration(final String loginUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n    }\n\n    public CasConfiguration(final String loginUrl, final CasProtocol protocol) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl);\n        this.protocolConfiguration.setProtocol(protocol);\n    }\n\n    public CasConfiguration(final String loginUrl, final String prefixUrl) {\n        this.urlConfiguration = new CasUrlConfiguration(loginUrl, prefixUrl);\n    }\n\n    @Override\n    protected void internalInit(final boolean forceReinit) {\n        if (CommonHelper.isBlank(getLoginUrl()) && CommonHelper.isBlank(getPrefixUrl()) && CommonHelper.isBlank(getRestUrl())) {\n            throw new TechnicalException(\"loginUrl, prefixUrl and restUrl cannot be all blank\");\n        }\n\n        initializeClientConfiguration();\n\n        initializeLogoutHandler();\n\n        if (privateKeyPath != null) {\n            final String algo;\n            if (privateKeyAlgorithm != null) {\n                algo = privateKeyAlgorithm;\n            } else {\n                algo = \"RSA\";\n            }\n            this.privateKey = PrivateKeyUtils.createKey(privateKeyPath, algo);\n        }\n    }\n\n    protected void initializeClientConfiguration() {\n        urlConfiguration.initializeClientConfiguration();\n    }\n\n    protected void initializeLogoutHandler() {\n        if (this.logoutHandler == null) {\n            this.logoutHandler = new DefaultLogoutHandler();\n        }\n    }\n\n    public TicketValidator retrieveTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).retrieveTicketValidator(context);\n    }\n\n    protected TicketValidator buildSAMLTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildSAMLTicketValidator(context);\n    }\n\n    protected void addPrivateKey(final Cas20ServiceTicketValidator validator) {\n        if (this.privateKey != null) {\n            validator.setPrivateKey(this.privateKey);\n        }\n    }\n\n    protected TicketValidator buildCas30ProxyTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas30ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas30TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas30TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20ProxyTicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas20ProxyTicketValidator(context);\n    }\n\n    protected TicketValidator buildCas20TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas20TicketValidator(context);\n    }\n\n    protected TicketValidator buildCas10TicketValidator(final WebContext context) {\n        return new CasTicketValidatorFactory(this).buildCas10TicketValidator(context);\n    }\n\n    public String getEncoding() {\n        return encoding;\n    }\n\n    public void setEncoding(final String encoding) {\n        this.encoding = encoding;\n    }\n\n    public String computeFinalLoginUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalLoginUrl(context);\n    }\n\n    public String getLoginUrl() {\n        return urlConfiguration.getLoginUrl();\n    }\n\n    public void setLoginUrl(final String loginUrl) {\n        urlConfiguration.setLoginUrl(loginUrl);\n    }\n\n    public String getPrefixUrl() {\n        return urlConfiguration.getPrefixUrl();\n    }\n\n    public String computeFinalPrefixUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalPrefixUrl(context);\n    }\n\n    public void setPrefixUrl(final String prefixUrl) {\n        urlConfiguration.setPrefixUrl(prefixUrl);\n    }\n\n    public HostnameVerifier getHostnameVerifier() {\n        return hostnameVerifier;\n    }\n\n    public void setHostnameVerifier(final HostnameVerifier hostnameVerifier) {\n        this.hostnameVerifier = hostnameVerifier;\n    }\n\n    public SSLSocketFactory getSslSocketFactory() {\n        return sslSocketFactory;\n    }\n\n    public void setSslSocketFactory(final SSLSocketFactory sslSocketFactory) {\n        this.sslSocketFactory = sslSocketFactory;\n    }\n\n    public Map<String, String> getCustomParams() {\n        return customParams;\n    }\n\n    public void setCustomParams(final Map<String, String> customParams) {\n        this.customParams = customParams;\n    }\n\n    public long getTimeTolerance() {\n        return protocolConfiguration.getTimeTolerance();\n    }\n\n    public void setTimeTolerance(final long timeTolerance) {\n        protocolConfiguration.setTimeTolerance(timeTolerance);\n    }\n\n    public CasProtocol getProtocol() {\n        return protocolConfiguration.getProtocol();\n    }\n\n    public void setProtocol(final CasProtocol protocol) {\n        protocolConfiguration.setProtocol(protocol);\n    }\n\n    public boolean isRenew() {\n        return protocolConfiguration.isRenew();\n    }\n\n    public void setRenew(final boolean renew) {\n        protocolConfiguration.setRenew(renew);\n    }\n\n    public boolean isGateway() {\n        return protocolConfiguration.isGateway();\n    }\n\n    public void setGateway(final boolean gateway) {\n        protocolConfiguration.setGateway(gateway);\n    }\n\n    public boolean isAcceptAnyProxy() {\n        return protocolConfiguration.isAcceptAnyProxy();\n    }\n\n    public void setAcceptAnyProxy(final boolean acceptAnyProxy) {\n        protocolConfiguration.setAcceptAnyProxy(acceptAnyProxy);\n    }\n\n    public ProxyList getAllowedProxyChains() {\n        return protocolConfiguration.getAllowedProxyChains();\n    }\n\n    public void setAllowedProxyChains(final ProxyList allowedProxyChains) {\n        protocolConfiguration.setAllowedProxyChains(allowedProxyChains);\n    }\n\n    public void setAllowedProxies(final List<String> allowedProxies) {\n        protocolConfiguration.setAllowedProxies(allowedProxies);\n    }\n\n    public LogoutHandler getLogoutHandler() {\n        return logoutHandler;\n    }\n\n    public LogoutHandler findLogoutHandler() {\n        init();\n        return logoutHandler;\n    }\n\n    public void setLogoutHandler(final LogoutHandler logoutHandler) {\n        this.logoutHandler = logoutHandler;\n    }\n\n    public TicketValidator getDefaultTicketValidator() {\n        return defaultTicketValidator;\n    }\n\n    public void setDefaultTicketValidator(final TicketValidator defaultTicketValidator) {\n        this.defaultTicketValidator = defaultTicketValidator;\n    }\n\n    public CasProxyReceptor getProxyReceptor() {\n        return proxyReceptor;\n    }\n\n    public void setProxyReceptor(final CasProxyReceptor proxyReceptor) {\n        this.proxyReceptor = proxyReceptor;\n    }\n\n    public String getPostLogoutUrlParameter() {\n        return postLogoutUrlParameter;\n    }\n\n    public void setPostLogoutUrlParameter(final String postLogoutUrlParameter) {\n        this.postLogoutUrlParameter = postLogoutUrlParameter;\n    }\n\n    public String getRestUrl() {\n        return urlConfiguration.getRestUrl();\n    }\n\n    public void setRestUrl(final String restUrl) {\n        urlConfiguration.setRestUrl(restUrl);\n    }\n\n    public String computeFinalRestUrl(final WebContext context) {\n        init();\n        return urlConfiguration.computeFinalRestUrl(context);\n    }\n\n    public UrlResolver getUrlResolver() {\n        return urlConfiguration.getUrlResolver();\n    }\n\n    public void setUrlResolver(final UrlResolver urlResolver) {\n        urlConfiguration.setUrlResolver(urlResolver);\n    }\n\n    public void addCustomParam(final String name, final String value) {\n        this.customParams.put(name, value);\n    }\n\n    public String getMethod() {\n        return method;\n    }\n\n    public void setMethod(final String method) {\n        this.method = method;\n    }\n\n    public String getPrivateKeyPath() {\n        return privateKeyPath;\n    }\n\n    public void setPrivateKeyPath(final String privateKeyPath) {\n        this.privateKeyPath = privateKeyPath;\n    }\n\n    public String getPrivateKeyAlgorithm() {\n        return privateKeyAlgorithm;\n    }\n\n    public void setPrivateKeyAlgorithm(final String privateKeyAlgorithm) {\n        this.privateKeyAlgorithm = privateKeyAlgorithm;\n    }\n\n    @Override\n    public String toString() {\n        return CommonHelper.toNiceString(this.getClass(), \"loginUrl\", this.getLoginUrl(), \"prefixUrl\", this.getPrefixUrl(), \"restUrl\", this.getRestUrl(),\n                \"protocol\", this.getProtocol(), \"renew\", this.isRenew(), \"gateway\", this.isGateway(), \"encoding\", this.encoding,\n                \"logoutHandler\", this.logoutHandler, \"acceptAnyProxy\", this.isAcceptAnyProxy(), \"allowedProxyChains\", this.getAllowedProxyChains(),\n                \"proxyReceptor\", this.proxyReceptor, \"timeTolerance\", this.getTimeTolerance(), \"postLogoutUrlParameter\",\n                this.postLogoutUrlParameter, \"defaultTicketValidator\", this.defaultTicketValidator, \"urlResolver\", this.getUrlResolver(),\n                \"method\", this.method, \"privateKeyPath\", this.privateKeyPath, \"privateKeyAlgorithm\", this.privateKeyAlgorithm);\n    }\n}\n"
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