# 数据库工具脚本
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

try:
    import pymysql
    from werkzeug.security import generate_password_hash
except ImportError:
    print("需要安装: pip install pymysql werkzeug")
    exit(1)

load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'charset': 'utf8mb4'
}

DB_CONFIG_WITH_DB = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'IA'),
    'charset': 'utf8mb4'
}

def create_database():
    """创建数据库和表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        with open('init_schema.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
            statements = []
            current_statement = []
            delimiter = ';'
            
            for line in sql_content.split('\n'):
                original_line = line
                line = line.strip()
                
                if not line or line.startswith('--'):
                    continue
                
                if line.upper().startswith('DELIMITER'):
                    if '//' in line:
                        delimiter = '//'
                    else:
                        delimiter = ';'
                    continue
                
                current_statement.append(original_line)
                
                if delimiter == '//' and line.endswith('//'):
                    statement = '\n'.join(current_statement).rstrip('//').strip()
                    if statement:
                        statements.append(statement)
                    current_statement = []
                elif delimiter == ';' and line.endswith(';'):
                    statement = '\n'.join(current_statement).rstrip(';').strip()
                    if statement:
                        statements.append(statement)
                    current_statement = []
            
            if current_statement:
                statement = '\n'.join(current_statement).strip()
                if statement:
                    statements.append(statement)
            
            success_count = 0
            error_count = 0
            
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                        success_count += 1
                        if 'CREATE TABLE' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建表: {match.group(1)}")
                        elif 'CREATE INDEX' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+INDEX\s+(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建索引: {match.group(1)}")
                        elif 'CREATE OR REPLACE VIEW' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+OR\s+REPLACE\s+VIEW\s+(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建视图: {match.group(1)}")
                        elif 'CREATE TRIGGER' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+TRIGGER\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建触发器: {match.group(1)}")
                        elif 'CREATE PROCEDURE' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+PROCEDURE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建存储过程: {match.group(1)}")
                        elif 'CREATE FUNCTION' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+FUNCTION\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"创建函数: {match.group(1)}")
                    except Exception as e:
                        error_msg = str(e)
                        if ('already exists' in error_msg.lower() or 
                            'Duplicate' in error_msg or 
                            'Duplicate key name' in error_msg or
                            '1061' in error_msg):
                            success_count += 1
                            continue
                        error_count += 1
                        print(f"执行失败: {statement[:80]}...")
                        print(f"错误: {error_msg}")
            
            print(f"\n共执行 {success_count} 条SQL，失败 {error_count} 条")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("数据库结构创建完成")
        return True
        
    except Exception as e:
        print(f"创建数据库失败: {str(e)}")
        return False

def insert_mock_data():
    """插入初始数据"""
    try:
        connection = pymysql.connect(**DB_CONFIG_WITH_DB)
        cursor = connection.cursor()
        
        print("开始插入数据...")
        
        with open('insert_mock_data.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
            lines = []
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--') and not line.upper().startswith('USE '):
                    lines.append(line)
            
            current_statement = []
            statements = []
            
            for line in lines:
                current_statement.append(line)
                if line.endswith(';'):
                    statement = ' '.join(current_statement).rstrip(';').strip()
                    if statement:
                        statements.append(statement)
                    current_statement = []
            
            if current_statement:
                statement = ' '.join(current_statement).strip()
                if statement:
                    statements.append(statement)
            
            success_count = 0
            error_count = 0
            
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                        success_count += 1
                        if success_count % 5 == 0:
                            print(f"已执行 {success_count} 条SQL...")
                    except Exception as e:
                        error_msg = str(e)
                        if 'Duplicate entry' in error_msg or '1062' in error_msg:
                            success_count += 1
                            continue
                        error_count += 1
                        print(f"执行失败: {statement[:80]}...")
                        print(f"错误: {error_msg}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"\n数据插入完成！成功: {success_count} 条，失败: {error_count} 条")
        return True
        
    except Exception as e:
        print(f"插入数据失败: {str(e)}")
        return False

def create_default_users():
    """创建默认用户（已合并到insert_mock_data.sql中，此函数保留用于兼容）"""
    print("默认用户已在insert_mock_data.sql中定义，无需单独创建")
    return True

def apply_enhancements():
    """应用数据库增强功能"""
    try:
        connection = pymysql.connect(**DB_CONFIG_WITH_DB)
        cursor = connection.cursor()
        
        print("开始应用数据库增强功能...")
        
        with open('database_enhancements.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
            statements = []
            current_statement = []
            in_delimiter_block = False
            
            for line in sql_content.split('\n'):
                line = line.strip()
                
                if not line or line.startswith('--'):
                    continue
                
                if line.upper().startswith('USE '):
                    continue
                
                if line.upper().startswith('DELIMITER'):
                    if '//' in line:
                        in_delimiter_block = True
                        continue
                    elif in_delimiter_block:
                        in_delimiter_block = False
                        if current_statement:
                            statements.append(' '.join(current_statement))
                            current_statement = []
                        continue
                
                current_statement.append(line)
                
                if in_delimiter_block:
                    if line.endswith('//'):
                        statement = ' '.join(current_statement).rstrip('//').strip()
                        if statement:
                            statements.append(statement)
                        current_statement = []
                else:
                    if line.endswith(';'):
                        statement = ' '.join(current_statement).rstrip(';').strip()
                        if statement:
                            statements.append(statement)
                        current_statement = []
            
            if current_statement:
                statement = ' '.join(current_statement).strip()
                if statement:
                    statements.append(statement)
            
            success_count = 0
            error_count = 0
            
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                        success_count += 1
                        if 'CREATE INDEX' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"  [OK] 创建索引: {match.group(1)}")
                        elif 'CREATE OR REPLACE VIEW' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+OR\s+REPLACE\s+VIEW\s+(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"  [OK] 创建视图: {match.group(1)}")
                        elif 'CREATE TRIGGER' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+TRIGGER\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"  [OK] 创建触发器: {match.group(1)}")
                        elif 'CREATE PROCEDURE' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+PROCEDURE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"  [OK] 创建存储过程: {match.group(1)}")
                        elif 'CREATE FUNCTION' in statement.upper():
                            import re
                            match = re.search(r'CREATE\s+FUNCTION\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', statement, re.IGNORECASE)
                            if match:
                                print(f"  [OK] 创建函数: {match.group(1)}")
                    except Exception as e:
                        error_msg = str(e)
                        if ('already exists' in error_msg.lower() or 
                            'Duplicate' in error_msg or 
                            'Duplicate key name' in error_msg or
                            '1061' in error_msg):
                            success_count += 1
                            continue
                        error_count += 1
                        print(f"  [FAIL] 执行失败: {statement[:60]}...")
                        print(f"         错误: {error_msg}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"\n数据库增强功能应用完成！成功: {success_count} 条，失败: {error_count} 条")
        return True
        
    except Exception as e:
        print(f"应用数据库增强功能失败: {str(e)}")
        return False

def generate_insert_sql():
    """生成INSERT SQL语句脚本（从mock_data.py读取数据）"""
    try:
        # 添加项目路径
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.mock_data import (
            MOCK_USERS, MOCK_ARTICLES, MOCK_TOOLS, MOCK_CASES, MOCK_TERMS,
            MOCK_RESOURCES, MOCK_ETHICS_TOPICS, MOCK_FORUM_POSTS, MOCK_LEARNING_PATHS
        )
        
        def escape_sql_string(s):
            """转义SQL字符串"""
            if s is None:
                return 'NULL'
            if isinstance(s, datetime):
                return f"'{s.strftime('%Y-%m-%d %H:%M:%S')}'"
            s = str(s).replace("'", "''").replace("\\", "\\\\")
            return f"'{s}'"
        
        sql_lines = []
        sql_lines.append("-- IA 模拟数据插入脚本")
        sql_lines.append("-- 生成时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql_lines.append("-- 使用数据库")
        sql_lines.append("USE IA;")
        sql_lines.append("")
        
        # 插入用户
        sql_lines.append("-- 插入用户数据")
        sql_lines.append("INSERT INTO users (id, username, email, password_hash, role, created_at, avatar) VALUES")
        user_values = []
        for user in MOCK_USERS:
            created_at = user.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            user_values.append(f"({user['id']}, {escape_sql_string(user['username'])}, {escape_sql_string(user['email'])}, {escape_sql_string(user['password'])}, {escape_sql_string(user['role'])}, {escape_sql_string(created_at)}, {escape_sql_string(user.get('avatar'))})")
        sql_lines.append(",\n".join(user_values) + ";")
        sql_lines.append("")
        
        # 插入文章
        sql_lines.append("-- 插入文章数据")
        sql_lines.append("INSERT INTO articles (id, title, content, url, category, cover_image, views, likes, author_id, created_at, updated_at, is_featured) VALUES")
        article_values = []
        for article in MOCK_ARTICLES:
            created_at = article.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            article_values.append(f"({article['id']}, {escape_sql_string(article['title'])}, {escape_sql_string(article['content'])}, {escape_sql_string(article.get('url'))}, {escape_sql_string(article.get('category'))}, {escape_sql_string(article.get('cover_image'))}, {article.get('views', 0)}, {article.get('likes', 0)}, {article.get('author_id')}, {escape_sql_string(created_at)}, {escape_sql_string(created_at)}, {1 if article.get('is_featured') else 0})")
        sql_lines.append(",\n".join(article_values) + ";")
        sql_lines.append("")
        
        # 插入工具
        sql_lines.append("-- 插入工具数据")
        sql_lines.append("INSERT INTO tools (id, name, description, url, category, icon, rating, rating_count, created_at) VALUES")
        tool_values = []
        for tool in MOCK_TOOLS:
            created_at = tool.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            tool_values.append(f"({tool['id']}, {escape_sql_string(tool['name'])}, {escape_sql_string(tool['description'])}, {escape_sql_string(tool.get('url'))}, {escape_sql_string(tool.get('category'))}, {escape_sql_string(tool.get('icon'))}, {tool.get('rating', 0.0)}, {tool.get('rating_count', 0)}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(tool_values) + ";")
        sql_lines.append("")
        
        # 插入案例
        sql_lines.append("-- 插入案例数据")
        sql_lines.append("INSERT INTO cases (id, title, description, industry, image, external_link, tags, created_at) VALUES")
        case_values = []
        for case in MOCK_CASES:
            created_at = case.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            case_values.append(f"({case['id']}, {escape_sql_string(case['title'])}, {escape_sql_string(case['description'])}, {escape_sql_string(case.get('industry'))}, {escape_sql_string(case.get('image'))}, {escape_sql_string(case.get('external_link'))}, {escape_sql_string(case.get('tags'))}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(case_values) + ";")
        sql_lines.append("")
        
        # 插入术语
        sql_lines.append("-- 插入术语数据")
        sql_lines.append("INSERT INTO terms (id, term, definition, category, related_terms, examples, created_at) VALUES")
        term_values = []
        for term in MOCK_TERMS:
            created_at = term.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            term_values.append(f"({term['id']}, {escape_sql_string(term['term'])}, {escape_sql_string(term['definition'])}, {escape_sql_string(term.get('category'))}, {escape_sql_string(term.get('related_terms'))}, {escape_sql_string(term.get('examples'))}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(term_values) + ";")
        sql_lines.append("")
        
        # 插入资源
        sql_lines.append("-- 插入资源数据")
        sql_lines.append("INSERT INTO resources (id, title, author, type, description, cover_image, url, created_at) VALUES")
        resource_values = []
        for resource in MOCK_RESOURCES:
            created_at = resource.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            resource_values.append(f"({resource['id']}, {escape_sql_string(resource['title'])}, {escape_sql_string(resource.get('author'))}, {escape_sql_string(resource.get('type'))}, {escape_sql_string(resource.get('description'))}, {escape_sql_string(resource.get('cover_image'))}, {escape_sql_string(resource.get('url'))}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(resource_values) + ";")
        sql_lines.append("")
        
        # 插入伦理专题
        sql_lines.append("-- 插入伦理专题数据")
        sql_lines.append("INSERT INTO ethics_topics (id, title, slug, description, background, key_issues, expert_views, likes, created_at) VALUES")
        ethics_values = []
        for topic in MOCK_ETHICS_TOPICS:
            created_at = topic.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            ethics_values.append(f"({topic['id']}, {escape_sql_string(topic['title'])}, {escape_sql_string(topic.get('slug'))}, {escape_sql_string(topic.get('description'))}, {escape_sql_string(topic.get('background'))}, {escape_sql_string(topic.get('key_issues'))}, {escape_sql_string(topic.get('expert_views'))}, {topic.get('likes', 0)}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(ethics_values) + ";")
        sql_lines.append("")
        
        # 插入论坛帖子
        sql_lines.append("-- 插入论坛帖子数据")
        sql_lines.append("INSERT INTO forum_posts (id, title, content, user_id, category, views, likes, created_at, updated_at) VALUES")
        post_values = []
        for post in MOCK_FORUM_POSTS:
            created_at = post.get('created_at', datetime.now())
            if isinstance(created_at, str):
                created_at = datetime.now()
            post_values.append(f"({post['id']}, {escape_sql_string(post['title'])}, {escape_sql_string(post['content'])}, {post['user_id']}, {escape_sql_string(post.get('category'))}, {post.get('views', 0)}, {post.get('likes', 0)}, {escape_sql_string(created_at)}, {escape_sql_string(created_at)})")
        sql_lines.append(",\n".join(post_values) + ";")
        sql_lines.append("")
        
        # 写入文件
        with open('insert_mock_data.sql', 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_lines))
        
        print("SQL文件生成成功: insert_mock_data.sql")
        print(f"共生成 {len(MOCK_USERS)} 个用户, {len(MOCK_ARTICLES)} 篇文章, {len(MOCK_TOOLS)} 个工具, {len(MOCK_CASES)} 个案例, {len(MOCK_TERMS)} 个术语, {len(MOCK_RESOURCES)} 个资源, {len(MOCK_ETHICS_TOPICS)} 个伦理专题, {len(MOCK_FORUM_POSTS)} 个论坛帖子")
        return True
        
    except Exception as e:
        print(f"生成SQL文件失败: {str(e)}")
        return False

def print_step(step_num, total_steps, description):
    """打印步骤信息"""
    print(f"\n{'='*70}")
    print(f"步骤 {step_num}/{total_steps}: {description}")
    print(f"{'='*70}")

def init_system():
    """系统初始化：创建数据库、插入数据并启动服务器"""
    print("\n" + "="*70)
    print("AICove 系统初始化")
    print("="*70)
    
    total_steps = 3
    step = 1
    
    print_step(step, total_steps, "创建数据库结构")
    step += 1
    try:
        if create_database():
            print("✓ 数据库结构创建成功")
        else:
            print("✗ 数据库结构创建失败")
            return False
    except Exception as e:
        print(f"✗ 创建数据库结构时出错: {str(e)}")
        return False
    
    time.sleep(1)
    
    print_step(step, total_steps, "插入初始数据")
    step += 1
    try:
        if insert_mock_data():
            print("✓ 初始数据插入成功")
        else:
            print("✗ 初始数据插入失败")
            return False
    except Exception as e:
        print(f"✗ 插入数据时出错: {str(e)}")
        return False
    
    time.sleep(1)
    
    print_step(step, total_steps, "启动Web服务器")
    print("\n" + "="*70)
    print("系统初始化完成！")
    print("="*70)
    print("\n默认账号信息：")
    print("  超级管理员: superadmin / superadmin123")
    print("  管理员: admin / admin123")
    print("  普通用户: user / user123")
    print("\n正在启动Web服务器...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("="*70 + "\n")
    
    try:
        from app import create_app
        from config import Config
        
        app = create_app(Config)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        return True
    except Exception as e:
        print(f"\n✗ 启动服务器失败: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'create':
            create_database()
        elif cmd == 'insert':
            insert_mock_data()
        elif cmd == 'users':
            create_default_users()
        elif cmd == 'enhance':
            apply_enhancements()
        elif cmd == 'generate-sql':
            generate_insert_sql()
        elif cmd == 'init':
            try:
                success = init_system()
                sys.exit(0 if success else 1)
            except KeyboardInterrupt:
                print("\n\n初始化已取消")
                sys.exit(1)
        else:
            print("用法: python db_utils.py [create|insert|users|enhance|generate-sql|init]")
            print("  create      - 创建数据库结构")
            print("  insert      - 插入初始数据")
            print("  users       - 创建默认用户（已废弃）")
            print("  enhance     - 应用数据库增强功能（已废弃）")
            print("  generate-sql - 从mock_data.py生成insert_mock_data.sql")
            print("  init        - 一键初始化系统（创建数据库、插入数据、启动服务器）")
    else:
        print("用法: python db_utils.py [create|insert|users|enhance|generate-sql|init]")
        print("  create      - 创建数据库结构")
        print("  insert      - 插入初始数据")
        print("  users       - 创建默认用户（已废弃）")
        print("  enhance     - 应用数据库增强功能（已废弃）")
        print("  generate-sql - 从mock_data.py生成insert_mock_data.sql")
        print("  init        - 一键初始化系统（创建数据库、插入数据、启动服务器）")

