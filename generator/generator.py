from db.db import get_db
from sqlalchemy.orm import Session
from db.participant_schema import Participant
from db.participant_model import Participant as ParticipantModel
from logger import logger
from html2image import Html2Image
import qrcode
import base64
from io import BytesIO
from generator.upload_tickets import upload_file
from db.config import SRV_BASE_URL


hti = Html2Image(output_path='tickets', browser_executable='chrome-win/chrome.exe')

qr_content = "https://fossuok.org/events/15"
base_url = "https://mp3domain.sirv.com/summit_25/"

template_1 = """
<body>
    <div class="ticket">
      <div class="qr-section">
        <img src="{qr_code}" alt="QR Code" />
      </div>
      <div class="details-section">
        <div class="event-title">Open Dev Summit <span class="year">'25</span></div>
        <div class="event-name">Workshop 1: Linux Fundamentals</div>
        <div class="event-date">26 APRIL 2025</div>
        <div class="">9 AM</div>

        <div class="participant">{name}</div>
      </div>
      <div class="dev-section">
        <div class="vertical-text">Open Dev Summit '25</div>
        <img src="{foss_logo}" class="foss-logo" alt="Foss Logo" />
      </div>
      <div class="dev-section">
        <div class="faculty">
          Faculty of Computing and Technology<br />University of Kelaniya
        </div>
      </div>
    </div>
  </body>
"""
css_1 = """
body {
  background: radial-gradient(
      circle at top left,
      rgba(114, 22, 55, 0.3) 0%,
      transparent 40%
    ),
    radial-gradient(
      circle at bottom right,
      rgba(114, 22, 55, 0.3) 0%,
      transparent 40%
    ),
    #0c0618;
  background-repeat: no-repeat;
  background-size: cover;
  margin: 0;
  padding: 0;
  font-family: "Montserrat", Arial, sans-serif;
}
.ticket {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  color: #fff;
  width: 800px;
  height: 280px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}
.qr-section {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 260px;
  min-width: 260px;
  border-right: 2px solid #444;
  padding: 0 24px;
}
.qr-section img {
  background: #fff;
  border-radius: 8px;
  width: 230px;
  height: 230px;
  object-fit: contain;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
}
.details-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 32px 32px 32px 32px;
  position: relative;
}
.event-title {
  font-size: 2.2em;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 1px;
  color: #f1f1f1;
  font-family: "Ubuntu", sans-serif;
}
.event-title .year {
  color: #a7c7f9;
  font-size: 1.1em;
  font-weight: 800;
  filter: drop-shadow(1px 1px 3px #232323);
  font-family: "Ubuntu", sans-serif;
}
.event-date {
  font-size: 1.2em;
  margin-bottom: 8px;
  margin-top: 16px;
  letter-spacing: 1px;
  color: #d1d1d1;
}
.event-time {
  font-size: 1.1em;
  margin-bottom: 18px;
  color: #b0b0b0;
}
.participant {
  font-size: 1.3em;
  font-weight: 700;
  margin-top: 18px;
  margin-bottom: 10px;
  color: #fff;
}
.dev-section {
  border-left: 2px solid #444;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  min-width: 80px;
  position: relative;
}
.foss-logo {
  width: 60px;
  height: 90px;
  background: transparent;
  margin-bottom: 10px;
  margin-top: 10px;
  object-fit: contain;
}
.summit-logo{
width: 260px;
height: 200px;
background: transparent;
margin-bottom: 14px;
margin-top: 10px;
object-fit: contain;
}
.vertical-text {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  font-size: 1em;
  color: #eee;
  font-weight: 500;
  letter-spacing: 2px;
  margin-top: 10px;
  text-align: center;
}
.faculty {
  font-size: 0.9em;
  color: #ccc;
  margin-top: 12px;
  line-height: 1.2;
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  text-align: center;
}
.event-name {
  font-size: 0.9em;
  font-weight: 500;
  margin-top: 2px;
  color: #b0b0b0;
}
"""

# Path to your logo image (should be a base64 data URI for embedding)
def image_to_base64(path):
    with open(path, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode()
    
foss_logo_b64 = image_to_base64("D:/Projects/Foss Attendance Marker/Vivent-ticket-generator/assets/fosslogo.png")

def generate_ticket(participant: Participant) -> str:
    """
    Generate a ticket for the participant and save it locally.

    Args:
        participant (Participant): The participant object.

    Returns:
        str: The file path of the generated ticket.
    """
    try:
        content = f"{qr_content}?ticket_id={participant.ticketId}"

        qr = qrcode.make(content)
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()
        qr_base64 = f"data:image/png;base64,{qr_base64}"

        # Fill the HTML template
        html = template_1.format(
            name=f"{participant.firstName} {participant.lastName}",
            event="Workshop 1: Linux Fundamentals",
            qr_code=qr_base64,
            foss_logo=foss_logo_b64,
        )

        # Convert UUID to string and use it as a safe filename
        ticket_id_str = str(participant.ticketId)
        safe_name = "".join(c for c in ticket_id_str if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"{safe_name}.png"
        file_path = f"D:/Projects/Foss Attendance Marker/Vivent-ticket-generator/tickets/{filename}"

        # Save the ticket as PNG
        hti.screenshot(html_str=html, css_str=css_1, save_as=filename, size=(800, 280))

        logger.info(f"Ticket saved as {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error generating ticket: {e}")
        return None



def update_participant_ticket_link(event_id: int, db: Session):
    """
    Generate tickets for participants, upload them to Sirv, and update the ticket link in the database.

    Args:
        event_id (int): The event ID to filter participants.
        db (Session): The database session.
    """
    participants = db.query(ParticipantModel).filter_by(eventId=event_id).all()

    for participant in participants:
        logger.info(f"Processing participant: {participant.firstName} {participant.lastName}")
        if not participant.ticket_link:
            # Generate the ticket
            ticket_path = generate_ticket(participant)
            if ticket_path:
                # Upload the ticket to Sirv
                upload_response = upload_file(ticket_path)
                if upload_response:
                    # Construct the public URL for the uploaded ticket
                    ticket_link = f"{SRV_BASE_URL}/{participant.ticketId}.png"
                    participant.ticket_link = ticket_link
                    db.commit()
                    logger.info(f"Updated ticket link for {participant.firstName} {participant.lastName}")
                else:
                    logger.error(f"Failed to upload ticket for {participant.firstName} {participant.lastName}")
            else:
                logger.error(f"Failed to generate ticket for {participant.firstName} {participant.lastName}")
        else:
            logger.info(f"Ticket already generated for {participant.firstName} {participant.lastName}")


if __name__ == "__main__":
    event_id = 2  # Example event ID
    with get_db() as db:
        update_participant_ticket_link(event_id, db)
    logger.info("Ticket generation and upload process completed.")
