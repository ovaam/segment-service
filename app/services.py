import random
from sqlalchemy.orm import Session
from . import models, schemas

def distribute_segment(db: Session, slug: str, percentage: float):
    # Получаем или создаем сегмент
    segment = db.query(models.Segment).filter(models.Segment.slug == slug).first()
    if not segment:
        segment = models.Segment(slug=slug)
        db.add(segment)
        db.commit()
        db.refresh(segment)
    
    # Получаем ВСЕХ активных пользователей
    all_users = db.query(models.User).filter(models.User.is_active == True).all()
    if not all_users:
        return 0
    
    # Вычисляем сколько нужно добавить
    target_count = int(len(all_users) * percentage / 100)
    current_in_segment = len(segment.users)
    
    # Если уже достаточно пользователей
    if current_in_segment >= target_count:
        return current_in_segment
    
    # Получаем пользователей НЕ в сегменте
    users_not_in_segment = [
        user for user in all_users 
        if segment not in user.segments
    ]
    
    # Выбираем случайных пользователей
    needed = min(target_count - current_in_segment, len(users_not_in_segment))
    selected_users = random.sample(users_not_in_segment, needed)
    
    # Добавляем сегмент пользователям
    for user in selected_users:
        user.segments.append(segment)
    
    db.commit()
    return target_count