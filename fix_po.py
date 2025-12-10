import re

file_path = '/srv/landing/locale/ru/LC_MESSAGES/django.po'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the fuzzy entry with context "footer"
pattern = r'(#: templates/pages/home\.html:\d+\n)#, fuzzy\n#\| msgid "Privacy Policy"\nmsgctxt "footer"\nmsgid "Privacy Policy"\nmsgstr "Политикой конфиденциальности"'

replacement = r'\1msgctxt "footer"\nmsgid "Privacy Policy"\nmsgstr "Политика конфиденциальности"'

new_content = re.sub(pattern, replacement, content)

if new_content == content:
    # Try a more generic pattern if line numbers changed or exact format differs
    print("Exact match not found, trying generic pattern...")
    pattern = r'#, fuzzy\n#\| msgid "Privacy Policy"\nmsgctxt "footer"\nmsgid "Privacy Policy"\nmsgstr ".*?"'
    replacement = r'msgctxt "footer"\nmsgid "Privacy Policy"\nmsgstr "Политика конфиденциальности"'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated django.po")
