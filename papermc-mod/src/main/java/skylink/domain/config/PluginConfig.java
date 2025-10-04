package skylink.domain.config;

import skylink.SkyLink;

public class PluginConfig {
    private final String host;
    private final int port;

    private final String defaultCity;
    private SkyLink plugin;

    public PluginConfig() {
        this.host = getConfigValue("SKYLINK_HOST", "config.host", "localhost");
        this.port = Integer.parseInt(getConfigValue("SKYLINK_PORT", "config.port", "8080"));
        this.defaultCity = getConfigValue("SKYLINK_CITY", "location.city", "UK/London");
    }

    public String getConfigValue(String envKey, String ymlKey, String defaultValue) {
        String envValue = System.getenv(envKey);
        if (envValue != null && !envValue.isEmpty()) return envValue;

        String ymlValue = plugin.getConfig().getString(ymlKey);
        if (ymlValue != null && !ymlValue.isEmpty()) return ymlValue;

        return defaultValue;
    }

    public String getHost() { return host; }
    public int getPort() { return port; }

    public String getDefaultCity() { return defaultCity; }
}
