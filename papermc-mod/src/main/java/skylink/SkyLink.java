package skylink;

import skylink.infrastructure.commands.SkyLinkCommand;
import skylink.domain.config.PluginConfig;

import org.bukkit.plugin.java.JavaPlugin;

public class SkyLink extends JavaPlugin {
    private SkyLinkCommand skylinkCommand;
    private PluginConfig config;

    @Override
    public void onEnable() {
        getLogger().info("SkyLink starting up...");
        saveDefaultConfig();

        config = new PluginConfig();
        skylinkCommand = new SkyLinkCommand(config);

        getCommand("skylink").setExecutor(skylinkCommand);
        getCommand("skylink").setTabCompleter(skylinkCommand);

        getLogger().info("SkyLink enabled successfully!");
    }

    @Override
    public void onDisable() {
        getLogger().info("SkyLink disabled.");
    }
}
