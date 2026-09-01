const pages = {
  welcome: document.getElementById("page-welcome"),
  personal: document.getElementById("page-personal"),
  health: document.getElementById("page-health"),
  report: document.getElementById("page-report"),
  prevention: document.getElementById("page-prevention"),
};

const showPage = (pageKey) => {
  Object.values(pages).forEach((p) => p.classList.add("hidden"));
  pages[pageKey].classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const setActivePage = (pageKey) => {
  showPage(pageKey);
};

const startButton = document.getElementById("startButton");
startButton.addEventListener("click", () => setActivePage("personal"));

const backButtons = document.querySelectorAll(".back");
backButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (!pages.health.classList.contains("hidden")) setActivePage("personal");
    else if (!pages.personal.classList.contains("hidden")) setActivePage("welcome");
    else if (!pages.report.classList.contains("hidden")) setActivePage("health");
    else if (!pages.prevention.classList.contains("hidden")) setActivePage("report");
  });
});

const heightMetersInput = document.getElementById("height");
const heightCmInput = document.getElementById("heightCm");
const heightFtInput = document.getElementById("heightFt");
const heightInInput = document.getElementById("heightIn");
const weightInput = document.getElementById("weight");
const bmiValue = document.getElementById("bmiValue");
const bmiTag = document.getElementById("bmiTag");

const heightUnitRadios = document.querySelectorAll("input[name=heightUnit]");
const heightMetersSection = document.getElementById("heightMeters");
const heightCmSection = document.getElementById("heightCmWrapper");
const heightFtSection = document.getElementById("heightFtWrapper");

const getHeightMeters = () => {
  const unit = document.querySelector("input[name=heightUnit]:checked").value;

  if (unit === "cm") {
    const cm = parseFloat(heightCmInput.value) || 0;
    return cm / 100;
  }

  if (unit === "ft") {
    const ft = parseFloat(heightFtInput.value) || 0;
    const inch = parseFloat(heightInInput.value) || 0;
    return (ft * 12 + inch) * 0.0254;
  }

  const m = parseFloat(heightMetersInput.value) || 0;
  return m;
};

const getBmiTag = (bmi) => {
  if (!bmi || isNaN(bmi) || bmi === 0) return { label: "—", className: "" };
  if (bmi < 18.5) return { label: "Underweight", className: "tag--low" };
  if (bmi < 25) return { label: "Normal", className: "tag--normal" };
  if (bmi < 30) return { label: "Overweight", className: "tag--high" };
  return { label: "Obese", className: "tag--high" };
};

const updateBmi = () => {
  const h = getHeightMeters();
  const w = parseFloat(weightInput.value) || 0;
  const bmi = h > 0 ? w / (h * h) : 0;
  const display = bmi > 0 ? bmi.toFixed(1) : "-";

  bmiValue.textContent = display;
  const { label, className } = getBmiTag(bmi);
  bmiTag.textContent = label;
  bmiTag.className = `tag ${className}`;
};

const setHeightUnit = () => {
  const unit = document.querySelector("input[name=heightUnit]:checked").value;
  heightMetersSection.classList.toggle("hidden", unit !== "m");
  heightCmSection.classList.toggle("hidden", unit !== "cm");
  heightFtSection.classList.toggle("hidden", unit !== "ft");
  updateBmi();
};

heightUnitRadios.forEach((radio) => radio.addEventListener("change", setHeightUnit));

[heightMetersInput, heightCmInput, heightFtInput, heightInInput, weightInput].forEach((el) =>
  el.addEventListener("input", updateBmi)
);

setHeightUnit();

const toHealthButton = document.getElementById("toHealthForm");
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
});

document.getElementById("name").addEventListener("input", function() {
    document.getElementById("nameError").style.display = "none";
    this.style.borderColor = "";
});

const submitButton = document.getElementById("submitButton");
const overallRiskEl = document.getElementById("overallRisk");
const riskLevelEl = document.getElementById("riskLevel");
const resultContainer = document.getElementById("resultContainer");
const preventionList = document.getElementById("preventionList");
const riskChartCtx = document.getElementById("riskChart").getContext("2d");

let riskChart;

const getRiskLevel = (score) => {
  if (score < 30) return { label: "Low", color: "rgba(34, 197, 94, 0.9)" };
  if (score < 60) return { label: "Medium", color: "rgba(234, 179, 8, 0.9)" };
  return { label: "High", color: "rgba(248, 113, 113, 0.9)" };
};

