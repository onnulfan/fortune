# -*- coding: utf-8 -*-

import csv
from itertools import *
import random

# 원격 데이터 요청 
# 로컬 데이터 업데이트 
# 로컬 데이터 읽기 

# 데이터 구조에 입력 
D = []  # D[] = 당청번호 데이터
K = []  # K[] = 당청번호별 가중치
B = []  # B[] = 빌드 데이터
C = []  # C[] = 완성 데이터
CR = [] # CR[] = 제외수 미적용 
E = []  # E[] = 제외수
EA = [] # EA[] = 제외수 전체 
CL = [] # CL[] = 제외수 포함한 리스트
LN = [] # 추천숫자 제한

i = 0

# 적용 변수
rev = 1 # True : ASC(low 빈출순), False : DESC(high 빈출순) 
EXCEP = 10 # 제외수 범위 

MAX = 6 # 셈플링 공략개수 , 6이상 수 
WEEK = 5 # 최근 몇주간 번호 제외

WON = 50000
GAME = WON / 1000 # 게임 개수
ESUM = 3 # 최근 출현 횟수가 1번인 수의 합 
AE = 10 # 선택숫자 추천횟수 제한 

# 적용 알고리즘
aa = 1  # 1 제외수 삽입, 2 빈출별 정렬

div = []
#803,5,9,14,26,30,43,2


