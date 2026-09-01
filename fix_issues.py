import re

# 1. Update style.css
with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix input targeting so it doesn't break radio buttons
css = css.replace(
'''.form-field input,
.form-field select {''',
'''.form-field input:not([type="radio"]),
.form-field select {'''
)
css = css.replace(
'''.form-field input::placeholder {''',
'''.form-field input:not([type="radio"])::placeholder {'''
)
css = css.replace(
'''.form-field input:focus, .form-field select:focus {''',
'''.form-field input:not([type="radio"]):focus, .form-field select:focus {'''
)

# Ensure toggle inputs look like native radio buttons
css = css.replace('.toggle input { accent-color: var(--primary); }', '.toggle input { accent-color: var(--primary); appearance: auto; width: auto; margin: 0; padding: 0; }')

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update app.js
with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_error_logic = '''  if (!nameInput) {
    nameError.style.display = "block";
    document.getElementById("name").style.borderColor = "#ef4444";
    return;
  }'''

new_error_logic = '''  if (!nameInput) {
    nameError.style.display = "block";
    const nameEl = document.getElementById("name");
    nameEl.style.borderColor = "#ef4444";
    nameEl.scrollIntoView({ behavior: "smooth", block: "center" });
    nameEl.focus();
    return;
  }'''

js = js.replace(old_error_logic, new_error_logic)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed radio buttons and auto-scroll")
