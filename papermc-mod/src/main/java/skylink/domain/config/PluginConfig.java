package skylink.domain.config;

import skylink.SkyLink;

public class PluginConfig {
    private final String apiHost;

    private final int apiPort;
    private final int syncIntervalSeconds;
    private final boolean syncEnabled;

    private String city;

    public PluginConfig() {
        this.apiHost = getConfigValue("SKYLINK_API_HOST", "api.host", "localhost");
        this.apiPort = Integer.parseInt(getConfigValue("SKYLINK_API_PORT", "api.port", "8080"));
        this.syncIntervalSeconds = Integer.parseInt(getConfigValue("SKYLINK_SYNC_INTERVAL", "sync.interval_seconds", "120"));
        this.syncEnabled = Boolean.parseBoolean(getConfigValue("SKYLINK_SYNC_ENABLED", "sync.enabled", "true"));
        this.city = getConfigValue("SKYLINK_CITY", "location.city", "London");
    }

    public String getConfigValue(String envKey, String ymlKey, String defaultValue) {
        String envValue = System.getenv(envKey);
        if (envValue != null && !envValue.isEmpty()) return envValue;

        String ymlValue = SkyLink.getInstance().getConfig().getString(ymlKey);
        if (ymlValue != null && !ymlValue.isEmpty()) return ymlValue;

        return defaultValue;
    }

    public String getApiHost() { return apiHost; }

    public int getApiPort() { return apiPort; }
    public int getSyncIntervalSeconds() { return syncIntervalSeconds; }

    public boolean isSyncEnabled() { return syncEnabled; }
    
    public String getCity() { return city; }
    
    public void setCity(String city) {
        this.city = city;
    }
    
    public String getApiBaseUrl() {
        return apiHost + ":" + apiPort;
    }
}
