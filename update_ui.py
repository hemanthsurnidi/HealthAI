import re

# Update style.css
with open('static/css/style.css', 'r') as f:
    css = f.read()

css = css.replace(
    ''':root {
  --bg: #050814;
  --surface: rgba(255, 255, 255, 0.08);
  --surface-strong: rgba(255, 255, 255, 0.12);
  --text: rgba(255, 255, 255, 0.92);
  --muted: rgba(255, 255, 255, 0.68);
  --primary: #7c3aed;
  --primary-2: #23c0f7;
  --accent: #f97316;
  --shadow: 0 24px 48px rgba(0, 0, 0, 0.35);''',
    ''':root {
  --bg: #121212;
  --surface: rgba(255, 255, 255, 0.05);
  --surface-strong: rgba(255, 255, 255, 0.1);
  --text: #ffffff;
  --muted: #aaaaaa;
  --primary: #ffffff;
  --primary-2: #eeeeee;
  --accent: #cccccc;
  --shadow: 0 24px 48px rgba(0, 0, 0, 0.5);'''
)

css = css.replace(
    '''body {
  margin: 0;
  font-family: var(--font);
  background: radial-gradient(circle at 0% 0%, rgba(124, 58, 237, 0.8), transparent 45%),
    radial-gradient(circle at 100% 20%, rgba(35, 192, 247, 0.6), transparent 50%),
    radial-gradient(circle at 25% 75%, rgba(249, 115, 22, 0.4), transparent 55%),
    #050814;
  color: var(--text);
  overflow-x: hidden;
}''',
    '''body {
  margin: 0;
  font-family: var(--font);
  background: #121212;
  color: var(--text);
  overflow-x: hidden;
}'''
)

css = css.replace('rgba(124, 58, 237, 0.45)', 'rgba(255, 255, 255, 0.05)')
css = css.replace('rgba(35, 192, 247, 0.45)', 'rgba(255, 255, 255, 0.05)')
css = css.replace('rgba(249, 115, 22, 0.35)', 'rgba(255, 255, 255, 0.03)')
css = css.replace('linear-gradient(135deg, rgba(124, 58, 237, 0.72), rgba(35, 192, 247, 0.72))', '#333333')
css = css.replace('linear-gradient(120deg, var(--primary), var(--primary-2))', '#ffffff')
css = css.replace('box-shadow: 0 18px 35px rgba(124, 58, 237, 0.3);', 'box-shadow: 0 18px 35px rgba(255, 255, 255, 0.1);')
css = css.replace('color: white;', 'color: #000000;')

form_field_old = '''.form-field input,
.form-field select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 14px;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  outline: none;
  transition: border var(--transition), box-shadow var(--transition);
}

.form-field input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

.form-field input:focus,
.form-field select:focus {
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.25);
  border-color: rgba(124, 58, 237, 0.7);
}'''

form_field_new = '''.form-field input,
.form-field select {
  background: #eef2f6;
  border: 1px solid #d1d5db;
  border-radius: 50px;
  padding: 16px 24px;
  color: #111111;
  font-size: 1.05rem;
  outline: none;
  transition: border var(--transition), box-shadow var(--transition);
  width: 100%;
}

.form-field input::placeholder {
  color: #6b7280;
}

.form-field input:focus,
.form-field select:focus {
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.3);
  border-color: #999999;
}'''

css = css.replace(form_field_old, form_field_new)

# dropdown colors
css = css.replace('''select,
select option {
  color: #0f172a !important;
  background: #ffffff !important;
}

select option:checked {
  background: #2563eb !important;
  color: #ffffff !important;
}''', '''select option {
  color: #000000 !important;
  background: #ffffff !important;
}

select option:checked {
  background: #333333 !important;
  color: #ffffff !important;
}''')

with open('static/css/style.css', 'w') as f:
    f.write(css)

# Update index.html
with open('templates/index.html', 'r') as f:
    html = f.read()

# Replace input-card wrappers
input_card_pattern = re.compile(r'<div class="input-card">\s*<div class="input-card__icon">.*?</div>\s*<div>\s*<label>(.*?)</label>\s*<select id="(.*?)">', re.DOTALL)
html = input_card_pattern.sub(r'<div class="form-field">\n              <label>\1</label>\n              <select id="\2">', html)

# Close divs correctly
html = html.replace('</select>\n              </div>\n            </div>', '</select>\n            </div>')

# Fix card--small wrapping height and weight
html = html.replace('<div class="card card--small" id="heightMeters">', '<div class="form-field" id="heightMeters">')
html = html.replace('<div class="card card--small hidden" id="heightCm">', '<div class="form-field hidden" id="heightCm">')
html = html.replace('<div class="card card--small hidden" id="heightFt">', '<div class="form-field hidden" id="heightFt">')
html = html.replace('<div class="card card--small">', '<div class="form-field">')

html = html.replace('<p class="card__title">Height (m)</p>', '<label>Height (m)</label>')
html = html.replace('<p class="card__title">Height (cm)</p>', '<label>Height (cm)</label>')
html = html.replace('<p class="card__title">Feet / Inches</p>', '<label>Feet / Inches</label>')
html = html.replace('<p class="card__title">Weight (kg)</p>', '<label>Weight (kg)</label>')

with open('templates/index.html', 'w') as f:
    f.write(html)

print("Updated style.css and index.html")
