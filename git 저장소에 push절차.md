##윈도우즈 자격증명 → Git 저장소 연결 → 확인 → push 절차

## 1. 자격증명관리자 > 윈도우즈 자격증명 > 일반자격증명 
- 인터넷 또는 네트워크 주소: githttps://github.com
- 사용자 이름: <내GitHub아이디>
- 암호: xxx

## 2. Git 저장소 연결

```bash
git init
git remote add origin https://github.com/<내GitHub아이디>/<저장소이름>.git
```
## 3. 원격 저장소 확인: 명령은 현재 연결된 원격 저장소를 출력합니다.

```bash
git remote -v
```
예시 출력:

```bash
origin  https://github.com/<내GitHub아이디>VoiceAI_math.git (fetch)
origin  https://github.com/<내GitHub아이디>/VoiceAI_math.git (push)
```

---

## 4. 파일 추가 및 커밋

```bash
git add .
git commit -m "Initial project import"
```

---

## 5. 브랜치 이름 확인 / main으로 변경

```bash
git branch -M main
```

---

## 6. GitHub에 push

```bash
git push -u origin main
```

---

## 전체 한 번에 정리

```bash
git init
git remote add origin https://github.com/<내GitHub아이디>/VoiceAI_math.git
git remote -v
git add .
git commit -m "Initial project import"
git branch -M main
git push -u origin main
```