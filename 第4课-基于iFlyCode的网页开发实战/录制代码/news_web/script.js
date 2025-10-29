// 新闻数据
const newsData = [
    {
        id: 1,
        title: "全国两会开幕，政府工作报告发布",
        source: "新华社",
        hotValue: 9850000,
        time: "2023-03-05 09:30",
        summary: "第十四届全国人民代表大会第一次会议在北京人民大会堂开幕，国务院总理李克强作政府工作报告，回顾过去五年工作并提出今年发展主要预期目标。",
        thumbnail: "https://via.placeholder.com/120x80?text=两会"
    },
    {
        id: 2,
        title: "中国成功发射新一代载人飞船试验船",
        source: "央视新闻",
        hotValue: 8765000,
        time: "2023-03-04 11:20",
        summary: "我国在文昌航天发射场用长征五号B遥二运载火箭成功将新一代载人飞船试验船发射升空，飞船顺利进入预定轨道。",
        thumbnail: "https://via.placeholder.com/120x80?text=航天"
    },
    {
        id: 3,
        title: "全国GDP增长5.2%，经济持续恢复向好",
        source: "人民日报",
        hotValue: 7654000,
        time: "2023-03-03 10:15",
        summary: "国家统计局发布数据显示，2022年我国GDP突破120万亿元，同比增长5.2%，国民经济顶住压力持续恢复，经济总量再上新台阶。",
        thumbnail: "https://via.placeholder.com/120x80?text=经济"
    },
    {
        id: 4,
        title: "教育部发布2023年高考改革方案",
        source: "中国教育报",
        hotValue: 6543000,
        time: "2023-03-02 14:40",
        summary: "教育部召开新闻发布会，介绍2023年高考改革方案，将进一步深化考试内容改革，加强素质教育导向。",
        thumbnail: "https://via.placeholder.com/120x80?text=教育"
    },
    {
        id: 5,
        title: "全国多地调整疫情防控措施",
        source: "健康中国",
        hotValue: 5432000,
        time: "2023-03-01 16:25",
        summary: "根据疫情形势变化，北京、上海、广州等多地调整疫情防控措施，优化核酸检测策略，保障群众正常生产生活秩序。",
        thumbnail: "https://via.placeholder.com/120x80?text=疫情"
    },
    {
        id: 6,
        title: "中国科学家在量子计算领域取得重大突破",
        source: "科技日报",
        hotValue: 4321000,
        time: "2023-02-28 09:50",
        summary: "中国科学技术大学潘建伟团队在国际上首次实现光量子计算优越性，标志着我国在量子计算领域取得重要进展。",
        thumbnail: "https://via.placeholder.com/120x80?text=科技"
    },
    {
        id: 7,
        title: "2023年中央一号文件发布，聚焦乡村振兴",
        source: "农民日报",
        hotValue: 3210000,
        time: "2023-02-27 11:30",
        summary: "2023年中央一号文件《关于做好2023年全面推进乡村振兴重点工作的意见》发布，提出全面推进乡村振兴重点工作。",
        thumbnail: "https://via.placeholder.com/120x80?text=农业"
    },
    {
        id: 8,
        title: "中国女足夺得亚洲杯冠军",
        source: "体育周报",
        hotValue: 2100000,
        time: "2023-02-26 20:15",
        summary: "在印度举行的女足亚洲杯决赛中，中国女足3-2逆转韩国队，时隔16年再次夺得亚洲杯冠军。",
        thumbnail: "https://via.placeholder.com/120x80?text=体育"
    },
    {
        id: 9,
        title: "全国首条跨海高铁福厦高铁开通运营",
        source: "中国铁路",
        hotValue: 1987000,
        time: "2023-02-25 08:00",
        summary: "我国首条跨海高铁——福厦高铁正式开通运营，设计时速350公里，全长277公里，连接福州和厦门两大城市。",
        thumbnail: "https://via.placeholder.com/120x80?text=交通"
    },
    {
        id: 10,
        title: "中国科学家发现新冠治疗新靶点",
        source: "生命科学",
        hotValue: 1876000,
        time: "2023-02-24 15:45",
        summary: "中国科学院团队发现新冠病毒感染人体细胞的新机制，并鉴定出多个潜在药物靶点，为开发新型抗病毒药物提供重要线索。",
        thumbnail: "https://via.placeholder.com/120x80?text=医学"
    },
    {
        id: 11,
        title: "全国多地迎来春季旅游高峰",
        source: "文旅中国",
        hotValue: 1765000,
        time: "2023-02-23 12:30",
        summary: "随着天气转暖，全国多地迎来春季旅游高峰，黄山、西湖、九寨沟等景区游客量明显增加。",
        thumbnail: "https://via.placeholder.com/120x80?text=旅游"
    },
    {
        id: 12,
        title: "中国新能源汽车产销量连续8年全球第一",
        source: "经济日报",
        hotValue: 1654000,
        time: "2023-02-22 10:20",
        summary: "工信部发布数据显示，2022年我国新能源汽车产销量分别完成705.8万辆和688.7万辆，连续8年保持全球第一。",
        thumbnail: "https://via.placeholder.com/120x80?text=汽车"
    }
];

