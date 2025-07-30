from fpdf import FPDF
from utils.ticket_manager import get_all_tickets
import os
from datetime import datetime, timedelta

def generate_pdf(mode="all"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    now = datetime.now()

    title = "Support Ticket Summary - "
    title += "Last 24h" if mode == "24h" else "Complete History"
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    tickets = get_all_tickets()
    count = 0

    for user_id, ticket in tickets.items():
        created_at = ticket.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        if mode == "24h" and (not created_at or (now - created_at) > timedelta(hours=24)):
            continue

        count += 1
        pdf.multi_cell(0, 10, f"""
User ID: {user_id}
Name: {ticket['user_name']}
Language: {ticket.get('language', 'Unknown')}
Status: {ticket['status']}
Message: {ticket['message']}
Reply: {ticket['reply'] or 'No reply yet'}
Created At: {created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Unknown'}
        """)
        pdf.ln(5)

    if count == 0:
        pdf.cell(0, 10, txt="No tickets found.", ln=True)

    filename = f"ticket_report_{mode}.pdf"
    output_path = os.path.join("reports", filename)
    os.makedirs("reports", exist_ok=True)
    pdf.output(output_path)
    return output_path
