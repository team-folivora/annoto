tmux new -d -s main-session
tmux split-window -h -t main-session
tmux send-keys -t main-session.0 "cd ~/annoto/api" ENTER
tmux send-keys -t main-session.0 "[ -d venv ] || python3 -m virtualenv venv" ENTER
tmux send-keys -t main-session.0 "source venv/bin/activate" ENTER
tmux send-keys -t main-session.0 "pip install -r requirements-dev.txt" ENTER
tmux send-keys -t main-session.0 "python3 -m mod &> >(tee ~/output-api.log)" ENTER
tmux send-keys -t main-session.1 "cd ~/annoto/static" ENTER
tmux send-keys -t main-session.1 "npm install" ENTER
tmux send-keys -t main-session.1 "npm run dev &> >(tee ~/output-static.log)" ENTER
tmux a -t main-session

