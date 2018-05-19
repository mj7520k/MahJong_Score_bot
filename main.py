import re
import time
import twitter

# 定数
PARENT = 0
CHILD  = 1

TUMO   = 0
RON    = 1

child_table = [
8000, 8000, 12000, 12000, 16000, 16000, 16000, 24000, 24000, 32000
]

parent_table = list(map(lambda x : int(x * 1.5), child_table))

point_table = [parent_table, child_table]

# 10の位を切り上げ
def round_up(point):
    if point % 100 != 0:
        return point - (point % 100) + 100
    return point

# 和了り方に応じて点数の文字列を生成
def to_str(point, bc):
    point_str = ""

    if bc["winning"] == TUMO:
        if bc["dealer"] == CHILD:
            point_str = str(round_up(point // 4)) + "-" + str(round_up(point // 2))
        else:
            point_str = str(round_up(point // 3)) + "ALL"
    else:
        point_str = str(point)

    return point_str

# 満貫以上の点数の計算
def more_than_mangan(before_calc):
    bc = before_calc
    point = point_table[bc["dealer"]][(13 if bc["han"] > 13 else bc["han"]) - 4]

    return to_str(point, bc)

# 満貫未満の点数の計算
def less_than_mangan(before_calc):
    bc = before_calc
    point = round_up(bc["hu"] * (4 if bc["dealer"] == CHILD else 6) * 2 ** (han + 2))

    return to_str(point, bc)

# 点数を計算
def calculation_point(before_calculation):
    
    hu_list = [20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110]
    if before_calculation["hu"] not in hu_list or before_calculation["han"] == 0:
        return None
    if before_calculation["han"] <= 3 or (before_calculation["han"] == 4 and before_calculation["hu"] <= 30):
        point = less_than_mangan(before_calculation)
    else:
        point = more_than_mangan(before_calculation)

    return point

# 和了り情報から点数情報を生成、リスト化して返す
def get_results(pass_mentions):
    results = []

    for mention in pass_mentions:
        point = calculation_point(mention["before_calculation"])
        if point == None:
            print("Error > get_result_data : point None!")
            point = "Calculation Error!"
        result = {"id" : mention["id"], "screen_name" : mention["screen_name"], "result" : point}
        results.append(result)

    return results

# 和了り情報の形式が正しいか判定
# 正しいメンションをリスト化
def select_pass_mentions(mentions):
    pass_mentions = []

    for mention in mentions:
        if re.search(r"[0-9]+-[0-9]+-(p|c)-(t|r)", mention["text"]):
            before_calculation_str = re.search(r"[0-9]*-[0-9]*-(p|c)-(t|r)", mention["text"]).group()
            splits = before_calculation_str.split('-')
            han     = int(splits[0])
            hu      = int(splits[1])
            dealer  = PARENT if splits[2] == "p" else CHILD
            winning = TUMO if splits[3] == "t" else RON
            before_calculation = {"han" : han, "hu" : hu, "dealer" : dealer, "winning" : winning}
            pass_mention = {"id" : mention["id"], "screen_name" : mention["screen_name"], "before_calculation" : before_calculation}
            pass_mentions.append(pass_mention)
        else:
            print("Error > check_call_mentions : Format Error!")

    return pass_mentions

# ツイート内に判定オプションがあるメンションをリスト化
def select_option_mentions(mentions):
    option_mentions = []

    for mention in mentions:
        if re.search(r"-mahP", mention["text"]):
            option_mention = {"id" : mention["id"], "screen_name" : mention["user"]["screen_name"], "text" : mention["text"]}
            option_mentions.append(option_mention)

    return option_mentions

def main():
    oauth = twitter.init()
    
    since_id = None

    while True:
        mentions = twitter.get_mentions(oauth, since_id)
        if mentions:
            since_id = mentions[0]["id"]
        option_mentions = select_option_mentions(mentions)
        pass_mentions = select_pass_mentions(option_mentions)
        results = get_results(pass_mentions)
        twitter.result_reply(oauth, results)

        time.sleep(15)

if __name__ == "__main__":
    main()
