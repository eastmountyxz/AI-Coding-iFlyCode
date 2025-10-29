// 新闻数据
const newsData = [
    {
        id: 1,
        title: "全国两会即将召开，代表委员陆续抵京",
        source: "新华社",
        hot: 9856321,
        time: "2023-03-01 08:15",
        summary: "全国政协十四届一次会议和十四届全国人大一次会议将分别于3月4日和5日在北京开幕。来自各地的全国人大代表和全国政协委员陆续抵京，准备参加即将召开的全国两会。",
        image: "https://via.placeholder.com/300x200?text=全国两会",
        category: "国内"
    },
    {
        id: 2,
        title: "中国空间站将迎来首位女性航天员",
        source: "央视新闻",
        hot: 8765432,
        time: "2023-03-01 10:30",
        summary: "据中国载人航天工程办公室消息，神舟十五号载人飞行任务将于近期实施，此次任务将首次有女性航天员进入中国空间站。",
        image: "https://via.placeholder.com/300x200?text=中国空间站",
        category: "科技"
    },
    {
        id: 3,
        title: "2023年GDP增长目标设定为5%左右",
        source: "人民日报",
        hot: 7654321,
        time: "2023-03-01 09:45",
        summary: "国务院总理在政府工作报告中提出，2023年发展主要预期目标是：国内生产总值增长5%左右；城镇新增就业1200万人左右，城镇调查失业率5.5%左右。",
        image: "https://via.placeholder.com/300x200?text=GDP增长目标",
        category: "财经"
    },
    {
        id: 4,
        title: "全国多地迎来开学季，校园防疫措施优化",
        source: "中国教育报",
        hot: 6543210,
        time: "2023-03-01 07:20",
        summary: "随着春季学期开学，全国多地中小学和高校陆续迎来学生返校。各地教育部门优化校园防疫措施，确保师生健康安全。",
        image: "https://via.placeholder.com/300x200?text=开学季",
        category: "教育"
    },
    {
        id: 5,
        title: "中国科学家在量子计算领域取得重大突破",
        source: "科技日报",
        hot: 5432109,
        time: "2023-02-28 15:10",
        summary: "中国科学技术大学潘建伟团队在国际上首次实现基于纠缠的量子密钥分发，这一成果发表在《自然》杂志上，标志着我国在量子通信领域继续保持国际领先地位。",
        image: "https://via.placeholder.com/300x200?text=量子计算",
        category: "科技"
    },
    {
        id: 6,
        title: "北京冬奥会一周年纪念活动举行",
        source: "北京日报",
        hot: 4321098,
        time: "2023-02-28 14:05",
        summary: "在北京冬奥会成功举办一周年之际，北京市举行系列纪念活动，回顾冬奥精彩瞬间，展望后冬奥时代发展。",
        image: "https://via.placeholder.com/300x200?text=北京冬奥会",
        category: "体育"
    },
    {
        id: 7,
        title: "全国新冠疫苗接种超34亿剂次",
        source: "国家卫健委",
        hot: 3210987,
        time: "2023-02-28 11:30",
        summary: "截至2月28日，31个省（自治区、直辖市）和新疆生产建设兵团累计报告接种新冠病毒疫苗340567.8万剂次。",
        image: "https://via.placeholder.com/300x200?text=新冠疫苗",
        category: "国内"
    },
    {
        id: 8,
        title: "中国电影春节档票房突破100亿元",
        source: "国家电影局",
        hot: 2109876,
        time: "2023-02-27 18:45",
        summary: "2023年春节档电影票房达100.67亿元，创下中国影史春节档票房第二的好成绩。《满江红》《流浪地球2》等影片表现亮眼。",
        image: "https://via.placeholder.com/300x200?text=春节档电影",
        category: "娱乐"
    },
    {
        id: 9,
        title: "中国新能源汽车产销量连续8年全球第一",
        source: "工信部",
        hot: 1987654,
        time: "2023-02-27 16:20",
        summary: "2022年我国新能源汽车持续爆发式增长，产销分别完成705.8万辆和688.7万辆，同比分别增长96.9%和93.4%，连续8年保持全球第一。",
        image: "https://via.placeholder.com/300x200?text=新能源汽车",
        category: "财经"
    },
    {
        id: 10,
        title: "中国科学家发现新冠治疗新靶点",
        source: "中国科学院",
        hot: 1876543,
        time: "2023-02-27 14:10",
        summary: "中国科学院微生物研究所团队发现新冠病毒核衣壳蛋白与人类蛋白相互作用的新机制，为开发新型抗新冠病毒药物提供了新靶点。",
        image: "https://via.placeholder.com/300x200?text=新冠治疗",
        category: "科技"
    }
];

