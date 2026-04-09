import re

# Read the file
with open('all_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic multi-line strings with proper single-line concatenated strings
old_pattern = r'return """I apologize.*?topics listed above\."""'

new_text = '''no_context_msg = (
                    "I apologize, but I could not find relevant information in the college documents to answer your question.\\n\\n"
                    "This might be because:\\n"
                    "- The information is not available in the current documents\\n"
                    "- The question might need to be more specific\\n"
                    "- The topic might not be covered in the college materials\\n\\n"
                    "To get better help, you could try asking about:\\n"
                    "- College admission requirements and procedures\\n"
                    "- Academic programs and course details\\n"
                    "- Campus facilities and services\\n"
                    "- Student policies and code of conduct\\n"
                    "- Fee structure and scholarship information\\n"
                    "- Faculty and department information\\n\\n"
                    "Please try rephrasing your question with more specific terms or ask about the topics listed above."
                )
                return no_context_msg'''

# Replace all occurrences
content = re.sub(old_pattern, new_text, content, flags=re.DOTALL)

# Write back
with open('all_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all_data.py")