const makeRiskCard = (disease) => {
  const { label: levelLabel, color } = getRiskLevel(disease.risk);
  const card = document.createElement("div");
  card.className = "result-card";

  card.innerHTML = `
    <div class="result-card__header">
      <div>
        <h3 class="result-card__title">${disease.name}</h3>
        <div class="result-card__tag" style="background: ${color}22; color: ${color};">${levelLabel}</div>
      </div>
      <div class="result-card__score">${disease.risk.toFixed(1)}%</div>
    </div>
    <div class="result-card__details">
      <p><strong>Why?</strong></p>
      <p>${disease.why.length ? disease.why.join(", ") : "No clear risk factors detected."}</p>
    </div>
  `;

  return card;
};

const renderChart = (diseases) => {
  const labels = diseases.map((d) => d.name);
  const values = diseases.map((d) => Number(d.risk.toFixed(1)));
  const colors = diseases.map((_, i) => `rgba(30, 41, 59, ${0.9 - (i * 0.1)})`);

  if (riskChart) {
    riskChart.destroy();
    riskChart = null;
  }

  riskChart = new Chart(riskChartCtx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Risk (%)",
          data: values,
          backgroundColor: colors,
          borderRadius: 14,
          maxBarThickness: 28,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: "rgba(0,0,0,0.1)",
          },
          ticks: {
            color: "#334155",
            stepSize: 20,
          },
        },
        x: {
          ticks: {
            color: "#334155",
          },
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "#000000",
          titleColor: "#ffffff",
          bodyColor: "#ffffff",
          borderColor: "#000000",
          borderWidth: 1,
        },
      },
    },
  });
};

const renderReport = (data) => {
  const overall = data.diseases.reduce((sum, item) => sum + item.risk, 0) / data.diseases.length;
  const overallRiskText = `${overall.toFixed(1)}%`;
  const overallLevel = getRiskLevel(overall);

  overallRiskEl.textContent = overallRiskText;
  riskLevelEl.textContent = overallLevel.label;
  riskLevelEl.style.color = overallLevel.color;

  resultContainer.innerHTML = "";
  data.diseases.forEach((d) => {
    resultContainer.appendChild(makeRiskCard(d));
  });

  renderChart(data.diseases);

    const getPreventionMeta = (step) => {
    const text = step.toLowerCase();
    if (text.includes("exercise") || text.includes("activity")) return { icon: "fa-person-running", color: "#334155" };
    if (text.includes("weight") || text.includes("bmi")) return { icon: "fa-weight-scale", color: "#334155" };
    if (text.includes("sugar") || text.includes("food") || text.includes("eat") || text.includes("vegetable") || text.includes("diet")) return { icon: "fa-apple-whole", color: "#334155" };
    if (text.includes("water") || text.includes("drink")) return { icon: "fa-glass-water", color: "#334155" };
    if (text.includes("sleep")) return { icon: "fa-bed", color: "#334155" };
    if (text.includes("stress") || text.includes("relax") || text.includes("meditation")) return { icon: "fa-spa", color: "#334155" };
    if (text.includes("smoking") || text.includes("alcohol")) return { icon: "fa-ban-smoking", color: "#334155" };
    if (text.includes("blood pressure") || text.includes("glucose") || text.includes("monitor")) return { icon: "fa-heart-pulse", color: "#334155" };
    return { icon: "fa-check-circle", color: "#334155" };
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
        <p style="font-size: 1.1rem; font-weight: 600; margin: 0;">${step}</p>
      </div>
    `;
    preventionList.appendChild(card);
  });
};

submitButton.addEventListener("click", async () => {
  const heightMeters = getHeightMeters();

  const payload = {
    name: document.getElementById("name").value,
    age: Number(document.getElementById("age").value),
    gender: document.getElementById("gender").value,
    height: heightMeters,
    weight: Number(document.getElementById("weight").value),
    bmi: Number(bmiValue.textContent),
    glucose: Number(document.getElementById("glucose").value),
    blood_pressure: Number(document.getElementById("bloodPressure").value),
    cholesterol: Number(document.getElementById("cholesterol").value),
    heart_rate: Number(document.getElementById("heartRate").value),
    sleep_hours: Number(document.getElementById("sleepHours").value),
    stress_level: Number(document.getElementById("stressLevel").value),
    physical_activity: Number(document.getElementById("physicalActivity").value),
    daily_steps: Number(document.getElementById("dailySteps").value),
    smoking: Number(document.getElementById("smoking").value),
  };

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  renderReport(data);
  setActivePage("report");
});

document.getElementById("toPrevention").addEventListener("click", () => {
  setActivePage("prevention");
});

document.getElementById("startOver").addEventListener("click", () => {
  setActivePage("welcome");
});

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
