import re

# 1. Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove name error span as we will use a generic form error
name_error_span = '''<span id="nameError" style="color: #ef4444; font-size: 0.85rem; margin-top: 8px; display: none; font-weight: 600; margin-left: 14px;"><i class="fa-solid fa-circle-exclamation"></i> Please enter your name</span>'''
html = html.replace(name_error_span, '')
# Also handle if it had different spacing
html = re.sub(r'\s*<span id="nameError".*?</span>', '', html)

# Age
html = html.replace('value="45"', 'placeholder="Your age"')

# Gender
html = html.replace('<select id="gender">', '<select id="gender">\n                <option value="" selected disabled>Select gender</option>')

# Height M
html = html.replace('value="1.70"', 'placeholder="e.g. 1.70"')
# Height CM
html = html.replace('value="170"', 'placeholder="e.g. 170"')
# Height FT IN
html = html.replace('value="5" placeholder="ft"', 'placeholder="ft"')
html = html.replace('value="7" placeholder="in"', 'placeholder="in"')
# Weight
html = html.replace('value="85"', 'placeholder="e.g. 85"')

# Add generic form error above actions for personal info page
# Since actions class appears in multiple pages, let's use regex to target the one in page-personal
personal_page_pattern = re.compile(r'(<div class="divider">Height</div>.*?)(<div class="actions">\s*<button class="btn btn--ghost back">Back</button>\s*<button class="btn btn--primary" id="toHealthForm">Next</button>\s*</div>)', re.DOTALL)

replacement = r'\1<div id="formError" style="color: #ef4444; font-size: 0.95rem; margin-top: 16px; display: none; font-weight: 600; text-align: right;"><i class="fa-solid fa-circle-exclamation"></i> Please fill in all fields correctly.</div>\n          \2'
html = personal_page_pattern.sub(replacement, html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.js
with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_logic = '''const toHealthButton = document.getElementById("toHealthForm");
toHealthButton.addEventListener("click", () => {
  const requiredFields = ["name", "age", "gender", "weight"];
  const heightUnit = document.querySelector('input[name="heightUnit"]:checked').value;
  if (heightUnit === "m") requiredFields.push("height");
  else if (heightUnit === "cm") requiredFields.push("heightCm");
  else requiredFields.push("heightFt", "heightIn");

  let firstInvalid = null;
  requiredFields.forEach(id => {
    const el = document.getElementById(id);
    if (!el.value.trim()) {
      el.style.borderColor = "#ef4444";
      if (!firstInvalid) firstInvalid = el;
    } else {
      el.style.borderColor = "";
    }
  });

  const formError = document.getElementById("formError");
  if (firstInvalid) {
    if(formError) formError.style.display = "block";
    firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
    firstInvalid.focus();
    return;
  }
  
  if(formError) formError.style.display = "none";
  setActivePage("health");
});

["name", "age", "gender", "weight", "height", "heightCm", "heightFt", "heightIn"].forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    el.addEventListener("input", function() {
      this.style.borderColor = "";
      const formError = document.getElementById("formError");
      if(formError) formError.style.display = "none";
    });
  }
});'''

# Using Regex to replace the old logic
pattern = re.compile(r'const toHealthButton = document\.getElementById\("toHealthForm"\);\n.*?(?:this\.style\.borderColor = "";\n\}\);|setActivePage\("health"\);\n\}\);)', re.DOTALL)
js = pattern.sub(new_logic, js)

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Removed default values and added comprehensive validation.")
