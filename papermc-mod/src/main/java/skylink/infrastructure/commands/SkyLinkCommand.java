package skylink.infrastructure.commands;

import skylink.infrastructure.commands.location.CityCommand;
import skylink.infrastructure.sync.WeatherSyncService;
import skylink.infrastructure.api.SkyLinkApiClient;

import skylink.domain.config.PluginConfig;

import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.command.Command;

import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.List;

public class SkyLinkCommand implements CommandExecutor, TabCompleter {
    private final PluginConfig config;
    private final CityCommand cityCommand;
    private final WeatherSyncService syncService;
    private final SkyLinkApiClient apiClient;

    public SkyLinkCommand(PluginConfig config, WeatherSyncService syncService, SkyLinkApiClient apiClient) {
        this.config = config;
        this.syncService = syncService;
        this.apiClient = apiClient;
        this.cityCommand = new CityCommand(config);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("§cThis command can only be used by players.");
            return true;
        }

        Player player = (Player) sender;

        if (!player.hasPermission("skylink.use")) {
            player.sendMessage("§cYou don't have permission to use this command.");
            return true;
        }

        if (args.length < 1) {
            sendHelp(player);
            return true;
        }

        String subcommand = args[0].toLowerCase();
        
        switch (subcommand) {
            case "city" -> {
                if (args.length < 2) {
                    player.sendMessage("§6Current city: §f" + config.getCity());
                    player.sendMessage("§7Usage: /skylink city <city name>");

                    return true;
                }

                String[] cityArgs = new String[args.length - 1];
                System.arraycopy(args, 1, cityArgs, 0, args.length - 1);
                boolean result = cityCommand.onCommand(sender, command, label, cityArgs);
                
                // Trigger immediate sync after city change
                if (result) {
                    player.sendMessage("§6Syncing weather for new city...");
                    syncService.sync();
                }
                
                return result;
            }

            case "sync" -> {
                if (!player.hasPermission("skylink.admin")) {
                    player.sendMessage("§cYou don't have permission to use this command.");
                    return true;
                }

                player.sendMessage("§6Forcing weather sync...");
                syncService.sync();
                player.sendMessage("§aSync complete!");

                return true;
            }

            case "status" -> {
                sendStatus(player);
                return true;
            }

            case "start" -> {
                if (!player.hasPermission("skylink.admin")) {
                    player.sendMessage("§cYou don't have permission to use this command.");
                    return true;
                }

                if (syncService.isRunning()) {
                    player.sendMessage("§eSyncing is already running.");
                }

                else {
                    syncService.start();
                    player.sendMessage("§aWeather sync started!");
                }

                return true;
            }

            case "stop" -> {
                if (!player.hasPermission("skylink.admin")) {
                    player.sendMessage("§cYou don't have permission to use this command.");
                    return true;
                }

                if (!syncService.isRunning()) {
                    player.sendMessage("§eSyncing is not running.");
                }

                else {
                    syncService.stop();
                    player.sendMessage("§cWeather sync stopped!");
                }

                return true;
            }

            default -> {
                player.sendMessage("§cUnknown subcommand: " + subcommand);
                sendHelp(player);
                return true;
            }
        }
    }

    private void sendHelp(Player player) {
        player.sendMessage("§6§l=== SkyLink Commands ===");
        player.sendMessage("§e/skylink city [name] §7- View or set synced city");
        player.sendMessage("§e/skylink status §7- View sync status");

        if (player.hasPermission("skylink.admin")) {
            player.sendMessage("§e/skylink sync §7- Force immediate sync");
            player.sendMessage("§e/skylink start §7- Start weather syncing");
            player.sendMessage("§e/skylink stop §7- Stop weather syncing");
        }
    }

    private void sendStatus(Player player) {
        player.sendMessage("§6§l=== SkyLink Status ===");
        player.sendMessage("§eCity: §f" + config.getCity());
        player.sendMessage("§eAPI: §f" + config.getApiBaseUrl());
        player.sendMessage("§eAPI Health: " + (apiClient.isHealthy() ? "§aOnline" : "§cOffline"));
        player.sendMessage("§eSyncing: " + (syncService.isRunning() ? "§aEnabled" : "§cDisabled"));
        player.sendMessage("§eSync Interval: §f" + config.getSyncIntervalSeconds() + "s");
        
        if (syncService.getLastSyncTime() > 0) {
            long secondsAgo = (System.currentTimeMillis() - syncService.getLastSyncTime()) / 1000;

            player.sendMessage("§eLast Sync: §f" + secondsAgo + "s ago");
            player.sendMessage("§eLast Ticks: §f" + syncService.getLastSyncedTicks());
            player.sendMessage("§eLast Weather: " + (syncService.isLastSyncedThunder() ? "§9Thunder" : syncService.isLastSyncedRain() ? "§bRain" : "§aClear"));
        }

        else {
            player.sendMessage("§7No sync data yet.");
        }
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        List<String> completions = new ArrayList<>();

        if (args.length == 1) {
            String partial = args[0].toLowerCase();
            for (String sub : List.of("city", "status", "sync", "start", "stop")) {
                if (sub.startsWith(partial)) {
                    if (sub.equals("sync") || sub.equals("start") || sub.equals("stop")) {
                        if (sender.hasPermission("skylink.admin")) completions.add(sub);
                    }

                    else {
                        completions.add(sub);
                    }
                }
            }
        }

        else if (args.length >= 2 && args[0].equalsIgnoreCase("city")) {
            String[] cityArgs = new String[args.length - 1];
            System.arraycopy(args, 1, cityArgs, 0, args.length - 1);
            return cityCommand.onTabComplete(sender, command, alias, cityArgs);
        }

        return completions;
    }
}