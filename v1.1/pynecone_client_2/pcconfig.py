import pynecone as pc


config = pc.Config(
    app_name="pynecone_client_2",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
