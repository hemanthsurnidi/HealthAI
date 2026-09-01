import re

css_content = """/* Core */
:root {
  --bg: #ffffff;
  --surface: #ffffff;
  --surface-strong: #f3f4f6;
  --text: #000000;
  --muted: #4b5563;
  --primary: #000000;
  --primary-2: #111111;
  --accent: #333333;
  --shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  --radius: 18px;
  --radius-sm: 12px;
  --font: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --transition: 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

body {
  margin: 0;
  font-family: var(--font);
  background: #ffffff;
  color: #000000;
  overflow-x: hidden;
}

a {
  color: inherit;
  text-decoration: none;
}

select option {
  color: #000000 !important;
  background: #ffffff !important;
}

select option:checked {
  background: #f3f4f6 !important;
  color: #000000 !important;
}

.app {
  min-height: 100vh;
  position: relative;
  padding-bottom: 80px;
}

.background {
  display: none;
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 18px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e5e7eb;
}

.brand {
  display: flex;
  gap: 14px;
  align-items: center;
}

.brand__icon {
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: #000000;
}

.brand__icon i {
  font-size: 22px;
  color: #ffffff;
}

.brand__text h1 {
  margin: 0;
  font-size: 1.15rem;
  letter-spacing: 0.8px;
  font-weight: 700;
  color: #000000;
}

.brand__text p {
  margin: 2px 0 0;
  font-size: 0.85rem;
  color: #4b5563;
}

.nav-actions .pill {
  font-size: 0.85rem;
  border-radius: 999px;
  padding: 10px 16px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  color: #000000;
  font-weight: 600;
  transition: transform var(--transition), background var(--transition);
}

.nav-actions .pill:hover {
  transform: translateY(-1px);
  background: #f9fafb;
}

.main {
  position: relative;
  z-index: 2;
  padding: 40px 32px 80px;
  max-width: 1080px;
  margin: 0 auto;
}

.page {
  position: relative;
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

.hidden {
  display: none !important;
}

.hero {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 34px;
  align-items: center;
}

.hero__copy h2 {
  margin: 0 0 16px;
  font-size: 2.4rem;
  line-height: 1.1;
  font-weight: 800;
  color: #000000;
}

.hero__copy p {
  margin: 0 0 28px;
  font-size: 1.05rem;
  max-width: 520px;
  color: #374151;
}

.stat-card {
  display: flex;
  gap: 18px;
  align-items: center;
  padding: 18px 22px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: transform var(--transition);
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-card__icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: #f3f4f6;
}

.stat-card__icon i {
  font-size: 20px;
  color: #000000;
}

.stat-card__value {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
  color: #000000;
}

.stat-card__label {
  font-size: 0.85rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.btn {
  border: none;
  border-radius: 16px;
  padding: 14px 22px;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: transform var(--transition), background var(--transition);
}

.btn--primary {
  background: #000000;
  color: #ffffff;
}

.btn--primary:hover {
  transform: translateY(-2px);
  background: #1f2937;
}

.btn--ghost {
  background: #ffffff;
  border: 2px solid #000000;
  color: #000000;
}

.btn--ghost:hover {
  background: #f3f4f6;
}

.card {
  border-radius: var(--radius);
  background: #ffffff;
  padding: 32px;
  border: 1px solid #e5e7eb;
}

.card__header h2 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  color: #000000;
}

.card__header p {
  margin: 6px 0 0;
  color: #4b5563;
}

.grid {
  display: grid;
  gap: 18px;
}

.grid--2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.grid--3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (max-width: 900px) {
  .grid--2, .grid--3 {
    grid-template-columns: 1fr;
  }
  .hero {
    grid-template-columns: 1fr;
  }
}

.form-field {
  display: flex;
  flex-direction: column;
}

.form-field label {
  font-weight: 700;
  margin-bottom: 10px;
  color: #000000;
}

.form-field input,
.form-field select {
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 50px;
  padding: 16px 24px;
  color: #000000;
  font-size: 1.05rem;
  font-weight: 600;
  outline: none;
  transition: box-shadow var(--transition);
  width: 100%;
  appearance: none;
}

.form-field select {
  cursor: pointer;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23000000%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 1.5rem top 50%;
  background-size: 0.65rem auto;
}

.form-field input::placeholder {
  color: #9ca3af;
  font-weight: 500;
}

.form-field input:focus,
.form-field select:focus {
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1);
}

.bmi-preview {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 18px;
}

.bmi__info {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 20px;
}

.bmi__info .label {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #4b5563;
}

.bmi__info h3 {
  margin: 0;
  font-size: 2.1rem;
  font-weight: 800;
  color: #000000;
}

.tag {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  background: #000000 !important;
  color: #ffffff !important;
}

.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 32px 0 18px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #000000;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 2px;
  background: #e5e7eb;
}

.toggle {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.toggle label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 14px;
  background: #ffffff;
  border: 1px solid #000000;
  cursor: pointer;
  font-weight: 600;
  color: #000000;
  transition: background var(--transition);
}

.toggle input {
  accent-color: #000000;
}

.toggle label:hover {
  background: #f3f4f6;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 30px;
}

.dashboard {
  display: grid;
  gap: 24px;
}

.dashboard__header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.dashboard__summary {
  display: flex;
  gap: 14px;
  align-items: center;
}

.summary-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 16px 18px;
  min-width: 150px;
}

.summary-card__value {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  color: #000000;
}

.summary-card__label {
  font-size: 0.85rem;
  color: #4b5563;
  margin-top: 4px;
  font-weight: 700;
}

#riskChart {
  width: 100% !important;
  max-height: 260px;
  margin-bottom: 24px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.card-grid {
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
}

.result-card {
  padding: 18px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  transition: transform var(--transition);
}

.result-card:hover {
  transform: translateY(-4px);
  border-color: #000000;
}

.result-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.result-card__title {
  margin: 0;
  font-weight: 800;
  color: #000000;
}

.result-card__score {
  font-size: 1.75rem;
  font-weight: 800;
  color: #000000;
}

.result-card__tag {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  background: #000000 !important;
  color: #ffffff !important;
  font-size: 0.75rem;
  font-weight: 800;
}

.result-card__details {
  margin-top: 10px;
  font-size: 0.92rem;
  color: #4b5563;
  line-height: 1.45;
}

.result-card__details strong {
  color: #000000;
}

.prevention-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.premium-tip-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 24px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  transition: transform 0.2s, box-shadow 0.2s;
  gap: 20px;
  opacity: 0;
  animation: slideUpFade 0.6s forwards;
}

.premium-tip-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-color: #000000;
}

.tip-card__icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  background: #000000 !important;
}

.tip-card__icon i {
  font-size: 24px;
  color: #ffffff !important;
}

.tip-card__content p {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #000000 !important;
  line-height: 1.5;
}

@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .dashboard__header {
    flex-direction: column;
    align-items: stretch;
  }
  .actions {
    justify-content: center;
  }
}
"""

