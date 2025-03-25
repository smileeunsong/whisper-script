# 🎵 Whisper 음성-텍스트 변환 스크립트

[OpenAI Whisper](https://github.com/openai/whisper)를 사용하여 한국어 음성 파일을 텍스트로 변환하는 스크립트입니다.

## 설치 방법

```bash
brew install ffmpeg
pip install openai-whisper torch
```

## 사용 방법

```bash
python script.py 입력파일.mp3 출력파일.txt
```

## 주의사항

- ffmpeg가 설치되어 있어야 합니다
- GPU가 있으면 더 빠르게 변환됩니다
