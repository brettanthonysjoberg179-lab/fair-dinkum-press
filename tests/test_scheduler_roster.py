import pytest
from datetime import datetime
from scripts.autonomous.scheduler_roster import AutonomousEnterpriseOrchestrator

def test_june_first_reset_check():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True)
    # Test June 1 trigger logic
    june_1 = datetime(2027, 6, 1, 0, 0, 0)
    assert orch.is_annual_kickoff(june_1) is True
    
    other_date = datetime(2027, 10, 19, 0, 0, 0)
    assert orch.is_annual_kickoff(other_date) is False

def test_orchestrator_initialization():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True, db_path="data/test_business.db")
    assert orch.dry_run is True
    assert orch.publishing_engine is not None
    assert orch.lead_triage is not None
    assert orch.gmail_gateway is not None
    assert orch.saas_ops is not None

def test_hourly_tasks():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True, db_path="data/test_business.db")
    result = orch.run_hourly_tasks()
    assert result["status"] in ["healthy", "degraded", "success"]

def test_daily_tasks():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True, db_path="data/test_business.db")
    result = orch.run_daily_tasks()
    assert result["status"] == "success"

def test_annual_reset_protocol():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True, db_path="data/test_business.db")
    result = orch.run_annual_reset()
    assert result["status"] == "annual_reset_completed"
