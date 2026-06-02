# Universe 프로젝트 구조 설명

## 프로젝트 한줄 설명

Python과 웹 자산을 사용하는 3D 우주/태양계 시각화 프로젝트입니다. 행성/위성/소행성 텍스처와 glTF 모델을 로드해 궤도와 천체를 시각적으로 보여줍니다.

## 기본 작동 흐름

- run.py 또는 src/universe/main.py가 로컬 실행 진입점을 제공합니다.
- src/universe/orbits.py와 solar_data.py가 천체 데이터와 궤도 계산을 담당합니다.
- assets의 텍스처와 소행성 glTF 모델이 실제 3D 장면 렌더링 재료로 사용되고 tests가 궤도/표시 로직을 검증합니다.

## 문서 기준

- 아래 목록은 `git ls-files`로 확인되는 Git 추적 파일을 기준으로 작성했습니다.
- `.git`, `node_modules`, `build`, `.gradle`, 임시 업로드/출력물처럼 Git이 관리하지 않는 폴더는 제외했습니다.
- 폴더 표는 코드와 자산이 어떤 책임으로 나뉘는지, 파일 표는 각 파일이 실제로 무엇을 담당하는지 설명합니다.

## 폴더별 설명 (16개)

| 폴더 | 설명 |
| --- | --- |
| `.` | 프로젝트 루트입니다. 실행/빌드 설정, README, 전체 구조 문서, 최상위 진입 파일이 모여 있습니다. |
| `.vscode` | VS Code에서 이 프로젝트를 열 때 사용하는 편집기 설정을 보관합니다. |
| `assets` | 프로젝트 실행 화면이나 렌더링에 필요한 이미지, 3D 모델, 텍스처 자산의 상위 폴더입니다. |
| `assets/models` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/bennu` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/eros` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/gaspra` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/ida` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/mathilde` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/models/asteroids/vesta` | 3D 장면에 로드할 glTF 모델과 모델별 바이너리/텍스처 파일을 보관합니다. |
| `assets/textures` | 행성, 위성, 소행성 표면에 입힐 이미지 텍스처를 보관합니다. |
| `scripts` | 외부 자산을 내려받거나 프로젝트 데이터를 준비하는 보조 스크립트를 보관합니다. |
| `src` | Python 패키지 소스 루트입니다. 실제 import 가능한 패키지 코드를 이 아래에 배치합니다. |
| `src/universe` | Universe Python 패키지입니다. 실행 로직, 궤도 계산, 태양계 데이터 정의가 들어 있습니다. |
| `tests` | 자동 테스트 폴더입니다. Python 단위 테스트나 Playwright 브라우저 테스트가 들어 있습니다. |

## 파일별 설명 (93개)

