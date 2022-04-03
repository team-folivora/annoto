{ cd ~/annoto/api; pip install -r requirements-dev.txt; python3 -m mod; } > ~/output-api.log 2>&1 &
{ cd ~/annoto/static; npm install; npm run dev; } > ~/output-static.log 2>&1 &
bash
