package skylink.infrastructure.api;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import skylink.domain.config.PluginConfig;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Optional;
import java.util.logging.Logger;

public class SkyLinkApiClient {
    private final HttpClient httpClient;
    private final PluginConfig config;
    private final Gson gson;
    private final Logger logger;

    public SkyLinkApiClient(PluginConfig config, Logger logger) {
        this.config = config;
        this.logger = logger;
        this.gson = new Gson();
        this.httpClient = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();
    }

    public record TimeResponse(int ticks) {}
    public record PrecipitationResponse(boolean rain, boolean thunder) {}

    public Optional<TimeResponse> getTime(String city) {
        try {
            String url = config.getApiBaseUrl() + "/time?city=" + encodeCity(city);
            HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).timeout(Duration.ofSeconds(10)).GET().build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            
            if (response.statusCode() == 200) {
                JsonObject json = gson.fromJson(response.body(), JsonObject.class);
                int ticks = json.get("ticks").getAsInt();
                return Optional.of(new TimeResponse(ticks));
            }

            else {
                logger.warning("Failed to get time from API: HTTP " + response.statusCode());
                return Optional.empty();
            }
        }

        catch (Exception e) {
            logger.warning("Error fetching time from API: " + e.getMessage());
            return Optional.empty();
        }
    }

    public Optional<PrecipitationResponse> getPrecipitation(String city) {
        try {
            String url = config.getApiBaseUrl() + "/precipitation?city=" + encodeCity(city);
            HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).timeout(Duration.ofSeconds(10)).GET().build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            
            if (response.statusCode() == 200) {
                JsonObject json = gson.fromJson(response.body(), JsonObject.class);
                boolean rain = json.get("rain").getAsBoolean();
                boolean thunder = json.get("thunder").getAsBoolean();
                return Optional.of(new PrecipitationResponse(rain, thunder));
            }

            else {
                logger.warning("Failed to get precipitation from API: HTTP " + response.statusCode());
                return Optional.empty();
            }
        }

        catch (Exception e) {
            logger.warning("Error fetching precipitation from API: " + e.getMessage());
            return Optional.empty();
        }
    }

    public boolean isHealthy() {
        try {
            String url = config.getApiBaseUrl() + "/health";
            HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).timeout(Duration.ofSeconds(5)).GET().build();
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            return response.statusCode() == 200;
        }

        catch (Exception e) {
            return false;
        }
    }

    private String encodeCity(String city) {
        return java.net.URLEncoder.encode(city, java.nio.charset.StandardCharsets.UTF_8);
    }
}
