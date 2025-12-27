.PHONY: start stop status restart logs run list

PID_FILE := .scheduler.pid
LOG_FILE := scheduler.log

start:
	@if [ -f $(PID_FILE) ] && kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
		echo "Scheduler already running (PID: $$(cat $(PID_FILE)))"; \
	else \
		nohup uv run python scheduler.py > $(LOG_FILE) 2>&1 & echo $$! > $(PID_FILE); \
		echo "Scheduler started (PID: $$(cat $(PID_FILE)))"; \
		echo "Logs: make logs"; \
	fi

stop:
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		if kill -0 $$PID 2>/dev/null; then \
			kill $$PID; \
			rm $(PID_FILE); \
			echo "Scheduler stopped"; \
		else \
			rm $(PID_FILE); \
			echo "Scheduler not running (stale PID file removed)"; \
		fi \
	else \
		echo "Scheduler not running"; \
	fi

status:
	@if [ -f $(PID_FILE) ] && kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
		echo "Scheduler running (PID: $$(cat $(PID_FILE)))"; \
	else \
		echo "Scheduler not running"; \
	fi

restart: stop
	@sleep 1
	@$(MAKE) start

logs:
	tail -f $(LOG_FILE)

run:
	uv run python main.py

list:
	@uv run python list_projects.py
