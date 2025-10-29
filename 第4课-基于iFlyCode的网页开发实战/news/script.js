// script.js
document.addEventListener('DOMContentLoaded', () => {
    // 热榜数据
    const newsData = [
        {
            rank: 1,
            title: '神舟十八号成功发射',
            source: '央视新闻',
            hot: 9527000,
            time: '2024-03-20 09:00',
            summary: '我国载人航天工程取得重大进展...',
            thumb: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
        },
        // 更多数据...
    ];

    // 初始化渲染
    function renderList(data) {
        const container = document.getElementById('hotList');
        container.innerHTML = data.map(item => `
            <div class="hot-item">
                <div class="rank">${item.rank <= 3 ? '🔥' : item.rank}</div>
                <div class="content">
                    <h3>${item.title}</h3>
                    <div class="meta">
                        <span>${item.source}</span>
                        <span>${new Date(item.time).toLocaleTimeString()}</span>
                    </div>
                    <p>${item.summary}</p>
                </div>
                <div class="hot-value">${(item.hot/10000).toFixed(1)}万</div>
            </div>
        `).join('');
    }

    // 主题切换
    document.querySelector('.theme-toggle').addEventListener('click', () => {
        document.documentElement.setAttribute('data-theme',
            document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'
        );
    });

    // 表单验证
    document.getElementById('submitForm').addEventListener('submit', e => {
        e.preventDefault();
        // 验证逻辑...
    });
});