// DOM元素
const newsList = document.getElementById('newsList');
const pagination = document.getElementById('pagination');
const themeToggle = document.getElementById('themeToggle');
const backToTop = document.getElementById('backToTop');
const contributeModal = document.getElementById('contributeModal');
const successModal = document.getElementById('successModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const closeSuccessModalBtn = document.getElementById('closeSuccessModalBtn');
const okSuccessBtn = document.getElementById('okSuccessBtn');
const contributeForm = document.getElementById('contributeForm');
const sortButtons = document.querySelectorAll('.sort-btn');

// 当前页和排序方式
let currentPage = 1;
const itemsPerPage = 8;
let currentSort = 'hot';

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    renderNewsList();
    renderPagination();
    setupEventListeners();
});

// 渲染新闻列表
function renderNewsList() {
    newsList.innerHTML = '';
    
    // 排序新闻
    const sortedNews = [...newsData];
    if (currentSort === 'hot') {
        sortedNews.sort((a, b) => b.hotValue - a.hotValue);
    } else {
        sortedNews.sort((a, b) => new Date(b.time) - new Date(a.time));
    }
    
    // 分页
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedNews = sortedNews.slice(startIndex, startIndex + itemsPerPage);
    
    paginatedNews.forEach((news, index) => {
        const rank = startIndex + index + 1;
        const newsItem = document.createElement('div');
        newsItem.className = 'news-card';
        newsItem.innerHTML = `
            <div class="rank ${rank <= 3 ? 'top3' : ''}">
                ${rank}
                ${rank === 1 ? '🏆' : rank <= 3 ? '🔥' : ''}
            </div>
            <div class="content">
                <div class="header">
                    <h3 class="title">${news.title}</h3>
                    <img src="${news.thumbnail}" alt="${news.title}缩略图" class="thumbnail">
                </div>
                <div class="meta">
                    <span class="source">${news.source}</span>
                    <span class="hot">热度: ${formatNumber(news.hotValue)}</span>
                    <span class="time">${formatDate(news.time)}</span>
                </div>
                <p class="summary">${news.summary}</p>
            </div>
        `;
        newsList.appendChild(newsItem);
    });
}

