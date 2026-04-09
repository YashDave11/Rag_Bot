import codecs

# Read file
with codecs.open('all_data.py', 'r', 'utf-8') as f:
    content = f.read()

# Replace smart quotes with regular quotes
content = content.replace('\u2019', "'")  # Right single quotation mark
content = content.replace('\u2018', "'")  # Left single quotation mark  
content = content.replace('\u201c', '"')  # Left double quotation mark
content = content.replace('\u201d', '"')  # Right double quotation mark

# Write back
with codecs.open('all_data.py', 'w', 'utf-8') as f:
    f.write(content)

print("Fixed smart quotes in all_data.py")
