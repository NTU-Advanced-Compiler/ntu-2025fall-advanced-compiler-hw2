#!/usr/bin/env bash
# Usage: ./run_testcase.sh <testcase.bril> [threshold_file] [local_dce|lvn+local_dce]


TESTCASE="$1"
THRESHOLD_FILE="$2"
MODE="$3" 
LVN_PY="./src/lvn.py"
DCE_PY="./src/local_dce.py"

# Read threshold: first non-empty, non-comment line
if [[ ! -f "$THRESHOLD_FILE" ]]; then
  echo "Error: threshold file '$THRESHOLD_FILE' not found." >&2
  exit 2
fi

THRESHOLD="$(awk '
  /^[[:space:]]*#/ {next}      # skip comments
  /^[[:space:]]*$/ {next}      # skip blanks
  {gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0); print; exit}
' "$THRESHOLD_FILE")"

if ! [[ "$THRESHOLD" =~ ^[0-9]+$ ]]; then
  echo "Error: threshold must be an integer; got: '$THRESHOLD' (from $THRESHOLD_FILE)" >&2
  exit 2
fi

# Run command 1
cmd1_output="$(bril2json < "$TESTCASE" | brili -p  1>/dev/null 2>prof.log)"
cmd1_inst="$(awk -F': *' '/^total_dyn_inst:/{print $2; exit}' prof.log)"


# Run command 2
cmd2_output=
case "$MODE" in
  "local_dce")
    bril2json < "$TESTCASE" \
    | python3 "$DCE_PY" \
    | brili -p 1>/dev/null 2>prof.log
    ;;
  "lvn+local_dce")
    bril2json < "$TESTCASE" \
    | python3 "$LVN_PY" \
    | python3 "$DCE_PY" \
    | brili -p 1>/dev/null 2>prof.log
    ;;
  *)
    echo "Error: unknown mode '$MODE' (use 'local_dce' or 'lvn+local_dce')." >&2
    exit 2
    ;;
esac
cmd2_inst="$(awk -F': *' '/^total_dyn_inst:/{print $2; exit}' prof.log)"

rm -f prof.log


# Validate extraction
for n in "$cmd1_inst" "$cmd2_inst"; do
  if ! [[ "$n" =~ ^[0-9]+$ ]]; then
    echo "Error: failed to parse total_dyn_inst from one of the commands." >&2
    echo "--- cmd1 ---"
    echo "$cmd1_inst"
    echo "--- cmd2 ---"
    echo "$cmd2_inst"
    exit 2
  fi
done

# Compare and decide
if (( cmd2_inst < cmd1_inst && cmd2_inst <= THRESHOLD )); then
  echo "PASS"
  echo "--- Initial total_dyn_inst ---"
  echo "$cmd1_inst"
  echo "--- Optimized total_dyn_inst ---" 
  echo "$cmd2_inst"
  exit 0
else
  echo "FAIL"
  echo "--- Initial total_dyn_inst ---"
  echo "$cmd1_inst"
  echo "--- Optimized total_dyn_inst ---" 
  echo "$cmd2_inst"
  exit 1
fi
