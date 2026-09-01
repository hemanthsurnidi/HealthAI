import re

# 1. Update index.html for stethoscope
with open('templates/index.html', 'r') as f:
    html = f.read()

html = html.replace('<i class="fa-solid fa-heart-pulse"></i>', '<i class="fa-solid fa-stethoscope"></i>', 1)

with open('templates/index.html', 'w') as f:
    f.write(html)

# 2. Update app.js for name validation and prevention card content
with open('static/js/app.js', 'r') as f:
    js = f.read()

old_validation = '''const toHealthButton = document.getElementById("toHealthForm");
toHealthButton.addEventListener("click", () => setActivePage("health"));'''

new_validation = '''const toHealthButton = document.getElementById("toHealthForm");
toHealthButton.addEventListener("click", () => {
  const nameInput = document.getElementById("name").value.trim();
  if (!nameInput) {
    alert("Please enter your name to proceed.");
    return;
  }
  setActivePage("health");
});'''

js = js.replace(old_validation, new_validation)

old_card = '''      <div class="tip-card__content">
        <h3>${step.split(" ").slice(0, 3).join(" ")}...</h3>
        <p>${step}</p>
      </div>'''

new_card = '''      <div class="tip-card__content">
        <p style="font-size: 1.1rem; font-weight: 600; margin: 0; color: white;">${step}</p>
      </div>'''

js = js.replace(old_card, new_card)

with open('static/js/app.js', 'w') as f:
    f.write(js)

# 3. Update style.css for single column layout
with open('static/css/style.css', 'r') as f:
    css = f.read()

old_grid = '''.prevention-grid {
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}'''

new_grid = '''.prevention-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}'''

css = css.replace(old_grid, new_grid)

with open('static/css/style.css', 'w') as f:
    f.write(css)

print("Applied fixes")
