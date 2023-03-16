class Config:
    __username: str = "dvhplhgj"
    __password: str = "U816tz85GqSFz0kM98S-S3x2SjAV6Xl_"
    __host: str = "hansken.db.elephantsql.com"
    __database: str = "dvhplhgj"
    __port: int = 5432

    link = f"postgresql://{__username}:{__password}@{__host}:{__port}/{__database}"
