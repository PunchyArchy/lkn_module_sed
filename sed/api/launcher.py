from sed.api.main import app
import sys
import uvicorn


uvicorn.run(app, host='localhost', port=9002)
