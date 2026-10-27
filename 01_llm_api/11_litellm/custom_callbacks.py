"""A pre-call hook - the proxy repairing a request before an engine sees it.

`drop_params` in `litellm_config.yaml` already removes a PARAMETER an engine does
not understand. It cannot touch what is INSIDE the messages, and one engine here
is strict about that.

THE PROBLEM

Unsloth Studio rejects a `name` field on any message that is not a tool result:

    400 messages.2: Value error, "name" is only valid on role="tool" messages.

OpenAI's own API allows `name` on a user or assistant message - it is how you
label who spoke in a conversation with several participants. LM Studio and Ollama
accept it. Unsloth Studio is stricter than the specification, and its check runs
in the HTTP layer, so the model never sees the request at all.

This is not a corner case. Any framework that labels its messages hits it. The
`deepagents` lessons in `Version_3/06_langchain-ai/3_deepagents` tag a sub-agent's
own assistant messages with the sub-agent name, so `4_subagents` and
`8_research_agent` failed on every `unsloth-*` alias while the other six lessons
passed.

WHY THE FIX BELONGS HERE

The whole point of the proxy is that engine differences live in ONE place. Fixing
it in each lesson would mean every framework, in every language, repeating the
same repair. Fixing it here means a lesson keeps sending correct OpenAI messages
and never learns that Unsloth is fussy.

The repair is safe. `name` is a label, not content: no model reads it, no engine
needs it, and dropping it changes no answer. It is removed only for the
`unsloth-*` aliases, so every other engine still gets the message unchanged.

WIRING

Three things must line up, and the hook is silent if one is missing:

    docker-compose.yml    mounts this file at /app/custom_callbacks.py
    litellm_config.yaml   `callbacks: custom_callbacks.proxy_handler_instance`
    this file             defines that instance at module level
"""

from typing import Any, Literal, Optional, Union

from litellm.caching.caching import DualCache
from litellm.integrations.custom_logger import CustomLogger


class UnslothMessageFix(CustomLogger):
    """Removes `name` from every non-tool message, for Unsloth aliases only."""

    async def async_pre_call_hook(
        self,
        user_api_key_dict: Any,
        cache: DualCache,
        data: dict,
        call_type: Literal[
            "completion",
            "acompletion",
            "embedding",
            "aembedding",
            "text_completion",
            "atext_completion",
        ],
    ) -> Optional[Union[Exception, str, dict]]:
        # `data["model"]` is still the ALIAS the client sent - this hook runs
        # before the router picks a deployment. The substring test also matches
        # the real model id, in case that changes.
        if "unsloth" not in str(data.get("model", "")).lower():
            return data

        for message in data.get("messages", []):
            if isinstance(message, dict) and message.get("role") != "tool":
                message.pop("name", None)

        return data


# The config points at this exact name: `custom_callbacks.proxy_handler_instance`.
proxy_handler_instance = UnslothMessageFix()
