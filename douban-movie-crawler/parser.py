from datetime import datetime
from utils import logger

def parse_movie_info(detail_soup):
    """解析电影详情页信息"""
    try:
        info = {}
        
        # 提取基本信息
        info['title'] = detail_soup.find('span', property='v:itemreviewed').text.strip()
        
        # 提取上映日期
        release_date_element = detail_soup.find('span', property='v:initialReleaseDate')
        if release_date_element:
            release_date_str = release_date_element.get('content', '').split('(')[0]
            try:
                info['release_date'] = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            except ValueError:
                info['release_date'] = None
        else:
            info['release_date'] = None
            
        # 提取其他信息
        info_div = detail_soup.find('div', id='info')
        if info_div:
            info_text = info_div.get_text(strip=True)
            
            # 提取国家、语言、片长等
            info['country'] = _extract_info(info_text, '制片国家/地区:')
            info['language'] = _extract_info(info_text, '语言:')
            info['runtime'] = _extract_runtime(detail_soup)
            info['imdb'] = _extract_info(info_text, 'IMDb:')
            info['aka'] = _extract_info(info_text, '又名:')
            
        # 提取评分和评分人数
        rating_num = detail_soup.find('strong', property='v:average')
        info['rating'] = float(rating_num.text.strip()) if rating_num else 0.0
        
        rating_count = detail_soup.find('span', property='v:votes')
        info['rating_count'] = int(rating_count.text.strip()) if rating_count else 0
        
        # 提取简介
        summary = detail_soup.find('span', property='v:summary')
        info['summary'] = summary.get_text(strip=True) if summary else ''
        
        return info
    except Exception as e:
        logger.error(f"解析电影信息失败: {e}")
        return {}

def parse_directors(detail_soup):
    """解析电影导演信息"""
    directors = []
    try:
        director_elements = detail_soup.select('a[rel="v:directedBy"]')
        for element in director_elements:
            director_id = element['href'].split('/')[-2]
            director_name = element.text
            directors.append({'id': director_id, 'name': director_name})
    except Exception as e:
        logger.error(f"解析导演信息失败: {e}")
    return directors

def parse_writers(detail_soup):
    """解析电影编剧信息"""
    writers = []
    try:
        writer_section = detail_soup.find('span', string='编剧')
        if writer_section:
            writer_elements = writer_section.find_next('span').find_all('a')
            for element in writer_elements:
                writer_id = element['href'].split('/')[-2]
                writer_name = element.text
                writers.append({'id': writer_id, 'name': writer_name})
    except Exception as e:
        logger.error(f"解析编剧信息失败: {e}")
    return writers

def parse_actors(detail_soup):
    """解析电影演员信息"""
    actors = []
    try:
        actor_elements = detail_soup.select('a[rel="v:starring"]')
        for element in actor_elements:
            actor_id = element['href'].split('/')[-2]
            actor_name = element.text
            actors.append({'id': actor_id, 'name': actor_name})
    except Exception as e:
        logger.error(f"解析演员信息失败: {e}")
    return actors

def parse_genres(detail_soup):
    """解析电影类型信息"""
    genres = []
    try:
        genre_elements = detail_soup.select('span[property="v:genre"]')
        for element in genre_elements:
            genre_id = element.text
            genre_name = element.text
            genres.append({'id': genre_id, 'name': genre_name})
    except Exception as e:
        logger.error(f"解析类型信息失败: {e}")
    return genres

def parse_reviews(detail_soup, movie_id):
    """解析电影短评信息"""
    reviews = []
    try:
        review_elements = detail_soup.select('div.comment-item')
        for element in review_elements:
            review_id = element.get('data-cid')
            user_name = element.select_one('span.comment-info a').text
            rating_element = element.select_one('span.comment-info span.rating')
            rating = None
            if rating_element:
                rating_text = rating_element.get('title')
                rating_map = {'力荐': 5, '推荐': 4, '还行': 3, '较差': 2, '很差': 1}
                rating = rating_map.get(rating_text)
            content = element.select_one('span.short').text
            date_str = element.select_one('span.comment-time').get('title').strip()
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            
            reviews.append({
                'review_id': review_id,
                'movie_id': movie_id,
                'user_name': user_name,
                'rating': rating,
                'content': content,
                'publish_date': date
            })
    except Exception as e:
        logger.error(f"解析评论信息失败: {e}")
    return reviews

def _extract_info(text, keyword):
    """辅助函数：从文本中提取指定关键词后内容"""
    if keyword in text:
        start_idx = text.index(keyword) + len(keyword)
        end_idx = text.find('\n', start_idx)
        if end_idx == -1:
            end_idx = len(text)
        return text[start_idx:end_idx].strip()
    return ''

def _extract_runtime(soup):
    """提取电影时长"""
    runtime_span = soup.find('span', property='v:runtime')
    if runtime_span:
        try:
            return int(runtime_span.get('content'))
        except (ValueError, TypeError):
            pass
    return None
    