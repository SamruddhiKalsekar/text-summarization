alert('THE FILE IS LOADED

	import re
q1 = "select empid, ename as info from employee where emp >= teacher;"
q2 = "	select ename as info, empid from employee where teacher <= emp;"


def Convert(string): 
    li = list(string.split(",")) 
    return li 
  
# # Driver code     

# print(Convert(query)) 
# li1=Convert(query)
# print(li1)
# res = list(zip(range(li1), li1)) 
# print("List after conversion to tuple list : " + str(res))
def convert_tuple(tup):
    str = ''.join(tup)
    return str


def convert_keywords_to_upper(query):
    '''
    Converts all the keywords SELECT, FROM, WHERE, GROUP BY, HAVING and ORDER BY 
    to uppercase if they are in lower case.
    '''
    keywords = [
        ('SELECT', 'select'),
        ('FROM', 'from'),
        ('WHERE', 'where'),
        ('GROUP BY', 'group by'),
        ('HAVING', 'having'),
        ('ORDER BY', 'order by'),
        ('AS','as')
    ]

    for kw in keywords:
        if kw[1] in query:
            query = query.replace(kw[1], kw[0])

    return query

def get_order_of_keywords(query):
    '''
    Returns the keywords in order.
    '''
    keywords = [ 'GROUP BY', 'HAVING', 'ORDER BY']
    di = {}

    for k in keywords:
        try:
            di[k] = query.index(k)
        except Exception as e:
            pass

    keywords_ordered = {k: v for k, v in sorted(di.items(), key=lambda item: item[1])}
    return keywords_ordered.keys()

def split_sql(query):
    '''
    Splits the sql query on keywords.
    '''
    keywords_regex = {
      
        'GROUP BY': ' GROUP BY (?P<GROUP_BY>.*)',
        'HAVING': ' HAVING (?P<HAVING>.*)',
        'ORDER BY': ' ORDER BY (?P<ORDER_BY>.*)'
    }

    query = convert_keywords_to_upper(query)
    regex = r'SELECT (?P<SELECT>.*) FROM (?P<FROM>.*) WHERE (?P<WHERE>.*)'

    kw_ordered = get_order_of_keywords(query) 

    for k in kw_ordered:
        regex = regex + keywords_regex[k]

    r = re.compile(regex)
    return [m.groupdict() for m in r.finditer(query)][0]


def get_order_of_keys(query):
    '''
    Returns the keywords in order.
    '''
    keywords = ['SELECT', 'AS','FROM' ,'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY']
    di = {}

    for k in keywords:
        try:
            di[k] = query.index(k)
        except Exception as e:
            pass

    keywords_ordered = {k: v for k, v in sorted(di.items(), key=lambda item: item[1])}
    return keywords_ordered.keys()


# def compare_condition(li):
# 	new_list =[]
# 	for item in li:
# 		if '=' in item:
# 			col,mid

def replace_operators(li):
	new_list =[]
	for item in li:
		if '>=' in item:
			trial= item.replace(">=", "Greaterthanequalto")
			print(trial)
			new_list.append(' '.join(trial))
		if '<=' in item:
			trial=item.replace("<=", "Lessthanequalto")
			new_list.append(' '.join(trial))

	return 	new_list	


def remove_word_after_as(li):
    new_list = []
    for item in li:
        if 'AS' in item:
            col, _, _ = item.split()
            print(col)
            new_list.append(' '.join([col]))
        else:
            new_list.append(item)

    return new_list


query1 = convert_keywords_to_upper(q1)
kw_ordered_1 = get_order_of_keys(query1) 
query2 = convert_keywords_to_upper(q2)
kw_ordered_2 = get_order_of_keys(query2)
if (list(kw_ordered_1) == list(kw_ordered_2)):
	
	print("key match")



	#AS
	new1=[]
	new2=[]
	q1 = split_sql(q1)
	q2 = split_sql(q2)

	new1 = q1['SELECT']
	new2 = q2['SELECT']

	s1=new1.split(",")
	s2=new2.split(",")
	converted_list1=[]
	converted_list2=[]
	for i in s1:
	    converted_list1.append(i.strip())
	for i in s2:
	    converted_list2.append(i.strip())

	converted_list1.sort()
	converted_list2.sort()

	new_list1 = remove_word_after_as(converted_list1)
	new_list2 = remove_word_after_as(converted_list2)

	print(new_list1)
	print(new_list2)


	#WHERE

	w1 = q1['WHERE']
	w2 = q2['WHERE']
	p1=re.sub(";.*$", "", w1)
	p2=re.sub(";.*$", "", w2)
	a1=p1.split(" ")
	a2=p2.split(" ")

	converted_lista1 = []
	converted_lista2 = []
	for i in a1:
	    converted_lista1.append(i.strip())
	for i in a2:
	    converted_lista2.append(i.strip())

	converted_lista1.sort()
	converted_lista2.sort()
	   
	where_list1 = replace_operators(converted_lista1)
	where_list2 = replace_operators(converted_lista2)


	print(where_list1)
	print(where_list2)

	#CHECK

	if new_list1 == new_list2 and w1==w2:

		print('direct matching')
	elif new_list1 == new_list2 and where_list1==where_list2:

		print('matching')
	else:
		print('not matching')
		
else:
	print("key order not matching - query incorrect")

    # print(s1)
    # print(s2)

  # p=re.sub("AS.*$", "", sam)
  # print(p)
  # text = 'dept AS sam'
  # head, sep, tail = text.partition('AS')
  # print(head)



