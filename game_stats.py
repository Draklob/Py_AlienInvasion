class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_stts):
        """Initialize statistics."""
        self.ai_stts = ai_stts

        self.player_lives = self.ai_stts.player_lives
        self.score = 0
        self.level = 1

        # Start Alien Invasion in an active state.
        self.game_active = False

        # The game is already running.
        self.game_running = False

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        print("Reseting stats")
        self.player_lives = self.ai_stts.player_lives
        self.score = 0
        self.level = 1

