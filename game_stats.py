class GameStats():
    """Following game stats."""

    def __init__(self, ai_settings):
        """Initis stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Inits stats that change during the game."""
        self.ships_left = self.ai_settings.ship_limit
