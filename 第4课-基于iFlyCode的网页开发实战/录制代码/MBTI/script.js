// 题库数据 [共20题]
const questions = [
    {
        question: "你更愿意参加社交聚会还是独自阅读？",
        optionA: { text: "参加聚会（E）", value: "E" },
        optionB: { text: "独自阅读（I）", value: "I" }
    },
    {
        question: "做决定时你更依赖事实数据还是个人价值观？",
        optionA: { text: "事实数据（T）", value: "T" },
        optionB: { text: "个人价值观（F）", value: "F" }
    },
    {
        question: "你更喜欢计划好的行程还是随性的安排？",
        optionA: { text: "详细计划（J）", value: "J" },
        optionB: { text: "灵活随意（P）", value: "P" }
    },
    {
        question: "面对新环境时你通常感到兴奋还是焦虑？",
        optionA: { text: "兴奋尝试（E）", value: "E" },
        optionB: { text: "谨慎观察（I）", value: "I" }
    },
    {
        question: "解决问题时你更倾向于逻辑分析还是共情理解？",
        optionA: { text: "逻辑分析（T）", value: "T" },
        optionB: { text: "共情理解（F）", value: "F" }
    },
    {
        question: "你更喜欢有规律的生活节奏还是自由支配时间？",
        optionA: { text: "规律作息（J）", value: "J" },
        optionB: { text: "自由安排（P）", value: "P" }
    },
    {
        question: "接收信息时你更关注细节事实还是整体概念？",
        optionA: { text: "细节事实（S）", value: "S" },
        optionB: { text: "整体概念（N）", value: "N" }
    },
    {
        question: "团队合作中你更擅长组织协调还是创意启发？",
        optionA: { text: "组织协调（J）", value: "J" },
        optionB: { text: "创意启发（P）", value: "P" }
    },
    {
        question: "压力大时你倾向于立即行动还是冷静思考？",
        optionA: { text: "立即行动（T）", value: "T" },
        optionB: { text: "冷静思考（F）", value: "F" }
    },
    {
        question: "学习新事物时你喜欢系统化教学还是自主探索？",
        optionA: { text: "系统教学（J）", value: "J" },
        optionB: { text: "自主探索（P）", value: "P" }
    },
    {
        question: "空闲时间你更喜欢户外活动还是室内创作？",
        optionA: { text: "户外活动（E）", value: "E" },
        optionB: { text: "室内创作（I）", value: "I" }
    },
    {
        question: "评价他人时你更看重实际成就还是潜在潜力？",
        optionA: { text: "实际成就（T）", value: "T" },
        optionB: { text: "潜在潜力（F）", value: "F" }
    },
    {
        question: "日常沟通中你更喜欢直截了当还是委婉含蓄？",
        optionA: { text: "直截了当（T）", value: "T" },
        optionB: { text: "委婉含蓄（F）", value: "F" }
    },
    {
        question: "面对冲突你倾向于主动解决还是回避等待？",
        optionA: { text: "主动解决（E）", value: "E" },
        optionB: { text: "回避等待（I）", value: "I" }
    },
    {
        question: "完成任务时你更注重效率还是完美质量？",
        optionA: { text: "高效完成（J）", value: "J" },
        optionB: { text: "追求完美（P）", value: "P" }
    },
    {
        question: "记忆信息时你更容易记住数字列表还是故事画面？",
        optionA: { text: "数字列表（S）", value: "S" },
        optionB: { text: "故事画面（N）", value: "N" }
    },
    {
        question: "制定目标时你更倾向短期可实现还是长期理想化？",
        optionA: { text: "短期目标（J）", value: "J" },
        optionB: { text: "长期理想（P）", value: "P" }
    },
    {
        question: "表达情感时你更喜欢言语交流还是肢体语言？",
        optionA: { text: "言语交流（T）", value: "T" },
        optionB: { text: "肢体语言（F）", value: "F" }
    },
    {
        question: "选择工作环境时你更喜欢结构化团队还是自由职业？",
        optionA: { text: "结构化团队（J）", value: "J" },
        optionB: { text: "自由职业（P）", value: "P" }
    },
    {
        question: "面对未知领域你更愿意提前准备还是即兴发挥？",
        optionA: { text: "提前准备（J）", value: "J" },
        optionB: { text: "即兴发挥（P）", value: "P" }
    }
];

// 初始化变量
let currentQuestion = 0;
let scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
let userAnswers = new Array(questions.length).fill(null);

// DOM元素
const questionText = document.getElementById('question-text');
const optionButtons = document.querySelectorAll('.option-btn');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress-bar');
const resultArea = document.getElementById('result-area');
const mbtiType = document.getElementById('mbti-type');
const personalityChartCtx = document.getElementById('personality-chart').getContext('2d');
const personalityDescription = document.getElementById('personality-description');

// 初始化进度条
updateProgressBar();

// 显示当前题目
function displayQuestion() {
    const q = questions[currentQuestion];
    questionText.textContent = q.question;
    optionButtons[0].textContent = q.optionA.text;
    optionButtons[1].textContent = q.optionB.text;
    
    // 恢复按钮状态
    optionButtons.forEach(btn => btn.disabled = false);
    
    // 如果是已回答过的题目，高亮显示原答案
    if (userAnswers[currentQuestion]) {
        const selectedOption = userAnswers[currentQuestion];
        optionButtons[selectedOption === 'A' ? 0 : 1].classList.add('selected');
    }
}

