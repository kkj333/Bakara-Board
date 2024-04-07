import tkinter as tk
from tkinter import ttk
from modules.baccarat import Baccarat
from modules.board import make_bord

class App(tk.Frame):

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.master.title("バカラ罫線")
        self.master.geometry("1000x800")
        self.pack()
        self.create_widgets()
        self.card_hands = {
            'player': [],
            'banker': []
        }
        self.match_results_list = []
        self.game_count = 0
        self.game_status = '1ゲーム目'
        self.input_count = 0
        self.max_flip_count = 4
        self.game_result = ''
        self.is_draw_third_card = {
            'player': False,
            'banker': False
        }

    def create_table(self) -> None:
        header = list(range(1, 41))
        self.member_list = [['◽'] * 40 for _ in range(10)]
        self.tree = ttk.Treeview(self.master)
        # 列を作成
        self.tree['columns'] = list(range(len(header)))
        # ヘッダーの設定
        self.tree['show'] = 'headings'
        for i, text in enumerate(header):
           self.tree.column(i, width=30, anchor='center') 
           self.tree.heading(i, text=text)
        # データ挿入
        for member in self.member_list:
           self.tree.insert('', 'end', values=member)
        self.tree.pack()

    def create_widgets(self) -> None:
        # 罫線表を作る
        self.create_table()
        # input form
        self.label = ttk.Label(self, text='1~13で数値を入力してください。')
        self.label.pack()
        self.number_value = tk.IntVar()
        self.entry = ttk.Entry(self, textvariable=self.number_value)
        self.entry.pack()
        #  buttons
        self.flip_button = ttk.Button(self, text='カードを引く', command=self.flip_card)
        self.flip_button.pack()
        self.button = ttk.Button(self, text='次のゲーム', command=self.next_game)
        self.button.pack()
        self.button = ttk.Button(self, text='ゲームリセット', command=self.reset_game)
        self.button.pack()
        # messages log
        self.result_label = ttk.Label(self, text="Playerの1枚目の数字を入力してください。")
        self.result_label.pack()
        self.player_label = tk.Label(self, text="Player Cards:")
        self.player_label.pack()
        self.banker_label = tk.Label(self, text="Banker Cards:")
        self.banker_label.pack()
        return None

    def reset_game(self):
        self.match_results_list = []
        self.game_result = ''
        self.game_count = 0
        self.card_hands = {
            'player': [],
            'banker': []
        }
        self.is_draw_third_card = {
            'player': False,
            'banker': False
        }
        self.max_flip_count = 4
        self.input_count = 0
        self.result_label.config(text=f'{self.game_count+1}ゲーム目')
        self.player_label.config(text=f"Playerのカード:{self.card_hands['player']}")
        self.banker_label.config(text=f"Blayerのカード:{self.card_hands['banker']}")
        self.flip_button.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)

    def next_game(self):
        self.game_result = ''
        self.game_count += 1
        self.max_flip_count = 4
        self.card_hands = {
            'player': [],
            'banker': []
        }
        self.is_draw_third_card = {
            'player': False,
            'banker': False
        }
        self.flip_button.config(state=tk.NORMAL)
        self.input_count = 0
        self.result_label.config(text=f'{self.game_count+1}ゲーム目')
        self.player_label.config(text=f"Playerのカード:{self.card_hands['player']}")
        self.banker_label.config(text=f"Blayerのカード:{self.card_hands['banker']}")
        self.entry.delete(0, tk.END)

    def flip_cards_up_to_four(self, entered_value) -> None:
        # 4枚目までカードをめくる
        match self.input_count:
            case 1:
                self.card_hands['player'].append(entered_value)
            case 2:
                self.card_hands['player'].append(entered_value)
            case 3:
                self.card_hands['banker'].append(entered_value)
            case 4:
                self.card_hands['banker'].append(entered_value)
        return None

    def show_flip_third_card(self):
        """
        3枚目のカードを引く状態を判定して表示させる
        """ 
        if self.is_draw_third_card['player'] and self.is_draw_third_card['banker']:
            self.game_status = 'プレイヤーとバンカーは3枚目のカードをめくってください。'
            self.max_flip_count = 6
        elif self.is_draw_third_card['player'] and not self.is_draw_third_card['banker']:
            self.game_status = 'プレイヤーは3枚目のカードをめくってください。'
            self.max_flip_count = 5
        elif not self.is_draw_third_card['player'] and self.is_draw_third_card['banker']:
            self.game_status = 'バンカーは3枚目のカードをめくってください。'
            self.max_flip_count = 5
        else:
            self.game_status = 'プレイヤーとバンカーは追加カードはなしです。'

    def flip_fifth_card(self, entered_value):
        if self.is_draw_third_card['player'] and self.is_draw_third_card['banker']:
            self.card_hands['player'].append(entered_value)
        elif self.is_draw_third_card['player'] and not self.is_draw_third_card['banker']:
            self.card_hands['player'].append(entered_value)
        elif not self.is_draw_third_card['player'] and self.is_draw_third_card['banker']:
            self.card_hands['banker'].append(entered_value)

    def flip_sixth_card(self, entered_value):
        if self.is_draw_third_card['player'] and self.is_draw_third_card['banker']:
            self.card_hands['banker'].append(entered_value)

    def get_value(self) -> int:
        """ 値を取得して返す """
        try:
            entered_value = self.number_value.get()
        except Exception:
            self.result_label.config(text="指定した値が無効です。")
        if not Baccarat().check_value(entered_value):
            self.result_label.config(text="指定した値が0~13の範囲を超えています。")
            raise Exception
        return entered_value

    def write_board(self):
        try:
            self.member_list[0][0] = 0
            self.update_treeview()
        except IndexError:
            self.result_label.config(text="指定した位置が無効です。")

    def update_treeview(self) -> None:
        # Treeviewを更新する
        self.tree.delete(*self.tree.get_children())
        for member in self.member_list:
           self.tree.insert('', 'end', values=member)

    def flip_card(self) -> None:
        """カードの値を追加する"""
        # 入力値を取得する
        entered_value = self.get_value()
        # カードをめくる回数をカウントする
        if self.input_count <= self.max_flip_count:
            self.input_count += 1
        # カードを4枚目までカードを引く
        if self.input_count <= 4:
            self.flip_cards_up_to_four(entered_value)
        # 3枚目を引くか判定をする
        if self.input_count == 4:
            self.is_draw_third_card: dict[str, bool] = Baccarat().draw_third_card(
                self.card_hands['player'], 
                self.card_hands['banker']
            )
            # テキストボックスに結果を表示させる
            self.show_flip_third_card()

        # 追加でカードを引く
        match self.input_count:
            case 5:
                self.flip_fifth_card(entered_value)
            case 6:
                self.flip_sixth_card(entered_value)

        # ゲームの勝敗を判定する
        if self.input_count == self.max_flip_count:
            self.game_result: str = Baccarat().play_one_game(
                self.card_hands['player'], 
                self.card_hands['banker']
            )
            self.game_status = f'ゲームの判定処理 {self.game_result}'
            # カードを引かないようにする
            self.flip_button.config(state=tk.DISABLED)
            # ボードに結果を記録する
            self.match_results_list.append(self.game_result)
            make_bord(self.match_results_list, self.member_list)
            self.update_treeview()

        # カードの内容を表示する
        self.result_label.config(text=self.game_status)
        self.player_label.config(text=f"Playerのカード:{self.card_hands['player']}")
        self.banker_label.config(text=f"Blayerのカード:{self.card_hands['banker']}")

def main():
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()