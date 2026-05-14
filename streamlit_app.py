import random

# じゃんけんの手
hands = ["グー", "チョキ", "パー"]

print("じゃんけんゲーム！")
print("0: グー")
print("1: チョキ")
print("2: パー")

while True:
    # プレイヤー入力
    player = input("数字を入力してください (0〜2、終了:q): ")

    if player.lower() == "q":
        print("ゲーム終了！")
        break

    if not player.isdigit() or int(player) not in [0, 1, 2]:
        print("0〜2 の数字を入力してください。")
        continue

    player = int(player)

    # コンピュータの手
    computer = random.randint(0, 2)

    print(f"\nあなた: {hands[player]}")
    print(f"コンピュータ: {hands[computer]}")

    # 勝敗判定
    if player == computer:
        print("あいこ！")
    elif (
        (player == 0 and computer == 1) or
        (player == 1 and computer == 2) or
        (player == 2 and computer == 0)
    ):
        print("あなたの勝ち！")
    else:
        print("コンピュータの勝ち！")

    print("-" * 20)