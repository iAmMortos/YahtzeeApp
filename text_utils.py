def title_caps(s):
	new_words = []
	connectors = ['a', 'an', 'the', 'and', 'of', 'by', 'in']
	words = str(s).split()
	for i,word in enumerate(words):
		new_words += [('%s%s' % (word[0].upper(), word[1:].lower())) if (i == 0 or word not in connectors) else word]
	return ' '.join(new_words)
