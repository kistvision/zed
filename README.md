# zed

## ZED SDK 설치
[link](https://www.stereolabs.com/developers/release)에서 ZED SDK를 설치합니다. 이 코드는 ZED SDK 4.0에서 동작합니다. SDK 설치 후 재부팅합니다.

## 패키지 설명
ZED 카메라를 활용하기 위한 패키지입니다. zed.py의 ZEDCamera() 클래스에 카메라 SDK를 활용해 편리하게 기능을 사용할 수 있도록 함수들을 정의했습니다. 필요한 함수는 이 클래스의 함수를 호출해서 쓰시고, 그 외 필요한 함수는 공식 사이트 문서를 참고하세요.
`zed.py`를 실행하면 연결된 카메라 영상을 확인할 수 있습니다.

## AR glasses에 side-by-side 이미지 띄우는 예제
ZED SDK 4.0에서 동작 확인했습니다. 파이썬 OpenCV가 설치 되어 있어야 합니다. (pip install opencv-python)
ZED SDK 4.0 이전 버전을 사용하시는 경우 [zed.py] 파일의 48번째 줄에서 에러가 날 시, 48번째 줄을 주석 처리 한 뒤 45번째 줄을 주석 해제 하시면 됩니다.
Nreal 글래스를 연결한 뒤 [AR_glasses.py] 파일의 13번째 줄 'monitor_x'에 주모니터의 x축 길이 값을 입력합니다. (예제 코드는 주모니터 2560 X 1440 크기 환경에서 구현한 코드입니다.)
입력 후 아래 명령어를 실행합니다.

$ python AR_glasses.py 2i

출선구 앞에서 작업시 [AR_glasses.py] 파일의 19, 20번째 줄 주석을 해제하여 gain과 exposure를 조정할 수 있습니다.
Exposure 0, gain 50정도로 설정했을 때 적절한 영상을 얻을 수 있었습니다.

## 기타 예제 설명
카메라 gain, exposure를 10씩 증가시키며 얻은 이미지를 저장하는 예제:

    $ python POSCO_get_image.py 2i
    $ python POSCO_get_image.py mini

주의사항: gain, exposure를 변경한 후 카메라에 적용하는데 일정 시간이 걸립니다. 이유는 모르겠고, 그 시간도 일정하지 않아 넉넉하게 sleep을 줘야 제대로 된 영상을 얻을 수 있습니다. 몇 번 실험 후 매뉴얼하게 슬립 시간 지정하시면 됩니다.

비디오 영상 저장하는 예제:

    $ python POSCO_save_video.py

저장한 양안 영상을 스테레오 비디오로 변환하는 예제:

    $ python POSCO_make_video.py

비디오 저장 예제가 두개인 이유: resize, concat에 시간이 오래 걸려 실시간으로 비디오를 저장할 수 없습니다. 따로 저장 후 make_video.py에서 두 비디오를 resize, concat하여 스테레오 비디오로 저장합니다.
