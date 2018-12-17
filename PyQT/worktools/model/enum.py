from core import EnumLabel

"""
所有枚举类型
"""


# 牌类型
class CardType(EnumLabel):
    InitCard = 0  # 初始化的牌组
    HandCard = 1  # 手牌
    DealCard = 2  # 待发牌


# 游戏类型
class GameType(EnumLabel):
    ZIPAI = 1
    POKER = 2
    MJ = 3


# DeckWidget类型
class DeckType(EnumLabel):
    Hand = 0  # 手牌
    PerDeploy = 1  # 待发牌

    class Labels:
        Hand = '手牌'
        PerDeploy = '待发牌'


# 更新状态
class UpdateStatus(EnumLabel):
    Begin = 1
    Downloading = 2
    Downloaded = 3
    Success = 4
    Fail = 5
