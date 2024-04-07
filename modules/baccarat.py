
class Baccarat:
              
    def calc_score(self, hand) -> int:
        """SCOREを計算する"""
        score = 0
        for card in hand:
            score += card % 10 if card <= 10 else 0
        if score >= 10:
            score = int(str(score)[-1])
        else:
            pass
        return score

    def check_draw_player(self, player_score):
        """Player側の条件"""
        if player_score <= 5:
            return True
        elif player_score > 6:
            return False

    def check_draw_banker(self, banker_score, player_score):
        # bankerの条件
        if banker_score <= 2:
            return True
        elif banker_score == 3 and player_score != 8:
            return True
        elif banker_score == 4 and player_score in [2, 3, 4, 5, 6, 7]:
            return True
        elif banker_score == 5 and player_score in [4, 5, 6, 7]:
            return True
        elif banker_score == 6 and player_score in [6, 7]:
            return True
        else:
            return False

    def draw_third_card(self, player_hand:list[int], banker_hand:list[int]) -> dict[str, bool]:
        """3枚目のカードを引く処理判定する
        Return:
            True :3枚目を引く
            False:3枚目を引かない
        """
        result: dict[str, bool] = {
            "player" : False,
            "banker": False
        }
        max_card_count = 3
        if len(player_hand) < max_card_count:
            player_score: int = self.calc_score(player_hand)
            result['player'] = self.check_draw_player(player_score)
        else:
            pass

        if len(banker_hand) < max_card_count: 
            banker_score: int = self.calc_score(banker_hand)
            result['banker'] = self.check_draw_player(banker_score)
        else:
            pass

        return result

    def check_value(self, entered_value) -> bool:
        # 値のチェック
        if 0 <= entered_value <= 13:
            return True
        else: 
            return False
    
    def play_one_game(self, player_hand: list[int], banker_hand: list[int]) -> str:
        """ゲーム判定処理"""
        player_score: int = self.calc_score(player_hand)
        banker_score: int = self.calc_score(banker_hand)
        if player_score > banker_score:
            return "P"
        elif player_score < banker_score:
            return "B"
        else:
            return "D"
