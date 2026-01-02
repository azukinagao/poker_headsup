from deck import Deck
from player import Player
from hand_eval import evaluate_hand

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("You")
        self.opponent = Player("Bot")
        self.community_cards = []
        self.pot = 0

    def start_new_hand(self):
        self.player.reset_for_new_hand()
        self.opponent.reset_for_new_hand()
        self.deck = Deck()
        self.community_cards = []

        self.player.hand = self.deck.deal(2)
        self.opponent.hand = self.deck.deal(2)

        print(f"{self.player.name} の手札: {self.player.hand}")
        # print(f"{self.opponent.name} の手札: {self.opponent.hand}（← 本番は隠す）")
        print(f"{self.opponent.name} の手札: [??, ??]")

        # プリフロップ
        print("\n--- ベッティングラウンド（プリフロップ） ---")
        self.betting_round(is_preflop=True)

        if self.player.folded:
            print(f"{self.player.name} がフォールドしたので {self.opponent.name} の勝ち！")
            self.opponent.chips += self.pot
            return
        elif self.opponent.folded:
            print(f"{self.opponent.name} がフォールドしたので {self.player.name} の勝ち！")
            self.player.chips += self.pot
            return

        # フロップ
        self.community_cards += self.deck.deal(3)
        print(f"\nフロップ: {self.community_cards}")
        print("\n--- ベッティングラウンド（フロップ） ---")
        self.betting_round(is_preflop=False)
        if self.player.folded:
            print(f"{self.player.name} がフォールドしたので {self.opponent.name} の勝ち！")
            self.opponent.chips += self.pot
            return
        elif self.opponent.folded:
            print(f"{self.opponent.name} がフォールドしたので {self.player.name} の勝ち！")
            self.player.chips += self.pot
            return

        # ターン
        self.community_cards += self.deck.deal(1)
        print(f"\nターン: {self.community_cards}")
        print("\n--- ベッティングラウンド（ターン） ---")
        self.betting_round(is_preflop=False)
        if self.player.folded:
            print(f"{self.player.name} がフォールドしたので {self.opponent.name} の勝ち！")
            self.opponent.chips += self.pot
            return
        elif self.opponent.folded:
            print(f"{self.opponent.name} がフォールドしたので {self.player.name} の勝ち！")
            self.player.chips += self.pot
            return

        # リバー
        self.community_cards += self.deck.deal(1)
        print(f"\nリバー: {self.community_cards}")
        print("\n--- ベッティングラウンド（リバー） ---")
        self.betting_round(is_preflop=False)
        if self.player.folded:
            print(f"{self.player.name} がフォールドしたので {self.opponent.name} の勝ち！")
            self.opponent.chips += self.pot
            return
        elif self.opponent.folded:
            print(f"{self.opponent.name} がフォールドしたので {self.player.name} の勝ち！")
            self.player.chips += self.pot
            return
        self.showdown()

    def betting_round(self, is_preflop=False):
        # print("\n--- ベッティングラウンド（プリフロップ） ---" if is_preflop else "\n--- ベッティングラウンド ---")

        small_blind = 10
        big_blind = 20

        if is_preflop:
            # ブラインドの支払い（プリフロップのみ）
            self.player.chips -= small_blind
            self.player.current_bet = small_blind

            self.opponent.chips -= big_blind
            self.opponent.current_bet = big_blind

            self.pot = small_blind + big_blind
            turn_order = [self.player, self.opponent]  # SB → BB（You → Bot）
        else:
            pot = 0
            self.player.current_bet = 0
            self.opponent.current_bet = 0
            turn_order = [self.opponent, self.player]  # BB → SB（You 後攻）

        last_action_was_raise = False

        while True:
            for p in turn_order:
                if p.folded:
                    continue

                to_call = max(self.player.current_bet, self.opponent.current_bet) - p.current_bet

                # 有効なアクションの表示
                if to_call == 0:
                    valid_actions = ["check", "raise", "fold"]
                else:
                    valid_actions = ["call", "raise", "fold"]

                print(f"\n{p.name}のターン")
                print(f"現在のポット: {self.pot}")
                print(f"{p.name} のチップ: {p.chips}")
                print(f"{p.name} のベット: {p.current_bet}")
                print(f"可能なアクション: {', '.join(valid_actions)}")

                if p.name == "You":
                    action = input("アクションを選んでください: ").strip().lower()
                    while action not in valid_actions:
                        print("無効なアクションです。")
                        action = input(f"アクションを選んでください ({', '.join(valid_actions)}): ").strip().lower()
                else:
                    import random
                    action = random.choice(valid_actions)
                    print(f"{p.name}のアクション: {action}")

                # アクション処理
                if action == "fold":
                    p.folded = True
                    print(f"{p.name} はフォールドしました")
                    return  # ラウンド終了

                elif action == "check":
                    print(f"{p.name} はチェックしました")
                    continue  # 次のプレイヤーへ

                elif action == "call":
                    p.chips -= to_call
                    p.current_bet += to_call
                    self.pot += to_call
                    print(f"{p.name} はコールしました（{to_call}）")
                    if last_action_was_raise:
                        print("レイズに対してコールが返ったのでラウンド終了。")
                        print(f"{self.pot} ポットが確定しました")
                        self.player.current_bet = 0
                        self.opponent.current_bet = 0
                        return
                    last_action_was_raise = False

                elif action == "raise":
                    raise_amount = 20
                    total = to_call + raise_amount
                    p.chips -= total
                    p.current_bet += total
                    self.pot += total
                    print(f"{p.name} はレイズしました（+{raise_amount}）→ 合計 {total} のbet")
                    last_action_was_raise = True

            # レイズなしで両者のベット額が同じならラウンド終了（チェック or コール）
            if self.player.current_bet == self.opponent.current_bet and not last_action_was_raise:
                print("チェックでラウンド終了。")
                break

        print(f"ラウンド終了！ ポット: {self.pot}")
        self.player.current_bet = 0
        self.opponent.current_bet = 0

    def showdown(self):
        print("\n--- ショーダウン ---")
        
        player_hand = self.player.hand + self.community_cards
        opponent_hand = self.opponent.hand + self.community_cards

        print(f"あなたの手札: {self.player.hand}")
        print(f"Botの手札: {self.opponent.hand}")
        print(f"ボード: {self.community_cards}")

        player_eval, player_hand_name = evaluate_hand(player_hand)
        opponent_eval, opponent_hand_name = evaluate_hand(opponent_hand)

        player_rank_value, player_kicker = player_eval
        opponent_rank_value, opponent_kicker = opponent_eval

        # 数値のキッカーを文字に変換
        RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        player_kicker_str = RANKS[player_kicker - 2]  # 2がindex0なので-2する
        opponent_kicker_str = RANKS[opponent_kicker - 2]

        print(f"Your hand: {player_hand_name} (High card: {player_kicker_str})")
        print(f"Bot's hand: {opponent_hand_name} (High card: {opponent_kicker_str})")

        if player_eval > opponent_eval:
            print("あなたの勝ち！")
            self.player.chips += self.pot
        elif player_eval < opponent_eval:
            print("botの勝ち！")
            self.opponent.chips += self.pot
        else:
            print("引き分け！")
            self.player.chips += self.pot // 2
            self.opponent.chips += self.pot // 2

        self.pot = 0


if __name__ == "__main__":
    game = Game()
    game.start_new_hand()