// DOM元素
const newsList = document.getElementById('newsList');
const submitNewsBtn = document.getElementById('submitNewsBtn');
const submitModal = document.getElementById('submitModal');
const closeBtn = document.querySelector('.close-btn');
const submitForm = document.getElementById('submitForm');
const successMessage = document.getElementById('successMessage');
const backToTop = document.getElementById('backToTop');
const themeToggle = document.getElementById('themeToggle');
const sortButtons = document.querySelectorAll('.sort-btn');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const pageNumbers = document.querySelector('.page-numbers');

// 分页变量
let currentPage = 1;
const itemsPerPage = 5;
let currentSort = 'hot';
let filteredNews = [...newsData];

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    renderNewsList();
    setupPagination();
    
    // 检查本地存储中的主题偏好
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
});

// 渲染新闻列表
function renderNewsList() {
    newsList.innerHTML = '';
    
    // 排序新闻
    if (currentSort === 'hot') {
        filteredNews.sort((a, b) => b.hot - a.hot);
    } else {
        filteredNews.sort((a, b) => new Date(b.time) - new Date(a.time));
    }
    
    // 分页
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedNews = filteredNews.slice(startIndex, startIndex + itemsPerPage);
    
    paginatedNews.forEach((news, index) => {
        const globalIndex = startIndex + index;
        const rank = globalIndex + 1;
        
        const newsCard = document.createElement('div');
        newsCard.className = 'news-card';
        
        // 排名样式
        let rankClass = '';
        if (rank === 1) {
            rankClass = 'rank-1';
        } else if (rank === 2) {
            rankClass = 'rank-2';
        } else if (rank === 3) {
            rankClass = 'rank-3';
        }
        
        // 格式化热度值
        const formattedHot = formatHotValue(news.hot);
        
        // 格式化时间
        const formattedTime = formatDateTime(news.time);
        
        newsCard.innerHTML = `
            <div class="news-rank ${rankClass}">
                <span>${rank}</span>
                ${rank <= 3 ? (rank === 1 ? '<span>🏆</span>' : '<span>🔥</span>') : ''}
            </div>
            <div class="news-content">
                <div class="news-header">
                    <h3 class="news-title">${news.title}</h3>
                    <span class="news-source">${news.source}</span>
                </div>
                <p class="news-summary">${news.summary}</p>
                <div class="news-meta">
                    <span class="news-hot">热度: ${formattedHot}</span>
                    <span class="news-time">时间: ${formattedTime}</span>
                </div>
            </div>
            <img src="${news.image}" alt="${news.title}" class="news-image">
        `;
        
        newsList.appendChild(newsCard);
    });
}

// 格式化热度值
function formatHotValue(hot) {
    if (hot >= 1000000) {
        return (hot / 1000000).toFixed(1) + '百万';
    } else if (hot >= 10000) {
        return (hot / 10000).toFixed(1) + '万';
    }
    return hot;
}

// 格式化日期时间
function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 24) {
        return `${diffInHours}小时前`;
    } else {
        return date.toLocaleDateString('zh-CN');
    }
}

