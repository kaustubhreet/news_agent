def format_news(news):
    message = "🚀 *Daily Tech News*\n\n"

    for i, n in enumerate(news, 1):
        message += f"{i}. {n['summary']}\n\n"

    return message