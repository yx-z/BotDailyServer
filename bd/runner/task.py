from bd.component.email_template import EmailTemplate
from util.mail import Sender
from util.system import threaded
from util.web import HTML_NEW_LINE


@threaded
def send_email(
    sender: Sender,
    email_template: EmailTemplate,
    *,
    num_retry: int,
    retry_delay_seconds: int,
    timeout_seconds: int,
    **kwargs,
):
    email_template.sender = sender

    is_success, subject, body = email_template.instantiate(
        num_retry=num_retry,
        retry_delay_seconds=retry_delay_seconds,
        timeout_seconds=timeout_seconds,
        **kwargs,
    )
    body = HTML_NEW_LINE.join(body)

    if is_success:
        sender.send(email_template.recipient_emails, subject, body)
    else:
        sender.send(sender.email_address, subject, body)
