import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from backend.models import Candidate
from backend.database import get_db, get_active_db_type

logger = logging.getLogger(__name__)
router = APIRouter(tags=["analytics"])

@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    try:
        db_type = get_active_db_type()
        logger.info(f"📊 /dashboard-stats called — active DB: {db_type}")

        # ── Raw SQL count as sanity check ──────────────────────────────────
        try:
            raw_count = db.execute(text("SELECT COUNT(*) FROM hr_candidates")).scalar()
            logger.info(f"✅ Raw SQL COUNT(*) from hr_candidates = {raw_count}")
        except Exception as raw_err:
            logger.error(f"❌ Raw SQL failed: {raw_err}")
            raw_count = 0

        # ── ORM queries ────────────────────────────────────────────────────
        total_candidates = db.query(Candidate).count()
        logger.info(f"📦 ORM total_candidates = {total_candidates}")

        passed_count  = db.query(Candidate).filter(Candidate.status == "Passed").count()
        pending_count = db.query(Candidate).filter(Candidate.status == "Pending").count()
        failed_count  = db.query(Candidate).filter(Candidate.status == "Failed").count()
        logger.info(f"   Passed={passed_count}  Pending={pending_count}  Failed={failed_count}")

        # Today's activity (safely handle if created_at is missing)
        try:
            from datetime import datetime, time as dtime
            today_start = datetime.combine(datetime.now().date(), dtime.min)
            today_evaluated_count = db.query(Candidate).filter(Candidate.created_at >= today_start).count()
        except Exception:
            logger.warning("⚠️ Could not query today_evaluated (missing created_at column?)")
            today_evaluated_count = 0
        logger.info(f"   Today evaluated = {today_evaluated_count}")

        # Top performers (based on total_score)
        top_performers = db.query(Candidate).order_by(Candidate.total_score.desc()).limit(5).all()
        logger.info(f"   Top performers fetched: {len(top_performers)}")

        # Limit to 5000 for dashboard to match user request
        all_candidates = db.query(Candidate).order_by(Candidate.id.desc()).limit(5000).all()
        logger.info(f"   Candidates fetched: {len(all_candidates)}")

        return {
            "stats": {
                "total_candidates": total_candidates,
                "total_interviews": total_candidates,
                "passed": passed_count,
                "pending": pending_count,
                "failed": failed_count,
                "today_evaluated": today_evaluated_count,
                "raw_sql_count": raw_count,  # debug field
            },
            "top_performers": [
                {
                    "id": p.id,
                    "name": p.name,
                    "role": p.role,
                    "total_score": int(p.total_score or 0) if p.total_score else (
                        int(p.written_test or 0) +
                        int(p.technical_assessment or 0) +
                        int(p.pm_assessment or 0) +
                        int(p.hr_evaluation or 0)
                    ),
                    "status": p.status
                } for p in top_performers
            ],
            "all_candidates": [
                {
                    "id": c.id,
                    "name": c.name,
                    "role": c.role,
                    "total_score": int(c.total_score or 0) if c.total_score else (
                        int(c.written_test or 0) +
                        int(c.technical_assessment or 0) +
                        int(c.pm_assessment or 0) +
                        int(c.hr_evaluation or 0)
                    ),
                    "status": c.status,
                    "email": c.email,
                    "created_at": getattr(c, 'created_at', None)
                } for c in all_candidates
            ]
        }
    except Exception as e:
        logger.error(f"❌ Dashboard stats query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Database query failed",
                "message": str(e),
                "hint": "Check /health endpoint for database status.",
            }
        )
