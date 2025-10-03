package skylink.infrastructure.commands;

import skylink.infrastructure.commands.location.CoordCommand;
import skylink.infrastructure.commands.location.CityCommand;

import skylink.domain.config.PluginConfig;

import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.command.Command;
import org.bukkit.entity.Player;

public class SkyLinkCommand implements CommandExecutor, TabCompleter {
    private final CoordCommand coordCommand;
    private final CityCommand cityCommand;

    public SkyLinkCommand(PluginConfig config) {
        this.coordCommand = new CoordCommand(config);
        this.cityCommand = new CityCommand(config);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("§cThis command can only be used by players.");
            return true;
        }

        Player player = (Player) sender;

        if (!player.hasPermission("skylink.location")) {
            player.sendMessage("§cYou don't have permission to use this command.");
            return true;
        }

        if (args.length < 2) {
            player.sendMessage("§cUsage: /skylink <city|coordinates> <value>");
            player.sendMessage("§cExamples:");
            player.sendMessage("§c  /skylink city UK/London");
            player.sendMessage("§c  /skylink coordinates 51.5074 -0.1278");

            return true;
        }

        String subcommand = args[0].toLowerCase();
        
        if (subcommand.equals("city")) {
            String[] cityArgs = new String[args.length - 1];
            System.arraycopy(args, 1, cityArgs, 0, args.length - 1);

            return cityCommand.onCommand(sender, command, label, cityArgs);
        }

        else if (subcommand.equals("coordinates")) {
            String[] coordArgs = new String[args.length - 1];
            System.arraycopy(args, 1, coordArgs, 0, args.length - 1);
            return coordCommand.onCommand(sender, command, label, coordArgs);
            
        }

        else {
            player.sendMessage("§cInvalid subcommand! Use 'city' or 'coordinates'");
            return true;
        }
    }

    @Override
    public java.util.List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        java.util.List<String> completions = new java.util.ArrayList<>();

        if (args.length == 1) {
            if ("city".startsWith(args[0].toLowerCase())) completions.add("city");
            if ("coordinates".startsWith(args[0].toLowerCase())) completions.add("coordinates");
            
        }

        else if (args.length >= 2) {
            String subcommand = args[0].toLowerCase();
            
            if (subcommand.equals("city")) {
                String[] cityArgs = new String[args.length - 1];
                System.arraycopy(args, 1, cityArgs, 0, args.length - 1);
                return cityCommand.onTabComplete(sender, command, alias, cityArgs);
                
            }

            else if (subcommand.equals("coordinates")) {
                String[] coordArgs = new String[args.length - 1];
                System.arraycopy(args, 1, coordArgs, 0, args.length - 1);

                return coordCommand.onTabComplete(sender, command, alias, coordArgs);
            }
        }

        return completions;
    }
}