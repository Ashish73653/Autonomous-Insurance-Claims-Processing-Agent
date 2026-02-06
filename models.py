from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ClaimData:
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_dates: Optional[str] = None
    date_of_loss: Optional[str] = None
    time_of_loss: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    claimant: Optional[str] = None
    third_parties: Optional[str] = None
    contact_details: Optional[str] = None
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    estimated_damage: Optional[str] = None
    claim_type: Optional[str] = None
    attachments: Optional[str] = None
    initial_estimate: Optional[str] = None
