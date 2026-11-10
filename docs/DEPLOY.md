# Deploying the static game

The project is a dependency-free static web app. Build a lean deploy folder from the project root:

```powershell
python scripts/deploy/build_static.py
```

The script checks the project JSON and writes only the app, runtime data, and optimized assets to `dist/`. It leaves source prompts, original artwork, and project documents out of the deploy folder.

Preview the exact deploy output locally:

```powershell
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`, then upload the **contents of `dist/`** to a static hosting provider with `index.html` at the site root. No install or build dependencies are required beyond Python 3.

The game stores reading progress and scores in that browser's local storage. The data is local to the player's device and is not sent to a server.
