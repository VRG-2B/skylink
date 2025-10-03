package skylink.infrastructure.commands.location;

import skylink.domain.config.PluginConfig;

import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.command.Command;

import org.bukkit.entity.Player;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import java.net.URI;

import java.util.regex.Pattern;

public class CityCommand implements CommandExecutor, TabCompleter {
    private final PluginConfig config;
    private final HttpClient httpClient;

    private static final Pattern CITY_PATTERN = Pattern.compile("^[A-Za-z]+/[A-Za-z\\s]+$");

    public CityCommand(PluginConfig config) {
        this.config = config;
        this.httpClient = HttpClient.newHttpClient();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        Player player = (Player) sender;

        if (args.length != 1) {            
            player.sendMessage("§cUsage: /skylink city <Country/City>");
            player.sendMessage("§cExample: /skylink city UK/London");
            return true;
        }

        String cityInput = args[0];

        if (!CITY_PATTERN.matcher(cityInput).matches()) {
            player.sendMessage("§cInvalid city format! Use: Country/City (e.g., UK/London)");
            return true;
        }

        try {
            String url = "http://" + config.getHost() + ":" + config.getPort() + "/location/city";
            String jsonBody = "{\"city\": \"" + cityInput + "\"}";

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                player.sendMessage("§aLocation set to: " + cityInput);
            }

            else {
                player.sendMessage("§cFailed to set location. Server responded with status: " + response.statusCode());
            }
        }

        catch (Exception e) {
            player.sendMessage("§cError connecting to location service: " + e.getMessage());
        }

        return true;
    }

    @Override
    public java.util.List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        java.util.List<String> completions = new java.util.ArrayList<>();

        if (args.length == 1) {
            completions.add("UK/London");
            completions.add("US/New_York");
            completions.add("France/Paris");
        }

        return completions;
    }
}
