"""AuditCal starter: conservative checks for structured statistical claims."""
from .core import audit, AuditResult, SUPPORTED, FLAGGED, ABSTAIN
__all__ = ["audit", "AuditResult", "SUPPORTED", "FLAGGED", "ABSTAIN"]
