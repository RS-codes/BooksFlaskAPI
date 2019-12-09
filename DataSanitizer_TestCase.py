def validBookObject(bookObject):
	#if "keyName" in dictionaryObject
	if ("name" in bookObject 
			and "price" in bookObject 
				and "isbn" in bookObject):
		return	True
	else:
		return False

valid_object = {
	'name' : 'sample',
	'price' : 4.5,
	'isbn' : 963
}

missing_name = {
	'price' : 4.5,
	'isbn' : 963
}

missing_price = {
	'name' : 'sample',
	'isbn' : 963
}

missing_isbn = {
	'name' : 'sample',
	'price' : 4.5
}

empty_dictionary = {}