// 首次登录指引功能
(function() {
    'use strict';
    
    // 页面指引配置
    const pageGuides = {
        'index': {
            title: '欢迎来到 AICove！',
            content: '这是首页，您可以在这里查看最新资讯、热门大模型和社区动态。点击新手指引中的模块可以快速跳转到对应功能。',
            highlight: '.homepage-layout'
        },
        'ai_basics': {
            title: 'AI 基础模块',
            content: '这里包含核心概念、AI发展史和学习路径。核心概念展示8个重要AI术语，AI发展史可以左右滑动查看历史事件，学习路径提供不同角色的学习方案。',
            highlight: '.tab-buttons'
        },
        'ai_lab': {
            title: 'AI 实验室',
            content: 'AI游乐场提供图像生成、写作、翻译、编程等多种工具。模型透视可以可视化查看神经网络工作机制和词向量空间。',
            highlight: '.lab-tabs'
        },
        'applications': {
            title: '应用场景',
            content: '案例库展示不同行业的AI应用案例，可以通过左侧分类筛选。AI工具箱提供各种实用工具，同样支持分类筛选。',
            highlight: '.applications-tabs'
        },
        'ethics': {
            title: '伦理与未来',
            content: '这里讨论AI相关的伦理话题，包括AI安全、偏见与公平、就业影响、隐私保护等。您可以参与讨论、发表评论和点赞。',
            highlight: '.content-layout'
        },
        'resources': {
            title: '资源中心',
            content: 'AI术语表提供大量AI相关术语，可以通过26个字母快速筛选。推荐阅读包含书籍、论文、期刊、课程等学习资源。',
            highlight: '.resources-tabs'
        },
        'community': {
            title: '社区',
            content: '问答论坛可以查看和发布帖子，AI助教可以回答您的AI学习问题。您还可以查看收藏、消息等功能。',
            highlight: '.forum-layout'
        }
    };
    
    // 检查是否首次登录
    function checkFirstLogin() {
        if (!window.currentUser || !window.currentUser.is_authenticated) {
            return false;
        }
        
        // 从localStorage检查是否已经显示过指引
        const guideShown = localStorage.getItem('user_guide_shown');
        if (guideShown === 'true') {
            return false;
        }
        
        // 检查API
        fetch('/api/auth/check-first-login')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.first_login) {
                    showPageGuide();
                }
            })
            .catch(error => {
                console.error('检查首次登录失败:', error);
            });
        
        return true;
    }
    
    // 显示页面指引
    function showPageGuide() {
        const currentPath = window.location.pathname;
        let pageKey = 'index';
        
        // 根据路径确定页面
        if (currentPath.includes('/ai-basics')) pageKey = 'ai_basics';
        else if (currentPath.includes('/ai-lab')) pageKey = 'ai_lab';
        else if (currentPath.includes('/applications')) pageKey = 'applications';
        else if (currentPath.includes('/ethics')) pageKey = 'ethics';
        else if (currentPath.includes('/resources')) pageKey = 'resources';
        else if (currentPath.includes('/community')) pageKey = 'community';
        
        const guide = pageGuides[pageKey] || pageGuides['index'];
        
        // 创建指引遮罩层
        const overlay = document.createElement('div');
        overlay.className = 'user-guide-overlay';
        overlay.innerHTML = `
            <div class="user-guide-modal">
                <div class="user-guide-header">
                    <h3>${guide.title}</h3>
                    <button class="user-guide-close" onclick="closeUserGuide()">×</button>
                </div>
                <div class="user-guide-content">
                    <p>${guide.content}</p>
                </div>
                <div class="user-guide-footer">
                    <button class="btn btn-primary" onclick="closeUserGuide(true)">我知道了</button>
                    <button class="btn btn-outline" onclick="closeUserGuide(false)">不再提示</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // 高亮相关区域
        if (guide.highlight) {
            const highlightEl = document.querySelector(guide.highlight);
            if (highlightEl) {
                highlightEl.style.position = 'relative';
                highlightEl.style.zIndex = '1001';
                highlightEl.classList.add('guide-highlight');
            }
        }
    }
    
    // 关闭指引
    window.closeUserGuide = function(dontShowAgain) {
        const overlay = document.querySelector('.user-guide-overlay');
        if (overlay) {
            overlay.remove();
        }
        
        // 移除高亮
        const highlightEl = document.querySelector('.guide-highlight');
        if (highlightEl) {
            highlightEl.classList.remove('guide-highlight');
            highlightEl.style.position = '';
            highlightEl.style.zIndex = '';
        }
        
        // 如果选择不再提示，保存到localStorage
        if (dontShowAgain === false) {
            localStorage.setItem('user_guide_shown', 'true');
        }
    };
    
    // 页面加载完成后检查
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', checkFirstLogin);
    } else {
        checkFirstLogin();
    }
})();