// 设置分页
function setupPagination() {
    const totalPages = Math.ceil(filteredNews.length / itemsPerPage);
    pageNumbers.innerHTML = '';
    
    // 上一页按钮状态
    prevBtn.disabled = currentPage === 1;
    
    // 下一页按钮状态
    nextBtn.disabled = currentPage === totalPages;
    
    // 生成页码
    for (let i = 1; i <= totalPages; i++) {
        const pageNumber = document.createElement('span');
        pageNumber.className = `page-number ${i === currentPage ? 'active' : ''}`;
        pageNumber.textContent = i;
        pageNumber.addEventListener('click', () => {
            currentPage = i;
            renderNewsList();
            setupPagination();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        pageNumbers.appendChild(pageNumber);
    }
}

// 排序按钮事件
sortButtons.forEach(button => {
    button.addEventListener('click', () => {
        sortButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        currentSort = button.dataset.sort;
        currentPage = 1;
        renderNewsList();
        setupPagination();
    });
});

// 上一页按钮事件
prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderNewsList();
        setupPagination();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// 下一页按钮事件
nextBtn.addEventListener('click', () => {
    const totalPages = Math.ceil(filteredNews.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderNewsList();
        setupPagination();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// 投稿/纠错按钮事件
submitNewsBtn.addEventListener('click', () => {
    submitModal.style.display = 'flex';
});

// 关闭模态框
closeBtn.addEventListener('click', () => {
    submitModal.style.display = 'none';
});

// 点击模态框外部关闭
window.addEventListener('click', (e) => {
    if (e.target === submitModal) {
        submitModal.style.display = 'none';
    }
});

// 表单验证
submitForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // 重置错误消息
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => {
        msg.style.display = 'none';
        msg.textContent = '';
    });
    
    let isValid = true;
    
    // 验证标题
    const title = document.getElementById('title');
    if (!title.value.trim()) {
        showError(title, '标题不能为空');
        isValid = false;
    }
    
    // 验证链接
    const link = document.getElementById('link');
    if (!link.value.trim()) {
        showError(link, '链接不能为空');
        isValid = false;
    } else if (!isValidUrl(link.value)) {
        showError(link, '请输入有效的URL');
        isValid = false;
    }
    
    // 验证来源
    const source = document.getElementById('source');
    if (!source.value.trim()) {
        showError(source, '来源不能为空');
        isValid = false;
    }
    
    // 验证摘要
    const summary = document.getElementById('summary');
    if (!summary.value.trim()) {
        showError(summary, '摘要不能为空');
        isValid = false;
    }
    
    // 验证邮箱
    const email = document.getElementById('email');
    if (!email.value.trim()) {
        showError(email, '邮箱不能为空');
        isValid = false;
    } else if (!isValidEmail(email.value)) {
        showError(email, '请输入有效的邮箱地址');
        isValid = false;
    }
    
    if (isValid) {
        // 模拟表单提交
        setTimeout(() => {
            submitModal.style.display = 'none';
            submitForm.reset();
            
            // 显示成功消息
            successMessage.style.display = 'block';
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 3000);
        }, 500);
    }
});

// 显示错误消息
function showError(input, message) {
    const errorElement = input.nextElementSibling;
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// 验证URL
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

// 验证邮箱
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 返回顶部按钮
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTop.style.display = 'flex';
    } else {
        backToTop.style.display = 'none';
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// 主题切换
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        localStorage.setItem('darkMode', 'disabled');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
});

// 分类筛选
const categoryLinks = document.querySelectorAll('.category-list a');
categoryLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // 更新活动状态
        categoryLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // 筛选新闻
        const category = link.textContent;
        if (category === '全部') {
            filteredNews = [...newsData];
        } else {
            filteredNews = newsData.filter(news => news.category === category);
        }
        
        currentPage = 1;
        renderNewsList();
        setupPagination();
    });
});