console.log("🔥 NOVÝ SCRIPT.JS SE NAČETL");

const API_URL = "http://127.0.0.1:8000";

let allJobs = [];

async function loadJobs() {
  const token = localStorage.getItem("access_token");

  const res = await fetch(API_URL + "/jobs", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await res.json();

  if (!res.ok) {
    console.error("Načtení nabídek selhalo:", data);
    allJobs = [];
    showToast("❌ Nabídky se nepodařilo načíst.");
    return;
  }

  allJobs = data;

  const list = document.getElementById("jobs");
  const empty = document.getElementById("empty");

  list.innerHTML = "";

  if (data.length === 0) {
    empty.style.display = "block";
  } else {
    empty.style.display = "none";
  }

  applyFilters();
}

async function createJob() {
  const titleInput = document.getElementById("title");
  const companyInput = document.getElementById("company");
  const locationInput = document.getElementById("location");
  const salaryInput = document.getElementById("salary");
  const urlInput = document.getElementById("url");
  const contactInput = document.getElementById("contact");
  const noteInput = document.getElementById("note");

  const title = titleInput.value;
  const company = companyInput.value;
  const location = locationInput.value;
  const salary = salaryInput.value;
  const url = urlInput.value;
  const contact = contactInput.value;
  const note = noteInput.value;

  titleInput.classList.remove("input-error");
  companyInput.classList.remove("input-error");
  locationInput.classList.remove("input-error");

  let hasError = false;

  if (title.trim() === "") {
    titleInput.classList.add("input-error");
    hasError = true;
  }

  if (company.trim() === "") {
    companyInput.classList.add("input-error");
    hasError = true;
  }

  if (location.trim() === "") {
    locationInput.classList.add("input-error");
    hasError = true;
  }

  if (hasError) {
    showToast("⚠️ Vyplňte všechna pole.");
    return;
  }

  const token = localStorage.getItem("access_token");

  if (!token) {
    showToast("❌ Nejste přihlášeni.");
    return;
  }

  const response = await fetch(API_URL + "/jobs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      company,
      location,
      salary,
      url,
      contact,
      note,
    }),
  });

  if (!response.ok) {
    const data = await response.json();
    let errorMessage = "Nabídku se nepodařilo přidat.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    }

    showToast("❌ " + errorMessage);
    return;
  }

  document.getElementById("title").value = "";
  document.getElementById("company").value = "";
  document.getElementById("location").value = "";
  document.getElementById("salary").value = "";
  document.getElementById("url").value = "";
  document.getElementById("contact").value = "";
  document.getElementById("note").value = "";

  await loadJobs();

  showToast("✅ Nabídka byla přidána");
}

let jobToDelete = null;
let jobToEdit = null;

function deleteJob(id) {
  jobToDelete = id;
  const modal = document.getElementById("confirmModal");
  modal.style.display = "flex";
}

function editJob(job) {
  jobToEdit = job;

  document.getElementById("editTitle").value = job.title;
  document.getElementById("editCompany").value = job.company;
  document.getElementById("editLocation").value = job.location;
  document.getElementById("editSalary").value = job.salary || "";
  document.getElementById("editUrl").value = job.url || "";
  document.getElementById("editContact").value = job.contact || "";
  document.getElementById("editNote").value = job.note || "";

  const modal = document.getElementById("editModal");
  modal.style.display = "flex";
}

async function removeJob() {
  const token = localStorage.getItem("access_token");

  const response = await fetch(API_URL + "/jobs/" + jobToDelete, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const data = await response.json();
    let errorMessage = "Nabídku se nepodařilo odstranit.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    }

    showToast("❌ " + errorMessage);
    return;
  }

  await loadJobs();

  showToast("🗑️ Nabídka byla odstraněna");

  closeModal();
}

async function updateJob() {
  const title = document.getElementById("editTitle").value;
  const company = document.getElementById("editCompany").value;
  const location = document.getElementById("editLocation").value;
  const salary = document.getElementById("editSalary").value;
  const url = document.getElementById("editUrl").value;
  const contact = document.getElementById("editContact").value;
  const note = document.getElementById("editNote").value;
  const token = localStorage.getItem("access_token");

  const response = await fetch(API_URL + "/jobs/" + jobToEdit.id, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      company,
      location,
      salary,
      url,
      contact,
      note,
      status: jobToEdit.status,
    }),
  });

  if (!response.ok) {
    const data = await response.json();
    let errorMessage = "Nabídku se nepodařilo upravit.";

    if (typeof data.detail === "string") {
      errorMessage = data.detail;
    }

    showToast("❌ " + errorMessage);
    return;
  }

  await loadJobs();

  showToast("✏️ Nabídka byla upravena");

  closeEditModal();
}

