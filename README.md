# FileProcessor


--result_settings.json의 key 값들 설명--
1) "result_type" : 통계를 내는 종류
    PATENT 혹은 PAPER 이라는 값을 가짐.
    값이 PATENT일 경우 특허통계파일을 생성하고, 값이 PAPER일 경우 논문통계파일을 생성함.
    
2) "result_saving_abspath" : 통계파일을 저장할 절대경로

3) "loaded_file_nums": 통계를 내기 위해 사용되는 raw excel file들의 개수 (클라이언트가 불러오기를 통해 load한 excel 파일의 개수)

4) "loaded_file_abspaths": 통계를 내기 위해 사용자가 load한 excel 파일들 각각의 절대경로를 List[str]형태로 저장

5) "TPN_PAN_limit" 
    상훈업무정리 파일을 보면 "기본 파일의 "PAN" 갯수가 1-30개인 것은 자른다" 혹은 "기본파일의 TPN 개수가 1-30개인 것은 자른다"와 같은 지시사항이 있는데 여기서 30처럼 자르는 기준이 되는 값. 
    만약 TPN_PAN_limit=50이 될 경우, 기본 파일의 PAN/TPN 개수가 1-50개인 것을 자르게 된다.
