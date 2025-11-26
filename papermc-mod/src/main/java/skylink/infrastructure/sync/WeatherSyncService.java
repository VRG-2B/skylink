package skylink.infrastructure.sync;

import org.bukkit.Bukkit;
import org.bukkit.GameRule;
import org.bukkit.World;
import org.bukkit.scheduler.BukkitTask;
import skylink.SkyLink;
import skylink.domain.config.PluginConfig;
import skylink.infrastructure.api.SkyLinkApiClient;

import java.util.logging.Logger;

public class WeatherSyncService {
    private final SkyLink plugin;
    private final PluginConfig config;
    private final SkyLinkApiClient apiClient;
    private final Logger logger;

    private BukkitTask syncTask;

    private boolean running = false;
    private boolean lastSyncedRain = false;
    private boolean lastSyncedThunder = false;

    private int lastSyncedTicks = -1;
    private long lastSyncTime = 0;

    public WeatherSyncService(SkyLink plugin, PluginConfig config, SkyLinkApiClient apiClient) {
        this.plugin = plugin;
        this.config = config;
        this.apiClient = apiClient;
        this.logger = plugin.getLogger();
    }

    public void start() {
        if (running) {
            logger.warning("Weather sync service is already running!");
            return;
        }

        if (!config.isSyncEnabled()) {
            logger.info("Weather sync is disabled in config.");
            return;
        }

        // Disable vanilla day/night and weather cycles
        setGameRules(false);

        // Convert seconds to ticks (20 ticks per second)
        long intervalTicks = config.getSyncIntervalSeconds() * 20L;

        syncTask = Bukkit.getScheduler().runTaskTimerAsynchronously(plugin, this::sync, 0L, intervalTicks);
        running = true;
        logger.info("Weather sync service started! Syncing every " + config.getSyncIntervalSeconds() + " seconds.");
    }

    public void stop() {
        if (!running) return;

        if (syncTask != null) {
            syncTask.cancel();
            syncTask = null;
        }

        // Re-enable vanilla cycles when stopping
        setGameRules(true);

        running = false;
        logger.info("Weather sync service stopped.");
    }

    public void sync() {
        String city = config.getCity();

        // Fetch time
        apiClient.getTime(city).ifPresent(timeResponse -> {
            lastSyncedTicks = timeResponse.ticks();

            // Must run on main thread to modify world
            Bukkit.getScheduler().runTask(plugin, () -> {
                for (World world : Bukkit.getWorlds()) {
                    if (world.getEnvironment() == World.Environment.NORMAL) {
                        world.setTime(timeResponse.ticks());
                    }
                }
            });

            logger.fine("Synced time to " + timeResponse.ticks() + " ticks for city: " + city);
        });

        // Fetch precipitation
        apiClient.getPrecipitation(city).ifPresent(precipResponse -> {
            lastSyncedRain = precipResponse.rain();
            lastSyncedThunder = precipResponse.thunder();

            // Must run on main thread to modify world
            Bukkit.getScheduler().runTask(plugin, () -> {
                for (World world : Bukkit.getWorlds()) {
                    if (world.getEnvironment() == World.Environment.NORMAL) {
                        world.setStorm(precipResponse.rain());
                        world.setThundering(precipResponse.thunder());
                        
                        // Set duration to a long time since we're controlling it
                        if (precipResponse.rain()) world.setWeatherDuration(Integer.MAX_VALUE);
                        else world.setClearWeatherDuration(Integer.MAX_VALUE);
                    }
                }
            });

            logger.fine("Synced weather: rain=" + precipResponse.rain() + ", thunder=" + precipResponse.thunder());
        });

        lastSyncTime = System.currentTimeMillis();
    }

    private void setGameRules(boolean enabled) {
        Bukkit.getScheduler().runTask(plugin, () -> {
            for (World world : Bukkit.getWorlds()) {
                if (world.getEnvironment() == World.Environment.NORMAL) {
                    world.setGameRule(GameRule.DO_DAYLIGHT_CYCLE, enabled);
                    world.setGameRule(GameRule.DO_WEATHER_CYCLE, enabled);
                }
            }

            logger.info("Set doDaylightCycle and doWeatherCycle to " + enabled);
        });
    }

    public boolean isRunning() { return running; }
    public boolean isLastSyncedRain() { return lastSyncedRain; }
    public boolean isLastSyncedThunder() { return lastSyncedThunder; }

    public int getLastSyncedTicks() { return lastSyncedTicks; }
    public long getLastSyncTime() { return lastSyncTime; }
}
