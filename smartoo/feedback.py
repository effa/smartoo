from django.core.mail import mail_admins
import logging


logger = logging.getLogger(__name__)

MIN_TEXT_LENGTH = 3


def process_message_feedback(text, email, session_pk):
    # check message
    if len(text) < MIN_TEXT_LENGTH:
        raise ValueError("Message text is too short")

    #print session_pk
    #print text
    #print email

    # render message (email body)
    message = """
    text:
    {text}

    email:
    {email}

    session:
    {session}
    """.format(text=text, email=email, session=session_pk)

    logger.info("Email feedback: " + message)

    try:
        mail_admins('Smartoo: Message Feedback', message)
    except Exception as exc:
        logger.error('Sending mail failed: ' + (exc.message or unicode(type(exc))))
        raise
