# SOURCES_MANIFEST

`build_register.py` 입력 파일(저장소에 포함하지 않음). 입력은 Drive `N제 시스템` 수집 결과이며 파일 이름은 Drive 파일 ID다.

|파일(Drive ID)|원래 이름|행 수(헤더 제외)|바이트|sha256|
|---|---|---:|---:|---|
|1FfJDPEbaUvS3vUOnzQxoa6L2f3IohsT9|ARC_추가분_전체판정.csv|2027|2507119|99a7505f5b384d4fd02a6ffb7f2e23d519e28ea65c39e2f1ae059026956ef824|
|1xmPdU_z5Q-ztnIMluFJC4H5y7Utl4NIF|ARC_학교기출_정답교정.csv|53|17518|da1bc7599b40a6eca81c8aca232dbd5223f68ae03ca12b8e4c68a9c140b6c678|
|1FYY-CZlLjOeLcAUpIEeDQhV_C-ri126N|SCI_COLLECTOR_20261003_BATCH02/SOURCES.csv|1330|1049646|20ae7368a00de2a8f3e21853d026fdf2686fc3eddf8706c7df06a9f574c3b045|
|1gLbtopR32yaKLvv6WRPq6_IXcTN8kHEh|SOC_COLLECTOR_20261003_BATCH02/SOURCES.csv|1516|1194860|1335028dca9bdce4fb471a217c3f8b74791c9c78a0ede9ff72fd632e346b6baf|

레지스트리 재생성: `python3 bank/tools/build_register.py --judge <전체판정.csv> --gaya <정답교정.csv> --sources <SOURCES.csv ...>`
