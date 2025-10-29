document.addEventListener('DOMContentLoaded', function() {
    // 模拟数据
    const newsData = [
        {
            id: 1,
            title: '中央经济工作会议在京召开',
            source: '新华社',
            heat: 98,
            time: '202X-XX-XX 09:30',
            summary: '会议总结了今年经济工作，分析了当前经济形势，部署了明年经济工作重点任务...',
            thumb: 'https://via.placeholder.com/400x225?text=经济会议',
            category: 'politics'
        },
        {
            id: 2,
            title: '嫦娥六号探测器成功发射',
            source: '央视新闻',
            heat: 95,
            time: '202X-XX-XX 08:15',
            summary: '我国探月工程再次取得重大进展，嫦娥六号搭载多项科学载荷前往月球背面开展探测...',
            thumb: 'https://via.placeholder.com/400x225?text=嫦娥发射',
            category: 'tech'
        },
        {
            id: 3,
            title: '冬季流感高发期来临',
            source: '健康中国',
            heat: 92,
            time: '202X-XX-XX 14:20',
            summary: '国家卫健委发布最新流感预警，提醒公众做好个人防护，医疗机构加强应对措施...',
            thumb: 'https://via.placeholder.com/400x225?text=流感预防',
            category: 'society'
        },
        {
            id: 4,
            title: '新能源汽车销量创新高',
            source: '中国汽车报',
            heat: 88,
            time: '202X-XX-XX 11:45',
            summary: '乘联会数据显示，本月新能源汽车市场持续火爆，多个品牌单月销量突破历史记录...',
            thumb: 'https://via.placeholder.com/400x225?text=新能源汽车',
            category: 'business'
        },
        {
            id: 5,
            title: '全国多地迎来初雪',
            source: '中国气象局',
            heat: 85,
            time: '202X-XX-XX 07:30',
            summary: '受强冷空气影响，北方大部分地区出现明显降温降雪天气，交通部门启动应急预案...',
            thumb: 'https://via.placeholder.com/400x225?text=初雪美景',
            category: 'society'
        },
        {
            id: 6,
            title: '数字经济助力乡村振兴',
            source: '人民日报',
            heat: 82,
            time: '202X-XX-XX 16:10',
            summary: '各地积极探索数字技术在农业领域的应用，智慧农业平台帮助农民增产增收...',
            thumb: 'https://via.placeholder.com/400x225?text=数字乡村',
            category: 'business'
        },
        {
            id: 7,
            title: '医保药品目录新增67种药品',
            source: '国家医保局',
            heat: 78,
            time: '202X-XX-XX 13:25',
            summary: '新版国家医保药品目录正式公布，更多救命救急的好药纳入医保报销范围...',
            thumb: 'https://via.placeholder.com/400x225?text=医保新政',
            category: 'society'
        },
        {
            id: 8,
            title: '春运火车票明日开售',
            source: '中国铁路',
            heat: 75,
            time: '202X-XX-XX 10:50',
            summary: '202X年春运将于下月启动，铁路部门公布售票时间表和运力安排...',
            thumb: 'https://via.placeholder.com/400x225?text=春运抢票',
            category: 'society'
        },
        {
            id: 9,
            title: '人工智能赋能制造业升级',
            source: '科技日报',
            heat: 70,
            time: '202X-XX-XX 15:40',
            summary: '工信部推动AI技术与实体经济深度融合，一批智能工厂示范项目取得显著成效...',
            thumb: 'https://via.placeholder.com/400x225?text=智能制造',
            category: 'tech'
        },
        {
            id: 10,
            title: '文化遗产保护条例修订草案征求意见',
            source: '文化和旅游部',
            heat: 65,
            time: '202X-XX-XX 17:15',
            summary: '新修订的条例拟加大对历史文化名城名镇名村的保护力度，完善法律责任条款...',
            thumb: 'https://via.placeholder.com/400x225?text=文物保护',
            category: 'culture'
        },
        {
            id: 11,
            title: '职业教育法实施一周年成效显著',
            source: '教育部',
            heat: 62,
            time: '202X-XX-XX 09:05',
            summary: '产教融合深入推进，校企合作模式不断创新，技能人才培养质量持续提升...',
            thumb: 'https://via.placeholder.com/400x225?text=职教发展',
            category: 'education'
        },
        {
            id: 12,
            title: '食品安全抽检合格率达97.6%',
            source: '市场监管总局',
            heat: 58,
            time: '202X-XX-XX 12:30',
            summary: '最新抽检结果显示我国食品安全状况总体向好，但仍存在个别不合格产品...',
            thumb: 'https://via.placeholder.com/400x225?text=食品安全',
            category: 'society'
        }
    ];

    // DOM元素
    const newsList = document.getElementById('newsList');
    const sortBtns = document.querySelectorAll('.sort-btn');
    const prevPageBtn = document.querySelector('.page-btn.prev');
    const nextPageBtn = document.querySelector('.page-btn.next');
    const pageInfo = document.querySelector('.page-info');
    const backToTop = document.querySelector('.back-to-top');
    const themeToggle = document.querySelector('.theme-toggle');
    const modal = document.getElementById('contributionModal');
    const openModalBtn = document.getElementById('openContribution');
    const closeModal = document.querySelector('.close');
    const contributionForm = document.getElementById('contributionForm');
    const urlInput = document.getElementById('url');
    const emailInput = document.getElementById('email');
    const urlError = document.getElementById('urlError');
    const emailError = document.getElementById('emailError');
    const categoryFilter = document.querySelector('.category-filter');
    const sortInfo = document.querySelector('.sort-info');

    // 状态管理
    let currentSort = 'hot';
    let currentPage = 1;
    const itemsPerPage = 8;
    let filteredData = [...newsData];
    let selectedCategory = 'all';

    // 初始化页面
    renderNewsList();
    setupEventListeners();

    // 渲染新闻列表
    function renderNewsList() {
        newsList.innerHTML = '';
        
        // 排序逻辑
        if (currentSort === 'hot') {
            filteredData.sort((a, b) => b.heat - a.heat);
            sortInfo.textContent = '按热度排序 ↓';
        } else {
            filteredData.sort((a, b) => new Date(b.time) - new Date(a.time));
            sortInfo.textContent = '按时间排序 ↓';
        }
        
        // 分页逻辑
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedData = filteredData.slice(startIndex, endIndex);
        
        // 渲染卡片
        paginatedData.forEach((news, index) => {
            const card = document.createElement('article');
            card.className = `news-card rank-${index + 1}`;
            
            // 计算全局排名（考虑分页）
            const globalRank = startIndex + index + 1;
            
            card.innerHTML = `
                <div class="news-rank">${globalRank}</div>
                <div class="news-thumb" style="background-image: url('${news.thumb}')" aria-label="${news.title}缩略图"></div>
                <div class="news-content">
                    <h3 class="news-title">${news.title}</h3>
                    <div class="news-meta">
                        <span class="news-source">${news.source}</span>
                        <span class="news-heat">热度: ${news.heat}</span>
                        <span class="news-time">${news.time}</span>
                    </div>
                    <p class="news-abstract">${news.summary}</p>
                </div>
            `;
            
            newsList.appendChild(card);
        });
        
        // 更新分页信息
        const totalPages = Math.ceil(filteredData.length / itemsPerPage);
        pageInfo.textContent = `第${currentPage}页/共${totalPages}页`;
        
        // 更新分页按钮状态
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }

    // 设置事件监听器
    function setupEventListeners() {
        // 排序按钮
        sortBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                sortBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentSort = btn.dataset.sort;
                currentPage = 1;
                renderNewsList();
            });
        });
        
        // 分页按钮
        prevPageBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                renderNewsList();
            }
        });
        
        nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                renderNewsList();
            }
        });
        
        // 返回顶部
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        // 主题切换
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                themeToggle.textContent = '🌙';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                themeToggle.textContent = '☀️';
            }
        });
        
        // 模态框控制
        openModalBtn.addEventListener('click', () => {
            modal.style.display = 'block';
        });
        
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
        
        // 表单验证
        urlInput.addEventListener('input', validateUrl);
        emailInput.addEventListener('input', validateEmail);
        
        contributionForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            if (validateUrl() && validateEmail()) {
                // 模拟提交成功
                alert('提交成功！感谢您的投稿');
                contributionForm.reset();
                modal.style.display = 'none';
            }
        });
        
        // 分类筛选
        categoryFilter.addEventListener('change', (e) => {
            selectedCategory = e.target.value;
            if (selectedCategory === 'all') {
                filteredData = [...newsData];
            } else {
                filteredData = newsData.filter(news => news.category === selectedCategory);
            }
            currentPage = 1;
            renderNewsList();
        });
    }
    
    // 表单验证函数
    function validateUrl() {
        const isValid = urlInput.checkValidity();
        urlError.style.display = isValid ? 'none' : 'block';
        urlError.textContent = '请输入有效的URL（以http://或https://开头）';
        return isValid;
    }
    
    function validateEmail() {
        const isValid = emailInput.checkValidity();
        emailError.style.display = isValid ? 'none' : 'block';
        emailError.textContent = '请输入有效的邮箱地址';
        return isValid;
    }
});