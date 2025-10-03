package skylink.domain.config;

import skylink.SkyLink;

public class PluginConfig {
    private final String host;
    private final int port;

    private final String defaultCity;

    private final double defaultLatitude;
    private final double defaultLongitude;

    private SkyLink plugin;

    public PluginConfig(SkyLink plugin) {
        this.plugin = plugin;

        this.host = plugin.getConfigValue("SKYLINK_HOST", "config.host", "localhost");
        this.port = Integer.parseInt(plugin.getConfigValue("SKYLINK_PORT", "config.port", "8080"));

        this.defaultCity = plugin.getConfigValue("SKYLINK_CITY", "location.city", "UK/London");
        this.defaultLatitude = Double.parseDouble(plugin.getConfigValue("SKYLINK_LATITUDE", "location.latitude", "0"));
        this.defaultLongitude = Double.parseDouble(plugin.getConfigValue("SKYLINK_LONGITUDE", "location.longitude", "0"));
    }

    public String getHost() { return host; }
    public int getPort() { return port; }

    public String getDefaultCity() { return defaultCity; }

    public double getDefaultLatitude() { return defaultLatitude; }
    public double getDefaultLongitude() { return defaultLongitude; }
}
