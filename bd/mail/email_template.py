import logging
import time
from typing import List, Tuple, Optional, Set, Union

from bd.component.base_component import BaseComponent
from bd.component.templated_text import Subject
from util.io import interrupt_after
from util.send_email import Sender


class EmailTemplate:
    def __init__(
        self,
        subject: Optional[Subject] = None,
        components: Optional[List[BaseComponent]] = None,
        sender: Optional[Sender] = None,
        recipient_emails: Optional[Union[Set[str], str]] = None,
    ):
        self.subject = subject
        self.sender = sender
        self.recipient_emails = recipient_emails
        self.components = components

    def instantiate(
        self,
        *,
        retries: int = 0,
        retry_delay_seconds: int = 0,
        timeout_seconds: int = 0,
        **kwargs,
    ) -> Tuple[str, List[str]]:
        attrs = list(filter(lambda s: not s.startswith("__"), dir(self)))
        if any(a is None for a in attrs):
            raise Exception(f"Require not None {attrs}")

        @interrupt_after(timeout_seconds)
        def _instantiate():
            arg_dict = {"email_template": self}
            arg_dict.update(kwargs)
            logging.info("Instantiating Subject")
            subject = self.subject.get_div_str(**arg_dict)
            components = []
            for component in self.components:
                logging.info(f"Instantiating {component.get_name()}")
                try:
                    components.append(component.get_div_str(**arg_dict))
                except Exception as e:
                    logging.info(f"Got Exception {exception}")
                    if "to_str_func_on_error" in kwargs:
                        components.append(kwargs["to_str_func_on_error"]())
                    else:
                        raise e
            return subject, components

        try:
            return _instantiate()
        except Exception as exception:
            if retries > 0:
                retries -= 1
                logging.warning(
                    f"Will do {retries} retries after {timeout_seconds} seconds"
                )
                time.sleep(retry_delay_seconds)
                self.instantiate(
                    retries=retries,
                    timeout_seconds=timeout_seconds,
                    retry_delay_seconds=retries,
                    **kwargs,
                )
            else:
                raise exception
