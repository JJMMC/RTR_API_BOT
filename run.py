from app import app
from scripts.sqlalch_update import update_scraped


if __name__ == "__main__":
    #update_scraped()

    app.run(debug=True)