function closeModal() {
  const modal = document.getElementById("confirmModal");
  modal.style.display = "none";
  jobToDelete = null;
}

function closeEditModal() {
  const modal = document.getElementById("editModal");
  modal.style.display = "none";
  jobToEdit = null;
}

function sortJobs() {
  applyFilters();
}

async function toggleFavorite(id) {
  let favorites = JSON.parse(localStorage.getItem("favorites")) || [];

  if (favorites.includes(id)) {
    favorites = favorites.filter((favoriteId) => favoriteId !== id);
    showToast("☆ Odebráno z oblíbených");
  } else {
    favorites.push(id);
    showToast("⭐ Přidáno do oblíbených");
  }

  localStorage.setItem("favorites", JSON.stringify(favorites));

  await loadJobs();
}

function showToast(message) {
  const toast = document.getElementById("toast");

  if (!toast) {
    console.error("Toast element nebyl nalezen.");
    return;
  }

  toast.textContent = message;
  toast.classList.remove("show");
  void toast.offsetWidth;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 6000);
}

window.onload = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const showFavorites = urlParams.get("favorites") === "true";

  if (showFavorites) {
    document.getElementById("favoriteOnly").checked = true;
  }

  loadJobs();

  document.getElementById("confirmDelete").addEventListener("click", removeJob);
  document.getElementById("cancelDelete").addEventListener("click", closeModal);
  document
    .getElementById("cancelEdit")
    .addEventListener("click", closeEditModal);
  document.getElementById("saveEdit").addEventListener("click", updateJob);
  document.getElementById("search").addEventListener("input", searchJobs);
  document.getElementById("sort").addEventListener("change", sortJobs);
  document
    .getElementById("favoriteOnly")
    .addEventListener("change", filterFavorites);

  const menuButton = document.getElementById("menuButton");
  const menuDropdown = document.getElementById("menuDropdown");

  if (menuButton && menuDropdown) {
    menuButton.addEventListener("click", () => {
      menuDropdown.classList.toggle("open");
    });

    document.addEventListener("click", (event) => {
      if (
        !menuButton.contains(event.target) &&
        !menuDropdown.contains(event.target)
      ) {
        menuDropdown.classList.remove("open");
      }
    });
  }
};

function renderJobs(jobs) {
  const list = document.getElementById("jobs");

  list.innerHTML = "";

  jobs.forEach((job) => {
    const div = document.createElement("div");
    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    const isFavorite = favorites.includes(job.id);

    div.className = isFavorite
      ? "job job-animation favorite-job"
      : "job job-animation";

    div.innerHTML = `
      <div class="job-info">
        <h3>
          💼 ${job.title}
        </h3>

        <p>
          🏢 ${job.company}
        </p>

        <p>
          📍 ${job.location}
        </p>

        ${
          job.salary
            ? `
        <p>
          💰 ${job.salary}
        </p>
        `
            : ""
        }

        ${
          job.url
            ? `
        <a class="job-link" href="${job.url}" target="_blank">
          🔗 Otevřít nabídku
        </a>
        `
            : ""
        }

        ${
          job.contact
            ? `
        <details class="job-details">
          <summary>👤 Kontakt</summary>
          <p>${job.contact}</p>
        </details>
        `
            : ""
        }

        ${
          job.note
            ? `
        <details class="job-details">
          <summary>📝 Poznámka</summary>
          <p>${job.note}</p>
        </details>
        `
            : ""
        }

        <div class="status-row">
          <div class="status-badge status-${job.status}">
            ${job.status}
          </div>

          <select onchange="changeStatus(${job.id}, this.value)">
            <option ${job.status === "Aktivní" ? "selected" : ""}>
              Aktivní
            </option>

            <option ${job.status === "Životopis odeslán" ? "selected" : ""}>
              Životopis odeslán
            </option>

            <option ${job.status === "Pohovor" ? "selected" : ""}>
              Pohovor
            </option>

            <option ${job.status === "Přijato" ? "selected" : ""}>
              Přijato
            </option>

            <option ${job.status === "Zamítnuto" ? "selected" : ""}>
              Zamítnuto
            </option>
          </select>
        </div>

        ${
          job.created_at
            ? `
        <p class="job-date">
          📅 ${job.created_at}
        </p>
        `
            : ""
        }

        <div class="job-buttons">
          <button
            class="edit-btn"
            onclick='editJob(${JSON.stringify(job)})'>
            ✏️ Upravit
          </button>

          <button
            class="ai-btn"
            onclick="analyzeJob(${job.id})">
            🤖 AI analyzovat
          </button>

          <button
            class="${isFavorite ? "favorite-btn active" : "favorite-btn"}"
            onclick="toggleFavorite(${job.id})">
            ${isFavorite ? "⭐ Oblíbené" : "🤍 Oblíbené"}
          </button>

          <button
            class="delete-btn"
            onclick="deleteJob(${job.id})">
            🗑️ Smazat
          </button>
        </div>
      </div>
    `;

    list.appendChild(div);
  });
}

