// MBTI题库（简化版20题）
const questions = [
    {
        question: "你更喜欢哪种社交方式？",
        optionA: "参加聚会（E）",
        optionB: "独自思考（I）",
        dimension: "EI"
    },
    {
        question: "面对新事物时，你更倾向于？",
        optionA: "尝试新鲜事物（S）",
        optionB: "深入研究细节（N）",
        dimension: "SN"
    },
    {
        question: "做决定时你更依赖？",
        optionA: "逻辑分析（T）",
        optionB: "情感价值（F）",
        dimension: "TF"
    },
    {
        question: "你更喜欢的生活方式是？",
        optionA: "按计划行事（J）",
        optionB: "灵活应变（P）",
        dimension: "JP"
    },
    {
        question: "工作中你更享受？",
        optionA: "团队合作（E）",
        optionB: "独立工作（I）",
        dimension: "EI"
    },
    {
        question: "学习新知识时你倾向于？",
        optionA: "实践操作（S）",
        optionB: "理论学习（N）",
        dimension: "SN"
    },
    {
        question: "解决问题时你优先考虑？",
        optionA: "客观事实（T）",
        optionB: "他人感受（F）",
        dimension: "TF"
    },
    {
        question: "周末安排你更喜欢？",
        optionA: "提前计划好（J）",
        optionB: "随性而为（P）",
        dimension: "JP"
    },
    {
        question: "表达观点时你倾向于？",
        optionA: "直接陈述（E）",
        optionB: "委婉暗示（I）",
        dimension: "EI"
    },
    {
        question: "获取信息的方式你更喜欢？",
        optionA: "观察现实（S）",
        optionB: "想象可能（N）",
        dimension: "SN"
    },
    {
        question: "评价标准你更看重？",
        optionA: "效率质量（T）",
        optionB: "和谐共处（F）",
        dimension: "TF"
    },
    {
        question: "时间管理上你属于？",
        optionA: "严格守时（J）",
        optionB: "弹性时间（P）",
        dimension: "JP"
    },
    {
        question: "压力下你会？",
        optionA: "积极行动（E）",
        optionB: "冷静反思（I）",
        dimension: "EI"
    },
    {
        question: "创意构思时你擅长？",
        optionA: "具体实施（S）",
        optionB: "抽象规划（N）",
        dimension: "SN"
    },
    {
        question: "冲突处理时你倾向？",
        optionA: "理性解决（T）",
        optionB: "调和关系（F）",
        dimension: "TF"
    },
    {
        question: "日常习惯你更接近？",
        optionA: "规律有序（J）",
        optionB: "自由随意（P）",
        dimension: "JP"
    },
    {
        question: "接收信息的主要渠道？",
        optionA: "视觉观察（E）",
        optionB: "内心感受（I）",
        dimension: "EI"
    },
    {
        question: "记忆方式你更有效？",
        optionA: "实际经验（S）",
        optionB: "概念理解（N）",
        dimension: "SN"
    },
    {
        question: "决策速度你表现为？",
        optionA: "快速果断（T）",
        optionB: "谨慎权衡（F）",
        dimension: "TF"
    },
    {
        question: "未来规划你倾向于？",
        optionA: "明确目标（J）",
        optionB: "开放可能性（P）",
        dimension: "JP"
    }
];

// 初始化变量
let currentQuestion = 0;
let answers = new Array(questions.length).fill(null);
let scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
let selectedOption = null;

// DOM元素
const questionText = document.getElementById('question-text');
const optionA = document.getElementById('optionA');
const optionB = document.getElementById('optionB');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress');
const quizContainer = document.getElementById('quiz-container');
const resultContainer = document.getElementById('result-container');
const mbtiType = document.getElementById('mbti-type');
const personalityDesc = document.getElementById('personality-description');
const restartBtn = document.getElementById('restart-btn');

// 加载题目
function loadQuestion() {
    const q = questions[currentQuestion];
    questionText.textContent = q.question;
    optionA.textContent = q.optionA;
    optionB.textContent = q.optionB;
    
    // 重置按钮状态
    optionA.disabled = false;
    optionB.disabled = false;
    
    // 恢复已选答案
    if (answers[currentQuestion] !== null) {
        if (answers[currentQuestion] === 'A') {
            optionA.classList.add('selected');
            optionB.classList.remove('selected');
            updateScore(q.dimension, q.optionA.slice(-2));
        } else {
            optionB.classList.add('selected');
            optionA.classList.remove('selected');
            updateScore(q.dimension, q.optionB.slice(-2));
        }
    }
    
    // 更新进度条
    progressBar.style.width = `${((currentQuestion + 1) / questions.length) * 100}%`;
    
    // 更新导航按钮状态
    prevBtn.disabled = currentQuestion === 0;
    nextBtn.textContent = currentQuestion === questions.length - 1 ? '查看结果' : '下一题';
}

