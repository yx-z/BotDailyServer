import threading
from typing import Tuple

from bd.mail.email_template import EmailTemplate
from util.system import exception_as_str
from util.web import HTML_NEW_LINE


def threaded(job_func):
    def job(*args, **kwargs):
        job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
        job_thread.start()

    return job


def instantiate_email_template(
    email_template: EmailTemplate,
    *,
    retries: int = 0,
    retry_delay_seconds: int = 0,
    timeout_seconds: int = 0,
    **kwargs,
) -> Tuple[bool, str, str]:
    try:
        subject, body = email_template.instantiate(
            retries=retries,
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
    email_template: EmailTemplate,
    *,
    retries: int = 0,
    retry_delay_seconds: int = 0,
    timeout_seconds: int = 0,
    **kwargs,
):
    is_success, subject, body = instantiate_email_template(
        email_template,
        retries=retries,
        retry_delay_seconds=retry_delay_seconds,
        timeout_seconds=timeout_seconds,
        **kwargs,
    )
    sender = email_template.sender
    if is_success:
        sender.send(email_template.recipient_emails, subject, body)
    else:
        if sender is None:
            raise Exception(f"Require not None sender")
        sender.send(sender.email_address, subject, body)
