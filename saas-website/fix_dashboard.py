with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('.bubble-preview {', '.chat-bubble-preview {')
text = text.replace('.bubble-preview.size', '.chat-bubble-preview.size')
text = text.replace('.bubble-preview.position', '.chat-bubble-preview.position')
text = text.replace('class="bubble-preview"', 'class="chat-bubble-preview"')

# Also ensure no-pulse and no-shadow exist
no_pulse_css = '''
.chat-bubble-preview.no-pulse { animation: none !important; }
.chat-bubble-preview.no-shadow { box-shadow: none !important; }
'''
if '.chat-bubble-preview.no-pulse' not in text:
    text = text.replace('/* Chat Widget Preview */', no_pulse_css + '\n    /* Chat Widget Preview */')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed dashboard.html CSS classes.')
