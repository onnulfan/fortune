# -*- coding: utf-8 -*-

import csv
from itertools import *
import random

# 원격 데이터 요청 
# 로컬 데이터 업데이트 
# 로컬 데이터 읽기 

# 데이터 구조에 입력 
D = []  # D[] = 당청번호 데이터
DD = []  # DD[] = 당청번호 데이터
K = []  # K[] = 당청번호별 가중치
B = []  # B[] = 빌드 데이터
C = []  # C[] = 완성 데이터
CR = [] # CR[] = 제외수 미적용 
E = []  # E[] = 제외수
ES = []
EA = [] # EA[] = 제외수 전체 
CL = [] # CL[] = 제외수 포함한 리스트
LN = [] # 추천숫자 제한

i = 0

# 적용 변수
rev = 1 # True : ASC(low 빈출순), False : DESC(high 빈출순) 
EXCEP = 10 # 제외수 범위 

MAX = 6 # 셈플링 공략개수 , 6이상 수 
WEEK = 5 # 최근 몇주간 번호 제외

WON = 20000
GAME = WON / 1000 # 게임 개수
AE = 20 # 선택숫자 추천횟수 제한 

SIM = 500 # 시뮬레이션 회차
LD = []  # 최신데이터  

INCOME = 0

TOTAL_INCOME = 0
TOTAL_COST = 0

# 적용 알고리즘
aa = 1  # 1 제외수 삽입, 2 빈출별 정렬

div = []

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
	while cnt < 46:
		count_num.append([cnt, 0])
		cnt += 1

	return count_num

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
	# for aii in ai[:need]:
	# 	nr.append(aii[0])	

	ee = E[:]
	ee.sort(key=lambda x:x[:][1], reverse=False)
	ee = filter(lambda x:x[:][0] not in nr, ee)

	tcnt = 0

	while cnt < 45:
		ein = filter(lambda x:x[:][1] == cnt, ee)
		tcnt += len(ein)
		if(tcnt == 45): 
			break 

		for einn in ein:
			kkk = filter(lambda x:x[:][0] == einn[0], K)[0]
			kkt.append(kkk)

		kkt.sort(key=lambda x:x[:][1], reverse=True)
		eea.extend([x[0] for x in kkt])

		kkt = []

		cnt += 1

	nr.extend(eea)

	print 'c', len(nr), nr
	return nr

def make_combination(nr):
	p = nr[:]
	pos0 = 0
	pos1 = 0
	pos2 = 0
	cnt = 0

	for nrr in nr:
		tmp = filter(lambda x:x[:][0] == nrr, ES)[0][1]
		if (tmp == 0):
			pos0 = cnt
		elif (tmp == 1):
			pos1 = cnt
		elif (tmp == 2):
			pos2 = cnt
		cnt += 1

	cnt = 0
	p0 = list(combinations(nr[:pos0],3))
	p1 = list(combinations(nr[pos0:pos2],2))
	p2 = list(combinations(nr[pos2:],1))
	
	p0 = [list(i) for i in p0]	
	p1 = [list(i) for i in p1]	
	p2 = [list(i) for i in p2]	

	tmp = p0[10].extend(p1[10])
	print len(p0), len(p1), len(p2) 
	print p2

	while True:
		if (len(p0) < cnt or len(p1) < cnt or len(p2) < cnt ):
			# p.append(p0[cnt].extend(p1[cnt]).extend(p2[cnt]))
			break

		cnt += 1

	p = list(combinations(nr,6))
	return p

def limited_number(t, cl):
	ln = init_limited_number()

	for cll in cl:
		for tt in t:
			if(tt in cll):
				ln[tt-1][1] += 1
				if(ln[tt-1][1] > AE):
					return False
	return True

def make_game_list_a1(nr):
	global CL, LN
	cnt = 0
	cl = []

	# 순열
	# p = list(permutations(nr[: 20 if GAME > 20 else 10],6))
	p = list(combinations(nr,6))
	# p = make_combination(nr)

	print('TOTAL :', len(p), 'CREAT :', GAME)
	
	while True:
		t = list(p[cnt][:])	
		t.sort()

		if(t not in cl):
			if (limited_number(t, cl) == True):
				cl.append(t)
				print ('.'),

			# if(div == t):
			# 	print 'WINWINWIN', cnt	
		cnt += 1

		if(len(cl) > GAME or len(p) <= cnt):
		# if(len(p) <= cnt):
			# print 'cnt', cnt, LN
			print ('.')
			break

	CL = cl[:GAME]

