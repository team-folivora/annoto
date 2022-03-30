'''This file enables quick debug mode execution of the API'''

import uvicorn

if __name__ == '__main__':
    uvicorn.run("mod.src.app:APP", host="127.0.0.1", port=5000, reload=True)
