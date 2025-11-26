package skylink;

import skylink.infrastructure.commands.SkyLinkCommand;
import skylink.infrastructure.sync.WeatherSyncService;
import skylink.infrastructure.api.SkyLinkApiClient;
import skylink.domain.config.PluginConfig;

import org.bukkit.plugin.java.JavaPlugin;

public class SkyLink extends JavaPlugin {
    private static SkyLink instance;

    private WeatherSyncService syncService;
    private SkyLinkCommand skylinkCommand;
    private SkyLinkApiClient apiClient;
    private PluginConfig pluginConfig;

    @Override
    public void onEnable() {
        instance = this;

        getLogger().info("SkyLink starting up...");
        saveDefaultConfig();

        pluginConfig = new PluginConfig();
        apiClient = new SkyLinkApiClient(pluginConfig, getLogger());
        syncService = new WeatherSyncService(this, pluginConfig, apiClient);

        skylinkCommand = new SkyLinkCommand(pluginConfig, syncService, apiClient);

        getCommand("skylink").setExecutor(skylinkCommand);
        getCommand("skylink").setTabCompleter(skylinkCommand);

        syncService.start();

        getLogger().info("SkyLink enabled successfully!");
        getLogger().info("API endpoint: " + pluginConfig.getApiBaseUrl());
        getLogger().info("Syncing city: " + pluginConfig.getCity());
    }

    @Override
    public void onDisable() {
        if (syncService != null) syncService.stop();
        getLogger().info("SkyLink disabled.");
    }

    public static SkyLink getInstance() { return instance; }

    public PluginConfig getPluginConfig() { return pluginConfig; }
    public SkyLinkApiClient getApiClient() { return apiClient; }
    public WeatherSyncService getSyncService() { return syncService; }
}
