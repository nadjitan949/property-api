from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.database import SessionLocal
from app.model.otp import Otp

def clean_expired_otps():
    """
    Tâche planifiée qui supprime physiquement tous les OTP expirés de la BDD.
    """
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        deleted_count = db.query(Otp).filter(Otp.expires_at < now).delete(synchronize_session=False)
        db.commit()
        
        if deleted_count > 0:
            print(f"[CRON] Nettoyage : {deleted_count} OTP expirés supprimés avec succès.")
            
    except Exception as e:
        db.rollback()
        print(f"[CRON] Erreur lors du nettoyage des OTP : {str(e)}")
    finally:
        db.close()

def start_cron_jobs():
    """
    Initialise et démarre le planificateur de tâches en arrière-plan.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_expired_otps, 'interval', hours=1, id='otp_cleaner')
    
    scheduler.start()
    print("[CRON] Le planificateur de tâches est actif (Nettoyage OTP : toutes les heures).")