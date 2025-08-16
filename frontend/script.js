const API_BASE = ""; 

const sidebar = document.querySelector('.company-list');

sidebar.addEventListener('scroll', () => {
  sidebar.style.setProperty('--top-shadow-opacity', sidebar.scrollTop > 0 ? 1 : 0);
  sidebar.style.setProperty('--bottom-shadow-opacity', sidebar.scrollHeight - sidebar.scrollTop > sidebar.clientHeight + 1 ? 1 : 0);
});

const state = {
  companies: [],
  selected: null,
  chart: null,
};

function fmtNumber(n){
  if(n == null || isNaN(n)) return "-";
  return Number(n).toLocaleString();
}
function fmtPrice(n){
  if(n == null || isNaN(n)) return "-";
  return Number(n).toLocaleString(undefined, {maximumFractionDigits:2});
}

async function loadCompanies(){
  const res = await fetch(`${API_BASE}/api/companies`);
  const data = await res.json();
  state.companies = data;
  renderCompanyList();
}

function renderCompanyList(filter=""){
  const ul = document.getElementById("companyList");
  ul.innerHTML = "";
  const items = state.companies.filter(c => (c.name + c.ticker).toLowerCase().includes(filter.toLowerCase()));
  items.forEach(c => {
    const li = document.createElement("li");
    li.textContent = `${c.name} (${c.ticker})`;
    li.onclick = () => selectCompany(c);
    if(state.selected && state.selected.ticker === c.ticker) li.classList.add("active");
    ul.appendChild(li);
  });
}

async function selectCompany(c){
  state.selected = c;
  document.getElementById("selectedName").textContent = `${c.name} (${c.ticker})`;
  [...document.querySelectorAll(".company-list li")].forEach(li => li.classList.remove("active"));
  renderCompanyList(document.getElementById("search").value); // re-render to apply active class

  const period = document.getElementById("period").value;
  const interval = document.getElementById("interval").value;
  const url = `${API_BASE}/api/history?ticker=${encodeURIComponent(c.ticker)}&period=${period}&interval=${interval}&predict=true`;
  const res = await fetch(url);
  if(!res.ok){
    alert("Failed to fetch history for " + c.ticker);
    return;
  }
  const data = await res.json();
  updateStats(data.stats, data.prediction);
  drawChart(data.data);
}

function updateStats(stats, pred){
  document.getElementById("stat_last").textContent = fmtPrice(stats.last_close);
  document.getElementById("stat_high").textContent = fmtPrice(stats["52w_high"]);
  document.getElementById("stat_low").textContent = fmtPrice(stats["52w_low"]);
  document.getElementById("stat_vol").textContent = fmtNumber(stats.avg_volume_30d);
  document.getElementById("stat_rsi").textContent = fmtPrice(stats.rsi_14);
  document.getElementById("stat_pred").textContent = pred ? fmtPrice(pred.predicted_close) : "-";
}

function drawChart(rows){
  const labels = rows.map(r => r.date);
  const prices = rows.map(r => r.close);
  const ctx = document.getElementById('chart').getContext('2d');
  if(state.chart){
    state.chart.destroy();
  }
  state.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Close',
        data: prices,
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: { display: true, title: { display: false } },
        y: { display: true, title: { display: false }, ticks:{ callback: (v)=> fmtPrice(v) } }
      },
      plugins: {
        legend: { display: true },
        tooltip: {
          callbacks: {
            label: (ctx) => `Close: ${fmtPrice(ctx.parsed.y)}`
          }
        }
      }
    }
  });

}
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("search").addEventListener("input", (e)=> renderCompanyList(e.target.value));
  document.getElementById("period").addEventListener("change", ()=> state.selected && selectCompany(state.selected));
  document.getElementById("interval").addEventListener("change", ()=> state.selected && selectCompany(state.selected));

  // Init
  loadCompanies().then(()=> {
    if(state.companies.length){
      selectCompany(state.companies[0]);
    }
  });
});

