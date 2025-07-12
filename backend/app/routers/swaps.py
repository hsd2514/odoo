
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/swaps", tags=["Swaps"])

# Example Pydantic models
class SwapRequest(BaseModel):
    offered_skill: str
    wanted_skill: str
    message: Optional[str] = None

class SwapResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    offered_skill: str
    wanted_skill: str
    status: str  # pending, accepted, rejected, completedW
    message: Optional[str] = None

# In-memory store for demo
swaps_db = []

@router.post("/", response_model=SwapResponse)
async def send_swap_request(request: SwapRequest):
    """Send a new swap request."""
    swap = SwapResponse(
        id=len(swaps_db) + 1,
        sender_id=1,  # Example, replace with auth
        receiver_id=2,  # Example, replace with actual user
        offered_skill=request.offered_skill,
        wanted_skill=request.wanted_skill,
        status="pending",
        message=request.message,
    )
    swaps_db.append(swap)
    return swap

@router.get("/incoming", response_model=List[SwapResponse])
async def get_incoming_swaps():
    """Get received swap requests."""
    # Example: filter by receiver_id
    return [s for s in swaps_db if s.receiver_id == 1]

@router.get("/outgoing", response_model=List[SwapResponse])
async def get_outgoing_swaps():
    """Get sent swap requests."""
    # Example: filter by sender_id
    return [s for s in swaps_db if s.sender_id == 1]

@router.put("/{swap_id}", response_model=SwapResponse)
async def update_swap_status(swap_id: int, status: str):
    """Accept, reject, or complete a swap request."""
    for swap in swaps_db:
        if swap.id == swap_id:
            swap.status = status
            return swap
    raise HTTPException(status_code=404, detail="Swap not found")
