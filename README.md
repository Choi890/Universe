# Universe - 3D Solar System

Ursina/Panda3D로 만든 3D 태양계 관측 프로젝트입니다. 첫 화면부터 태양계 전체가 보이도록 구성했고, 행성 위치는 JPL 근사 Keplerian orbital elements로 계산합니다. 행성, 항성, 소행성 표면은 NASA/JPL 자료를 기준으로 구성하고, 지구는 NASA Blue Marble/Black Marble/Clouds 자료와 전용 셰이더로 보강했습니다.

## 구현 범위

- 검은 우주 배경과 절차적 별 배경
- 태양, 8개 행성, Ceres, Pluto
- 주요 위성 15개
- 고해상도 UV 구체 메시 기반 천체 렌더링
- 실제/대표 행성 표면 텍스처
- 태양 광구 입상 질감, 흑점, 코로나 글로우 셰이더
- NASA 기반 지구 낮 표면, 야간 도시광, 구름 맵
- 지구 전용 낮/밤 경계, 대기 림, 석양 림, 바다 반사 셰이더
- 태양 방향 기반 행성 조명, 야간면, 대기 림 셰이더
- 금성/토성/천왕성/해왕성의 실제 관측 색감 기반 고해상도 대표 텍스처
- 목성 Cassini 전역 맵 기반 텍스처
- 모든 행성/위성을 완전한 구 형태로 표시
- NASA OSIRIS-REx Bennu 이미지 기반 소행성 표면 텍스처
- Saturn/Uranus 다층 고리와 Cassini Division 스타일 간극
- 행성 자전, 공전, 축 기울기
- 행성별 타원 궤도선
- Mars와 Jupiter 사이 소행성대
- 궤도 관측 카메라와 6자유도 자유 비행 카메라
- 기본값이 현실과 같은 1초=1초 시간 흐름
- 필요할 때 조절 가능한 시간 배속 시뮬레이션

## 설치

```powershell
python -m pip install -r requirements.txt
```

## 실행

```powershell
python run.py
```

## 조작

- `C`: 궤도 카메라 / 자유 비행 카메라 전환
- `W/A/S/D`: 바로 자유 비행 모드로 전환하며 이동
- 자유 비행: `마우스 오른쪽 버튼`을 누른 채 시점 회전
- 자유 비행: `마우스 왼쪽 버튼`을 누른 채 앞으로 이동, `마우스 가운데 버튼`은 뒤로 이동
- 태양/행성 클릭: 해당 천체 360도 검사 보기와 NASA/JPL 원본 이미지 표시
- 검사 보기: 마우스 드래그로 회전, 마우스 휠로 확대/축소
- `ESC`: 태양계 전체 보기로 복귀
- 궤도 카메라: `마우스 오른쪽 드래그` 또는 `방향키`로 회전
- 궤도 카메라: `마우스 휠`로 확대/축소
- 자유 비행: 마우스로 시점 회전
- 자유 비행: `W/A/S/D` 전후좌우 이동
- 자유 비행: `Q/E` 아래/위 이동
- 자유 비행: `Z/X` 롤 회전
- 자유 비행: `Shift` 고속, `Ctrl` 저속, `마우스 휠` 이동 속도 조절
- `F`: 다음 천체로 초점 이동
- `1`: 태양계 전체 보기
- `O`: 궤도선 표시 토글
- `L`: 라벨 표시 토글
- `M`: 위성 표시 토글
- `P`: 일시정지
- `T`: 현재 실제 UTC 시각으로 다시 동기화하고 1배속으로 복귀
- `[` / `]`: 시간 배속 감소/증가

## 스케일

실제 태양계의 거리와 행성 반지름 비율은 차이가 너무 커서 그대로 렌더링하면 행성이 거의 보이지 않습니다. 이 프로젝트는 태양 중심 행성 거리와 궤도 위치를 AU 기준의 동일 선형 스케일로 배치해 실제 거리 비율을 유지합니다. 화면에서 관찰할 수 있도록 천체 반지름과 위성 거리는 시각적으로 확대했습니다. 기본 시간은 실행 순간의 실제 UTC 시각에서 시작하며 1초가 실제 1초로 흐릅니다.

데이터 기준:

- NASA/JPL Planetary Physical Parameters: https://ssd.jpl.nasa.gov/planets/phys_par.html
- NASA/JPL Approximate Positions of the Planets: https://ssd.jpl.nasa.gov/planets/approx_pos.html
- NASA/JPL planetary texture maps: https://maps.jpl.nasa.gov/
- NASA Sun Facts: https://science.nasa.gov/sun/facts/
- NASA Sunspots: https://science.nasa.gov/sun/sunspots/
- NASA Blue Marble Next Generation: https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/base-topography-bathymetry/
- NASA Earth at Night maps: https://science.nasa.gov/earth/earth-observatory/earth-at-night/maps/
- NASA Visible Earth Blue Marble Clouds: https://visibleearth.nasa.gov/images/57747/blue-marble-clouds
- NASA Photojournal Jupiter Cylindrical Map: https://science.nasa.gov/photojournal/cassinis-best-maps-of-jupiter-cylindrical-map/
- NASA Photojournal Venus Colorized Clouds: https://science.nasa.gov/photojournal/venus-colorized-clouds/
- NASA Photojournal Saturn in Color: https://science.nasa.gov/photojournal/saturn-in-color/
- NASA Photojournal Uranus Final Image: https://science.nasa.gov/photojournal/uranus-final-image/
- NASA Photojournal Neptune True Color of Clouds: https://science.nasa.gov/photojournal/neptune-true-color-of-clouds/
- NASA Bennu Mosaic: https://science.nasa.gov/resource/bennu-mosaic/
- NASA SDO Sun image: https://science.nasa.gov/photojournal/image-of-sun-from-nasas-solar-dynamics-observatory/

## 텍스처 다시 받기

텍스처가 없거나 새로 받고 싶을 때:

```powershell
python scripts/fetch_textures.py
```

## 테스트

```powershell
python -m unittest discover -s tests
```
