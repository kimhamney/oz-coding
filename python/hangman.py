import random

words = ["apple", "banana", "orange", "grape", "lemon"]
count = 10;

word = random.choice(words)
correctList = list('_' * len(word))

while count > 0:
    count -= 1

    guess = input("알파벳 한 글자를 입력해주세요: ").lower()

    isCorrect = False
    for idx, value in enumerate(word):
        if value == guess:
            isCorrect = True
            correctList[idx] = guess
            
    if isCorrect:
        if ''.join(correctList) == word:
            print(f'성공! 다맞췄습니다! 정답 : {word}')
            break
        else:    
            print('단어를 맞추셨군요. 더 힘내봐요')
    else:
        print(f'틀렸습니다. 남은 시도 횟수 : {count}')

    print(*correctList, sep=" ")
    
    if count == 0:
        print(f'실패입니다. 정답 : {word}')