import sentry_sdk

sentry_sdk.init(
    dsn="https://62a0bdb5b9b5cb73233e28527aacfae7@o4505835118592000.ingest.sentry.io/4505835128356864",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

division_by_zero = 1 / 0