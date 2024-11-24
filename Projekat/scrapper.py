from googlesearch import search
from unstructured.partition.html import partition_html

def search_fn(query, num):
	results = []
	for j in search(query, tld="co.in", num=num, stop=num, pause=2):
		results.append(j)

	return results


def extract_content(results):
    ispis = []  # A list to store the string representations
    for result in results:
        elements = partition_html(url=result)  # Assuming `partition_html` works as expected
        ispis.extend([str(el) for el in elements])  # Add the string representations to the list
    
    return ''.join(ispis)  # Concatenate the list into a single string