// 选择选项
function selectOption(option) {
    const q = questions[currentQuestion];
    const selectedValue = option === 'A' ? q.optionA.value : q.optionB.value;
    
    // 更新分数
    scores[selectedValue]++;
    userAnswers[currentQuestion] = option;
    
    // 高亮选中按钮
    optionButtons.forEach(btn => btn.classList.remove('selected'));
    optionButtons[option === 'A' ? 0 : 1].classList.add('selected');
    
    // 自动跳转到下一题（如果是最后一题则显示结果）
    setTimeout(() => {
        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            updateProgressBar();
            displayQuestion();
        } else {
            showResults();
        }
    }, 500);
}

// 上一题
function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        updateProgressBar();
        displayQuestion();
    }
}

// 下一题
function nextQuestion() {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        updateProgressBar();
        displayQuestion();
    }
}

// 更新进度条
function updateProgressBar() {
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    progressBar.style.width = `${progress}%`;
    prevBtn.disabled = currentQuestion === 0;
    nextBtn.disabled = currentQuestion === questions.length - 1;
}

// 显示结果
function showResults() {
    // 计算MBTI类型
    const eiScore = scores['E'] + scores['I'];
    const snScore = scores['S'] + scores['N'];
    const tfScore = scores['T'] + scores['F'];
    const jpScore = scores['J'] + scores['P'];
    
    const eiPreferred = scores['E'] > scores['I'] ? 'E' : 'I';
    const snPreferred = scores['S'] > scores['N'] ? 'S' : 'N';
    const tfPreferred = scores['T'] > scores['F'] ? 'T' : 'F';
    const jpPreferred = scores['J'] > scores['P'] ? 'J' : 'P';
    
    const mbtiCode = eiPreferred + snPreferred + tfPreferred + jpPreferred;
    
    // 显示结果
    mbtiType.textContent = mbtiCode;
    
    // 创建图表数据
    const chartData = {
        labels: ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P'],
        datasets: [{
            label: '性格维度得分',
            data: [
                scores['E'], scores['I'], 
                scores['S'], scores['N'], 
                scores['T'], scores['F'], 
                scores['J'], scores['P']
            ],
            backgroundColor: [
                'rgba(231, 76, 60, 0.7)', // E
                'rgba(52, 152, 219, 0.7)', // I
                'rgba(46, 204, 113, 0.7)', // S
                'rgba(155, 89, 182, 0.7)', // N
                'rgba(241, 196, 15, 0.7)', // T
                'rgba(230, 126, 34, 0.7)', // F
                'rgba(41, 128, 185, 0.7)', // J
                'rgba(142, 68, 173, 0.7)'  // P
            ],
            borderWidth: 1
        }]
    };
    
    // 销毁旧图表并创建新图表
    const myChart = new Chart(personalityChartCtx, {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
    
    // 生成性格描述
    const descriptions = {
        'ISTJ': '您是务实可靠的守护者型人格，重视传统和秩序，擅长组织和管理。',
        'ISFJ': '您是温暖体贴的保护者型人格，忠诚友善，注重细节和服务他人。',
        'INFJ': '您是富有洞察力的理想主义者，追求精神深度和人类福祉。',
        'INFP': '您是充满创造力的梦想家，重视个人价值观和内心和谐。',
        'ISTP': '您是灵活独立的手艺人型人格，擅长实际操作和技术解决方案。',
        'ISFP': '您是敏感的艺术型人格，重视美感和个人表达的自由。',
        'INTJ': '您是战略思维的策略家型人格，具有长远眼光和独立思考能力。',
        'INTP': '您是创新思维的思考者型人格，热爱理论分析和知识探索。',
        'ESTP': '您是精力充沛的实践者型人格，善于应变和即时决策。',
        'ESFP': '您是热情洋溢的表演者型人格，喜欢与人互动和享受当下。',
        'ENFP': '您是富有感染力的组织者型人格，擅长激励他人和创造可能性。',
        'ENTP': '您是机智多变的创新者型人格，喜欢挑战常规和头脑风暴。',
        'ESTJ': '您是果断高效的执行者型人格，擅长领导和建立结构化体系。',
        'ESFJ': '您是热心肠的组织者型人格，重视人际关系和社会和谐。',
        'ENFJ': '您是鼓舞人心的导师型人格，擅长培养人才和实现共同愿景。',
        'ENTJ': '您是远见卓识的领导者型人格，具备强大的战略规划和执行力。'
    };
    
    personalityDescription.textContent = descriptions[mbtiCode] || `您的MBTI类型为 ${mbtiCode}，这是一种独特的性格组合。`;
    
    // 切换到结果页面
    document.getElementById('question-area').classList.add('hidden');
    document.querySelector('.navigation').classList.add('hidden');
    resultArea.classList.remove('hidden');
}

// 重新开始测试
function restartQuiz() {
    currentQuestion = 0;
    scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
    userAnswers = new Array(questions.length).fill(null);
    
    resultArea.classList.add('hidden');
    document.getElementById('question-area').classList.remove('hidden');
    document.querySelector('.navigation').classList.remove('hidden');
    
    updateProgressBar();
    displayQuestion();
}

// 初始化显示第一题
displayQuestion();