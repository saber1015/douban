from database import DatabaseHandler, Movie, Director, MovieDirectorRelation, Writer, MovieWriterRelation, Actor, MovieActorRelation, Genre, MovieGenreRelation, Review
from driver import create_driver
from parser import parse_movie_info, parse_directors, parse_writers, parse_actors, parse_genres, parse_reviews
from utils import random_sleep, logger
from config import CRAWL_CONFIG
from datetime import datetime
import argparse
from bs4 import BeautifulSoup
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='豆瓣电影Top250爬虫')
    parser.add_argument('--pages', type=int, default=None, help='指定要爬取的页数')
    parser.add_argument('--start', type=int, default=0, help='从第几页开始爬取(默认为0)')
    args = parser.parse_args()
    
    # 初始化数据库
    db_handler = DatabaseHandler()
    db_handler.create_tables()
    
    # 获取已有电影ID
    existing_movie_ids = db_handler.get_existing_movie_ids()
    logger.info(f"数据库中已有 {len(existing_movie_ids)} 部电影")
    
    # 创建浏览器驱动
    driver = create_driver()
    
    # 开始爬取
    base_url = CRAWL_CONFIG['base_url']
    current_page = args.start
    total_movies = 0
    failed_movies = []
    
    try:
        while True:
            # 检查是否达到指定页数
            if args.pages is not None and current_page >= args.start + args.pages:
                logger.info(f"已达到指定页数 {args.pages}，爬取结束")
                break
                
            page_url = f"{base_url}?start={current_page*25}"
            logger.info(f"正在爬取第 {current_page+1} 页: {page_url}")
            
            # 请求页面
            driver.get(page_url)
            random_sleep()
            
            # 解析页面
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            movie_items = soup.select('div.item')
            
            if not movie_items:
                logger.info("没有找到更多电影，爬取结束")
                break
                
            # 处理每部电影
            for item in movie_items:
                try:
                    # 提取电影基本信息
                    link = item.find('a')['href']
                    movie_id = int(link.split('/')[-2])
                    
                    # 检查是否已存在
                    if CRAWL_CONFIG['mode'] == 'incremental' and movie_id in existing_movie_ids:
                        logger.info(f"电影 {movie_id} 已存在，跳过")
                        continue
                        
                    # 访问电影详情页
                    logger.info(f"正在爬取电影 {movie_id} 详情: {link}")
                    driver.get(link)
                    random_sleep()
                    
                    # 解析电影详情
                    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    movie_info = parse_movie_info(detail_soup)
                    
                    # 获取封面URL
                    cover_img = detail_soup.select_one('#mainpic img')
                    cover_url = cover_img.get('src') if cover_img else ''
                    
                    # 保存电影信息到数据库
                    save_movie_to_db(db_handler, movie_id, link, movie_info, cover_url)
                    
                    # 保存关联信息
                    save_relations(db_handler, movie_id, detail_soup)
                    
                    total_movies += 1
                    logger.info(f"成功保存电影 {movie_id}: {movie_info.get('title', '未知标题')}")
                    
                except Exception as e:
                    logger.error(f"处理电影 {link} 失败: {e}")
                    failed_movies.append(link)
                    
            # 下一页
            current_page += 1
            
    except Exception as e:
        logger.error(f"爬取过程中发生严重错误: {e}")
    finally:
        # 清理资源
        driver.quit()
        db_handler.close()
        logger.info(f"爬取完成，共新增 {total_movies} 部电影")
        if failed_movies:
            logger.warning(f"共有 {len(failed_movies)} 部电影爬取失败")
            for failed_url in failed_movies:
                logger.warning(f"失败URL: {failed_url}")

def save_movie_to_db(db_handler, movie_id, url, movie_info, cover_url):
    """保存电影信息到数据库"""
    now = datetime.now()
    
    # 创建电影对象
    movie = Movie(
        movie_id=movie_id,
        title=movie_info.get('title', ''),
        release_date=movie_info.get('release_date'),
        country=movie_info.get('country', ''),
        language=movie_info.get('language', ''),
        runtime=movie_info.get('runtime', 0),
        rating=movie_info.get('rating', 0.0),
        rating_count=movie_info.get('rating_count', 0),
        cover_url=cover_url,
        summary=movie_info.get('summary', ''),
        url=url,
        imdb=movie_info.get('imdb', ''),
        aka=movie_info.get('aka', ''),
        created_at=now,
        updated_at=now
    )
    
    # 添加到数据库
    db_handler.session.add(movie)
    
    # 提交事务
    try:
        db_handler.session.commit()
    except Exception as e:
        db_handler.session.rollback()
        logger.error(f"保存电影失败: {e}")
        raise

