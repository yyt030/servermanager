#��װpython3.5.2����������װʱ���ϵͳ��������
xp���԰�װ3.4�汾


#����project���⻷��
1: cd servermanager
2: pyvenv venv
3: venv\Scripts\activate


#��װ����������whl��
4: cd install
5: pip install --no-index -f . -r requirements.txt


#��ʼ������db�ͱ�ṹ
6: cd servermanager
7: python -m manager db init 
   python -m manager db migrate
   python -m manager db upgrade


#��ʼ�����̲�������
8: python -m manager init_static_data && python -m manager init_test_data


#��pycharm����app
9: ���ù��������venv����Ϊ�ù���Ĭ�ϵĽ�������start app