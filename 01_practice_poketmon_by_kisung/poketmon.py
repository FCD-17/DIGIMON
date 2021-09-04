# 필요한 패키지 불러오기 
import pypokedex                  # PokeAPI를 사용할 수 있는 파이썬 패키지
import pandas as pd               # pandas 패키지 
import numpy as np                # numpy 패키지 
from PIL import Image             # Python Image Library
from pyfiglet import Figlet       # 파이썬 코드에서 아스키 문자를 받아 아스키 폰트로 렌더링 해주는 패키지
from colors import color, cyan    # 파이썬 출력 문자 색상 변경 패키지 - pip install ansicolors
import requests                   # API를 불러올 때 사용하는 패키지 

# 먼저 터미널 스크린 clear
print("\x1b[2J", end='')

# pandas 패키지로 포켓몬네임 csv 파일 불러오기 - 한글이름과 영어 이름으로 구성되어 있음.
df = pd.read_csv('poke_names.csv')

# 한국어 네임 입력 

name_ko = ''                                                       # 빈칸으로 초기화

while name_ko != '끝':                                              # 끝이라고 입력하면 while 루프를 종료 
    name_ko = input('포켓몬 이름을 입력해주세요: ')                       # 포켓몬 입력창
    if len(df.loc[df['name_ko'] == name_ko, 'name_en']) ==0:       # 만약 검색 된 것이 없다면 
        continue                                                   # 위로 다시 반환 
    name_en = df.loc[df['name_ko'] == name_ko, 'name_en'].item()   # 만약 검색 결과가 있으면 영어 이름으로 반환하여 변수에 저장

    print("\x1b[2J", end='')                                       # 다시 터미널 스크린 clear

    p = pypokedex.get(name=name_en)                                # pypoke API를 사용해서 영어 이름으로 검색후 결과를 P라는 변수에 저장 

    img_url = p.sprites.front['default']                           # P 결과의 앞면 이미지를 불러오고 기본 이미지를 넣고 선언한 변수에 저장
    img = np.array(Image.open(requests.get(img_url, 
          stream=True).raw).resize((32, 32)).convert('RGB'),       # 사이즈를 32 x 32로 줄여 색깔을 입힌 이미지를 변수에 저장 
          dtype=np.uint8)
    
    for row in img:
        for pixel in row:                                           # 한 픽셀식 받아와서 터미널에 색깔을 입히는 작업 
            print(color('  ', bg=f'rgb({pixel[0]}, {pixel[1]}, {pixel[2]})'), end='')  # 정사각형 모양에 
        print()                                                                        # 터미널 백그라운드를 rgb 형태로 지정

    print(cyan(Figlet().renderText(f'{p.dex} - {p.name.upper()}')))  # Figlet을 통해 랜더텍스트에 포켓몬 번호와 이름을 대문자로 하늘색으로 출력
    print(Figlet(font='slant').renderText(' / '.join(p.types)))      # Figlet을 통해 슬랜트라는 폰트를 이용, 타입을 슬레시로 구분하여 표시 

    # 스텟창 구현 함수 - 프로그레스바를 이용하여 생명력, 공격력, 방어력, 스피드의 데이터를 출력 
    def print_stats(iteration, total, prefix='', suffix='', length=100, fill='█'):
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {iteration} {suffix}')
    
    print_stats(p.base_stats.hp, 100, 'HP ', length=60)
    print_stats(p.base_stats.attack, 100, 'ATK', length=60)
    print_stats(p.base_stats.defense, 100, 'DEF', length=60)
    print_stats(p.base_stats.speed, 100, 'SPD', length=60)    