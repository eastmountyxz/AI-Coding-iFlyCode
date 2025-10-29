const newsData = [
  {
    id: 1,
    title: "国产大飞机完成新航线首飞",
    source: "新华网",
    heat: 987654,
    timestamp: "2024-05-12T09:30:00",
    summary: "C919国产大飞机完成上海至北京定期航线首飞，标志着国产民航运输能力再获突破。",
    category: "科技",
    image: "https://via.placeholder.com/400x240?text=News+1"
  },
  {
    id: 2,
    title: "多省出台稳就业新政支持高校毕业生",
    source: "央视新闻",
    heat: 865432,
    timestamp: "2024-05-12T08:45:00",
    summary: "围绕高校毕业生就业，多省发布系列扶持政策，涵盖补贴、培训、岗位拓展等措施。",
    category: "经济",
    image: "https://via.placeholder.com/400x240?text=News+2"
  },
  {
    id: 3,
    title: "全国首个无人驾驶公交线路投入运营",
    source: "人民网",
    heat: 812340,
    timestamp: "2024-05-12T07:50:00",
    summary: "深圳上线全国首个全场景无人驾驶公交线路，日均运送乘客突破5000人次。",
    category: "科技",
    image: "https://via.placeholder.com/400x240?text=News+3"
  },
  {
    id: 4,
    title: "中国女排夺得世界联赛首站冠军",
    source: "新华社",
    heat: 689123,
    timestamp: "2024-05-11T22:10:00",
    summary: "中国女排在世界女排联赛首站比赛中击败劲旅夺冠，主攻手斩获全场MVP。",
    category: "体育",
    image: "https://via.placeholder.com/400x240?text=News+4"
  },
  {
    id: 5,
    title: "长三角一体化示范区发布数字政务合作框架",
    source: "解放日报",
    heat: 534890,
    timestamp: "2024-05-11T18:20:00",
    summary: "示范区三地联合推出数字政务合作框架，实现政务服务事项跨域通办。",
    category: "社会",
    image: "https://via.placeholder.com/400x240?text=News+5"
  },
  {
    id: 6,
    title: "新冠疫苗加强针覆盖率持续提升",
    source: "健康时报",
    heat: 498765,
    timestamp: "2024-05-11T16:05:00",
    summary: "国家卫健委发布数据显示，全国新冠疫苗加强针接种覆盖率持续提升，重点人群完成率达92%。",
    category: "健康",
    image: "https://via.placeholder.com/400x240?text=News+6"
  },
  {
    id: 7,
    title: "世界智能大会聚焦人工智能安全治理",
    source: "科技日报",
    heat: 478990,
    timestamp: "2024-05-11T13:40:00",
    summary: "与会专家呼吁加强人工智能安全治理，推动行业标准制定与国际合作。",
    category: "科技",
    image: "https://via.placeholder.com/400x240?text=News+7"
  },
  {
    id: 8,
    title: "大型史诗话剧《长城》首演收获好评",
    source: "中国文化报",
    heat: 365432,
    timestamp: "2024-05-10T19:30:00",
    summary: "融合多媒体舞台技术的史诗话剧《长城》在北京首演，以创新视角讲述长城故事。",
    category: "文娱",
    image: "https://via.placeholder.com/400x240?text=News+8"
  }
];

const state = {
  sortBy: "heat",
  currentPage: 1,
  itemsPerPage: 4,
  filter: "全部",
  searchKeyword: ""
};

const hotlistItems = document.getElementById("hotlistItems");
const sortSelect = document.getElementById("sortSelect");
const paginationInfo = document.getElementById("paginationInfo");
const prevPageBtn = document.getElementById("prevPage");
const nextPageBtn = document.getElementById("nextPage");
const filterButtons = document.querySelectorAll(".filter-btn");
const searchForm = document.querySelector(".search-form");
const searchInput = document.getElementById("searchInput");
const themeToggle = document.getElementById("themeToggle");
const backToTopBtn = document.getElementById("backToTop");
const openFormBtn = document.getElementById("openForm");
const modal = document.getElementById("submissionModal");
const closeModalBtn = modal.querySelector(".modal-close");
const submissionForm = document.getElementById("submissionForm");
const successMessage = document.getElementById("formSuccess");

function sortData(data) {
  const sorted = [...data];
  if (state.sortBy === "heat") {
    sorted.sort((a, b) => b.heat - a.heat);
  } else if (state.sortBy === "time") {
    sorted.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  }
  return sorted;
}

function filterData(data) {
  return data.filter(item => {
    const matchFilter = state.filter === "全部" || item.category === state.filter;
    const matchKeyword = item.title.includes(state.searchKeyword.trim());
    return matchFilter && matchKeyword;
  });
}

