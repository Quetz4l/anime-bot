from src import secret

TEST_MODE = True

# logger.add("logs/log.json",
#            format="{time} {level} {message}",
#            level="DEBUG",
#            rotation="512 KB",
#            compression="zip",
#            serialize=True
#            )

settings = {
    'API_TOKEN': secret.API_TOKEN,
    'ADMIN_ID': secret.ADMIN_ID,
    'EMOJI_ON': "✅ ",
    'EMOJI_OFF': "❌ ",
}
