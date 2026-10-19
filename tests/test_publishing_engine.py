import pytest
from scripts.autonomous.publishing_engine import PublishingEngine, run_publishing_cycle
from scripts.autonomous.database import init_db

def test_publishing_cycle(tmp_path):
    db_path = tmp_path / "test_business.db"
    conn = init_db(str(db_path))
    engine = PublishingEngine(dry_run=True, db_path=str(db_path))
    result = engine.execute_cycle()
    assert result["status"] == "success"
    assert "article_title" in result
    assert "url" in result

def test_run_publishing_cycle(tmp_path):
    db_path = tmp_path / "test_business.db"
    init_db(str(db_path))
    result = run_publishing_cycle(dry_run=True, db_path=str(db_path))
    assert result["status"] == "success"
    assert "article_title" in result