// STARÁ VERZE renderJobs - záloha

function filterFavorites() {
  const checkbox = document.getElementById("favoriteOnly");
  const favorites = JSON.parse(localStorage.getItem("favorites")) || [];

  if (checkbox.checked) {
    const favoriteJobs = allJobs.filter((job) => favorites.includes(job.id));
    renderJobs(favoriteJobs);
  } else {
    renderJobs(allJobs);
  }
}

function searchJobs() {
  applyFilters();
}

async function changeStatus(id, status) {
  await fetch(`http://127.0.0.1:8000/jobs/${id}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      status: status,
    }),
  });

  loadJobs();
}

function applyFilters() {
  let filteredJobs = [...allJobs];

  // FILTR OBLÍBENÝCH
  const favoriteOnly = document.getElementById("favoriteOnly");

  if (favoriteOnly && favoriteOnly.checked) {
    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    filteredJobs = filteredJobs.filter((job) => favorites.includes(job.id));
  }

  // FILTR STATUSU
  const statusFilter = document.getElementById("statusFilter");

  if (statusFilter && statusFilter.value !== "all") {
    filteredJobs = filteredJobs.filter(
      (job) => job.status === statusFilter.value,
    );
  }

  // VYHLEDÁVÁNÍ
  const searchValue = document.getElementById("search").value.toLowerCase();

  if (searchValue !== "") {
    filteredJobs = filteredJobs.filter((job) => {
      return (
        job.title.toLowerCase().includes(searchValue) ||
        job.company.toLowerCase().includes(searchValue) ||
        job.location.toLowerCase().includes(searchValue)
      );
    });
  }

  // ŘAZENÍ
  const sortValue = document.getElementById("sort").value;

  if (sortValue === "title") {
    filteredJobs.sort((a, b) => a.title.localeCompare(b.title));
  }

  if (sortValue === "company") {
    filteredJobs.sort((a, b) => a.company.localeCompare(b.company));
  }

  updateStats();
  renderJobs(filteredJobs);
}

const statusFilter = document.getElementById("statusFilter");

if (statusFilter) {
  statusFilter.addEventListener("change", applyFilters);
}

function updateStats() {
  const active = allJobs.filter((job) => job.status === "Aktivní").length;

  const sent = allJobs.filter(
    (job) => job.status === "Životopis odeslán",
  ).length;

  const interview = allJobs.filter((job) => job.status === "Pohovor").length;
  const accepted = allJobs.filter((job) => job.status === "Přijato").length;
  const rejected = allJobs.filter((job) => job.status === "Zamítnuto").length;

  document.getElementById("countActive").textContent = active;
  document.getElementById("countSent").textContent = sent;
  document.getElementById("countInterview").textContent = interview;
  document.getElementById("countAccepted").textContent = accepted;
  document.getElementById("countRejected").textContent = rejected;
}

async function searchWithAI() {
  const position = document.getElementById("aiPosition").value.trim();
  const location = document.getElementById("aiLocation").value.trim();
  const skills = document.getElementById("aiSkills").value.trim();
  const workType = document.getElementById("aiWorkType").value;

  const results = document.getElementById("aiResults");
  const button = document.getElementById("aiSearchButton");

  if (!position) {
    showToast("⚠️ Zadej, jakou práci hledáš.");
    return;
  }

  results.innerHTML = `
    <div class="ai-loading">
      🤖 Hledám vhodné pracovní nabídky...
    </div>
  `;

  button.disabled = true;
  button.textContent = "🤖 Hledám...";

  try {
    const response = await fetch(API_URL + "/ai/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        position: position,
        location: location,
        skills: skills,
        workType: workType,
      }),
    });

    if (!response.ok) {
      throw new Error("AI endpoint vrátil chybu.");
    }

    const data = await response.json();

    console.log("AI odpověď:", data);

    if (data.jobs.length === 0) {
      results.innerHTML = `
        <div class="ai-result-message">
          🔎 Nenašel jsem žádné odpovídající nabídky.
        </div>
      `;
    } else {
      results.innerHTML = `
        <div class="ai-results-header">
          <h3>🤖 Nalezené nabídky</h3>
        </div>

        <div class="ai-job-results">
          ${[...data.jobs]
            .sort((a, b) => b.match_score - a.match_score)
            .map(
              (job) => `
              <div class="ai-job-card ${job.match_score >= 80 ? "ai-top-match" : ""}">
                ${
                  job.match_score >= 80
                    ? `<div class="ai-top-badge">⭐ TOP SHODA</div>`
                    : ""
                }

                <div class="ai-match-score">
                  <div class="ai-match-score-header">
                    <span>🤖 AI shoda</span>
                    <strong>
                      ${job.match_score !== null ? job.match_score + " %" : "Nelze určit"}
                    </strong>
                  </div>

                  ${
                    job.match_score !== null
                      ? `
                    <div class="ai-score-bar">
                      <div
                        class="ai-score-fill"
                        style="width: ${job.match_score}%">
                      </div>
                    </div>

                    <div class="ai-match-level match-${
                      job.match_score >= 80
                        ? "high"
                        : job.match_score >= 50
                          ? "medium"
                          : "low"
                    }">
                      ${job.match_level}
                    </div>
                  `
                      : `
                    <div class="ai-no-score">
                      ℹ️ Pro vyhodnocení shody zadej své dovednosti.
                    </div>
                  `
                  }
                </div>

                <h4>💼 ${job.title}</h4>

                <p>🏢 ${job.company}</p>

                <p>📍 ${job.location}</p>

                ${job.salary ? `<p>💰 ${job.salary}</p>` : ""}

                ${
                  job.url
                    ? `
                  <a
                    class="job-link"
                    href="${job.url}"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    🔗 Otevřít nabídku
                  </a>
                `
                    : ""
                }

                <div class="ai-match-details">
                  <div>
                    <strong>✅ Tvé dovednosti:</strong>

                    ${
                      job.matched_skills.length
                        ? job.matched_skills
                            .map(
                              (skill) =>
                                `<span class="skill-match">${skill}</span>`,
                            )
                            .join("")
                        : "<span>Žádná shoda</span>"
                    }
                  </div>

                  <div>
                    <strong>⚠️ Chybějící dovednosti:</strong>

                    ${
                      job.missing_skills.length
                        ? job.missing_skills
                            .map(
                              (skill) =>
                                `<span class="skill-missing">${skill}</span>`,
                            )
                            .join("")
                        : "<span>Nic nechybí 🎉</span>"
                    }
                  </div>
                </div>

                <div class="ai-recommendation">
                  ⭐ ${job.recommendation}
                </div>

                <div class="ai-match-explanation">
                  💡 ${job.match_explanation}
                </div>

                ${
                  job.description
                    ? `
                  <details class="ai-job-details">
                    <summary>📄 Zobrazit podrobnosti nabídky</summary>
                    <div class="ai-job-description">
                      ${job.description}
                    </div>
                  </details>
                `
                    : ""
                }

                <div class="job-reference">
                  🆔 Referenční číslo: ${job.source_id}
                </div>

                <div class="ai-job-separator"></div>
              </div>
            `,
            )
            .join("")}
        </div>
      `;
    }
  } catch (error) {
    console.error("AI hledání selhalo:", error);

    results.innerHTML = `
      <div class="ai-result-error">
        ❌ Nepodařilo se získat pracovní nabídky.
      </div>
    `;

    showToast("❌ Chyba při AI hledání.");
  } finally {
    button.disabled = false;
    button.textContent = "🤖 Hledat pomocí AI";
  }
}

async function analyzeJob(id) {
  const job = allJobs.find((job) => job.id === id);

  if (!job) {
    showToast("❌ Nabídku se nepodařilo najít.");
    return;
  }

  const modal = document.getElementById("aiModal");
  const content = document.getElementById("aiAnalysisContent");

  modal.style.display = "flex";

  content.innerHTML = `
    <div class="ai-loading">
      🤖 AI analyzuje pracovní nabídku...
    </div>
  `;

  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch(API_URL + "/ai/analyze-job", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: job.title,
        company: job.company,
        location: job.location,
        salary: job.salary || "",
        url: job.url || "",
        contact: job.contact || "",
        note: job.note || "",
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("AI analýza selhala:", data);

      content.innerHTML = `
        <p>❌ AI analýzu se nepodařilo dokončit.</p>
      `;

      return;
    }

    const analysis = data.analysis;
    const sections = analysis.split(/\n(?=🎯|🛠️|💡|⚠️|💰|⭐)/);

    content.innerHTML = `
      <div class="ai-analysis-result">
        ${sections
          .map((section) => {
            const lines = section.trim().split("\n");
            const title = lines.shift();
            const text = lines.join("<br>");

            return `
              <div class="ai-analysis-section">
                <h3>${title}</h3>
                <div class="ai-analysis-text">
                  ${text}
                </div>
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  } catch (error) {
    console.error("Chyba AI analýzy:", error);

    content.innerHTML = `
      <p>❌ Nastala chyba při komunikaci s AI.</p>
    `;
  }
}

document.getElementById("closeAiModal").addEventListener("click", () => {
  document.getElementById("aiModal").style.display = "none";
});
