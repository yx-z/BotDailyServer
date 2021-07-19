import logging
import time
from typing import List, Tuple, Optional, Set, Union

from bd.component import BDComponent
from bd.component.templated_text import Subject
from util.system import interrupt_after, exception_as_str

InstantiatedEmail = Tuple[bool, str, str]


class EmailTemplate:
    def __init__(
        self,
        subject: Optional[Subject] = None,
        components: Optional[List[BDComponent]] = None,
        recipient_emails: Optional[Union[Set[str], str]] = None,
    ):
        self.subject = subject
        self.components = components
        self.recipient_emails = recipient_emails

    def instantiate(
        self,
        *,
        num_retry: int = 0,
        retry_delay_seconds: int = 0,
        timeout_seconds: int = 60,
        **kwargs,
    ) -> InstantiatedEmail:
        if any(a is None for a in [self.subject, self.components]):
            raise Exception(f"Require not None subject and components")

        arg_dict = {"email_template": self}
        arg_dict.update(kwargs)

        @interrupt_after(timeout_seconds)
        def _instantiate() -> InstantiatedEmail:
            components = []
            is_subject_success = True
            is_success = True
            for component in [self.subject] + self.components:
                logging.info(f"Instantiating {component.get_name()}")
                try:
                    components.append(component.get_str(**arg_dict))
                    logging.info(f"Instantiated {component.get_name()}")
                except Exception as e:
                    if num_retry == 0:
                        is_success = False
                        if component == self.subject:
                            is_subject_success = False
                        logging.error(e)
                        components.append(exception_as_str(e).replace("\n", "<br>"))
                    else:
                        raise e
            subject = (
                components[0] if is_subject_success else "Error instantiating subject"
            )
            return is_success, subject, "<br>".join(components[1:])

        try:
            return _instantiate()
        except Exception as exception:
            if num_retry > 0:
                num_retry -= 1
                logging.warning(
                    f"Will do {num_retry} retries after {timeout_seconds} seconds"
                )
                time.sleep(retry_delay_seconds)
                return self.instantiate(
                    num_retry=num_retry,
                    timeout_seconds=timeout_seconds,
                    retry_delay_seconds=retry_delay_seconds,
                    **kwargs,
                )
            else:
                raise exception
