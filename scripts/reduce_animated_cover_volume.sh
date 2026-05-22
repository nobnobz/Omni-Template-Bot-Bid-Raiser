#!/usr/bin/env bash
set -u

TARGET_DIR="Other/animated covers"
VOLUME_FILTER="volume=0.65"
RUN_ID="$$-$(date +%s)"

processed=0
skipped_no_audio=0
failed=0
total=0

failed_files=()
skipped_files=()

cleanup() {
  if [[ -d "$TARGET_DIR" ]]; then
    find "$TARGET_DIR" -type f -name ".volume-reduce-${RUN_ID}.*" -delete
  fi
}
trap cleanup EXIT INT TERM

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required but was not found." >&2
  exit 1
fi

if ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe is required but was not found." >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory not found: $TARGET_DIR" >&2
  exit 1
fi

has_encoder() {
  ffmpeg -hide_banner -loglevel error -encoders 2>/dev/null | grep -Eq "[[:space:]]$1[[:space:]]"
}

webm_audio_encoder="libopus"
if ! has_encoder "libopus"; then
  webm_audio_encoder="libvorbis"
fi

process_file() {
  local input="$1"
  local dir base ext lower_ext output_format audio_encoder tmp_file

  dir="$(dirname "$input")"
  base="$(basename "$input")"
  ext="${base##*.}"
  lower_ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"

  if ! ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$input" | grep -q .; then
    echo "SKIP no audio: $input"
    skipped_no_audio=$((skipped_no_audio + 1))
    skipped_files+=("$input")
    return 0
  fi

  case "$lower_ext" in
    mp4)
      output_format="mp4"
      audio_encoder="aac"
      ;;
    mov)
      output_format="mov"
      audio_encoder="aac"
      ;;
    m4v)
      output_format="mp4"
      audio_encoder="aac"
      ;;
    webm)
      output_format="webm"
      audio_encoder="$webm_audio_encoder"
      ;;
    *)
      return 0
      ;;
  esac

  tmp_file="$(mktemp "$dir/.volume-reduce-${RUN_ID}.XXXXXX")" || {
    echo "FAIL temp file: $input" >&2
    failed=$((failed + 1))
    failed_files+=("$input")
    return 0
  }

  if ffmpeg -hide_banner -loglevel error -y \
    -i "$input" \
    -map 0 \
    -map_metadata 0 \
    -c copy \
    -c:v copy \
    -c:a "$audio_encoder" \
    -af "$VOLUME_FILTER" \
    -f "$output_format" \
    "$tmp_file"; then
    if [[ -s "$tmp_file" ]]; then
      mv -f "$tmp_file" "$input"
      echo "OK: $input"
      processed=$((processed + 1))
    else
      rm -f "$tmp_file"
      echo "FAIL empty output: $input" >&2
      failed=$((failed + 1))
      failed_files+=("$input")
    fi
  else
    rm -f "$tmp_file"
    echo "FAIL ffmpeg: $input" >&2
    failed=$((failed + 1))
    failed_files+=("$input")
  fi
}

while IFS= read -r -d '' file; do
  total=$((total + 1))
  process_file "$file"
done < <(find "$TARGET_DIR" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.webm' \) -print0)

echo
echo "Summary"
echo "Total matching files: $total"
echo "Processed: $processed"
echo "Skipped without audio: $skipped_no_audio"
echo "Failed: $failed"

if (( skipped_no_audio > 0 )); then
  echo
  echo "Skipped files:"
  printf '  %s\n' "${skipped_files[@]}"
fi

if (( failed > 0 )); then
  echo
  echo "Failed files:"
  printf '  %s\n' "${failed_files[@]}"
fi

if (( failed > 0 )); then
  exit 1
fi