def save_relations(db_handler, movie_id, detail_soup):
    """保存电影关联信息到数据库"""
    now = datetime.now()
    
    # 保存导演信息
    directors = parse_directors(detail_soup)
    for director in directors:
        # 检查导演是否已存在
        director_obj = db_handler.session.query(Director).filter(
            Director.director_id == director['id']
        ).first()
        
        if not director_obj:
            # 创建新导演
            director_obj = Director(
                director_id=director['id'],
                name=director['name'],
                created_at=now,
                updated_at=now
            )
            db_handler.session.add(director_obj)
            db_handler.session.flush()  # 获取新创建的ID
            
        # 创建电影-导演关联
        relation = MovieDirectorRelation(
            movie_id=movie_id,
            director_id=director_obj.id,
            created_at=now,
            updated_at=now
        )
        db_handler.session.add(relation)
    
    # 保存编剧信息
    writers = parse_writers(detail_soup)
    for writer in writers:
        # 检查编剧是否已存在
        writer_obj = db_handler.session.query(Writer).filter(
            Writer.writer_id == writer['id']
        ).first()
        
        if not writer_obj:
            # 创建新编剧
            writer_obj = Writer(
                writer_id=writer['id'],
                name=writer['name'],
                created_at=now,
                updated_at=now
            )
            db_handler.session.add(writer_obj)
            db_handler.session.flush()  # 获取新创建的ID
            
        # 创建电影-编剧关联
        relation = MovieWriterRelation(
            movie_id=movie_id,
            writer_id=writer_obj.id,
            created_at=now,
            updated_at=now
        )
        db_handler.session.add(relation)
    
    # 保存演员信息
    actors = parse_actors(detail_soup)
    for actor in actors:
        # 检查演员是否已存在
        actor_obj = db_handler.session.query(Actor).filter(
            Actor.actor_id == actor['id']
        ).first()
        
        if not actor_obj:
            # 创建新演员
            actor_obj = Actor(
                actor_id=actor['id'],
                name=actor['name'],
                created_at=now,
                updated_at=now
            )
            db_handler.session.add(actor_obj)
            db_handler.session.flush()  # 获取新创建的ID
            
        # 创建电影-演员关联
        relation = MovieActorRelation(
            movie_id=movie_id,
            actor_id=actor_obj.id,
            created_at=now,
            updated_at=now
        )
        db_handler.session.add(relation)
    
    # 保存类型信息
    genres = parse_genres(detail_soup)
    for genre in genres:
        # 检查类型是否已存在
        genre_obj = db_handler.session.query(Genre).filter(
            Genre.genre_id == genre['id']
        ).first()
        
        if not genre_obj:
            # 创建新类型
            genre_obj = Genre(
                genre_id=genre['id'],
                genre_name=genre['name'],
                created_at=now,
                updated_at=now
            )
            db_handler.session.add(genre_obj)
            db_handler.session.flush()  # 获取新创建的ID
            
        # 创建电影-类型关联
        relation = MovieGenreRelation(
            movie_id=movie_id,
            genre_id=genre_obj.id,
            created_at=now,
            updated_at=now
        )
        db_handler.session.add(relation)
    
    # 保存评论信息
    reviews = parse_reviews(detail_soup, movie_id)
    for review in reviews:
        # 检查评论是否已存在
        review_obj = db_handler.session.query(Review).filter(
            Review.review_id == review['review_id']
        ).first()
        
        if not review_obj:
            # 创建新评论
            review_obj = Review(
                review_id=review['review_id'],
                movie_id=movie_id,
                user_name=review['user_name'],
                rating=review['rating'],
                content=review['content'],
                publish_date=review['publish_date'],
                created_at=now,
                updated_at=now
            )
            db_handler.session.add(review_obj)
    
    # 提交所有关联数据
    try:
        db_handler.session.commit()
    except Exception as e:
        db_handler.session.rollback()
        logger.error(f"保存关联数据失败: {e}")
        raise

if __name__ == "__main__":
    main()
    