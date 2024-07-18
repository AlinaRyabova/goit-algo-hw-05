import timeit
import gdown
from tabulate import tabulate
import chardet

# Завантаження файлів з Google Диску
def download_file_from_google_drive(file_id, output):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output, quiet=False)

# Завантаження текстових файлів
download_file_from_google_drive('18_R5vEQ3eDuy2VdV3K5Lu-R-B-adxXZh', 'article1.txt')
download_file_from_google_drive('13hSt4JkJc11nckZZz2yoFHYL89a4XkMZ', 'article2.txt')

# Функція для визначення кодування файлу
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Читання текстів з файлів з автоматичним визначенням кодування
def read_file(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

try:
    text1 = read_file('article1.txt')
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")

try:
    text2 = read_file('article2.txt')
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")

# Алгоритм Кнута-Морріса-Пратта (KMP)
def kmp_search(text, pattern):
    def kmp_table(pattern):
        table = [0] * len(pattern)
        j = 0
        for i in range(1, len(pattern)):
            if pattern[i] == pattern[j]:
                j += 1
                table[i] = j
            else:
                if j > 0:
                    j = table[j - 1]
                    i -= 1
                else:
                    table[i] = 0
        return table

    table = kmp_table(pattern)
    m, n = len(pattern), len(text)
    i = j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j > 0:
                j = table[j - 1]
            else:
                i += 1
    return -1

# Алгоритм Боєра-Мура (BM)
def bm_search(text, pattern):
    def bad_char_table(pattern):
        table = [-1] * 256
        for i in range(len(pattern)):
            table[ord(pattern[i]) % 256] = i
        return table

    table = bad_char_table(pattern)
    m, n = len(pattern), len(text)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - table[ord(text[s + j]) % 256])
    return -1

# Алгоритм Рабіна-Карпа (RK)
def rk_search(text, pattern):
    d = 256
    q = 101
    m, n = len(pattern), len(text)
    h = 1
    p = 0
    t = 0

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1

# Вимірювання часу виконання за допомогою timeit
def measure_time(func, text, pattern):
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=1000)

# Підрядки для пошуку
existing_substring = "структури даних"
non_existing_substring = "not present"

# Вимірювання часу для кожного алгоритму та кожного підрядка в обох текстах
results = {
    "text1_existing": {
        "kmp": measure_time(kmp_search, text1, existing_substring),
        "bm": measure_time(bm_search, text1, existing_substring),
        "rk": measure_time(rk_search, text1, existing_substring),
    },
    "text1_non_existing": {
        "kmp": measure_time(kmp_search, text1, non_existing_substring),
        "bm": measure_time(bm_search, text1, non_existing_substring),
        "rk": measure_time(rk_search, text1, non_existing_substring),
    },
    "text2_existing": {
        "kmp": measure_time(kmp_search, text2, existing_substring),
        "bm": measure_time(bm_search, text2, existing_substring),
        "rk": measure_time(rk_search, text2, existing_substring),
    },
    "text2_non_existing": {
        "kmp": measure_time(kmp_search, text2, non_existing_substring),
        "bm": measure_time(bm_search, text2, non_existing_substring),
        "rk": measure_time(rk_search, text2, non_existing_substring),
    },
}

# Форматування результатів у вигляді таблиці
table_data = [
    ["text1_existing", "Існуючий підрядок", results["text1_existing"]["kmp"], results["text1_existing"]["bm"], results["text1_existing"]["rk"]],
    ["text1_non_existing", "Неіснуючий підрядок", results["text1_non_existing"]["kmp"], results["text1_non_existing"]["bm"], results["text1_non_existing"]["rk"]],
    ["text2_existing", "Існуючий підрядок", results["text2_existing"]["kmp"], results["text2_existing"]["bm"], results["text2_existing"]["rk"]],
    ["text2_non_existing", "Неіснуючий підрядок", results["text2_non_existing"]["kmp"], results["text2_non_existing"]["bm"], results["text2_non_existing"]["rk"]],
]

headers = ["Текст", "Підрядок", "KMP (сек)", "BM (сек)", "RK (сек)"]

# Вивід таблиці
print(tabulate(table_data, headers=headers, tablefmt="pretty"))

# Висновки
conclusions = [
    ("text1_existing", "BM", results["text1_existing"]["bm"]),
    ("text1_non_existing", "BM", results["text1_non_existing"]["bm"]),
    ("text2_existing", "BM", results["text2_existing"]["bm"]),
    ("text2_non_existing", "BM", results["text2_non_existing"]["bm"]),
]

print("\nНайшвидший алгоритм для кожного випадку:")
for text, algo, time in conclusions:
    print(f"- {text}: {algo} з часом {time:.6f} seconds")

print("\nВисновок:")
print("Алгоритм Боєра-Мура (BM) демонструє найкращі показники швидкості для всіх випадків.")

#+--------------------+---------------------+----------------------+---------------------+----------------------+
#|       Текст        |      Підрядок       |      KMP (сек)       |      BM (сек)       |       RK (сек)       |
#+--------------------+---------------------+----------------------+---------------------+----------------------+
#|   text1_existing   |  Існуючий підрядок  |  0.3222286999807693  | 0.07222729997010902 |  0.6715334999607876  |
#| text1_non_existing | Неіснуючий підрядок |  4.193724300013855   |  1.358704200014472  |  9.957731599977706   |
#|   text2_existing   |  Існуючий підрядок  | 0.016281200048979372 | 0.01286469999467954 | 0.025331500044558197 |
#| text2_non_existing | Неіснуючий підрядок |  4.971765799971763   | 1.8203945999848656  |  16.882760100008454  |
#+--------------------+---------------------+----------------------+---------------------+----------------------+

##Найшвидший алгоритм для кожного випадку:
#text1_existing: BM з часом 0.072227 seconds
#text1_non_existing: BM з часом 1.358704 seconds
#text2_existing: BM з часом 0.012865 seconds
#text2_non_existing: BM з часом 1.820395 seconds

##Висновок:
#Алгоритм Боєра-Мура (BM) демонструє найкращі показники швидкості для всіх випадків.