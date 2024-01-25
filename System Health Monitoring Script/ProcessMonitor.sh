#!/bin/bash

# Define thresholds
CPU_THRESHOLD=70
MEMORY_THRESHOLD=75
DISK_THRESHOLD=70
PROCESS_THRESHOLD=40
CHECK_INTERVAL_SECONDS=90

get_current_datetime() {
    date +"%Y-%m-%d %H:%M:%S"
}

# CPU usage monitor
check_cpu() {
    local cpu_usage=$(top -b -n 1 | awk '/%Cpu/{print $2}' | cut -d. -f1)
    if [ "$cpu_usage" -gt "$CPU_THRESHOLD" ]; then
        echo "$(get_current_datetime) - Alert: High CPU usage detected - $cpu_usage%"
    fi
}

# Memory usage monitor
check_memory() {
    local memory_usage=$(free | awk '/Mem/{print $3/$2 * 100}' | cut -d. -f1)
    if [ "$memory_usage" -gt "$MEMORY_THRESHOLD" ]; then
        echo "$(get_current_datetime) - Alert: High memory usage detected - $memory_usage%"
    fi
}

# Disk space monitor
check_disk() {
    local disk_usage=$(df -h / | awk '/\//{print $(NF-1)}' | cut -d% -f1)
    if [ "$disk_usage" -gt "$DISK_THRESHOLD" ]; then
        echo "$(get_current_datetime) - Alert: High disk usage detected - $disk_usage%"
    fi
}

# Processes monitor
check_processes() {
    local process_count=$(ps aux --no-heading | wc -l)
    if [ "$process_count" -gt 100 ]; then
        echo "$(get_current_datetime) - Alert: High number of running processes detected - $process_count"
    fi
}


main() {
  while true; do
    check_cpu
    check_memory
    check_disk
    check_processes

    sleep "$CHECK_INTERVAL_SECONDS"
done
}

main