function renderHotlist() {
  const sorted = sortData(newsData);
  const filtered = filterData(sorted);
  const totalItems = filtered.length;
  const totalPages = Math.ceil(totalItems / state.itemsPerPage) || 1;

  if (state.currentPage > totalPages) {
    state.currentPage = totalPages;
  }

  const startIndex = (state.currentPage - 1) * state.itemsPerPage;
  const paginatedItems = filtered.slice(startIndex, startIndex + state.itemsPerPage);

  hotlistItems.innerHTML = "";

  paginatedItems.forEach((item, index) => {
    const globalIndex = sorted.findIndex(news => news.id === item.id);
    const rank = globalIndex + 1;
    const icon = rank === 1 ? "🏆" : rank <= 3 ? "🔥" : "";
    const listItem = document.createElement("li");
    listItem.className = "hot-card";
    listItem.innerHTML = `
      <div class="hot-card-header">
        <span class="hot-card-rank" aria-label="排名">${rank.toString().padStart(2, "0")}</span>
        ${icon ? `<span class="hot-card-icon" aria-hidden="true">${icon}</span>` : ""}
        <div class="hot-card-meta">
          <span aria-label="来源">${item.source}</span>
          <span aria-label="热度">热度 ${item.heat.toLocaleString()}</span>
          <span aria-label="时间">${formatTime(item.timestamp)}</span>
        </div>
      </div>
      <div class="hot-card-image">
        <img src="${item.image}" alt="${item.title} 缩略图" loading="lazy" />
      </div>
      <div class="hot-card-content">
        <h3>${item.title}</h3>
        <p>${item.summary}</p>
      </div>
    `;
    listItem.setAttribute("data-category", item.category);
    hotlistItems.appendChild(listItem);
  });

  paginationInfo.textContent = `${state.currentPage} / ${totalPages}`;
  prevPageBtn.disabled = state.currentPage === 1;
  nextPageBtn.disabled = state.currentPage === totalPages;
}

function formatTime(timestamp) {
  const date = new Date(timestamp);
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;
}

sortSelect.addEventListener("change", event => {
  state.sortBy = event.target.value;
  state.currentPage = 1;
  renderHotlist();
});

prevPageBtn.addEventListener("click", () => {
  if (state.currentPage > 1) {
    state.currentPage -= 1;
    renderHotlist();
  }
});

nextPageBtn.addEventListener("click", () => {
  state.currentPage += 1;
  renderHotlist();
});

filterButtons.forEach(button => {
  button.addEventListener("click", () => {
    filterButtons.forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
    state.filter = button.dataset.filter;
    state.currentPage = 1;
    renderHotlist();
  });
});

searchForm.addEventListener("submit", event => {
  event.preventDefault();
  state.searchKeyword = searchInput.value;
  state.currentPage = 1;
  renderHotlist();
});

const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
  document.body.classList.add("dark-theme");
  themeToggle.setAttribute("aria-pressed", "true");
}

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-theme");
  const isDark = document.body.classList.contains("dark-theme");
  themeToggle.setAttribute("aria-pressed", String(isDark));
  localStorage.setItem("theme", isDark ? "dark" : "light");
});

window.addEventListener("scroll", () => {
  if (window.scrollY > 200) {
    backToTopBtn.style.display = "flex";
  } else {
    backToTopBtn.style.display = "none";
  }
});

backToTopBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

openFormBtn.addEventListener("click", () => toggleModal(true));
closeModalBtn.addEventListener("click", () => toggleModal(false));
modal.addEventListener("click", event => {
  if (event.target === modal) {
    toggleModal(false);
  }
});

document.addEventListener("keydown", event => {
  if (event.key === "Escape" && modal.getAttribute("aria-hidden") === "false") {
    toggleModal(false);
  }
});

function toggleModal(open) {
  modal.setAttribute("aria-hidden", open ? "false" : "true");
  document.body.style.overflow = open ? "hidden" : "";
  if (open) {
    submissionForm.querySelector("input, textarea").focus();
  } else {
    submissionForm.reset();
    resetErrors();
    successMessage.hidden = true;
  }
}

submissionForm.addEventListener("submit", event => {
  event.preventDefault();
  const isValid = validateForm();
  if (isValid) {
    successMessage.hidden = false;
    submissionForm.reset();
    setTimeout(() => {
      toggleModal(false);
    }, 1800);
  }
});

submissionForm.addEventListener("reset", () => {
  resetErrors();
  successMessage.hidden = true;
});

function validateForm() {
  resetErrors();
  let valid = true;

  const title = submissionForm.newsTitle.value.trim();
  const link = submissionForm.newsLink.value.trim();
  const source = submissionForm.newsSource.value.trim();
  const summary = submissionForm.newsSummary.value.trim();
  const email = submissionForm.email.value.trim();

  if (!title) {
    setError("titleError", "请填写标题");
    valid = false;
  }

  const urlPattern = /^(https?:\/\/)[\w.-]+(?:\.[\w\.-]+)+(?:[\w\-\._~:\/?#\[\]@!$&'()*+,;=.]+)?$/;
  if (!link || !urlPattern.test(link)) {
    setError("linkError", "请输入有效的链接（需以http或https开头）");
    valid = false;
  }

  if (!source) {
    setError("sourceError", "请填写来源");
    valid = false;
  }

  if (!summary) {
    setError("summaryError", "请填写摘要");
    valid = false;
  }

  const emailPattern = /^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$/;
  if (!email || !emailPattern.test(email)) {
    setError("emailError", "请输入有效的邮箱地址");
    valid = false;
  }

  return valid;
}

function setError(id, message) {
  const errorElement = document.getElementById(id);
  errorElement.textContent = message;
}

function resetErrors() {
  submissionForm.querySelectorAll(".error").forEach(el => (el.textContent = ""));
}

renderHotlist();
filterButtons[0].classList.add("active");
