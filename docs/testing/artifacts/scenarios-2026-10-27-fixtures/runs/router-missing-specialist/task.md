Can you look at our ADK assistant and work out how to make a user's language preference survive a restart? Use whatever skills are installed, but don't install anything new.

---
Situation (from the person asking): The installed catalog and filesystem contain only the entry skill, with no sibling specialists. The existing Python application has an agent factory, an authenticated request scope and a SQLite store. The user authorizes inspection and local changes but explicitly excludes installation. The entry skill remains the primary available skill while it identifies the missing domain guidance.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.