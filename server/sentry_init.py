import sentry_sdk

from config import settings


def init_sentry() -> None:
    """No-op if SENTRY_DSN is unset, so this is safe to call in dev without an account."""
    if not settings.sentry_dsn:
        return
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        environment="hackathon",
    )
