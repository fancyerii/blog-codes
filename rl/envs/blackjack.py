import gym
from gym import spaces
from gym.utils import seeding

def cmp(a, b):
    return int((a > b)) - int((a < b))

# 1 = Ace, 2-10 = Number cards, Jack/Queen/King = 10
deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def draw_card(np_random):
    return np_random.choice(deck)


def draw_hand(np_random):
    return [draw_card(np_random), draw_card(np_random)]


def usable_ace(hand):  # 是否有可用的Ace
    return 1 in hand and sum(hand) + 10 <= 21


def sum_hand(hand):  # 当前的和，Ace能用就加10。
    if usable_ace(hand):
            return sum(hand) + 10
    return sum(hand)


def is_bust(hand):  # 是否爆了
    return sum_hand(hand) > 21


def score(hand):  # 如果爆了0分，否则是当前的和
    return 0 if is_bust(hand) else sum_hand(hand)


def is_natural(hand):  # 是否natural牌
    return sorted(hand) == [1, 10]


class BlackjackEnv(gym.Env):
    """简单的blackjack环境
    Blackjack是一个纸牌游戏，目的是纸牌的和尽量接近21但是不能超过。这里的玩家是和一个
    固定策略的庄家。
    花牌(Jack, Queen, King)是10。 have point value 10.
    Ace即可以看成11也可以看成1，如果可以看成11那么就叫Usable。
    这个游戏可以任务牌的数量是无限的。因此每次取牌的概率是固定的。
    游戏开始时玩家和庄家都有两张牌，庄家的一张牌是亮出来的。
    玩家可以要牌或者停止要牌。如果玩家的牌超过21点，则庄家获胜。
    如果玩家没有超过21点就停止要牌，则轮到庄家要牌，这里的庄家是采取固定的策略——如果没超过16就
    继续要牌，如果超过16（大于等于17）则停止要牌。如果庄家超过21点则玩家获胜，
    否则比较两人牌的大小，大者获胜，一样大则平局。赢的reward是1，输了-1，平局0。
    """
    def __init__(self, natural=False):
        self.action_space = spaces.Discrete(2)
        # Tuple-1 1-31表示玩家的牌的和，注意如果玩家到了21点肯定不会再要牌，
        # 因此即使爆了和最大也是20+11=31，其实根据我们的分析12以下也
        # 没必要有，不过有也没关系。
        # Tuple-2 1-10表示庄家亮牌的点数
        # Tuple-3 0和1表示是否有可用的Ace
        self.observation_space = spaces.Tuple((
            spaces.Discrete(32),
            spaces.Discrete(11),
            spaces.Discrete(2)))
        self.seed()

        # 这个Flag表示如果玩家natural赢了的奖励是1.5倍。
        self.natural = natural
        # 开始游戏
        self.reset()
        self.nA = 2

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        if action:  # hit: 继续要牌
            self.player.append(draw_card(self.np_random))
            if is_bust(self.player):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else:  # stick: 玩家不要牌了，模拟庄家的策略直到游戏结束。
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(draw_card(self.np_random))
            reward = cmp(score(self.player), score(self.dealer))
            # 如果self.natural并且玩家通过natural获胜，这是1.5倍奖励
            if self.natural and is_natural(self.player) and reward == 1:
                reward = 1.5
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))

    def reset(self):
        # 每人都来两张牌
        self.dealer = draw_hand(self.np_random)
        self.player = draw_hand(self.np_random)

        # 如果玩家的牌没到12点就自动帮他要牌
        while sum_hand(self.player) < 12:
            self.player.append(draw_card(self.np_random))

        return self._get_obs()