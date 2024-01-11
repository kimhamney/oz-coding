import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_input_nums():
    print("--- 로또 입력 메뉴 ---")
    print("1. 로또 번호 입력")
    print("2. 랜덤 번호 생성")
    input_type = input("입력 메뉴를 선택해주세요 : ")

    if input_type == "1":
        lotto_nums = get_manual_nums()
    else:
        lotto_nums = get_random_nums()

    return lotto_nums 

def get_manual_nums():
    lotto_nums = []
    while len(lotto_nums) < 6: # 로또 번호 6개 입력받기
        try:
            num = int(input(f"로또 번호를 입력해주세요 {len(lotto_nums) + 1}번째: "))
            if 1 <= num <= 45 and num not in lotto_nums:
                lotto_nums.append(num)
            else:
                print("1부터 45 사이의 중복되지 않는 숫자를 입력하세요.")
        except ValueError:
            print("숫자를 입력하세요.")
    
    return lotto_nums

def get_random_nums():
    return random.sample(range(1, 46), 6)

def get_winning_nums(round):
    load_data = load_nums(round)
    if load_data == None: # 저장된 데이터가 없으면 크롤링
        winning_nums, bonus_nums = crawling_lotto_data(round)
    else:
        winning_nums = load_data["win_nums"]
        bonus_nums = load_data["bonus_num"]

    return winning_nums, bonus_nums

def crawling_lotto_data(round):
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round}"

    options = webdriver.ChromeOptions()
    options.add_argument("headless") # 창 숨기는 옵션 추가

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # 당첨번호 + 보너스번호 읽기
    ball_elements = driver.find_elements(By.CLASS_NAME, "ball_645")
    ball_nums = [int(i.text) for i in ball_elements]

    win_nums = ball_nums[:6]
    bonus_num = ball_nums[-1]

    driver.quit()

    # file에 저장
    save_nums(round, win_nums, bonus_num)

    return win_nums, bonus_num

def load_nums(round):
    try:
        with open("winning_nums.json", "r") as file:
            json_data = json.load(file)
            round_data = json_data.get(str(round), [])
            if round_data:
                return round_data
    except Exception as e:
            return None

# 파일에서 데이터를 불러온 뒤 데이터 추가한 후 다시 저장
def save_nums(round, win_nums, bonus_num):
    load_datas = {}
    try:
        with open("winning_nums.json", 'r') as file:
            load_datas = json.load(file)
    except Exception as e:
        pass

    load_datas[round] = {"win_nums": win_nums, "bonus_num": bonus_num}

    with open("winning_nums.json", 'w') as file:
        json.dump(load_datas, file, indent=2)

def check_winning(input_nums, winning_nums):
    matching_nums = set(input_nums) & set(winning_nums)
    return len(matching_nums)

def print_result(round, input_nums, winning_nums, bonus_num, winning_count):
    print(f"--- {round}회 당첨 결과 ---")
    print(f"당첨 번호 : {winning_nums} + 보너스 : {bonus_num}")
    print(f"내 번호   : {input_nums}")

    rank = get_rank(winning_count, bonus_num in input_nums)
    if rank > 0:
        money = get_prize_money(rank)
        print(f"{winning_count}개 맞음, {rank}등 당첨!!! 당첨금 : {money}원")
    else:
        print(f"{winning_count}개 맞음, 낙첨되었습니다..") 

def get_rank(winning_count, is_bonus):
    if winning_count == 6:
        return 1
    elif winning_count == 5 and is_bonus: # 2등은 보너스 번호도 맞아야함
        return 2
    elif winning_count == 5:
        return 3
    elif winning_count == 4:
        return 4
    elif winning_count == 3:
        return 5
    else:
        return 0
    
def get_prize_money(rank):
    money_list = ["1,000,000,000", "10,000,000", "1,000,000", "50,000", "5,000"]
    return money_list[rank - 1]

if __name__ == "__main__":
    round = input("회차 번호를 입력해주세요 : ")
    input_nums = get_input_nums()
    winning_nums, bonus_num = get_winning_nums(round)
    winning_count = check_winning(input_nums, winning_nums)
    print_result(round, input_nums, winning_nums, bonus_num, winning_count)
    