tmux new -d -s main-session
tmux split-window -h -t main-session
tmux send-keys -t main-session.0 "cd ~/annoto/api" ENTER
tmux send-keys -t main-session.0 "python3 manage.py install dev" ENTER
tmux send-keys -t main-session.0 "python3 manage.py db-create" ENTER
tmux send-keys -t main-session.0 "python3 manage.py run &> >(tee ~/output-api.log)" ENTER
tmux send-keys -t main-session.1 "cd ~/annoto/static" ENTER
tmux send-keys -t main-session.1 "npm install --no-save" ENTER
tmux send-keys -t main-session.1 "npm run dev &> >(tee ~/output-static.log)" ENTER
tmux a -t main-session

