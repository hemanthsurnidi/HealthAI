import re

# 1. Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change Powered by AI to About
html = html.replace('<a href="#" class="pill">Powered by AI</a>', '<button id="aboutBtn" class="pill" style="cursor: pointer;">About</button>')

# Remove hero__visual
hero_visual_content = '''          <div class="hero__visual">
            <div class="stat-card">
              <div class="stat-card__icon"><i class="fa-solid fa-heartbeat"></i></div>
              <div>
                <div class="stat-card__value">72%</div>
                <div class="stat-card__label">avg. risk detected</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-card__icon"><i class="fa-solid fa-microscope"></i></div>
              <div>
                <div class="stat-card__value">6</div>
                <div class="stat-card__label">conditions analyzed</div>
              </div>
            </div>
          </div>'''

# Also support slightly different formats in case it changed
html = html.replace(hero_visual_content, '')
if 'class="hero__visual"' in html:
    # Use regex if exact replace failed
    html = re.sub(r'<div class="hero__visual">.*?</div>\s*</div>', '', html, flags=re.DOTALL)

modal_html = '''
      <!-- About Modal -->
      <div class="modal hidden" id="aboutModal">
        <div class="modal__backdrop" id="aboutCloseBackdrop"></div>
        <div class="modal__content card">
          <div class="card__header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h2 style="margin: 0;">About HealthAI</h2>
            <button class="btn btn--ghost" id="aboutCloseBtn" style="padding: 8px 12px; border-radius: 50%;"><i class="fa-solid fa-xmark"></i></button>
          </div>
          <p style="color: var(--muted); line-height: 1.6;">
            HealthAI is an advanced predictive health analytics dashboard. It analyzes your lifestyle and physical metrics to deliver personalized risk insights and actionable prevention guidance.
          </p>
          <div style="background: var(--surface-strong); padding: 16px; border-radius: 12px; margin-top: 20px; border: 1px solid var(--border);">
            <p style="color: var(--text); line-height: 1.6; font-weight: 600; margin: 0;">
              <i class="fa-solid fa-database" style="color: var(--primary); margin-right: 8px;"></i> Trained with real datasets
            </p>
            <p style="margin: 4px 0 0; font-size: 0.9rem; color: var(--muted);">Our machine learning models are trained using authentic clinical data to ensure accurate insights.</p>
          </div>
        </div>
      </div>
    </main>
'''
if 'id="aboutModal"' not in html:
    html = html.replace('</main>', modal_html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
with open('static/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Change .hero layout
css = css.replace(
'''.hero {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 40px;
  align-items: center;
}''',
'''.hero {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  min-height: 50vh;
  gap: 20px;
}'''
)

# Add Modal CSS
modal_css = '''
.modal {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal.hidden {
  display: none !important;
}
.modal__backdrop {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(4px);
}
.modal__content {
  position: relative;
  z-index: 101;
  width: 100%;
  max-width: 500px;
  animation: modalPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes modalPop {
  0% { opacity: 0; transform: scale(0.95) translateY(10px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
'''
if '.modal {' not in css:
    css += modal_css

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update app.js
with open('static/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

modal_js = '''
const aboutBtn = document.getElementById("aboutBtn");
const aboutModal = document.getElementById("aboutModal");
const aboutCloseBtn = document.getElementById("aboutCloseBtn");
const aboutCloseBackdrop = document.getElementById("aboutCloseBackdrop");

if(aboutBtn) {
  aboutBtn.addEventListener("click", () => {
    aboutModal.classList.remove("hidden");
  });
  
  const closeModal = () => aboutModal.classList.add("hidden");
  aboutCloseBtn.addEventListener("click", closeModal);
  aboutCloseBackdrop.addEventListener("click", closeModal);
}
'''
if 'aboutBtn.addEventListener' not in js:
    js += modal_js

with open('static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated about section and removed stat cards.")
