class GameStats():
    # 跟踪游戏的统计信息
    def __init__(self, ai_settings):
        # 初始化统计信息
        self.ai_setiings = ai_settings
        self.high_score = 0
        self.reset_stats()

        # 让游戏一开始出于非活动状态
        self.game_active = False

    def reset_stats(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.ai_setiings.ship_limit
        self.score = 0
        self.level = 1
