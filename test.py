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
