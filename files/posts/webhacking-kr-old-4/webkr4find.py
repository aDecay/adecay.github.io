from multiprocessing import Process

_hash = '' #해시 값(초록 문자열)을 입력
PARTS = 10 #csv 파일 개수

#csv 파일에서 해시 값을 찾으면 원본 값을 출력
def find(i):
	fname = 'hash_'+str(i)+'.csv'
	f = open(fname, 'r')
	while True:
		line = f.readline().strip()
		if not line:
			break
			
		data = line.split(',')
		if data[1] == _hash:
			print(data[0])
			break
	f.close()

if __name__ == '__main__':
	procs = []

	for i in range(PARTS):
		proc = Process(target=find, args=(i,))
		procs.append(proc)
		proc.start()

	for proc in procs:
		proc.join()