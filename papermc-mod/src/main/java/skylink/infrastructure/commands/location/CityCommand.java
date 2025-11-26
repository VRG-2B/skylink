package skylink.infrastructure.commands.location;

import skylink.domain.config.PluginConfig;

import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.command.Command;

import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.List;

public class CityCommand implements CommandExecutor, TabCompleter {
    private final PluginConfig config;

    // Common city suggestions
    private static final List<String> CITY_SUGGESTIONS = List.of(
        "Vilnius", "London", "New York", "Paris", "Tokyo", "Sydney",
        "Berlin", "Moscow", "Dubai", "Singapore", "Toronto",
        "Los Angeles", "Chicago", "Miami", "San Francisco"
    );

    public CityCommand(PluginConfig config) {
        this.config = config;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        Player player = (Player) sender;

        if (args.length < 1) {            
            player.sendMessage("§6Current city: §f" + config.getCity());
            player.sendMessage("§7Usage: /skylink city <city name>");
            player.sendMessage("§7Example: /skylink city London");

            return true;
        }

        // Join all args to support city names with spaces
        String cityInput = String.join(" ", args);

        if (cityInput.isBlank()) {
            player.sendMessage("§cPlease provide a valid city name!");
            return true;
        }

        config.setCity(cityInput);
        player.sendMessage("§aCity set to: §f" + cityInput);
        player.sendMessage("§7Weather will sync on next update cycle.");

        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        List<String> completions = new ArrayList<>();

        if (args.length >= 1) {
            String partial = String.join(" ", args).toLowerCase();
            for (String city : CITY_SUGGESTIONS) {
                if (city.toLowerCase().startsWith(partial)) completions.add(city);
            }
        }

        return completions;
    }
}
