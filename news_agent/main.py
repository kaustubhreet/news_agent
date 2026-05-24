# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from news_agent.services.news_pipeline import run_pipeline
# from news_agent.services.notification_service import send_all
# from news_agent.utils.formatter import format_news
# from news_agent.services.storage_service import save_news
from news_agent.utils.logger import logger
from news_agent.agents.graph import build_graph

if __name__ == "__main__":
    try:
        logger.info("App started")
        app = build_graph()
        logger.info("⚙️ Graph execution started")
        result = app.invoke({})
        logger.info("✅ Graph execution completed")
        
    except Exception as e:
        logger.error(f"❌ App failed: {e}")

#     print("✅ Inside main")
#     news = run_pipeline()
#     save_news(news)
#     message = format_news(news)
    
#     print("\n📊 Daily Tech News:\n")

#     for n in news[:15]:
#         print(f"• {n['summary']}")
    
#     print("📤 Sending to Telegram and Watsapp..")
#     send_all(message)

#     print(f"✅ Sent! Status")
#     logger.info("Notification send successfully")

# except Exception as e:
#     print("❌ Error:", e)