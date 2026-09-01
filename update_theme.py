import re

# 1. Update style.css
with open('static/css/style.css', 'r') as f:
    css = f.read()

# Update Theme Variables
css = css.replace(
    ''':root {
  --bg: #121212;
  --surface: rgba(255, 255, 255, 0.05);
  --surface-strong: rgba(255, 255, 255, 0.1);
  --text: #ffffff;
  --muted: #aaaaaa;
  --primary: #ffffff;
  --primary-2: #eeeeee;
  --accent: #cccccc;
  --shadow: 0 24px 48px rgba(0, 0, 0, 0.5);''',
    ''':root {
  --bg: #0b1120;
  --surface: rgba(30, 41, 59, 0.6);
  --surface-strong: rgba(30, 41, 59, 0.9);
  --text: #f8fafc;
  --muted: #94a3b8;
  --primary: #6366f1;
  --primary-2: #8b5cf6;
  --accent: #10b981;
  --shadow: 0 24px 48px rgba(0, 0, 0, 0.4);'''
)

# Update body
css = css.replace(
    '''body {
  margin: 0;
  font-family: var(--font);
  background: #121212;
  color: var(--text);
  overflow-x: hidden;
}''',
    '''body {
  margin: 0;
  font-family: var(--font);
  background: #0b1120;
  color: var(--text);
  overflow-x: hidden;
}'''
)

# Update Blobs
css = css.replace('rgba(255, 255, 255, 0.03)', 'rgba(99, 102, 241, 0.35)', 1) # blob 1
css = css.replace('rgba(255, 255, 255, 0.03)', 'rgba(16, 185, 129, 0.30)', 1) # blob 2
css = css.replace('rgba(255, 255, 255, 0.02)', 'rgba(217, 70, 239, 0.30)', 1) # blob 3

# Update Brand Icon
css = css.replace(
    '''background: #333333;
  box-shadow: 0 18px 35px rgba(0, 0, 0, 0.5);''',
    '''background: linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: 0 18px 35px rgba(99, 102, 241, 0.4);'''
)

# Update Primary Button
css = css.replace(
    '''background: #ffffff;
  box-shadow: 0 18px 35px rgba(255, 255, 255, 0.1);
  color: #000000;''',
    '''background: linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: 0 18px 35px rgba(99, 102, 241, 0.4);
  color: white;'''
)

# Revert tag colors to colorful
css = css.replace(
    '''.tag--low {
  background: rgba(255, 255, 255, 0.1);
  color: #aaaaaa;
}

.tag--normal {
  background: rgba(255, 255, 255, 0.2);
  color: #cccccc;
}

.tag--high {
  background: rgba(255, 255, 255, 0.9);
  color: #000000;}''',
    '''.tag--low {
  background: rgba(34, 197, 94, 0.18);
  color: #4ade80;
}

.tag--normal {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.tag--high {
  background: rgba(248, 113, 113, 0.2);
  color: #f87171;
}'''
)

# Add Premium Tip Card CSS
premium_css = '''
.premium-tip-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 24px;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease, border-color 0.3s ease;
  gap: 20px;
  opacity: 0;
  animation: slideUpFade 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  backdrop-filter: blur(10px);
}

.premium-tip-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(99, 102, 241, 0.5);
}

.tip-card__icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.tip-card__icon i {
  font-size: 24px;
  color: white;
}

.tip-card__content h3 {
  margin: 0 0 8px;
  font-size: 1.15rem;
  color: white;
  text-transform: capitalize;
  font-weight: 700;
}

.tip-card__content p {
  margin: 0;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.5;
}

@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
'''
if '.premium-tip-card' not in css:
    css += premium_css

with open('static/css/style.css', 'w') as f:
    f.write(css)

# 2. Update app.js
with open('static/js/app.js', 'r') as f:
    js = f.read()

old_prevention_js = '''  preventionList.innerHTML = "";
  data.prevention.forEach((step) => {
    const card = document.createElement("div");
    card.className = "tip-card";
    card.innerHTML = `
      <h3>✔ ${step.split(" ").slice(0, 5).join(" ")}...</h3>
      <p>${step}</p>
    `;
    preventionList.appendChild(card);
  });'''

new_prevention_js = '''  const getPreventionMeta = (step) => {
    const text = step.toLowerCase();
    if (text.includes("exercise") || text.includes("activity")) return { icon: "fa-person-running", color: "linear-gradient(135deg, #f59e0b, #ef4444)" };
    if (text.includes("weight") || text.includes("bmi")) return { icon: "fa-weight-scale", color: "linear-gradient(135deg, #10b981, #059669)" };
    if (text.includes("sugar") || text.includes("food") || text.includes("eat") || text.includes("vegetable") || text.includes("diet")) return { icon: "fa-apple-whole", color: "linear-gradient(135deg, #84cc16, #22c55e)" };
    if (text.includes("water") || text.includes("drink")) return { icon: "fa-glass-water", color: "linear-gradient(135deg, #3b82f6, #2563eb)" };
    if (text.includes("sleep")) return { icon: "fa-bed", color: "linear-gradient(135deg, #8b5cf6, #6366f1)" };
    if (text.includes("stress") || text.includes("relax") || text.includes("meditation")) return { icon: "fa-spa", color: "linear-gradient(135deg, #ec4899, #d946ef)" };
    if (text.includes("smoking") || text.includes("alcohol")) return { icon: "fa-ban-smoking", color: "linear-gradient(135deg, #64748b, #475569)" };
    if (text.includes("blood pressure") || text.includes("glucose") || text.includes("monitor")) return { icon: "fa-heart-pulse", color: "linear-gradient(135deg, #f43f5e, #e11d48)" };
    return { icon: "fa-check-circle", color: "linear-gradient(135deg, #6366f1, #4f46e5)" };
  };

  preventionList.innerHTML = "";
  data.prevention.forEach((step, i) => {
    const meta = getPreventionMeta(step);
    const card = document.createElement("div");
    card.className = "premium-tip-card";
    card.style.animationDelay = `${i * 0.1}s`;
    card.innerHTML = `
      <div class="tip-card__icon" style="background: ${meta.color}">
        <i class="fa-solid ${meta.icon}"></i>
      </div>
      <div class="tip-card__content">
        <h3>${step.split(" ").slice(0, 3).join(" ")}...</h3>
        <p>${step}</p>
      </div>
    `;
    preventionList.appendChild(card);
  });'''

if old_prevention_js in js:
    js = js.replace(old_prevention_js, new_prevention_js)
else:
    # try regex approach if exact match fails
    import re
    pattern = re.compile(r'preventionList\.innerHTML = "";\s*data\.prevention\.forEach\(\(step\) => \{.*?preventionList\.appendChild\(card\);\s*\}\);', re.DOTALL)
    js = pattern.sub(new_prevention_js, js)

with open('static/js/app.js', 'w') as f:
    f.write(js)

print("Updated style.css and app.js")
