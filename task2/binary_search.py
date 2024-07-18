def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None


    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            upper_bound = arr[mid]
            return (iterations, upper_bound)
        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]

    return (iterations, upper_bound)

# тестуємо нашу функцію:
sorted_array = [0.1, 0.4, 0.5, 0.8, 1.2, 2.3, 3.4, 4.8, 5.9]
target_value = 2.0

result = binary_search(sorted_array, target_value)
print(f"Кількість ітерацій: {result[0]}, Верхня межа: {result[1]}") # виводить: Кількість ітерацій: 3, Верхня межа: 2.3

    