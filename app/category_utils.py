from app.tagging_system import (
    normalize_article_category,
    normalize_tool_category,
    normalize_term_category,
    get_valid_categories_for_articles,
    get_valid_categories_for_tools,
    get_valid_categories_for_cases,
    get_valid_categories_for_terms
)

def filter_items_by_category(items, category, item_type='article'):
    if not category or category == 'all':
        return items
    
    filtered = []
    for item in items:
        item_category = item.get('category', '')
        
        if item_type == 'article':
            normalized = normalize_article_category(item_category)
            target_normalized = normalize_article_category(category)
        elif item_type == 'tool':
            normalized = normalize_tool_category(item_category)
            target_normalized = normalize_tool_category(category)
        elif item_type == 'case':
            normalized = item.get('industry', item_category)
            target_normalized = category
        elif item_type == 'term':
            normalized = normalize_term_category(item_category)
            target_normalized = normalize_term_category(category)
        else:
            normalized = item_category
            target_normalized = category
        
        if normalized == target_normalized or item_category == category:
            filtered.append(item)
    
    return filtered

def get_category_display_name(category, item_type='article'):
    if not category:
        return '全部'
    
    if category == 'all':
        return '全部'
    
    if item_type == 'article':
        normalized = normalize_article_category(category)
        return normalized if normalized else category
    
    if item_type == 'tool':
        normalized = normalize_tool_category(category)
        return normalized if normalized else category
    
    if item_type == 'term':
        normalized = normalize_term_category(category)
        return normalized if normalized else category
    
    return category

def get_all_categories_for_filter(item_type='article'):
    if item_type == 'article':
        return ['all'] + get_valid_categories_for_articles()
    elif item_type == 'tool':
        return ['all'] + get_valid_categories_for_tools()
    elif item_type == 'case':
        return ['all'] + get_valid_categories_for_cases()
    elif item_type == 'term':
        return ['all'] + get_valid_categories_for_terms()
    else:
        return ['all']

