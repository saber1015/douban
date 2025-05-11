import logging

from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, Date, DateTime, Text, BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from config import DB_CONFIG

# 创建数据库引擎
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class DatabaseHandler:
    def __init__(self):
        self.session = Session()
        
    def close(self):
        """关闭数据库会话"""
        self.session.close()
        
    def create_tables(self):
        """创建所有数据表"""
        Base.metadata.create_all(engine)
        
    def get_existing_movie_ids(self):
        """获取数据库中已存在的电影ID"""
        try:
            existing_movies = self.session.query(Movie).filter(Movie.deleted_at == None).all()
            return [movie.movie_id for movie in existing_movies]
        except Exception as e:
            logging.error(f"获取已有电影ID失败: {e}")
            return []

# 定义电影表
class Movie(Base):
    __tablename__ = 'movies'
    __table_args__ = {'comment': '豆瓣电影信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='电影自增ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    title = Column(String(255), nullable=False, default='', comment='电影标题')
    release_date = Column(Date, nullable=True, comment='上映日期')
    country = Column(String(255), nullable=False, default='', comment='制片国家/地区')
    language = Column(String(255), nullable=False, default='', comment='语言')
    runtime = Column(BIGINT, nullable=False, default=0, comment='电影时长')
    rating = Column(DECIMAL(3, 1), nullable=False, default=0.00, comment='电影评分')
    rating_count = Column(Integer, nullable=False, default=0, comment='评分人数')
    cover_url = Column(String(255), nullable=False, default='', comment='电影封面URL')
    summary = Column(Text, nullable=True, comment='电影简介')
    url = Column(String(255), nullable=False, default='', comment='电影详情页URL')
    imdb = Column(String(50), nullable=False, default='', comment='IMDb编号')
    aka = Column(String(255), nullable=False, default='', comment='又名')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义导演表
class Director(Base):
    __tablename__ = 'directors'
    __table_args__ = {'comment': '电影导演信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='导演自增ID')
    director_id = Column(Integer, nullable=False, default=0, comment='豆瓣导演ID')
    name = Column(String(255), nullable=False, default='', comment='导演姓名')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义电影与导演关联表
class MovieDirectorRelation(Base):
    __tablename__ = 'movie_director_relation'
    __table_args__ = {'comment': '电影与导演关联表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='关联表自增ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    director_id = Column(Integer, nullable=False, default=0, comment='豆瓣导演ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义编剧表
class Writer(Base):
    __tablename__ = 'writers'
    __table_args__ = {'comment': '电影编剧信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='编剧自增ID')
    writer_id = Column(Integer, nullable=False, default=0, comment='豆瓣编剧ID')
    name = Column(String(255), nullable=False, default='', comment='编剧姓名')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义电影与编剧关联表
class MovieWriterRelation(Base):
    __tablename__ = 'movie_writer_relation'
    __table_args__ = {'comment': '电影与编剧关联表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='关联表自增ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    writer_id = Column(Integer, nullable=False, default=0, comment='豆瓣编剧ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义演员表
class Actor(Base):
    __tablename__ = 'actors'
    __table_args__ = {'comment': '电影演员信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='演员自增ID')
    actor_id = Column(Integer, nullable=False, default=0, comment='豆瓣演员ID')
    name = Column(String(255), nullable=False, default='', comment='演员姓名')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义电影与演员关联表
class MovieActorRelation(Base):
    __tablename__ = 'movie_actor_relation'
    __table_args__ = {'comment': '电影与演员关联表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='关联表自增ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    actor_id = Column(Integer, nullable=False, default=0, comment='豆瓣演员ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义电影类型表
class Genre(Base):
    __tablename__ = 'genres'
    __table_args__ = {'comment': '电影类型信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='电影类型自增ID')
    genre_id = Column(String(50), nullable=False, default='', comment='电影类型ID')
    genre_name = Column(String(255), nullable=False, default='', comment='电影类型名称')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义电影与类型关联表
class MovieGenreRelation(Base):
    __tablename__ = 'movie_genre_relation'
    __table_args__ = {'comment': '电影与类型关联表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='关联表自增ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    genre_id = Column(String(50), nullable=False, default='', comment='电影类型ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

# 定义评论表
class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = {'comment': '电影评论信息表'}
    id = Column(Integer, primary_key=True, autoincrement=True, comment='评论自增ID')
    review_id = Column(String(50), nullable=False, default='', comment='豆瓣评论ID')
    movie_id = Column(Integer, nullable=False, default=0, comment='豆瓣电影ID')
    user_name = Column(String(255), nullable=False, default='', comment='评论用户姓名')
    rating = Column(Integer, nullable=False, default=0, comment='评论评分')
    content = Column(Text, nullable=True, comment='评论内容')
    publish_date = Column(DateTime, nullable=True, comment='评论发布时间')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')
    