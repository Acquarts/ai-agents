"""
Run this script once to register a Windows Task Scheduler job
that runs the AI news pipeline every day at 7:00 AM.

Usage:
    python scheduler/register_task.py
"""
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
PYTHON_EXE = sys.executable
SCRIPT_PATH = PROJECT_ROOT / "agents" / "run_pipeline.py"
TASK_NAME = "AINewsAgentDaily"


def register():
    task_xml = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-16"?>
        <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
          <RegistrationInfo>
            <Description>Fetches and summarizes daily AI news using Claude</Description>
          </RegistrationInfo>
          <Triggers>
            <CalendarTrigger>
              <StartBoundary>2026-04-05T07:00:00</StartBoundary>
              <Enabled>true</Enabled>
              <ScheduleByDay>
                <DaysInterval>1</DaysInterval>
              </ScheduleByDay>
            </CalendarTrigger>
          </Triggers>
          <Principals>
            <Principal id="Author">
              <LogonType>InteractiveToken</LogonType>
              <RunLevel>LeastPrivilege</RunLevel>
            </Principal>
          </Principals>
          <Settings>
            <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
            <ExecutionTimeLimit>PT30M</ExecutionTimeLimit>
            <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
            <IdleSettings>
              <StopOnIdleEnd>false</StopOnIdleEnd>
              <RestartOnIdle>false</RestartOnIdle>
            </IdleSettings>
            <Enabled>true</Enabled>
          </Settings>
          <Actions Context="Author">
            <Exec>
              <Command>{PYTHON_EXE}</Command>
              <Arguments>"{SCRIPT_PATH}"</Arguments>
              <WorkingDirectory>{PROJECT_ROOT}</WorkingDirectory>
            </Exec>
          </Actions>
        </Task>
    """)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".xml", delete=False, encoding="utf-16"
    ) as f:
        f.write(task_xml)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [
                "schtasks",
                "/Create",
                "/TN", TASK_NAME,
                "/XML", tmp_path,
                "/F",  # overwrite if exists
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[scheduler] Task '{TASK_NAME}' registered successfully.")
            print(f"[scheduler] Runs daily at 07:00 using: {PYTHON_EXE}")
            print(f"[scheduler] Script: {SCRIPT_PATH}")
        else:
            print(f"[scheduler] ERROR: {result.stderr}")
            sys.exit(1)
    finally:
        import os
        os.unlink(tmp_path)


if __name__ == "__main__":
    register()
