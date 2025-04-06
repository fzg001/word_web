/**
 * 视图控制模块 - 处理卡片紧凑视图切换
 */
(function() {
    // 在DOM加载完成后初始化
    document.addEventListener('DOMContentLoaded', function() {
        initViewControls();
    });

    /**
     * 初始化视图控制
     */
    function initViewControls() {
        console.log('初始化视图控制...');
        
        // 查找视图切换控件
        const viewOptions = document.querySelectorAll('input[name="card-view"]');
        if (!viewOptions || viewOptions.length === 0) {
            console.log('页面中没有找到视图控制元素');
            return;
        }
        
        // 加载已保存的视图设置
        const savedView = localStorage.getItem('wordweb_card_view') || 'default';
        console.log('已保存的视图设置:', savedView);
        
        // 设置单选按钮状态
        viewOptions.forEach(option => {
            if (option.value === savedView) {
                option.checked = true;
            }
            
            // 重新绑定事件监听器
            option.addEventListener('change', function() {
                if (this.checked) {
                    applyCardView(this.value);
                }
            });
        });
        
        // 强制应用当前视图
        applyCardView(savedView);
    }
    
    /**
     * 应用卡片视图
     * @param {string} viewType - 视图类型 ('default' 或 'compact')
     */
    function applyCardView(viewType) {
        console.log('应用视图:', viewType);
        
        if (viewType === 'compact') {
            document.documentElement.classList.add('compact-view');
        } else {
            document.documentElement.classList.remove('compact-view');
        }
        
        // 保存设置到localStorage
        localStorage.setItem('wordweb_card_view', viewType);
        
        // 更新所有卡片元素，确保视图切换生效
        updateCardElements();
    }
    
    /**
     * 更新所有卡片元素
     */
    function updateCardElements() {
        // 重新应用卡片样式
        const isCompact = document.documentElement.classList.contains('compact-view');
        const cards = document.querySelectorAll('.group-card');
        
        cards.forEach(card => {
            // 确保卡片结构符合当前视图模式
            if (isCompact) {
                // 检查是否已有卡片内部元素
                if (!card.querySelector('.card-inner')) {
                    // 创建卡片内部结构
                    createCompactCardStructure(card);
                }
            } else {
                // 如果切换回默认视图，可能需要移除一些紧凑视图特有的元素
                const cardInner = card.querySelector('.card-inner');
                if (cardInner) {
                    // 解构卡片内部元素，恢复默认结构
                    restoreDefaultCardStructure(card, cardInner);
                }
            }
        });
    }
    
    /**
     * 创建紧凑视图的卡片结构
     * @param {Element} card - 卡片元素
     */
    function createCompactCardStructure(card) {
        // 保存原始内容
        const originalContent = card.innerHTML;
        
        // 创建卡片内部结构
        const cardInner = document.createElement('div');
        cardInner.className = 'card-inner';
        
        // 创建卡片正面
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';
        cardFront.innerHTML = originalContent;
        
        // 创建卡片背面
        const cardBack = document.createElement('div');
        cardBack.className = 'card-back';
        
        // 提取链接创建背面按钮
        const links = card.querySelectorAll('a.btn');
        links.forEach(link => {
            const btn = document.createElement('a');
            btn.href = link.href;
            btn.className = 'back-btn ' + (link.classList.contains('btn-primary') ? 'study' : 
                           link.classList.contains('btn-success') ? 'order' : 'random');
            btn.textContent = link.textContent.trim();
            cardBack.appendChild(btn);
        });
        
        // 清空卡片
        card.innerHTML = '';
        
        // 添加新结构
        cardInner.appendChild(cardFront);
        cardInner.appendChild(cardBack);
        card.appendChild(cardInner);
    }
    
    /**
     * 恢复默认卡片结构
     * @param {Element} card - 卡片元素
     * @param {Element} cardInner - 卡片内部元素
     */
    function restoreDefaultCardStructure(card, cardInner) {
        // 获取卡片正面内容
        const cardFront = cardInner.querySelector('.card-front');
        if (cardFront) {
            // 恢复原始内容
            card.innerHTML = cardFront.innerHTML;
        }
    }
    
    // 导出公共方法
    window.viewControl = {
        init: initViewControls,
        applyView: applyCardView
    };
})();