| 파일 | 설명 |
| --- | --- |
| `.gitignore` | Git에 올리지 않을 빌드 산출물, 캐시, 개인 환경 파일을 지정하는 설정 파일입니다. 저장소에는 필요한 소스/자산만 남기도록 도와줍니다. |
| `.vscode/settings.json` | VS Code에서 이 프로젝트를 열 때 적용할 편집기/작업공간 설정을 저장하는 JSON 파일입니다. |
| `assets/models/asteroids/bennu/Bennu.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/bennu/Bennu.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/bennu/Bennu_normal.png` | 소행성 표면의 굴곡과 조명을 표현하기 위한 노멀맵 텍스처입니다. |
| `assets/models/asteroids/bennu/bennu_patch.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/bennu/bennu_patch_norm.png` | 소행성 표면의 굴곡과 조명을 표현하기 위한 노멀맵 텍스처입니다. |
| `assets/models/asteroids/bennu/bennu_whole.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/eros/433_eros.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/eros/433_eros.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/eros/eros_diff.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/eros/eros_norm.png` | 소행성 표면의 굴곡과 조명을 표현하기 위한 노멀맵 텍스처입니다. |
| `assets/models/asteroids/eyes_asteroid_models.json` | 소행성 모델 목록, 출처, 로딩 정보를 정리한 JSON 메타데이터 파일입니다. |
| `assets/models/asteroids/gaspra/gaspra.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/gaspra/gaspra.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/gaspra/gaspra_albedo.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/ida/asteroid_02_diff.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/ida/asteroid2_normals.png` | 소행성 표면의 굴곡과 조명을 표현하기 위한 노멀맵 텍스처입니다. |
| `assets/models/asteroids/ida/generic_asteroid_2.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/ida/generic_asteroid_2.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/mathilde/asteroid_03_diff.jpg` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/mathilde/asteroid3_normals.png` | 소행성 표면의 굴곡과 조명을 표현하기 위한 노멀맵 텍스처입니다. |
| `assets/models/asteroids/mathilde/generic_asteroid_3.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/mathilde/generic_asteroid_3.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/vesta/4_vesta.bin` | glTF 모델이 참조하는 바이너리 버퍼입니다. 실제 3D 정점/인덱스 데이터가 들어 있습니다. |
| `assets/models/asteroids/vesta/4_vesta.gltf` | 소행성 3D 모델의 glTF 장면 파일입니다. 메시, 머티리얼, 텍스처 참조를 정의합니다. |
| `assets/models/asteroids/vesta/vesta_04.png` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/models/asteroids/vesta/vesta_n.png` | 소행성 3D 모델 표면에 입히는 컬러/디퓨즈 텍스처 이미지입니다. |
| `assets/textures/asteroid.jpg` | Universe 3D 장면에서 asteroid 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/asteroid_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/bennu.jpg` | Universe 3D 장면에서 bennu 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/bennu_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/callisto.jpg` | Universe 3D 장면에서 callisto 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/ceres.jpg` | Universe 3D 장면에서 ceres 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/deimos.jpg` | Universe 3D 장면에서 deimos 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/earth.jpg` | Universe 3D 장면에서 earth 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/earth_clouds.png` | 행성 대기와 구름층을 별도 레이어로 표현하기 위한 텍스처 이미지입니다. |
| `assets/textures/earth_clouds_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/earth_night.jpg` | 지구 야간 조명처럼 밤쪽 표면 효과를 표현하기 위한 텍스처 이미지입니다. |
| `assets/textures/earth_night_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/enceladus.jpg` | Universe 3D 장면에서 enceladus 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/eros.jpg` | Universe 3D 장면에서 eros 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/eros_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/europa.jpg` | Universe 3D 장면에서 europa 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/ganymede.jpg` | Universe 3D 장면에서 ganymede 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/gaspra.jpg` | Universe 3D 장면에서 gaspra 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/gaspra_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/iapetus.jpg` | Universe 3D 장면에서 iapetus 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/ida.jpg` | Universe 3D 장면에서 ida 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/ida_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/io.jpg` | Universe 3D 장면에서 io 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/jupiter.jpg` | Universe 3D 장면에서 jupiter 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/jupiter_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/mars.jpg` | Universe 3D 장면에서 mars 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/mathilde.jpg` | Universe 3D 장면에서 mathilde 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/mathilde_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/mercury.jpg` | Universe 3D 장면에서 mercury 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/miranda.jpg` | Universe 3D 장면에서 miranda 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/moon.jpg` | Universe 3D 장면에서 moon 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/neptune.jpg` | Universe 3D 장면에서 neptune 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/neptune_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/oberon.jpg` | Universe 3D 장면에서 oberon 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/phobos.jpg` | Universe 3D 장면에서 phobos 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/pluto.jpg` | Universe 3D 장면에서 pluto 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/rhea.jpg` | Universe 3D 장면에서 rhea 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/saturn.jpg` | Universe 3D 장면에서 saturn 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/saturn_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/sun.jpg` | Universe 3D 장면에서 sun 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/sun_glow.png` | 태양 또는 밝은 천체의 발광 효과를 표현하는 보조 텍스처입니다. |
| `assets/textures/sun_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/titan.jpg` | Universe 3D 장면에서 titan 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/titania.jpg` | Universe 3D 장면에서 titania 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/triton.jpg` | Universe 3D 장면에서 triton 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/uranus.jpg` | Universe 3D 장면에서 uranus 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/uranus_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/venus.jpg` | Universe 3D 장면에서 venus 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/venus_clouds.png` | 행성 대기와 구름층을 별도 레이어로 표현하기 위한 텍스처 이미지입니다. |
| `assets/textures/venus_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `assets/textures/vesta.jpg` | Universe 3D 장면에서 vesta 천체 표면에 입히는 텍스처 이미지입니다. |
| `assets/textures/vesta_source.jpg` | 천체 텍스처의 원본 또는 출처 확인용 이미지입니다. 실제 표시용 텍스처와 비교하거나 재가공할 때 사용합니다. |
| `PROJECT_STRUCTURE.md` | 프로젝트의 모든 주요 폴더와 Git 추적 파일을 한글로 설명하는 구조 문서입니다. 처음 보는 사람이 경로별 역할을 빠르게 파악하기 위해 추가했습니다. |
| `pyproject.toml` | Python 프로젝트 메타데이터, 빌드/테스트 도구 옵션, 패키지 설정을 정의합니다. |
| `README.md` | 프로젝트 개요, 실행 방법, 주요 기능을 설명하는 기본 안내 문서입니다. |
| `requirements.txt` | Python 실행에 필요한 기본 패키지 목록입니다. `pip install -r requirements.txt`로 설치합니다. |
| `run.py` | Universe 프로젝트를 로컬에서 실행하는 Python 진입 스크립트입니다. 앱 서버 또는 시각화 실행 흐름을 시작합니다. |
| `scripts/fetch_asteroid_models.py` | 소행성 3D 모델 자산을 외부에서 내려받거나 로컬 assets 구조에 맞게 준비하는 보조 스크립트입니다. |
| `scripts/fetch_textures.py` | 행성/위성/소행성 텍스처 이미지를 내려받거나 assets/textures 폴더에 맞게 정리하는 보조 스크립트입니다. |
| `src/universe/__init__.py` | 해당 폴더를 Python 패키지로 인식시키는 초기화 파일입니다. 필요하면 패키지 공개 API를 이곳에서 정리합니다. |
| `src/universe/main.py` | Universe 패키지의 주요 실행 로직입니다. 앱 초기화와 우주 시각화 구동 흐름을 담당합니다. |
| `src/universe/orbits.py` | 천체의 궤도 계산, 위치 갱신, 표시 가능한 궤도 데이터 생성을 담당하는 Universe 핵심 모듈입니다. |
| `src/universe/solar_data.py` | 태양계 천체 이름, 반지름, 거리, 텍스처 경로 같은 시각화용 기본 데이터를 정의합니다. |
| `tests/test_inspect_visibility.py` | Universe 시각화에서 천체나 검사 대상이 화면에 표시 가능한 상태인지 검증하는 테스트입니다. |
| `tests/test_orbits.py` | Universe의 궤도 계산 함수가 기대한 값과 구조를 반환하는지 확인하는 테스트입니다. |

## 읽는 방법

- 먼저 폴더별 설명에서 큰 기능 묶음을 확인한 다음, 파일별 설명에서 실제 구현 파일을 찾으면 됩니다.
- Android 프로젝트는 `app/src/main/java` 아래 Kotlin 파일이 핵심 코드이고, `app/src/main/res`와 `app/src/main/assets`는 화면/모델/오디오 자산입니다.
- 웹 프로젝트는 `index.html`, `styles.css`, `script.js` 또는 `app.js`가 화면 구조, 스타일, 동작을 나눠 담당합니다.
- Python 프로젝트는 루트의 실행 스크립트와 `src`, `backend`, `scripts`, `tests` 폴더를 함께 보면 처리 흐름을 이해할 수 있습니다.