// 渲染分页
function renderPagination() {
    pagination.innerHTML = '';
    const totalPages = Math.ceil(newsData.length / itemsPerPage);
    
    // 上一页按钮
    const prevButton = document.createElement('button');
    prevButton.textContent = '上一页';
    prevButton.disabled = currentPage === 1;
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderNewsList();
            renderPagination();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
    pagination.appendChild(prevButton);
    
    // 页码按钮
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        if (i === currentPage) {
            pageButton.classList.add('active');
        }
        pageButton.addEventListener('click', () => {
            currentPage = i;
            renderNewsList();
            renderPagination();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        pagination.appendChild(pageButton);
    }
    
    // 下一页按钮
    const nextButton = document.createElement('button');
    nextButton.textContent = '下一页';
    nextButton.disabled = currentPage === totalPages;
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderNewsList();
            renderPagination();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
    pagination.appendChild(nextButton);
}

// 设置事件监听器
function setupEventListeners() {
    // 主题切换
    themeToggle.addEventListener('click', toggleTheme);
    
    // 返回顶部按钮
    window.addEventListener('scroll', toggleBackToTop);
    backToTop.addEventListener('click', scrollToTop);
    
    // 模态框
    openModalBtn.addEventListener('click', openContributeModal);
    closeModalBtn.addEventListener('click', closeContributeModal);
    closeSuccessModalBtn.addEventListener('click', closeSuccessModal);
    okSuccessBtn.addEventListener('click', closeSuccessModal);
    
    // 点击模态框外部关闭
    window.addEventListener('click', function(event) {
        if (event.target === contributeModal) {
            closeContributeModal();
        }
        if (event.target === successModal) {
            closeSuccessModal();
        }
    });
    
    // 表单提交
    contributeForm.addEventListener('submit', handleFormSubmit);
    
    // 排序按钮
    sortButtons.forEach(button => {
        button.addEventListener('click', () => {
            sortButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentSort = button.dataset.sort;
            currentPage = 1;
            renderNewsList();
            renderPagination();
        });
    });
}

// 切换主题
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const icon = themeToggle.querySelector('i');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }
}

// 显示/隐藏返回顶部按钮
function toggleBackToTop() {
    if (window.pageYOffset > 300) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }
}

// 滚动到顶部
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 打开投稿模态框
function openContributeModal() {
    contributeModal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// 关闭投稿模态框
function closeContributeModal() {
    contributeModal.classList.remove('show');
    document.body.style.overflow = '';
}

// 关闭成功模态框
function closeSuccessModal() {
    successModal.classList.remove('show');
    document.body.style.overflow = '';
}

// 处理表单提交
function handleFormSubmit(e) {
    e.preventDefault();
    
    // 重置错误信息
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => {
        msg.style.display = 'none';
    });
    
    // 获取表单数据
    const title = document.getElementById('title').value.trim();
    const url = document.getElementById('url').value.trim();
    const source = document.getElementById('source').value.trim();
    const summary = document.getElementById('summary').value.trim();
    const email = document.getElementById('email').value.trim();
    
    // 验证必填字段
    let isValid = true;
    
    if (!title) {
        document.getElementById('titleError').textContent = '请输入标题';
        document.getElementById('titleError').style.display = 'block';
        isValid = false;
    }
    
    if (!url) {
        document.getElementById('urlError').textContent = '请输入新闻链接';
        document.getElementById('urlError').style.display = 'block';
        isValid = false;
    } else if (!isValidUrl(url)) {
        document.getElementById('urlError').textContent = '请输入有效的URL';
        document.getElementById('urlError').style.display = 'block';
        isValid = false;
    }
    
    if (!source) {
        document.getElementById('sourceError').textContent = '请输入来源';
        document.getElementById('sourceError').style.display = 'block';
        isValid = false;
    }
    
    if (!summary) {
        document.getElementById('summaryError').textContent = '请输入摘要';
        document.getElementById('summaryError').style.display = 'block';
        isValid = false;
    }
    
    if (!email) {
        document.getElementById('emailError').textContent = '请输入邮箱';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    } else if (!isValidEmail(email)) {
        document.getElementById('emailError').textContent = '请输入有效的邮箱地址';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    if (isValid) {
        // 这里可以添加表单提交逻辑，如AJAX请求
        console.log('表单提交:', { title, url, source, summary, email });
        
        // 显示成功模态框
        contributeModal.classList.remove('show');
        successModal.classList.add('show');
        
        // 重置表单
        contributeForm.reset();
    }
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

// 格式化数字
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + '百万';
    } else if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toString();
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
        return `${Math.floor(diffInHours)}小时前`;
    } else {
        return date.toLocaleDateString('zh-CN');
    }
}