def update_progress(workdone):
    print("\r Progress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone * 100)), 
    # print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone*100), end="", flush=True)
    # sys.stdout.write("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone * 100))
    # sys.stdout.flush()
    pass

def string_to_int_array(aa):
	aa = map(int, aa)
	aa.sort()
	return aa

def get_weight(idx) :
	weight = 0
	for d in D:
		if(idx in map(int, d[2:8])):
			# print(len(D), int(d[0]), idx, weight)
			if(len(D)*(-1) == d[0]):
				weight += d[0] * 100
			else:
				weight += d[0]
	return weight 

def flat_dimension(cd) :
	cc = []
	for c1 in cd:
		for c2 in c1:
			cc.append(c2)
	return cc 

def remove_duplicate(aa):
	aa = list(set(aa))
	return aa

def frequent_number(aa):
	global E
	r = []
	t = remove_duplicate(aa)[:]
	cnt = 0

	while cnt < 45:	
		cnt += 1
		r.append([cnt, aa.count(cnt)])

	r.sort(key=lambda x:x[0], reverse=False)
	E = r[:]

	r = filter(lambda x:x[:][1] != 0, r)
	return r

def make_recommend_number(r):
	global C, CR
	C = CR[:]
	for rr in r:
		if(rr[0] in CR):
			C.remove(rr[0])

	if(len(C) <= 0):
		print('EXCEPTION : EMPTY RECOMMEND NUMBER ')

def make_except_number(aa):
	global EA
	EA = remove_duplicate(aa)[:]

def except_number() :
	global K,D
	ee = [] # week 빈출 임시변수 
	r = [] # week범위 자주 빈출 숫자 

	for dd in D[:WEEK]:
		ee.append(dd[2:8])

	ee = flat_dimension(ee)
	ee = string_to_int_array(ee)
	make_except_number(ee)

	r = frequent_number(ee)
	make_recommend_number(r)

def valid_extract_number():
	tol = []
	tol.append(CR)
	tol.append(EA)
	tol.append(C)

	tol = flat_dimension(tol)
	if(len(tol) < 6):
		return False
	return True

def init_limited_number():
	count_num = []
	cnt = 1
	while cnt < 45:
		count_num.append([cnt, 0])
		cnt += 1

	return count_num

def core_number():
	ai = []
	nr = []
	kkt = []
	kk = []
	eea = []
	need = 0
	cnt = 0
	
	ai = filter(lambda x:x[:][1] != 0, E)	
	ai.sort(key=lambda x:x[1], reverse=False)

	need = 0 if 6-len(C)<=0 else 6-len(C) 
	ai = filter(lambda x:x[:][0] in CR, ai)

	nr = C[:]
	for aii in ai[:need]:
		nr.append(aii[0])	

	ee = E[:]
	ee.sort(key=lambda x:x[:][1], reverse=False)
	ee = filter(lambda x:x[:][0] not in nr, ee)
	
	ttmp = []

	while cnt < 45:
		ein = filter(lambda x:x[:][1] == cnt, ee)
		if(len(ein) == 0): 
			break 

		for einn in ein:
			kkk = filter(lambda x:x[:][0] == einn[0], K)[0]
			kkt.append(kkk)

		kkt.sort(key=lambda x:x[:][1], reverse=True)
		eea.extend([x[0] for x in kkt])

		ttmp.extend([x for x in kkt])

		kkt = []

		cnt += 1

	# nrr = nr[:]
	# ttmp.sort(key=lambda x:x[:][1], reverse=True)
	# ttmp = [x[0] for x in ttmp]
	# nrr.extend(ttmp)

	nr.extend(eea)

	# print(nrr)
	print(nr)
	return nr

def make_pattern():
	ok = [0, 0, 0, 0, 0, 0]

	if(tt <= 7):
		ok[0] = 1
	elif(tt > 8 and tt <= 14):
		ok[1] = 1
	elif(tt > 15 and tt <= 21):
		ok[2] = 1
	elif(tt > 22 and tt <= 35):
		ok[3] = 1
	elif(tt > 36 and tt <= 45):
		ok[4] = 1
	pass

def check_sum(t):
	cs = 0
	
	for tt in t:
		tmp = filter(lambda x:x[:][0] == tt, E)
		if(tmp[0][1] == 1):
			cs += 1

	if(cs == ESUM):
		return True
	else: 
		return False

def limited_number(t):
	for tt in t:
		LN[tt-1][1] = LN[tt-1][1] + 1
		if (LN[tt-1][1] > AE): 
			return False
	return True

def make_game_list_a1(nr):
	global CL
	cnt = 0
	cl = []

	# 순열
	# p = list(combinations(nr[: 20 if GAME > 20 else 10],6))
	p = list(combinations(nr,6))
	print('TOTAL :', len(p), 'CREAT :', GAME)

	while True:
		t = list(p[cnt][:])	
		t.sort()
		# print(t)
		if(t not in cl):
			# if(check_sum(t) == True):
			# if(limited_number(t) == True):
			cl.append(t)
			pass

		# if(div == t): 
		# 	print(cnt)
		# 	break
			
		cnt += 1

		if(len(cl) > GAME or len(p) <= cnt):
		# if(len(p) <= cnt):
			break

	CL = cl[:GAME]

def aa_insert_recommend_number():
	make_game_list_a1(core_number())

def make_game_list_a2(nr):
	global CL
	cnt = 0 
	cl = []
	
	# 조합 
	# p = random.shuffle(nr[:20 if GAME > 20 else 10])
	p = list(combinations(nr[: 20 if GAME > 20 else 10],6))
	print('TOTAL :', len(p), 'CREAT :', GAME)

	while True:
		t = list(p[cnt][:])	
		t.sort()
		if(t not in cl):
			cl.append(t)

		cnt += 1

		if(len(cl) > GAME or len(p) <= cnt):
			break

	CL = cl[:GAME]

def aa_cycle_number():
	make_game_list_a2(core_number())

## main 

print('SAMPLING : ', MAX)
print('ORDER BY : ', 'LOW FREQUENT' if rev else 'HIGH FREQUENT')

f = open('./excel/lotto.csv', 'r')
rdr = csv.reader(f)

for line in rdr:
    line.insert(0, int(line[0])*(-1))
    D.append(line)
f.close()  

# K 가중치 구하기
while i < 45:
	i += 1
	K.append([i, get_weight(i)])

# 회차별 당청번호
# print(D)

# 변호별 가중치 정렬
K.sort(key=lambda x: x[1], reverse=rev)
# print(K)

# 샘플링 갯수로 추천수 
CR = [[c[0]] for c in K[:MAX]]
CR = flat_dimension(CR)
# print(CR)

LN = init_limited_number()

# 최근 몇주 당청번회 제외
except_number()

print('RECOMMAND : ', CR)
print('EXCEPT ALL : ',str(WEEK) + ' week(s)', EA)	
ES = E[:]
ES.sort(key=lambda x:x[:][1], reverse=False)
print('EXCEPT : ',str(WEEK) + ' week(s)', ES)	
print('CHOICE NUMBER : ', C)	
print('WIN', div)

if (aa == 1):
	print('### CHOICE LIST 필요수 삽입순열 ###')
	aa_insert_recommend_number()
elif(aa == 2):
	print('### CHOICE LIST 빈출별 정렬 ###')
	aa_cycle_number()

cnt = 0
for cl in CL:
	tmp = filter(lambda x:x == cl, div)
	if(len(tmp) == 0):
		cnt+= 1
		print(cnt, cl)
	else:
		print('CONGRATULATION')

print('### END ###') 

# for divv in div:
# 	tmp = filter(lambda x:x == divv, CL)
# 	print(tmp)
	# print(len(tmp))
	
