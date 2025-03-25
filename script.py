import whisper
import os
import subprocess
from pathlib import Path
import torch
import argparse

def prepare_audio(audio_path):
    """오디오 파일을 Whisper에 적합한 형식으로 준비"""
    output_path = str(Path(audio_path).with_suffix('.wav'))
    try:
        subprocess.run([
            'ffmpeg',
            '-i', audio_path,
            '-ar', '16000',  # Whisper 권장 샘플레이트
            '-ac', '1',      # 모노 채널
            '-c:a', 'pcm_s16le',
            output_path
        ], check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"오디오 변환 실패: {e.stderr.decode()}")

def transcribe_audio(audio_path, output_txt):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_path}")
    
    audio_path = os.path.abspath(audio_path)
    print(f"🎵 입력 파일: {audio_path}")
    
    print("🔄 오디오 파일 변환 중...")
    wav_path = prepare_audio(audio_path)
    
    try:
        print("📝 텍스트 변환 중...")
        model_path = os.path.expanduser("~/.cache/whisper/medium.pt")
        
        if not os.path.exists(model_path):
            print("⚠️ 모델 파일이 로컬에 없습니다. 다운로드가 필요합니다.")
            if not is_connected():
                raise RuntimeError("인터넷 연결이 필요합니다. 모델을 다운로드해야 합니다.")
        
        # CUDA 사용 가능 여부 확인
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cpu":
            print("⚠️ GPU가 감지되지 않아 CPU에서 실행됩니다. 변환 시간이 더 소요될 수 있습니다.")
        
        model = whisper.load_model("medium", device)
        result = model.transcribe(
            wav_path,
            language="ko",
            fp16=(device == "cuda")  # GPU에서만 FP16 사용
        )
        
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print(f"✅ 변환 완료! 결과가 {output_txt}에 저장되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise
    finally:
        # 임시 WAV 파일 정리
        if os.path.exists(wav_path) and wav_path != audio_path:
            os.remove(wav_path)

def is_connected():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MP3 파일을 텍스트로 변환하는 스크립트")
    parser.add_argument("input", type=str, help="입력할 MP3 파일 경로")
    parser.add_argument("output", type=str, help="출력할 TXT 파일 경로")
    
    args = parser.parse_args()
    transcribe_audio(args.input, args.output)
