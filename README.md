# OrigamiObjectCreator
> ### 종이접기를 이용한 절차적 모델링
```
종이접기 규칙에 따라 오브젝트를 스크립트로 작성하여 만들어 낼 수 있도록 하는 도구입니다.

blender의 scripting에 사용할 수 있도록 python 모듈인 bpy를 이용하여 module을 만들었으며,
실행 하는 경우 스크립트 형태로 존재하는 모델이 3D 오브젝트 형태로 생성되는 프로그램을 만들었습니다.  
```
<br>

<div align="center">
  <table>
    <tr>
      <th><img src="https://github.com/oeccsy/OrigamiObjectCreator/assets/77562357/e9002f99-19d2-4759-90c0-38a7116f76f7" width="460px" height="290px"/></th>
      <th><img src="https://github.com/oeccsy/OrigamiObjectCreator/assets/77562357/2b08b47a-1354-4d1e-b6f2-aade4c3688d4" width="460px" height="290px"/></th>
    </tr>
    <tr>
      <td align="center">▲ paper crane</td>
      <td align="center">▲ paper airplane</td>
    </tr>
  </table>
</div>

<div align="center">
  <table>
    <tr>
      <th> 개발 환경 </th>
      <th> 개발 기간 </th>
      <th> 개발 인원 </th>
    </tr>  
    <tr>
      <td align="center"> <code> blender </code> <code> python </code> </td>
      <td align="center"> <code> 21.12.29 ~ 22.01.27 </code> <br>
                          <code> 24.04.27 ~ 24.05.09 </code> </td>
      <td align="center"> <code> 본인 1명 </code> </td>
    </tr>
  </table>
</div>

<br>

## How to use
<img src="https://github.com/oeccsy/OrigamiObjectCreator/assets/77562357/8bd9562f-5dc3-42e7-835c-160f7930c19b" width="852px" height="480px"/>  

- [`fold.py`](https://github.com/oeccsy/OrigamiObjectCreator/blob/main/Program/Modules/fold.py) module을 blender editor에 적용합니다. [[적용 방법]](https://github.com/oeccsy/OrigamiObjectCreator/issues/3)
- blender scripting에 진입합니다.
- 원하는 vertex의 index를 확인하며 코드를 작성합니다. [[원하는 vertex의 index 확인 방법]](https://github.com/oeccsy/OrigamiObjectCreator/issues/4)

## Feature
- [다양한 Fold 기능 구현](https://github.com/oeccsy/OrigamiObjectCreator/issues/1) 

## Relate Project
- [RandomObjectCreator](https://github.com/oeccsy/RandomObjectCreator) ( 21.11.26 ~ 21.12.21 )
  
해당 프로젝트는 기존의 절차적 모델링 프로젝트에 종이접기를 접목하여 개발하였습니다.

<br>

## License
[blender](https://www.blender.org/)의 라이센스 정책에 따라 GPL 라이센스를 적용합니다.
