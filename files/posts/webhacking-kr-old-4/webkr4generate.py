from hashlib import sha1
from multiprocessing import Process

START, END = 10000000, 100000000
PARTS = 10	#프로세스 개수
SIZE = (END-START)//PARTS

#hash_i.csv 파일에 (원본 값), (해시 값)의 형태로 저장
#hash_0.csv ~ hash_(PARTS-1).csv 파일에 나누어 저장
def rainbow(i):
	start = START + SIZE * i
	end = start + SIZE

	fname = 'hash_'+str(i)+'.csv'
	f = open(fname, 'w')
	for x in range(start, end):
		chall4 = _hash = str(x)+'salt_for_you'
		for y in range(500):
			_hash = sha1(_hash.encode('utf-8')).hexdigest()
		data = chall4+','+_hash+'\n'
		f.write(data)
	f.close()

if __name__ == '__main__':
	procs = []

	for i in range(PARTS):
		proc = Process(target=rainbow, args=(i,))
		procs.append(proc)
		proc.start()

	for proc in procs:
		proc.join()