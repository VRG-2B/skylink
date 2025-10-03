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

public class CoordCommand implements CommandExecutor, TabCompleter {
    private final PluginConfig config;
    private final HttpClient httpClient;

    public CoordCommand(PluginConfig config) {
        this.config = config;
        this.httpClient = HttpClient.newHttpClient();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        Player player = (Player) sender;

        if (args.length != 2) {            
            player.sendMessage("§cUsage: /skylink coordinates <latitude> <longitude>");
            player.sendMessage("§cExample: /skylink coordinates 51.5074 -0.1278");
            return true;
        }

        double latitude, longitude;

        try {
            latitude = Double.parseDouble(args[0]);
            longitude = Double.parseDouble(args[1]);
        }

        catch (NumberFormatException e) {
            player.sendMessage("§cInvalid coordinates! Please enter valid numbers.");
            return true;
        }

        if (latitude < -90.0 || latitude > 90.0) {
            player.sendMessage("§cInvalid latitude! Must be between -90 and 90.");
            return true;
        }

        if (longitude < -180.0 || longitude > 180.0) {
            player.sendMessage("§cInvalid longitude! Must be between -180 and 180.");
            return true;
        }

        try {
            String url = "http://" + config.getHost() + ":" + config.getPort() + "/location/coordinates";
            String jsonBody = "{\"latitude\": " + latitude + ", \"longitude\": " + longitude + "}";

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                player.sendMessage("§aLocation set to coordinates: " + latitude + ", " + longitude);
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
            completions.add("51.5074");  // London latitude example
            completions.add("40.7128");  // NYC latitude example
        }

        else if (args.length == 2) {
            completions.add("-0.1278");  // London longitude example
            completions.add("-74.0060"); // NYC longitude example
        }

        return completions;
    }
}
