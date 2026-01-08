-- IA 数据库初始化脚本
-- 包含数据库创建、表结构、索引、视图、触发器、存储过程、函数等

-- 创建数据库
CREATE DATABASE IF NOT EXISTS IA CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE IA;

-- ============================================
-- 1. 表结构定义
-- ============================================

-- 1. 用户表（主表）
CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID（主键）',
    username VARCHAR(80) NOT NULL UNIQUE COMMENT '用户名（唯一）',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '邮箱（唯一）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    role VARCHAR(20) DEFAULT 'user' COMMENT '角色: user, admin, super_admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    avatar VARCHAR(255) COMMENT '头像路径',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 2. 文章表（依赖用户表）
CREATE TABLE IF NOT EXISTS articles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '文章ID（主键）',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容（简介）',
    url VARCHAR(500) COMMENT '文章URL（实际文章链接）',
    category VARCHAR(50) COMMENT '分类: 热门科普, 最新资讯等',
    cover_image VARCHAR(255) COMMENT '封面图片',
    views INT UNSIGNED DEFAULT 0 COMMENT '浏览量',
    likes INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    author_id INT UNSIGNED COMMENT '作者ID（外键）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_featured BOOLEAN DEFAULT FALSE COMMENT '是否精选',
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_category (category),
    INDEX idx_created_at (created_at),
    INDEX idx_author_id (author_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章表';

-- 3. AI工具表（独立表）
CREATE TABLE IF NOT EXISTS tools (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '工具ID（主键）',
    name VARCHAR(100) NOT NULL COMMENT '工具名称',
    description TEXT COMMENT '描述',
    url VARCHAR(255) COMMENT '工具链接',
    category VARCHAR(50) COMMENT '分类: 图像生成, 写作, 翻译, 编程等',
    icon VARCHAR(255) COMMENT '图标路径',
    rating DECIMAL(3,2) DEFAULT 0.00 COMMENT '评分',
    rating_count INT UNSIGNED DEFAULT 0 COMMENT '评分人数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_category (category),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI工具表';

-- 4. 应用案例表（独立表）
CREATE TABLE IF NOT EXISTS cases (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '案例ID（主键）',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    description TEXT COMMENT '描述',
    industry VARCHAR(50) COMMENT '行业: AI+医疗, AI+教育等',
    image VARCHAR(255) COMMENT '图片路径',
    external_link VARCHAR(255) COMMENT '外部链接',
    tags VARCHAR(200) COMMENT '标签（逗号分隔）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_industry (industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='应用案例表';

-- 5. 论坛帖子表（依赖用户表）
CREATE TABLE IF NOT EXISTS forum_posts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '帖子ID（主键）',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    category VARCHAR(50) COMMENT '分类: 问答, 讨论等',
    views INT UNSIGNED DEFAULT 0 COMMENT '浏览量',
    likes INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论坛帖子表';

-- 6. 评论表（依赖用户表、论坛帖子表、文章表）
CREATE TABLE IF NOT EXISTS comments (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '评论ID（主键）',
    content TEXT NOT NULL COMMENT '评论内容',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    forum_id INT UNSIGNED COMMENT '论坛帖子ID（外键）',
    article_id INT UNSIGNED COMMENT '文章ID（外键）',
    ethics_topic_id INT UNSIGNED COMMENT '伦理专题ID（外键）',
    parent_id INT UNSIGNED COMMENT '父评论ID（外键，用于回复）',
    likes INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (forum_id) REFERENCES forum_posts(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_forum_id (forum_id),
    INDEX idx_article_id (article_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- 7. AI术语表（独立表）
CREATE TABLE IF NOT EXISTS terms (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '术语ID（主键）',
    term VARCHAR(100) NOT NULL COMMENT '术语名称',
    definition TEXT NOT NULL COMMENT '定义',
    category VARCHAR(50) COMMENT '分类: LLM, Transformer, 扩散模型等',
    related_terms VARCHAR(200) COMMENT '相关术语ID（逗号分隔）',
    examples TEXT COMMENT '示例',
    image_path VARCHAR(500) COMMENT '概念图片路径（存储在images/concepts/）',
    video_url VARCHAR(500) COMMENT '视频链接URL（YouTube等）',
    video_title VARCHAR(200) COMMENT '视频标题',
    video_description TEXT COMMENT '视频描述',
    knowledge_graph_json TEXT COMMENT '知识图谱JSON数据',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_term (term),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI术语表';

-- 8. 推荐阅读资源表（独立表）
CREATE TABLE IF NOT EXISTS resources (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '资源ID（主键）',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    author VARCHAR(100) COMMENT '作者',
    type VARCHAR(50) COMMENT '类型: 书籍, 论文, 期刊, 课程',
    description TEXT COMMENT '描述',
    cover_image VARCHAR(255) COMMENT '封面图片',
    url VARCHAR(255) COMMENT '资源链接',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_type (type),
    INDEX idx_title (title(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='推荐阅读资源表';

-- 9. 伦理与未来专题表（独立表）
CREATE TABLE IF NOT EXISTS ethics_topics (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '专题ID（主键）',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    slug VARCHAR(100) NOT NULL UNIQUE COMMENT 'URL标识（唯一）',
    description TEXT COMMENT '描述',
    background TEXT COMMENT '背景介绍',
    key_issues TEXT COMMENT '关键问题',
    expert_views TEXT COMMENT '专家观点摘要',
    likes INT UNSIGNED DEFAULT 0 COMMENT '点赞数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='伦理与未来专题表';

-- 10. 用户反馈表（依赖用户表）
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '反馈ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    type VARCHAR(50) DEFAULT 'general' COMMENT '反馈类型: ai_assistant, general等',
    question VARCHAR(500) COMMENT '问题',
    content TEXT NOT NULL COMMENT '反馈内容',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态: pending, resolved',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户反馈表';

-- 11. 访问统计表（独立表）
CREATE TABLE IF NOT EXISTS visit_stats (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '统计ID（主键）',
    visit_date DATE NOT NULL COMMENT '访问日期',
    visit_count INT UNSIGNED DEFAULT 0 COMMENT '访问次数',
    UNIQUE KEY uk_visit_date (visit_date),
    INDEX idx_visit_date (visit_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='访问统计表';

-- 12. 用户收藏表（依赖用户表，多对多关系）
CREATE TABLE IF NOT EXISTS user_favorites (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '收藏ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    item_type VARCHAR(50) NOT NULL COMMENT '收藏类型: post, article等',
    item_id INT UNSIGNED NOT NULL COMMENT '收藏项ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_user_item (user_id, item_type, item_id),
    INDEX idx_user_id (user_id),
    INDEX idx_item (item_type, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- 13. 用户点赞表（依赖用户表，多对多关系）
CREATE TABLE IF NOT EXISTS user_likes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '点赞ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    item_type VARCHAR(50) NOT NULL COMMENT '点赞类型: post, comment等',
    item_id INT UNSIGNED NOT NULL COMMENT '点赞项ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '点赞时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_user_item (user_id, item_type, item_id),
    INDEX idx_user_id (user_id),
    INDEX idx_item (item_type, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户点赞表';

-- 14. 消息表（依赖用户表，自引用）
CREATE TABLE IF NOT EXISTS messages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '接收用户ID（外键）',
    from_user_id INT UNSIGNED NOT NULL COMMENT '发送用户ID（外键）',
    type VARCHAR(50) NOT NULL COMMENT '消息类型: reply, like, favorite',
    content VARCHAR(500) NOT NULL COMMENT '消息内容',
    related_type VARCHAR(50) COMMENT '关联类型: post, comment等',
    related_id INT UNSIGNED COMMENT '关联ID',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (from_user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- 15. 学习路径表（独立表）
CREATE TABLE IF NOT EXISTS learning_paths (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '路径ID（主键）',
    path_type VARCHAR(50) NOT NULL COMMENT '路径类型: beginner, professional, student',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    description TEXT COMMENT '描述',
    step_order INT UNSIGNED NOT NULL COMMENT '步骤顺序',
    step_title VARCHAR(200) NOT NULL COMMENT '步骤标题',
    step_description TEXT COMMENT '步骤描述',
    step_type VARCHAR(50) COMMENT '步骤类型',
    duration VARCHAR(50) COMMENT '时长',
    difficulty VARCHAR(50) COMMENT '难度',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_path_type (path_type),
    INDEX idx_step_order (path_type, step_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习路径表';

-- 16. 学习资源表（依赖学习路径表）
CREATE TABLE IF NOT EXISTS learning_resources (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '资源ID（主键）',
    learning_path_id INT UNSIGNED NOT NULL COMMENT '学习路径ID（外键）',
    step_order INT UNSIGNED NOT NULL COMMENT '步骤顺序',
    title VARCHAR(200) NOT NULL COMMENT '资源标题',
    url VARCHAR(255) COMMENT '资源链接',
    resource_type VARCHAR(50) COMMENT '资源类型: 文章, 教程, 视频等',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (learning_path_id) REFERENCES learning_paths(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_learning_path_id (learning_path_id),
    INDEX idx_step_order (learning_path_id, step_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习资源表';

-- 17. AI使用历史记录表（依赖用户表）
CREATE TABLE IF NOT EXISTS ai_usage_history (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '历史记录ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    tool_type VARCHAR(50) NOT NULL COMMENT '工具类型: image-gen, writing, translation, programming, ppt',
    input_text TEXT COMMENT '用户输入',
    output_text TEXT COMMENT 'AI输出',
    image_url VARCHAR(500) COMMENT '生成的图片URL（如果是图片生成）',
    file_path VARCHAR(500) COMMENT '生成的文件路径（代码、PPT等）',
    model_used VARCHAR(100) COMMENT '使用的AI模型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_tool_type (tool_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI使用历史记录表';

-- AI对话历史记录表（支持多轮对话）
CREATE TABLE IF NOT EXISTS ai_conversation_history (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '对话历史ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    tool_type VARCHAR(50) NOT NULL COMMENT '工具类型: image-gen, writing, translation, programming, ppt',
    title VARCHAR(200) COMMENT '对话标题（自动生成或用户自定义）',
    conversation_data TEXT NOT NULL COMMENT '对话内容（JSON格式存储）',
    model_used VARCHAR(100) COMMENT '使用的AI模型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_tool_type (tool_type),
    INDEX idx_created_at (created_at),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话历史记录表（支持多轮对话）';

-- 18. 搜索记录表（用于热门搜索词统计）
CREATE TABLE IF NOT EXISTS search_logs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '搜索记录ID（主键）',
    search_query VARCHAR(200) NOT NULL COMMENT '搜索关键词',
    search_type VARCHAR(50) DEFAULT 'general' COMMENT '搜索类型: general, advanced, ai',
    user_id INT UNSIGNED COMMENT '用户ID（外键，可为空，表示未登录用户）',
    result_count INT UNSIGNED DEFAULT 0 COMMENT '搜索结果数量',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '搜索时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_search_query (search_query),
    INDEX idx_created_at (created_at),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='搜索记录表';

-- 19. 用户头像上传记录表（用于文件命名管理）
CREATE TABLE IF NOT EXISTS user_uploads (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '上传记录ID（主键）',
    user_id INT UNSIGNED NOT NULL COMMENT '用户ID（外键）',
    file_type VARCHAR(50) NOT NULL COMMENT '文件类型: avatar, concept_image, article_image等',
    original_filename VARCHAR(255) NOT NULL COMMENT '原始文件名',
    stored_filename VARCHAR(255) NOT NULL COMMENT '存储文件名（带路径）',
    file_size INT UNSIGNED COMMENT '文件大小（字节）',
    mime_type VARCHAR(100) COMMENT 'MIME类型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_file_type (file_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户上传文件记录表';

-- ============================================
-- 2. 索引优化（补充复合索引）
-- ============================================

CREATE INDEX idx_articles_category_created ON articles(category, created_at DESC);
CREATE INDEX idx_articles_featured_views ON articles(is_featured, views DESC);
CREATE INDEX idx_forum_posts_category_created ON forum_posts(category, created_at DESC);
CREATE INDEX idx_forum_posts_likes_views ON forum_posts(likes DESC, views DESC);
CREATE INDEX idx_comments_forum_created ON comments(forum_id, created_at DESC);
CREATE INDEX idx_user_favorites_user_type ON user_favorites(user_id, item_type);
CREATE INDEX idx_user_likes_user_type ON user_likes(user_id, item_type);
CREATE INDEX idx_messages_user_read ON messages(user_id, is_read);
CREATE INDEX idx_search_logs_query_created ON search_logs(search_query, created_at DESC);
CREATE INDEX idx_terms_category_term ON terms(category, term);

-- ============================================
-- 3. 视图（简化常用查询）
-- ============================================

CREATE OR REPLACE VIEW v_hot_articles AS
SELECT 
    id, title, content, category, views, likes, created_at, is_featured
FROM articles
WHERE is_featured = TRUE
ORDER BY views DESC, likes DESC
LIMIT 20;

CREATE OR REPLACE VIEW v_latest_articles AS
SELECT 
    id, title, content, category, views, likes, created_at
FROM articles
ORDER BY created_at DESC
LIMIT 20;

CREATE OR REPLACE VIEW v_hot_posts AS
SELECT 
    fp.id, fp.title, fp.content, fp.category, fp.views, fp.likes, fp.created_at,
    u.username AS author_name,
    (SELECT COUNT(*) FROM comments WHERE forum_id = fp.id) AS comments_count
FROM forum_posts fp
LEFT JOIN users u ON fp.user_id = u.id
ORDER BY fp.likes DESC, fp.views DESC
LIMIT 20;

CREATE OR REPLACE VIEW v_user_stats AS
SELECT 
    u.id, u.username, u.email, u.role, u.created_at,
    (SELECT COUNT(*) FROM articles WHERE author_id = u.id) AS articles_count,
    (SELECT COUNT(*) FROM forum_posts WHERE user_id = u.id) AS posts_count,
    (SELECT COUNT(*) FROM comments WHERE user_id = u.id) AS comments_count,
    (SELECT COUNT(*) FROM user_favorites WHERE user_id = u.id) AS favorites_count,
    (SELECT COUNT(*) FROM user_likes WHERE user_id = u.id) AS likes_count
FROM users u;

CREATE OR REPLACE VIEW v_term_stats AS
SELECT 
    category,
    COUNT(*) AS term_count,
    COUNT(CASE WHEN image_path IS NOT NULL THEN 1 END) AS with_image_count,
    COUNT(CASE WHEN video_url IS NOT NULL THEN 1 END) AS with_video_count
FROM terms
GROUP BY category;

-- ============================================
-- 4. 触发器（自动维护数据一致性）
-- ============================================

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_delete_article_comments
AFTER DELETE ON articles
FOR EACH ROW
BEGIN
    DELETE FROM comments WHERE article_id = OLD.id;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_delete_forum_comments
AFTER DELETE ON forum_posts
FOR EACH ROW
BEGIN
    DELETE FROM comments WHERE forum_id = OLD.id;
    DELETE FROM user_favorites WHERE item_type = 'post' AND item_id = OLD.id;
    DELETE FROM user_likes WHERE item_type = 'post' AND item_id = OLD.id;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_delete_user_data
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    DELETE FROM user_favorites WHERE user_id = OLD.id;
    DELETE FROM user_likes WHERE user_id = OLD.id;
    DELETE FROM messages WHERE user_id = OLD.id OR from_user_id = OLD.id;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_update_article_views
BEFORE UPDATE ON articles
FOR EACH ROW
BEGIN
    IF NEW.views != OLD.views THEN
        SET NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_update_forum_post_views
BEFORE UPDATE ON forum_posts
FOR EACH ROW
BEGIN
    IF NEW.views != OLD.views THEN
        SET NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_update_post_comments_count
AFTER INSERT ON comments
FOR EACH ROW
BEGIN
    IF NEW.forum_id IS NOT NULL THEN
        UPDATE forum_posts 
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.forum_id;
    END IF;
END//
DELIMITER ;

-- ============================================
-- 5. 存储过程（常用操作封装）
-- ============================================

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_get_user_favorites(IN p_user_id INT UNSIGNED)
BEGIN
    SELECT 
        uf.id, uf.item_type, uf.item_id, uf.created_at,
        CASE 
            WHEN uf.item_type = 'article' THEN (SELECT title FROM articles WHERE id = uf.item_id)
            WHEN uf.item_type = 'post' THEN (SELECT title FROM forum_posts WHERE id = uf.item_id)
            ELSE NULL
        END AS item_title
    FROM user_favorites uf
    WHERE uf.user_id = p_user_id
    ORDER BY uf.created_at DESC;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_get_hot_searches(IN p_days INT, IN p_limit INT)
BEGIN
    SELECT 
        search_query, COUNT(*) AS search_count, MAX(created_at) AS last_search
    FROM search_logs
    WHERE created_at >= DATE_SUB(NOW(), INTERVAL p_days DAY)
    GROUP BY search_query
    ORDER BY search_count DESC, last_search DESC
    LIMIT p_limit;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_increment_article_views(IN p_article_id INT UNSIGNED)
BEGIN
    UPDATE articles 
    SET views = views + 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_article_id;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_increment_post_views(IN p_post_id INT UNSIGNED)
BEGIN
    UPDATE forum_posts 
    SET views = views + 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = p_post_id;
END//
DELIMITER ;

-- ============================================
-- 6. 函数（辅助计算）
-- ============================================

DELIMITER //
CREATE FUNCTION IF NOT EXISTS fn_article_hot_score(p_article_id INT UNSIGNED)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_score INT;
    SELECT (views + likes * 10) INTO v_score
    FROM articles
    WHERE id = p_article_id;
    RETURN IFNULL(v_score, 0);
END//
DELIMITER ;

DELIMITER //
CREATE FUNCTION IF NOT EXISTS fn_post_hot_score(p_post_id INT UNSIGNED)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_score INT;
    SELECT (fp.views + fp.likes * 10 + 
            (SELECT COUNT(*) FROM comments WHERE forum_id = p_post_id) * 5) INTO v_score
    FROM forum_posts fp
    WHERE fp.id = p_post_id;
    RETURN IFNULL(v_score, 0);
END//
DELIMITER ;

