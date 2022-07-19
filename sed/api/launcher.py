from sed.api.main import app
import sys
import uvicorn


uvicorn.run(app, host='0.0.0.0', port=8001)
