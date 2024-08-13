from sqlalchemy import text
from sqlalchemy.orm import Session

def select_attempt_fail(db: Session, nik, modified_at):
    query = text("""
        select attempt_fail from otp_list 
        WHERE nik = :nik and modified_at >= :modified_at
    """)
    result = db.execute(query, {
        'nik': nik,
        'modified_at': modified_at
    })
    row = result.fetchone()
    if row:
        return row[0]
    else:
        return None

def select_attempt_generate(db: Session, nik, modified_at):
    query = text("""
        SELECT attempt_generate FROM otp_list
        WHERE nik = :nik AND modified_at >= :modified_at
    """)
    result = db.execute(query, {
        'nik': nik,
        'modified_at': modified_at
    })
    row = result.fetchone()
    if row:
        return row[0]
    else:
        return None

def select_nik_exist(db: Session, nik):
    query = text("""
        SELECT 1 FROM otp_list
        WHERE nik = :nik
    """)
    result = db.execute(query, {
        'nik': nik
    })
    row = result.fetchone()    
    if row:
        return row[0]
    else:
        return None

def select_otp_code(db: Session, nik, key, modified_at):
    query = text("""
        SELECT otp_code FROM otp_list
        WHERE nik = :nik AND key = :key AND modified_at >= :modified_at
    """)
    result = db.execute(query, {
        'nik': nik,
        'key': key,
        'modified_at': modified_at
    })
    row = result.fetchone()    
    if row:
        return row[0]
    else:
        return None

def select_is_used(db: Session, nik):
    query = text("""
        SELECT is_used FROM otp_list
        WHERE nik = :nik
    """)
    result = db.execute(query, {
        'nik': nik
    })
    row = result.fetchone()    
    if row:
        return row[0]
    else:
        return None

def insert_otp(db: Session, nik, key, otp):
    query = text("""
        INSERT INTO otp_list (nik, key, otp_code, attempt_generate, attempt_fail, is_used, created_at, modified_at)
        VALUES (:nik, :key, :otp_code, :attempt_generate, :attempt_fail, FALSE, NOW(), NOW())
    """)
    db.execute(query, {
        'nik': nik,
        'key': key,
        'otp_code': otp,
        'attempt_generate': 1,
        'attempt_fail': 0
    })
    db.commit()

def update_attempt_generate(db: Session, key, otp, attempt_generate, nik):
    query = text("""
        UPDATE otp_list SET key = :key, otp_code = :otp, attempt_generate = :attempt_generate, is_used = FALSE, modified_at = NOW()
        WHERE nik = :nik
    """)
    db.execute(query, {
        'key': key,
        'otp': otp,
        'attempt_generate': attempt_generate,
        'nik': nik
    })
    db.commit()

def update_attempt_fail(db: Session, attempt_fail, nik):
    query = text("""
        UPDATE otp_list SET attempt_fail = :attempt_fail, modified_at = NOW()
        WHERE nik = :nik
    """)
    db.execute(query, {
        'attempt_fail': attempt_fail,
        'nik': nik
    })
    db.commit()

def update_otp_is_used(db: Session, nik):
    query = text("""
        UPDATE otp_list SET is_used = TRUE, modified_at = NOW()
        WHERE nik = :nik
    """)
    db.execute(query, {
        'nik': nik
    })
    db.commit()

def reset_otp(db: Session, key, otp, attempt_generate, nik):
    query = text("""
        UPDATE otp_list SET key = :key, otp_code = :otp, attempt_generate = :attempt_generate, attempt_fail = 0, modified_at = NOW(), is_used = FALSE
        WHERE nik = :nik
    """)
    db.execute(query, {
        'key': key,
        'otp': otp,
        'attempt_generate': attempt_generate,
        'nik': nik
    })
    db.commit()
