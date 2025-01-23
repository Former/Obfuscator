Obfuscator 
=============================

Быстрый старт
-----------

Запускать командой:

        python obfuscator.py test.py

Выходные файлы будут появлятся в текущей директории
В данном случае выходной файл будет test.py.txt

Пример, на входе test.py:

        import random

        def quicksort(nums):
           if len(nums) <= 1:
               return nums
           else:
               q = random.choice(nums)
               s_nums = []
               m_nums = []
               e_nums = []
               for n in nums:
                   if n < q:
                       s_nums.append(n)
                   elif n > q:
                       m_nums.append(n)
                   else:
                       e_nums.append(n)
               return quicksort(s_nums) + e_nums + quicksort(m_nums)

        def Test():
            def isEqualArray(a, b):
                return str(a) == str(b)
            qs1 = quicksort([5,4,3,2,1])
            qs2 = quicksort([1,2,3,2,1])
            assert isEqualArray(qs1, [1,2,3,4,5]), qs1
            assert isEqualArray(qs2, [1,1,2,2,3]), qs2

        Test()


На выходе test.py.ob.py:

        import random

        def hcNAp0wxjxkQ5eva(nums):
           if len(nums) <= 1:
               return nums
           else:
               tHwib_fqnjuwQj03 = random.choice(nums)
               m0btLbwZJ0HhJ5bf = []
               z3m9oEmNxw4Pj5Cw = []
               VUHYCXbxyNt3psaZ = []
               for n in nums:
                   if n < tHwib_fqnjuwQj03:
                       m0btLbwZJ0HhJ5bf.append(n)
                   elif n > tHwib_fqnjuwQj03:
                       z3m9oEmNxw4Pj5Cw.append(n)
                   else:
                       VUHYCXbxyNt3psaZ.append(n)
               return hcNAp0wxjxkQ5eva(m0btLbwZJ0HhJ5bf) + VUHYCXbxyNt3psaZ + hcNAp0wxjxkQ5eva(z3m9oEmNxw4Pj5Cw)

        def smMJTL87JYBQd8cY():
            def hH54fySTagkpxIIM(a, b):
                return str(a) == str(b)
            YnidnZuNIqk1ffYs = hcNAp0wxjxkQ5eva([5,4,3,2,1])
            Ogs1ll63MSx8mYOL = hcNAp0wxjxkQ5eva([1,2,3,2,1])
            assert hH54fySTagkpxIIM(YnidnZuNIqk1ffYs, [1,2,3,4,5]), YnidnZuNIqk1ffYs
            assert hH54fySTagkpxIIM(Ogs1ll63MSx8mYOL, [1,1,2,2,3]), Ogs1ll63MSx8mYOL

        smMJTL87JYBQd8cY()


Файл с исходными названиями test.py.map.txt:

        hcNAp0wxjxkQ5eva=quicksort
        tHwib_fqnjuwQj03=q
        m0btLbwZJ0HhJ5bf=s_nums
        z3m9oEmNxw4Pj5Cw=m_nums
        VUHYCXbxyNt3psaZ=e_nums
        smMJTL87JYBQd8cY=Test
        hH54fySTagkpxIIM=isEqualArray
        YnidnZuNIqk1ffYs=qs1
        Ogs1ll63MSx8mYOL=qs2



Защита от изменений
-----------

Можно воспользоваться защитой некоторых частей кода от зименений:
        import random

        def quicksort(nums):
           if len(nums) <= 1:
               return nums
           else:
               cur_num = random.choice(nums)
               # Защита от изменений
               #start_guard
               s_nums = []
               m_nums = []
               #stop_guard
               e_nums = []
               for num in nums:
                   if num < cur_num:
                       s_nums.append(num)
                   elif num > cur_num:
                       m_nums.append(num)
                   else:
                       e_nums.append(num)
               return quicksort(s_nums) + e_nums + quicksort(m_nums)

        def Test():
            # Частичная защита от изменений, можно задавать regexp, который включит всё найденное в список исключений (см. a_Array1, a_Array2)
            #start_guard (a_\w+)
            def isEqualArray(a_Array1, a_Array2):
            #stop_guard
                return str(a_Array1) == str(a_Array2)
            qs1 = quicksort([5,4,3,2,1])
            qs2 = quicksort([1,2,3,2,1])
            assert isEqualArray(qs1, [1,2,3,4,5]), qs1
            assert isEqualArray(qs2, [1,1,2,2,3]), qs2

        Test()
В итоге получится:
        import random

        def Fsl7HzERw5qcO3gg(E7m0MY_eWK902uqo):
           if len(E7m0MY_eWK902uqo) <= 1:
               return E7m0MY_eWK902uqo
           else:
               SEghmyuOtDjGTnXf = random.choice(E7m0MY_eWK902uqo)
               # Защита от изменений
               #start_guard
               s_nums = []
               m_nums = []
               #stop_guard
               LoRwON2cL87z8iKg = []
               for e2ssVgrgpkX8YYOS in E7m0MY_eWK902uqo:
                   if e2ssVgrgpkX8YYOS < SEghmyuOtDjGTnXf:
                       s_nums.append(e2ssVgrgpkX8YYOS)
                   elif e2ssVgrgpkX8YYOS > SEghmyuOtDjGTnXf:
                       m_nums.append(e2ssVgrgpkX8YYOS)
                   else:
                       LoRwON2cL87z8iKg.append(e2ssVgrgpkX8YYOS)
               return Fsl7HzERw5qcO3gg(s_nums) + LoRwON2cL87z8iKg + Fsl7HzERw5qcO3gg(m_nums)

        def G9vx2_qd1kBccOtt():
            # Частичная защита от изменений, можно задавать regexp, который включит всё найденное в список исключений (см. a_Array1, a_Array2)
            #start_guard (a_\w+)
            def WZ7tLXJhCrv12cXL(a_Array1, a_Array2):
            #stop_guard
                return str(a_Array1) == str(a_Array2)
            _ufy4oAhgD4pkjgY = Fsl7HzERw5qcO3gg([5,4,3,2,1])
            Ss8RU5G8zoNw0kU4 = Fsl7HzERw5qcO3gg([1,2,3,2,1])
            assert WZ7tLXJhCrv12cXL(_ufy4oAhgD4pkjgY, [1,2,3,4,5]), _ufy4oAhgD4pkjgY
            assert WZ7tLXJhCrv12cXL(Ss8RU5G8zoNw0kU4, [1,1,2,2,3]), Ss8RU5G8zoNw0kU4

        G9vx2_qd1kBccOtt()

Программа умеет обфусцировать сама себя!