// 更新分数
function updateScore(dimension, letter) {
    scores[letter]++;
}

// 选择答案
function selectAnswer(option) {
    selectedOption = option;
    const q = questions[currentQuestion];
    
    // 更新UI
    optionA.classList.remove('selected');
    optionB.classList.remove('selected');
    
    if (option === 'A') {
        optionA.classList.add('selected');
        updateScore(q.dimension, q.optionA.slice(-2));
        answers[currentQuestion] = 'A';
    } else {
        optionB.classList.add('selected');
        updateScore(q.dimension, q.optionB.slice(-2));
        answers[currentQuestion] = 'B';
    }
    
    // 禁用当前题目的选择
    optionA.disabled = true;
    optionB.disabled = true;
}

// 显示结果
function showResult() {
    // 计算MBTI类型
    const types = [];
    types.push(scores.E > scores.I ? 'E' : 'I');
    types.push(scores.S > scores.N ? 'S' : 'N');
    types.push(scores.T > scores.F ? 'T' : 'F');
    types.push(scores.J > scores.P ? 'J' : 'P');
    const fullType = types.join('');
    
    // 显示类型
    mbtiType.textContent = fullType;
    
    // 生成个性描述
    generatePersonalityDescription(fullType);
    
    // 绘制图表
    drawChart();
    
    // 切换容器显示
    quizContainer.style.display = 'none';
    resultContainer.style.display = 'block';
}

// 生成个性描述
function generatePersonalityDescription(type) {
    const descriptions = {
        'ISTJ': '您是务实可靠的管理者型人格。注重细节、遵守规则，具有出色的组织能力和责任感。适合从事管理、财务、法律等需要严谨态度的工作。',
        'ESTJ': '您是果断高效的领导者型人格。善于制定计划、分配任务，重视传统和秩序。适合担任团队领导、项目经理等角色。',
        'ISFJ': '您是忠诚体贴的保护者型人格。耐心细致、富有同情心，致力于帮助他人。适合从事护理、教育、社会服务等工作。',
        'ESFJ': '您是热情友善的组织者型人格。擅长人际互动、营造和谐氛围，关心他人需求。适合从事销售、公关、人力资源等领域。',
        'INTJ': '您是战略思维的创新者型人格。独立自主、富有远见，善于规划复杂项目。适合从事科研、战略规划、技术开发等智力密集型工作。',
        'ENTJ': '您是天生的领导者型人格。果决自信、目标导向，能够激励团队达成目标。适合创业、高管、咨询等挑战性职位。',
        'INTP': '您是逻辑缜密的思考者型人格。好奇心强、善于分析，追求知识深度。适合从事学术研究、系统开发、数据分析等专业领域。',
        'ENTP': '您是机智灵活的创新者型人格。思维敏捷、喜欢辩论，擅长发现新机会。适合从事市场营销、产品开发、创业等创新领域。',
        'ISFP': '您是艺术气质的创作家型人格。敏感细腻、追求美感，重视个人价值观。适合从事设计、音乐、写作等创意工作。',
        'ESFP': '您是充满活力的表演者型人格。乐观开朗、善于即兴发挥，享受当下生活。适合从事娱乐、演艺、活动策划等外向型职业。',
        'INFP': '您是理想主义的治愈者型人格。富有同理心、追求意义，重视人际关系。适合从事心理咨询、文学创作、公益慈善等工作。',
        'ENFP': '您是热情洋溢的倡导者型人格。充满创意、善于激励他人，关注可能性。适合从事培训、营销、品牌推广等影响力岗位。',
        'ISTP': '您是动手能力强的实践者型人格。务实专注、精于技艺，喜欢解决实际问题。适合从事工程、机械、计算机编程等技术领域。',
        'ESTP': '您是行动迅速的问题解决者型人格。适应力强、善于应对突发状况，享受冒险挑战。适合从事紧急救援、体育竞技、创业等动态领域。',
        'INFJ': '您是富有洞察力的顾问型人格。深刻理解人性、追求精神成长，具有独特视角。适合从事心理咨询、哲学研究、战略规划等深度工作。',
        'ENFJ': '您是富有魅力的教育家型人格。善于沟通、激励他人，关注共同成长。适合从事教学、教练、团队建设等领导力岗位。'
    };
    
    personalityDesc.textContent = descriptions[type] || '暂无详细描述，请参考专业资料了解您的MBTI类型特征。';
}

// 绘制图表
function drawChart() {
    const ctx = document.getElementById('score-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',