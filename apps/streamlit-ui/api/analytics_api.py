from api.client import APIClient
from utils.config import settings

class AnalyticsAPI(APIClient):
    def __init__(self):
        super().__init__(settings.ANALYTICS_SERVICE_URL)

    def get_listening_stats(self, days: int = 30):
        return self.get("/api/v1/analytics/listening-stats", params={"days": days})

    def get_mood_trends(self, days: int = 30):
        return self.get("/api/v1/analytics/mood-trends", params={"days": days})

    def get_personality(self):
        return self.get("/api/v1/analytics/personality")

    def get_year_in_review(self, year: int):
        return self.get("/api/v1/analytics/year-in-review", params={"year": year})