def weight_number(co):
	global ES, K

	p0 = []
	p1 = []
	p2 = []
	w = co[:]

	tmp = filter(lambda x:x[:][1] == 0, ES)
	for tmpp in tmp:
		p0.append([tmpp[0], filter(lambda x:x[:][0] == tmpp[0], K)[0][1]])

	p0.sort(key=lambda x:x[1], reverse=True)
	p0 = [x[0] for x in p0]	
	p0 = [x for x in p0 if x not in w[:len(C)]]

	tmp = filter(lambda x:x[:][1] == 1, ES)
	for tmpp in tmp:
		p1.append([tmpp[0], filter(lambda x:x[:][0] == tmpp[0], K)[0][1]])

	p1.sort(key=lambda x:x[1], reverse=True)
	p1 = [x[0] for x in p1]	

	tmp = filter(lambda x:x[:][1] == 2, ES)
	for tmpp in tmp:
		p2.append([tmpp[0], filter(lambda x:x[:][0] == tmpp[0], K)[0][1]])

	p2.sort(key=lambda x:x[1], reverse=True)
	p2 = [x[0] for x in p2]	

	w =  p0 + p1 + p2 

	# mv = len(co) 
	# ld = map(int, LD[0][2:8])
	# for ldd in ld:
	# 	if(co.index(ldd) < mv):
	# 		mv = co.index(ldd)
	
	# w = co[mv:]	

	print 'w', len(w), w

	return w 

def aa_insert_recommend_number():
	core = core_number()
	core = weight_number(core)
	make_game_list_a1(core)

## main 

def main():
	global D,DD,K,B,C,CR,E,EA,ES,CL,LN 
	global rev, EXCEP, MAX, WEEK, WON, INCOME, GAME, AE, SIM, LD, aa, div
	global TOTAL_INCOME, TOTAL_COST 

	i = 0
	K = []  # K[] = 당청번호별 가중치
	B = []  # B[] = 빌드 데이터	
	C = []  # C[] = 완성 데이터
	CR = [] # CR[] = 제외수 미적용 
	E = []  # E[] = 제외수
	ES = []
	EA = [] # EA[] = 제외수 전체 
	CL = [] # CL[] = 제외수 포함한 리스트
	LN = [] # 추천숫자 제한

	INCOME = 0

	# 적용 알고리즘
	aa = 1  # 1 제외수 삽입, 2 빈출별 정렬

	div = []

	D = DD[len(DD) - SIM+1:]
	if (len(DD) >= SIM):
		tmp = map(int,DD[len(DD) - SIM:len(DD) - SIM+1][0])
		print('SIMULATION : ',tmp[1])
		div = tmp[2:8]

	print('SAMPLING : ', MAX)
	print('ORDER BY : ', 'LOW FREQUENT' if rev else 'HIGH FREQUENT')

	LD = DD[len(DD) - SIM + 1:]
	print('LAST DATA : ',LD[0])

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

	print
	print('CHOICE NUMBER : ', C)	
	print('COST : ', WON)	
	print('WIN', div)
	print

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
			ttmp = len(set(cl).intersection(div))
			if(ttmp == 3): 
				ttmp = '5 WIN'
				INCOME += 5000
				print(cnt, cl, ttmp)
			elif(ttmp == 4): 
				ttmp = '4 WIN'
				INCOME += 50000
				print(cnt, cl, ttmp)
			elif(ttmp == 5): 
				ttmp = '3 WIN'
				INCOME += 1300000
				print(cnt, cl, ttmp)
			elif(ttmp == 6):
				ttmp = '1 WIN'
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				print('CONGRATULATION')
				return 100
			# else: ttmp = 'LOST'

		else:
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			print('CONGRATULATION')
			return 100

	TOTAL_INCOME += INCOME
	TOTAL_COST += WON

	print '###############'
	print 
	print 'INCOME', INCOME
	print 'TOTAL INCOME', TOTAL_INCOME 
	print 'TOTAL COST', TOTAL_COST 
	print 'PROFIT', TOTAL_INCOME - TOTAL_COST 
	print 
	print '###############'
	print('### END ###') 
	print 

f = open('./excel/lotto.csv', 'r')
rdr = csv.reader(f)

for line in rdr:
    line.insert(0, int(line[0])*(-1))
    DD.append(line)
f.close()  

print 'START' , SIM, len(DD)

cnt = SIM

if(SIM > len(DD)):
	main()
	for cll in CL:
		print cll
else:
	while cnt <= len(DD):
		if(main() == 100):
			break
		cnt += 1
		SIM = cnt
