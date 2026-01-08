// 主 JavaScript 文件

// 通用 AJAX 请求函数
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API请求错误:', error);
        return { success: false, message: '网络错误，请稍后重试' };
    }
}

// 显示消息提示
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 2rem;
        background: ${type === 'success' ? '#50C878' : type === 'error' ? '#E74C3C' : '#4A90E2'};
        color: #000000;
        border-radius: 4px;
        z-index: 10000;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        messageDiv.style.transition = 'opacity 0.3s';
        setTimeout(() => messageDiv.remove(), 300);
    }, 3000);
}

// 登录功能
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            
            const result = await apiRequest('/auth/login', 'POST', data);
            if (result.success) {
                showMessage('登录成功', 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage(result.message || '登录失败', 'error');
            }
        });
    }
    
    // 注册功能
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(registerForm);
            
            // 获取选中的兴趣
            const interests = [];
            formData.getAll('interests').forEach(val => interests.push(val));
            
            const data = {
                username: formData.get('username'),
                nickname: formData.get('nickname') || '',
                email: formData.get('email') || '',
                password: formData.get('password'),
                security_question: formData.get('security_question'),
                security_answer: formData.get('security_answer'),
                interests: interests
            };
            
            const result = await apiRequest('/auth/register', 'POST', data);
            if (result.success) {
                showMessage('注册成功', 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                showMessage(result.message || '注册失败', 'error');
            }
        });
    }
});

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 滚动显示动画
function initScrollReveal() {
    const reveals = document.querySelectorAll('.scroll-reveal');
    
    const revealOnScroll = () => {
        reveals.forEach(element => {
            const windowHeight = window.innerHeight;
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('revealed');
            }
        });
    };
    
    window.addEventListener('scroll', debounce(revealOnScroll, 10));
    revealOnScroll(); // 初始检查
}

// 全局回车发送功能：回车发送，Shift+Enter换行
function initEnterToSend() {
    document.addEventListener('keydown', function(event) {
        // 检查是否是文本域
        if (event.target.tagName === 'TEXTAREA') {
            const textarea = event.target;
            
            // 回车键且没有按Shift
            if (event.key === 'Enter' && !event.shiftKey) {
                // 检查是否有特定的处理函数（通过onkeydown属性）
                if (textarea.onkeydown) {
                    return; // 让特定处理函数处理
                }
                
                // 查找最近的表单
                const form = textarea.closest('form');
                if (form) {
                    event.preventDefault();
                    // 触发表单提交
                    const submitEvent = new Event('submit', { cancelable: true, bubbles: true });
                    form.dispatchEvent(submitEvent);
                }
            }
        }
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initEnterToSend(); // 初始化回车发送功能
    
    // 为所有卡片添加淡入动画
    const cards = document.querySelectorAll('.article-card, .case-card, .tool-card, .model-card, .topic-card, .resource-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        if (!card.classList.contains('card-animate')) {
            card.classList.add('card-animate');
        }
    });
    
    // 添加页面淡入效果
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// 切换用户菜单
function toggleUserMenu(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    const dropdown = document.getElementById('userMenuDropdown');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

