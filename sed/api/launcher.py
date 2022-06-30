from sed.api.main import app
import sys
import uvicorn


uvicorn.run(app, host=sys.argv[1], port=int(sys.argv[2]))
