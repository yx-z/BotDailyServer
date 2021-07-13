from typing import Tuple

from bd.mail.email_template import EmailTemplate
from util.mail import Sender
from util.system import exception_as_str, threaded
from util.web import HTML_NEW_LINE


def instantiate_email_template_str(
    email_template: EmailTemplate,
    *,
    retries: int = 0,
    retry_delay_seconds: int = 0,
    timeout_seconds: int = 0,
    **kwargs,
) -> Tuple[bool, str, str]:
    try:
        subject, body = email_template.instantiate(
            num_retry=retries,
            retry_delay_seconds=retry_delay_seconds,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )
        return True, subject, HTML_NEW_LINE.join(body)
    except Exception as exception:
        return (
            False,
            f"ERROR send {email_template.subject.get_name()} to {email_template.recipient_emails}",
            exception_as_str(exception),
        )


@threaded
def send_email(
    sender: Sender,
    email_template: EmailTemplate,
    *,
    retries: int = 0,
    retry_delay_seconds: int = 0,
    timeout_seconds: int = 0,
    **kwargs,
):
    email_template.sender = sender
    is_success, subject, body = instantiate_email_template_str(
        email_template,
        retries=retries,
        retry_delay_seconds=retry_delay_seconds,
        timeout_seconds=timeout_seconds,
        **kwargs,
    )
    if is_success:
        sender.send(email_template.recipient_emails, subject, body)
    else:
        sender.send(sender.email_address, subject, body)