with open("static/css/style.css", "w") as f:
    f.write(css_content)

# Update app.js ChartJS theme to light
with open('static/js/app.js', 'r') as f:
    js = f.read()

# Change chart colors to black/grey
js = js.replace('color: "rgba(255,255,255,0.12)"', 'color: "rgba(0,0,0,0.1)"')
js = js.replace('color: "rgba(255,255,255,0.74)"', 'color: "#000000"')
js = js.replace('color: "rgba(255,255,255,0.78)"', 'color: "#000000"')
js = js.replace('backgroundColor: "rgba(10, 14, 32, 0.95)"', 'backgroundColor: "#000000"')
js = js.replace('titleColor: "#fff"', 'titleColor: "#ffffff"')
js = js.replace('bodyColor: "#f5f7fb"', 'bodyColor: "#ffffff"')
js = js.replace('borderColor: "rgba(255,255,255,0.15)"', 'borderColor: "#000000"')

# Change chart bars to black
js = js.replace('const colors = diseases.map((d) => getRiskLevel(d.risk).color);', 'const colors = diseases.map(() => "#000000");')

# Change prevention js colors to black
js = js.replace('color: "linear-gradient(135deg, #f59e0b, #ef4444)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #10b981, #059669)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #84cc16, #22c55e)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #3b82f6, #2563eb)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #8b5cf6, #6366f1)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #ec4899, #d946ef)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #64748b, #475569)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #f43f5e, #e11d48)"', 'color: "#000000"')
js = js.replace('color: "linear-gradient(135deg, #6366f1, #4f46e5)"', 'color: "#000000"')

with open('static/js/app.js', 'w') as f:
    f.write(js)

print("Applied pure white and darkest black theme")
