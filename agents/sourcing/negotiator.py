from typing import Dict, Any, List
from agents.llm_router import get_model_for_task
from agents.db import get_db
import json
import asyncio

class NegotiationAgent:
    def __init__(self, tenant_id: str, supplier_id: str, supplier_email: str, target_price: float):
        self.tenant_id = tenant_id
        self.supplier_id = supplier_id
        self.supplier_email = supplier_email
        self.target_price = target_price

    async def generate_opening_email(self) -> Dict[str, str]:
        subject = f"Inquiry: Partnership & Pricing for Office Chairs"
        body = (
            f"Dear Supplier Team,\n\n"
            f"We've reviewed your products and are interested in a long-term partnership. "
            f"Given our projected volume, we are looking for a unit price around ₹{self.target_price}. "
            f"Could you please let us know if this is something we can work towards?\n\n"
            f"Best regards,\nProcurement Team | WeaveOS"
        )
        return {"subject": subject, "body": body}

    async def persist_negotiation(self, subject: str, body: str):
        db = await get_db()
        history = [{"role": "agent", "type": "email", "subject": subject, "content": body}]
        
        negotiation = await db.negotiation.create(
            data={
                "supplierId": self.supplier_id,
                "status": "AWAITING_REPLY",
                "history": json.dumps(history)
            }
        )
        
        await db.supplier.update(
            where={"id": self.supplier_id},
            data={"status": "NEGOTIATING"}
        )
        
        return negotiation.id
